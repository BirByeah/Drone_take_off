import threading, time
from communication.communication_macros import TABLE_BATTERY

from communication.serial_rasp import UART_Communication, CommunicationCore, task_status_list
from control.control_macros import *
from utility.log import *
from vision.vision import STATUS_BACKWARD, STATUS_FORWARD, Eye

task_index = 0

class ConcreteTasks:
    def __init__(self) -> None:
        self.logger = Logger("Concrete")
        
        self.drone_voltage_warning = False
        
    def drone_initialization(self):
        self.uart_communication = UART_Communication()
        self.communicationcore = CommunicationCore(self.uart_communication)

        self.Serial_thread = threading.Thread(None, 
                                              self.uart_communication.receive, 
                                              "serial_thread")
        
        self.ParseParam_thread = threading.Thread(None, 
                                                  self.communicationcore.parse_recv_bytes, 
                                                  "parseparam_thread")
        self.Serial_thread.start()
        self.logger.debug_log("Recv thread started.")
        self.ParseParam_thread.start()
        self.logger.debug_log("Parse thread started.")
    
    def take_off(self) ->None:
        while True:
            if task_status_list[task_index] == 1:
                #self.communicationcore.compose_command(CMD_FLY_MODE, (FLY_MODE_POS_HIGH,))
                FINISHED_TASK_LIST[task_index] = True
                return 
            time.sleep(0.02)
    
    def adjust_drone(self) -> None:
        self.logger.debug_log("Adjust task start!")
        self.do_wait_command(CMD_QUERY_MODE)
        return 
    
    def go_along_line_forward(self):
        self.do_wait_command(CMD_TRANSLATION, (0, 20, 0, 10, 0, 90))
        task_status_list[task_index] = 0
        self.eye = Eye(STATUS_FORWARD, self.communicationcore, task_index)
        self.eye.trace()
        FINISHED_TASK_LIST[task_index] = True
        return
        
    def beep(self):
        #self.do_wait_command(CMD_BEEP)
        task_status_list[task_index] = 1                #2022.10.24
        FINISHED_TASK_LIST[task_index] = True
        return
    
    def go_along_line_backward(self):
        self.do_wait_command(CMD_TRANSLATION, (0, 20, 0, 10, 2, 70))
        task_status_list[task_index] = 0
        self.eye = Eye(STATUS_BACKWARD, self.uart_communication, task_index)
        self.eye.trace()
        FINISHED_TASK_LIST[task_index] = True
        return
      
    def landing(self):
        self.do_wait_command(CMD_LANDING)
        return
            
    def do_wait_command(self, cmd, data = None):
        self.communicationcore.compose_command(cmd, data)
        while True:
            if task_status_list[task_index] == 1:
                FINISHED_TASK_LIST[task_index] = True
                return 
            time.sleep(0.03)
            
    def battery_voltage_check(self):
        if 1 <= self.communicationcore.param_table[TABLE_BATTERY] <= 10.5:
            self.logger.debug_log(f"Attention! Battery voltage:{self.communicationcore.param_table[TABLE_BATTERY]}!")
            self.drone_voltage_warning = True
        else:
            self.drone_voltage_warning = False

concretetasks = ConcreteTasks()
TASK_INDEX = 0
TASK = 1
TASK_PARAM = 2
TASK_NAME = 3

TASK_TAKE_OFF   = concretetasks.take_off
TASK_ADJUST     = concretetasks.adjust_drone
TASK_FORWARD    = concretetasks.go_along_line_forward
TASK_BEEP       = concretetasks.beep
TASK_BACKWARD   = concretetasks.go_along_line_backward
TASK_LANDING    = concretetasks.landing

TASK_TABLE = (
    (TASK_INDEX_TAKE_OFF,   TASK_TAKE_OFF,  (FLY_MODE_POS_HIGH), "TAKE_OFF"),
    (TASK_INDEX_ADJUST,     TASK_ADJUST,    (FLY_MODE_POS_HIGH), "ADJUST"),
    (TASK_INDEX_FORWARD,    TASK_FORWARD,   (FLY_MODE_POS_HIGH), "FORWARD"),
    (TASK_INDEX_BEEP,       TASK_BEEP,      (FLY_MODE_POS_HIGH), "BEEP"),
    (TASK_INDEX_BACKWARD,   TASK_BACKWARD,  (FLY_MODE_POS_HIGH), "BACKWARD"),
    (TASK_INDEX_BEEP,       TASK_BEEP,      (FLY_MODE_POS_HIGH), "BEEP"),
    (TASK_INDEX_LANDING,    TASK_LANDING,   (FLY_MODE_POS_HIGH), "LANDING"),
)

FINISHED_TASK_LIST = [
    False
] * TASK_NUM


task = TASK_TABLE[task_index][TASK]
task_param = TASK_TABLE[task_index][TASK_PARAM]
task_name = TASK_TABLE[task_index][TASK_NAME]

class TaskImplementation:
    def __init__(self) -> None:
        self.logger = Logger("Overall")
        
        self.concretetasks = concretetasks
    
    def task_arrangement(self):
        global task_index, task_name, task
        self.concretetasks.drone_initialization()
        self.thread_task = threading.Thread(None, task, task_name)
        self.logger.info_log(f"trying to start task {task_name}...")
        self.thread_task.start()
        self.logger.info_log(f"Task {task_name} has started!")
        while True:
            if self.concretetasks.drone_voltage_warning:
                self.logger.warning_log("Low electricity left! Emergency landing!")
                self.concretetasks.landing()
                return 
            else:
                print(f"task index:{task_index}")
                if FINISHED_TASK_LIST[task_index] == True:
                    self.logger.info_log(f"Task {task_name} has completed! \
                        Its status is {self.thread_task.is_alive()} now!")
                    task_index += 1
                    task = TASK_TABLE[task_index][TASK]
                    task_name = TASK_TABLE[task_index][TASK_NAME]
                    self.thread_task = threading.Thread(None, task, task_name)
                    self.thread_task.start()
                    self.logger.info_log(f"Task {task_name} has started!")
            self.concretetasks.battery_voltage_check()
            time.sleep(0.02)
    

