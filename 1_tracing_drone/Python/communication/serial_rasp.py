import time
import serial as ser
from utility.log import *
import sys
import numpy as np
import threading

from communication.communication_macros import *
from control.control_macros import *

recv_byte_buffer = []
lock_recv_parse = threading.Lock()
lock_recv_taskimp = threading.Lock()

if SYS.__contains__("Windows"):
    serial_port = "COM6"
elif SYS.__contains__("Linux"):
    serial_port = "/dev/ttyAMA0"
timeout = 0.5
baudrate = 500000

class UART_Communication:
    def __init__(self) -> None:
        self.logger = Logger("BSerial")
        self.send_byte_list = []
        
        self.recv_byte_list = []
        self.recv_going_flag = False            # When True, recv is going, 
                                                # can't clear the recv_byte_list.
        self.buffer_len = 0                     # the length of the buffer data in recv buffer
        self.data_len_recv = 0                  # the right data length indicated in fourth byte
        self.recv_check_result = (0, 0)         # the result from check_value_generator
        self.init_frame = False                 # before the first frame head was found, it is False
        
        self.open_serial()
    
    def open_serial(self) -> None:
        """open the serial

        Raises:
            e: the exception caused by opening the serial
        """
        self.logger.debug_log("Trying to open the serial...")
        try:
            self.serial = ser.Serial(serial_port, baudrate, timeout = timeout)
        except Exception as e:
            self.logger.critical_log(e)
        self.logger.debug_log("Serial config succeeded.")
        ser_stat = self.serial.is_open
        self.logger.info_log(f"Serial stat:{self.serial.is_open}")
        if not ser_stat:
            try:
                self.serial.open()
            except Exception as e:
                self.logger.critical_log(e)
            self.logger.debug_log("Serial opened successfully!")
        else:
            self.logger.debug_log("Serial has opened")

    def write(self,
              content:list) -> None:
        """write a command to STM
        """
        content = bytes(content)
        #self.logger.info_log(content.hex())
        self.serial.write(content)
        
    def read(self, 
            byte_size:int = 1) -> None:
        """read the info from STM

        Args:
            byte_size (int, optional): the size to read. Defaults to 1.

        Returns:
            bytes: received results
        """
        content = self.serial.read(byte_size)
        self.logger.debug_log(f"{content}")
        return content

    def to_byte(self,
                byte:int, 
                length:int = 1, 
                byteorder:str = sys.byteorder, 
                signed:bool = False) -> bytes:
        return byte.to_bytes(length, byteorder, signed=signed)

    def check_value_generator(self,
                  byteslist:list) -> tuple:
        """check the sum

        Args:
            byteslist (list): in the list should be int

        Returns:
            tuple: the first param in the tuple is sum, the second is add
        """
        sum = 0
        add = 0
        for i in byteslist:
            sum += i
            add += sum
        sum = sum & 255
        add = add & 255
        return (sum, add)

    def send(self,
             address:int,
             id:int, 
             data:list) -> int:
        """send a command to STM

        Args:
            address (int, optional): address. No Default!!!
            id (int, optional): id. No Default!!!
            data : data
            
        Return:
            sum(int) : the sum 
        """
        self.send_byte_list.clear()
        self.send_byte_list.append(FRAME_HEAD)
        if DEEP_DEBUG_MODE:
            if not address in ADDR_ARRAY:
                self.logger.critical_log(f"Unknown address{address} was given!")
            if not id in ID_ARRAY:
                self.logger.critical_log(f"Unknown ID({id}) was given!")
            if not data:
                self.logger.critical_log("Data is empty!!!")
        self.send_byte_list.append(address)
        self.send_byte_list.append(id)
        self.send_byte_list.append(len(data))
        self.send_byte_list.extend(data)
        
        temp = self.check_value_generator(self.send_byte_list)
        self.send_byte_list.append(temp[0])
        self.send_byte_list.append(temp[1])
        content = bytes(self.send_byte_list)
        self.serial.write(content)
        self.logger.info_log(f"Write:{content}")# .hex(' ')
        return temp

    def receive(self) -> None:
        """receive the data. No data was returned.
        """
        while True:#self.serial.in_waiting > 0
            recv_temp = int.from_bytes(self.serial.read(1), sys.byteorder)
            if not self.init_frame and recv_temp == FRAME_HEAD:
                self.init_frame = True
            if not self.recv_going_flag:
                self.recv_going_flag =True
                self.recv_byte_list.clear()
            if not self.init_frame:
                self.logger.debug_log(f"No frame head, continued.")
                continue
            if len(self.recv_byte_list) >= 26:
                self.init_frame = False
                self.recv_going_flag = False
                self.logger.warning_log("Data too long! Got back to empty state.")
                continue
            self.recv_byte_list.append(recv_temp)
            
            if len(self.recv_byte_list) == 4:           # check the data length
                self.data_len_recv = recv_temp
            elif len(self.recv_byte_list) == self.data_len_recv + 6 and self.data_len_recv != 0: # get enough bytes to form a frame
                if self.is_recv_right_byte():
                    self.put_data_into_buffer()
                else:
                    self.logger.warning_log(f"Unable to form a complete byte(although length is enough))! Got {self.recv_byte_list}")
                self.recv_going_flag = False
                self.data_len_recv = 0                    # recv done
            
    def is_recv_right_byte(self) -> bool:
        """To judge whether a byte list is valid

        Returns:
            bool: True if valid, vice versa.
        """
        if self.buffer_len == 4 + self.data_len_recv and self.data_len_recv != 0: # sum check byte
            self.recv_check_result = self.check_value_generator(self.recv_byte_list)
            if not self.recv_check_result[0] == self.recv_byte_list[-2]:
                self.logger.error_log(f"Fail to pass sum check. Raw data is {self.recv_byte_list}, \
                    the right sum check is {self.recv_check_result[0]}, but {self.recv_byte_list[-2]} was found.")
                return False
        if self.buffer_len == 5 + self.data_len_recv and self.data_len_recv != 0: # append check byte
            if not self.recv_check_result[1] == self.recv_byte_list[-1]:
                self.logger.error_log(f"Fail to pass append check. Raw data is {self.recv_byte_list}, \
                    the right append check is {self.recv_check_result[1]}, but {self.recv_byte_list[-1]} was found.")
                return False
        if not self.recv_byte_list[0] == 0xAA:
            self.logger.error_log(f"Invalid frame head found! It is {self.recv_byte_list[0]}")
            return False
        if DEEP_DEBUG_MODE:
            if not self.recv_byte_list[1] in ADDR_ARRAY:
                self.logger.error_log(f"Invalid address found! It is {self.recv_byte_list[1]}")
                return False
            if not self.recv_byte_list[2] in ID_ARRAY:
                self.logger.error_log(f"Invalid id found! It is {self.recv_byte_list[2]}")
                return False
            if not self.recv_byte_list[3] < 40:
                self.logger.error_log(f"Data much too long! It is {self.recv_byte_list[3]}")
                return False
        return True
    
    def put_data_into_buffer(self) -> None:
        """put the recv data into buffer for ParseTable to fetch
        """
        temp = tuple(self.recv_byte_list)
        self.logger.debug_log(f"Receive byte: {self.recv_byte_list}")
        lock_recv_parse.acquire()
        recv_byte_buffer.append(temp)
        #self.logger.info_log(f"Buffer length: {len(recv_byte_buffer)}") 
        lock_recv_parse.release()


task_status_list = [0] * TASK_NUM
class CommunicationCore:
    def __init__(self, serial_obj) -> None:
        self.param_table    = [0] * len(IN_PARAM_INFO_TABLE)
        self.byte_tuple     = tuple()
        self.id             = 16
        self.data_len       = 0
        self.serial_obj: UART_Communication = serial_obj
        self.command_list   = []            # for posit CMD
        
        self.waiting_for_check = tuple() # 0 for ID, 1 for sum check, 2 for append check
        self.check_tried_flag = False
        self.check_is_pass = False
        
        self.logger = Logger("Commu")
    
    def parse_recv_bytes(self) -> None:
        while True:
            # print(f"len: {len(recv_byte_buffer)}")
            if len(recv_byte_buffer) > 0:
                lock_recv_parse.acquire()
                self.byte_tuple = recv_byte_buffer.pop(0)
                lock_recv_parse.release()
                self.data_len = self.byte_tuple[DATA_LEN_BIT]
                self.filter()
    
    def filter(self) -> None:
        #self.logger.debug_log(f"Buffer length:{self.serial_obj.serial.in_waiting}")
        self.id = self.byte_tuple[ID_BIT]
        if not self.id in CARE_ABOUTS:
            return 
        if self.id == ID_DATA_VERI:
            ID_GET = self.parse_from_segment(TYPE_UINT8, (LEN_NOBIT, LEN_UINT8), FACTO_1)
            SC_GET = self.parse_from_segment(TYPE_UINT8, (LEN_UINT8, LEN_UINT8), FACTO_1)
            AC_GET = self.parse_from_segment(TYPE_UINT8, (LEN_UINT8 * 2, LEN_UINT8), FACTO_1)
            
            while self.waiting_for_check == tuple():
                self.logger.debug(f"waiting tuple is {self.waiting_for_check} now!")
                continue
            if not (ID_GET == self.waiting_for_check[0] and SC_GET == self.waiting_for_check[1] and AC_GET == self.waiting_for_check[2]):
                self.compose_command(0, 0, True)
                lock_recv_taskimp.acquire()
                self.check_tried_flag = True
                self.check_is_pass = False
                lock_recv_taskimp.release()
                self.logger.warning_log(f"Unmatched check value! \
                                        Got ID:{ID_GET} SC:{SC_GET} AC:{AC_GET},\
                                        sent ID:{self.waiting_for_check[0]} SC:{self.waiting_for_check[1]} \
                                        AC:{self.waiting_for_check[2]}.")
            else:
                lock_recv_taskimp.acquire()
                self.check_is_pass = True
                self.check_tried_flag = True
                lock_recv_taskimp.release()
                self.logger.debug_log(f"Message ID({ID_GET}) checked Ok.")
            return 
        if self.id == ID_TASK_STATUS:
            task_index = self.parse_from_segment(TYPE_UINT8, (LEN_NOBIT, LEN_UINT8), FACTO_1)
            task_status = self.parse_from_segment(TYPE_UINT8, (LEN_UINT8, LEN_UINT8), FACTO_1)
            lock_recv_taskimp.acquire()
            task_status_list[task_index] = task_status
            lock_recv_taskimp.release()
            self.logger.debug_log(f"Task status list:{task_status_list}")
            return
            
        temp_cnt = 0
        for index, info in enumerate(IN_PARAM_INFO_TABLE):
            info = info[1]
            if not self.id == info:
                temp_cnt += 1
                continue 
            self.param_info = IN_PARAM_INFO_TABLE[index]
            param_name = self.param_info[-1]
            self.param_table[index] = self.parse_from_segment(self.param_info[2],
                                                                        (self.param_info[3],
                                                                        self.param_info[4]),
                                                                        self.param_info[5])
            #self.logger.info_log(f"Parse done, {param_name} is {self.param_table[index]}")
        if len(IN_PARAM_INFO_TABLE) - temp_cnt == 0:
            self.logger.warning_log(f"ID:{self.id} does not exist.")
            return
            
    def parse_from_segment(self,
                     type:int,
                     data_range:tuple,
                     factor:int) -> float:
        """parse the segment where data lays.

        Args:
            type (int): type of data
            data_range (tuple): the start bit and offset of the data in the data segment. You don't have to add the frame head, etc.
            factor (int): the factor to divide

        Returns:
            float: the true value of the data
        """
        general_int = int.from_bytes(self.byte_tuple
                                     [DATA_START_BIT + data_range[0]:
                                         DATA_START_BIT + data_range[0] + data_range[1]],
                                     sys.byteorder)
        if not factor == FACTO_1:
            temp = int(self.change_data_type(general_int, type)) / factor
        else:
            temp = int(self.change_data_type(general_int, type))
        return temp
    
    def change_data_type(self,
                         data:int,
                         type:int) -> int:
        """change the type of the data from the raw int one to the specific one.

        Args:
            data (int): data
            type (int): type of the data

        Returns:
            int: the data of the true type, but haven't been divided.
        """
        if type == TYPE_UINT8:
            return np.uint8(data)
        elif type == TYPE_INT8:
            return np.int8(data)
        elif type == TYPE_UINT16:
            return np.uint16(data)
        elif type == TYPE_INT16:
            return np.int16(data)
        elif type == TYPE_UINT32:
            return np.uint32(data)
        elif type == TYPE_INT32:
            return np.int32(np.int64(data))
    
    def change_parameter(self,
                         *data) -> None:
        pass
    
    def compose_command(self,
                        cmd:tuple,
                        data = None,
                        resend_flag = False) -> None:
        """compose the command

        Args:
            cmd (tuple): CMD
        """
        if not resend_flag:
            self.command_list.clear()
            temp = OUT_COMMAND_INFO_TABLE[np.logical_and(cmd[0] == OUT_COMMAND_INFO_TABLE[:, 1], cmd[1] == OUT_COMMAND_INFO_TABLE[:, 2])][0]
            if temp.size == 0:
                return 
            self.command_list.extend(temp)
            if cmd == CMD_FLY_MODE:
                self.command_list.append(data[0])
                self.command_list.extend([0] * 7)
            elif cmd == CMD_LOCK_DOWN:
                self.command_list.extend([0] * 8)
            elif cmd == CMD_HOVERING:
                self.command_list.extend([0] * 8)
            elif cmd == CMD_TAKE_OFF:
                self.data_fill(data, LEN_UINT16)
            elif cmd == CMD_LANDING:
                self.command_list.extend([0] * 8)
            elif cmd == CMD_GO_UP:
                self.data_fill(data, LEN_UINT16)
            elif cmd == CMD_GO_DOWN:
                self.data_fill(data, LEN_UINT16)
            elif cmd == CMD_DEST_HEIGHT:
                self.data_fill(data, LEN_INT32)
            elif cmd == CMD_TRANSLATION:
                self.data_fill(data, LEN_UINT8)
            elif cmd == CMD_ADJUST:
                self.data_fill(data ,LEN_INT16)
            elif cmd == CMD_BEEP:
                self.command_list.extend([0] * 8)
            elif cmd == CMD_QUERY_MODE:
                self.command_list.extend([0] * 8)
            elif cmd == CMD_LEFT_YAW:
                self.data_fill(data, LEN_UINT16)
            elif cmd == CMD_RIGHT_YAW:
                self.data_fill(data, LEN_UINT16)
        send_again = True                       # send the CMD again when a error was found
        while send_again:                       # Very likely to be a infinite loop!!!
            lock_recv_taskimp.acquire()
            self.check_is_pass = False          # the flag whether it is right
            self.check_tried_flag = False       # whether it has tried to check
            lock_recv_taskimp.release()
            sum = self.serial_obj.send(NO_SPECIFIC_TARGET, ID_CMD, self.command_list)
            self.waiting_for_check = (ID_CMD, sum[0], sum[1])
            self.logger.debug_log("A CMD has been sent. Start check.")
            while not self.check_tried_flag:
                time.sleep(0.02)
            if self.check_is_pass:
                self.logger.debug_log("CMD check pass.")
                send_again = False
            else:
                self.logger.warning_log(f"CMD check failed! Trying to send again...")

    def data_fill(self,
                  data:list,
                  len_of_byte:int) ->None:
        """get the data fill in the byte list

        Args:
            data (list): the data tuple you want to get filled
            num_of_byte (int): the len type of a single byte
        """
        l = len(data)
        for i in range(l):
            for j in range((len_of_byte - 1) * 8, -1, -8): # 0, len_of_byte * 8, 8
                self.command_list.append(((data[i]) & (0xFF << j)) >> j) #(data[i] >> j) & 0xFF
        self.command_list.extend([0] * (8 - l * len_of_byte))
