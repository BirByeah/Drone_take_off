import cv2 as cv
import numpy as np
import time

from utility.log import Logger
from communication.serial_rasp import CommunicationCore, task_status_list
from control.control_macros import *

camera_index = 0
kernel = np.ones((9,9),np.uint8)
img_size = (480, 640, 3)
empty_img = np.zeros((img_size))
ACCUMULATE_NUM = 5

X1 = 0
Y1 = 1
X2 = 2
Y2 = 3

STATUS_FORWARD = 0
STATUS_BACKWARD = 0

START = 0
END = 1

step = 10 # cm
speed = 10

ADVANCE_MODE = False

class Eye:
    def __init__(self, sta, serial_obj, task_index) -> None:
        self.logger = Logger("Eye")
        self.serial_obj:CommunicationCore = serial_obj
        self.task_index = task_index
        self.cap:cv.VideoCapture = cv.VideoCapture(camera_index)
        self.status = sta
        
        self.img = None
        self.lines = None
        self.rough_point:np.ndarray = np.array([[0] * 4]*ACCUMULATE_NUM, np.uint32)
        self.rough_slope:np.ndarray = np.array([0] * ACCUMULATE_NUM, np.float32)
        self.precise_slope = 0
        self.precise_point = 0
        
        self.vis_temp_index = 0
        self.start_or_end = START
        
    def image_process_routine(self) -> None:
        ret, self.img = self.cap.read()
        #print(img_size[0] / 2)
        #self.img = self.img[0:int(img_size[0] / 2)]
        #cv.imshow("TEST_origin", self.img)#TODO:raspberry has some difference here!
        self.img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        #self.img = cv.GaussianBlur(self.img, (5, 5), 1.5)
        (ret, self.img) = cv.threshold(self.img, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
        self.img = cv.morphologyEx(self.img, cv.MORPH_OPEN, kernel)
        #self.img = cv.erode(self.img, kernel) # TODO: Here I changed this to erode
        self.img = cv.Laplacian(self.img, cv.CV_8U)
        
    def trace(self) ->None:
        while True:
            self.image_process_routine()
            #cv.imshow("TEST_routine", self.img)
            self.lines:np.ndarray = cv.HoughLinesP(self.img, 1, np.pi/180, 100, minLineLength=210, maxLineGap=25)
            try:
                for line in self.lines:
                    self.vis_temp_index += 1
                    self.vis_temp_index %= ACCUMULATE_NUM
                    self.rough_point[self.vis_temp_index] = line[0]
                    try:
                        self.rough_slope[self.vis_temp_index] = (self.rough_point[self.vis_temp_index][Y2] - self.rough_point[self.vis_temp_index][Y1]) / (self.rough_point[self.vis_temp_index][X2] - self.rough_point[self.vis_temp_index][X1])
                    except ZeroDivisionError:
                        self.rough_slope[self.vis_temp_index] = 4.1 # This is a guess
                    #cv.line(empty_img, (x1,y1), (x2,y2), (0,0,255), 2)
                    if self.vis_temp_index == ACCUMULATE_NUM - 1:
                        temp_median = np.median(self.rough_slope)
                        temp_index = (self.rough_slope == temp_median)
                        self.precise_point = self.rough_point[temp_index]
                        self.precise_slope = self.rough_slope[temp_index]
                        self.logger.debug_log(f"points:{self.precise_point}")
                        self.logger.debug_log(f"slopes:{self.precise_slope}")
            except TypeError:
                self.logger.warning_log("No line was found. Trying to get farther from the line...")
                #self.do_wait_command(CMD_TRANSLATION, (5, speed, 180))
                continue
            if abs(self.precise_slope) > 2:
                if self.start_or_end == END:
                    return
            self.adjust_itself()
            self.large_scale_move()
            self.rough_point.fill(0)
            self.rough_slope.fill(0)
            """k = cv.waitKey(1) & 0xFF
            if k == 27:
                break"""
                
    def adjust_itself(self):
        if abs(self.precise_slope) < 0.8:
            if self.start_or_end == START:
                self.start_or_end = END
                self.logger.info_log("Got into tracing mode.")
        if self.start_or_end == START:
            if self.status == STATUS_FORWARD:
                self.do_wait_command(CMD_TRANSLATION, (step, speed, 270))
            else:
                self.do_wait_command(CMD_TRANSLATION, (step, speed, 90))
        else:
            try:
                temp_points = self.rough_point[self.rough_slope < 0.8]
                temp_points_num = temp_points.shape[0]
                rough_center = (np.sum(temp_points[:, X2] + temp_points[:, X1]) / 2 / temp_points_num, np.sum(temp_points[:, Y2] + temp_points[:, Y1]) / 2 / temp_points_num)
            except Exception as e:
                self.logger.critical_log(f"ZeroDiv or TypeError?:{e}")
            if img_size[0] / 4 >= rough_center[1]:
                self.logger.info_log(f"Too low({rough_center[1]}), trying to get higher.")
                if ADVANCE_MODE:
                    self.do_wait_command(CMD_GO_UP, (2, speed))
                else:
                    self.do_wait_command(CMD_TRANSLATION, (5, speed, 180))
                self.logger.info_log(f"Successfully got higher.")
            elif 3 * img_size[0] / 4 <= rough_center[1]:
                self.logger.info_log(f"Too high({rough_center[1]}), trying to get higher.")
                if ADVANCE_MODE:
                    self.do_wait_command(CMD_GO_DOWN, (2, speed))
                else:
                    self.do_wait_command(CMD_TRANSLATION, (5, speed, 180))
                self.logger.info_log(f"Successfully got lower.")
        
        
    def large_scale_move(self):
        p1x = self.precise_point[0] # left point
        p1y = self.precise_point[1]
        p2x = self.precise_point[2] # right point
        p2y = self.precise_point[3]
        if self.status == STATUS_FORWARD:
            if ADVANCE_MODE:
                if self.precise_slope < 0:
                    self.do_wait_command(CMD_GO_DOWN, (-int(step * self.precise_slope), speed))
                elif self.precise_slope > 0:
                    self.do_wait_command(CMD_GO_UP, (int(step * self.precise_slope), speed))
            self.do_wait_command(CMD_TRANSLATION, (step, speed, 270))
        else:
            if ADVANCE_MODE:
                if self.precise_slope < 0:
                    self.do_wait_command(CMD_GO_UP, (-int(step * self.precise_slope), speed))
                elif self.precise_slope > 0:
                    self.do_wait_command(CMD_GO_DOWN, (int(step * self.precise_slope), speed))
            self.do_wait_command(CMD_TRANSLATION, (step, speed, 90))
    
    def do_wait_command(self, cmd, data):
        task_status_list[self.task_index] = 0
        self.serial_obj.compose_command(cmd, data)
        while task_status_list[self.task_index] == 0:
            time.sleep(0.02)
        
if __name__ == "__main__":
    pass