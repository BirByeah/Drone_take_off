import numpy as np

DEEP_DEBUG_MODE             = False

FRAME_HEAD                  = 0xAA

NO_SPECIFIC_TARGET          = 0xFF
ADDR_STM32                  = 0x11
ADDR_UPPER_COMPUTER         = 0xAF
ADDR_ANO_DATA_TRANSMITTER   = 0x10
ADDR_ANO_LIGHT_FLOW         = 0x22
ADDR_ANO_UWB                = 0x30
ADDR_ANO_IMU                = 0x60
ADDR_ANO_DRONE_CONTROLLER   = 0x61
ADDR_ANO_CONSOLE            = 0x66

ADDR_ARRAY        = (NO_SPECIFIC_TARGET,
                     ADDR_STM32,
                     ADDR_UPPER_COMPUTER,
                     ADDR_ANO_DATA_TRANSMITTER,
                     ADDR_ANO_LIGHT_FLOW,
                     ADDR_ANO_UWB,
                     ADDR_ANO_IMU,
                     ADDR_ANO_DRONE_CONTROLLER,
                     ADDR_ANO_CONSOLE,
                     )

ID_DATA_VERI                = 0x00
ID_INERTIA_SENSOR           = 0x01
ID_COMPASS_PRESSURE_TEMP    = 0x02
ID_POST_EULER               = 0x03
ID_POST_QUATE               = 0x04
ID_HEIGHT                   = 0x05
ID_MODE                     = 0x06
ID_VELOCITY                 = 0x07
ID_DEVIATION                = 0x08
ID_WIND_VELOCITY            = 0x09
ID_TARGET_POSE              = 0x0A
ID_TARGET_VELOCITY          = 0x0B
ID_GO_BACK                  = 0x0C
ID_VOLTAGE_CURRENT          = 0x0D
ID_PERIPHERAL               = 0x0E
ID_RBG_LIGHTNESS            = 0x0F
ID_LOG_STRING               = 0xA0
ID_LOG_STR_NUM              = 0xA1
ID_TASK_STATUS              = 0xA2 # special ID for confirming whether a task is accomplished or not.
ID_SPECIAL_DATA             = 0xA3
ID_PWM                      = 0x20
ID_POSE                     = 0x21
ID_GPS                      = 0x30
ID_POSITION_SENSOR          = 0x32
ID_VELOCITY_SENSOR          = 0x33
ID_DISTANCE_SENSOR          = 0x34
ID_REMOTE_CONTROL_DATA      = 0x40
ID_REAL_TIME_CONTROL        = 0x41
ID_ANO_LIGHT_FLOW           = 0x51
ID_GPS_POINT_READ           = 0x60
ID_GPS_POINT_WRITE          = 0x61
ID_CMD                      = 0xE0
ID_PARAM_READ               = 0xE1
ID_PARAM_WRITE              = 0xE2
ID_USER_DATA_1              = 0xF1
ID_USER_DATA_2              = 0xF2
ID_USER_DATA_3              = 0xF3
ID_USER_DATA_4              = 0xF4
ID_USER_DATA_5              = 0xF5
ID_USER_DATA_6              = 0xF6
ID_USER_DATA_7              = 0xF7
ID_USER_DATA_8              = 0xF8
ID_USER_DATA_9              = 0xF9
ID_USER_DATA_A              = 0xFA

ID_ARRAY                    = (
    ID_DATA_VERI                ,
    ID_INERTIA_SENSOR           ,
    ID_COMPASS_PRESSURE_TEMP    ,
    ID_POST_EULER               ,
    ID_POST_QUATE               ,
    ID_HEIGHT                   ,
    ID_MODE                     ,
    ID_VELOCITY                 ,
    ID_DEVIATION                ,
    ID_WIND_VELOCITY            ,
    ID_TARGET_POSE              ,
    ID_TARGET_VELOCITY          ,
    ID_GO_BACK                  ,
    ID_VOLTAGE_CURRENT          ,
    ID_PERIPHERAL               ,
    ID_RBG_LIGHTNESS            ,
    ID_LOG_STRING               ,
    ID_LOG_STR_NUM              ,
    ID_SPECIAL_DATA             ,
    ID_PWM                      ,
    ID_POSE                     ,
    ID_GPS                      ,
    ID_POSITION_SENSOR          ,
    ID_VELOCITY_SENSOR          ,
    ID_DISTANCE_SENSOR          ,
    ID_REMOTE_CONTROL_DATA      ,
    ID_REAL_TIME_CONTROL        ,
    ID_ANO_LIGHT_FLOW           ,
    ID_CMD                      ,
    ID_GPS_POINT_READ           ,
    ID_GPS_POINT_WRITE          ,
    ID_PARAM_READ               ,
    ID_PARAM_WRITE              ,
    ID_USER_DATA_1              ,
    ID_USER_DATA_2              ,
    ID_USER_DATA_3              ,
    ID_USER_DATA_4              ,
    ID_USER_DATA_5              ,
    ID_USER_DATA_6              ,
    ID_USER_DATA_7              ,
    ID_USER_DATA_8              ,
    ID_USER_DATA_9              ,
    ID_USER_DATA_A              
)

CID_FUNCTION    = 0x01
CID_CONTROL     = 0x10

ID_BIT          = 2
DATA_LEN_BIT    = 3
DATA_START_BIT  = 4
DATA_END_BIT    = -3

TYPE_UINT8      = 0
TYPE_INT8       = 1
TYPE_UINT16     = 2
TYPE_INT16      = 3
TYPE_UINT32     = 4
TYPE_INT32      = 5

LEN_NOBIT       = 0
LEN_UINT8       = 1
LEN_INT8        = 1
LEN_UINT16      = 2
LEN_INT16       = 2
LEN_UINT32      = 4
LEN_INT32       = 4

FACTO_1         = 1
FACTO_10        = 10
FACTO_100       = 100
FACTO_1000      = 1000
FACTO_10000     = 10000

TABLE_HEIGHT        = 0
TABLE_ACC_X         = 1
TABLE_ACC_Y         = 2
TABLE_ACC_Z         = 3
TABLE_SPD_X         = 4
TABLE_SPD_Y         = 5
TABLE_SPD_Z         = 6
TABLE_BATTERY       = 7
TABLE_TASK_STATUS   = 8
TABLE_AUX1          = 9         #WARNING:Those "AUX" is added but may not be used.(2022.10.22)
TABLE_AUX2          = 10
TABLE_AUX3          = 11
TABLE_AUX4          = 12
TABLE_AUX5          = 13
TABLE_AUX6          = 14
TABLE_DISPLACEMENT  = 15
TABLE_VELOCITY      = 16
TABLE_ANGLE         = 17


#the structure of this table is:
# index of the param in param_table     ID  TYPE    Start bit from DATA_LEN_BIT     BIT_LEN     FACTO
IN_PARAM_INFO_TABLE = np.array(
    (
        (TABLE_HEIGHT, ID_HEIGHT, TYPE_INT32, LEN_INT32, LEN_INT32, FACTO_1, "height"),
        (TABLE_ACC_X, ID_INERTIA_SENSOR, TYPE_INT16, LEN_NOBIT, LEN_INT16, FACTO_1, "acceleration in x"),
        (TABLE_ACC_Y, ID_INERTIA_SENSOR, TYPE_INT16, LEN_INT16, LEN_INT16, FACTO_1, "acceleration in y"),
        (TABLE_ACC_Z, ID_INERTIA_SENSOR, TYPE_INT16, LEN_INT16 * 2, LEN_INT16, FACTO_1, "acceleration in z"),
        (TABLE_SPD_X, ID_VELOCITY, TYPE_INT16, LEN_NOBIT, LEN_INT16, FACTO_1, "speed in x"),
        (TABLE_SPD_Y, ID_VELOCITY, TYPE_INT16, LEN_INT16, LEN_INT16, FACTO_1, "speed in y"),
        (TABLE_SPD_Z, ID_VELOCITY, TYPE_INT16, LEN_INT16 * 2, LEN_INT16, FACTO_1, "speed in z"),
        (TABLE_BATTERY, ID_VOLTAGE_CURRENT, TYPE_UINT16, LEN_NOBIT, LEN_UINT16, FACTO_100, "battery voltage"),
        (TABLE_TASK_STATUS, ID_TASK_STATUS, TYPE_UINT8, LEN_NOBIT, LEN_UINT8, FACTO_1, "task status"),
        (TABLE_AUX1, ID_REMOTE_CONTROL_DATA, TYPE_INT16, LEN_INT16 * 4, LEN_INT16, FACTO_1, "aux1"),
        (TABLE_AUX2, ID_REMOTE_CONTROL_DATA, TYPE_INT16, LEN_INT16 * 5, LEN_INT16, FACTO_1, "aux2"),
        (TABLE_AUX3, ID_REMOTE_CONTROL_DATA, TYPE_INT16, LEN_INT16 * 6, LEN_INT16, FACTO_1, "aux3"),
        (TABLE_AUX4, ID_REMOTE_CONTROL_DATA, TYPE_INT16, LEN_INT16 * 7, LEN_INT16, FACTO_1, "aux4"),
        (TABLE_AUX5, ID_REMOTE_CONTROL_DATA, TYPE_INT16, LEN_INT16 * 8, LEN_INT16, FACTO_1, "aux5"),
        (TABLE_AUX6, ID_REMOTE_CONTROL_DATA, TYPE_INT16, LEN_INT16 * 9, LEN_INT16, FACTO_1, "aux6"),
        (TABLE_DISPLACEMENT, ID_SPECIAL_DATA, TYPE_INT8, LEN_NOBIT, LEN_UINT8, FACTO_1, "displacement"),
        (TABLE_VELOCITY, ID_SPECIAL_DATA, TYPE_INT8, LEN_UINT8, LEN_UINT8, FACTO_1, "velocity"),
        (TABLE_ANGLE, ID_SPECIAL_DATA, TYPE_INT8, LEN_UINT8 * 2, LEN_UINT8, FACTO_1, "angle"),
    )
)

CARE_ABOUTS = (
    ID_HEIGHT,
    ID_INERTIA_SENSOR,
    ID_VELOCITY,
    ID_VOLTAGE_CURRENT,
    ID_TASK_STATUS,
    ID_REMOTE_CONTROL_DATA,
    ID_REAL_TIME_CONTROL,
    ID_DATA_VERI,
    ID_SPECIAL_DATA,
)

from control.control_macros import *

OUT_PARAM_INFO_TABLE = np.array(
    (
        (POS_CRTL_ROL, TYPE_INT16, FACTO_100),
        (POS_CRTL_PIT, TYPE_INT16, FACTO_100),
        (POS_CRTL_THR, TYPE_INT16, FACTO_1),
        (POS_CRTL_YAWDPS, TYPE_INT16, FACTO_1),
        (POS_CRTL_SPD_X, TYPE_INT16, FACTO_1),
        (POS_CRTL_SPD_Y, TYPE_INT16, FACTO_1),
        (POS_CRTL_SPD_Z, TYPE_INT16, FACTO_1)
    )
)

CMD_DATA_LEN        = 12

OUT_COMMAND_INFO_TABLE = np.array(
    (
        (CID_FUNCTION, CMD_FLY_MODE[0],     CMD_FLY_MODE[1]),
        (CID_CONTROL, CMD_UNLOCK[0],        CMD_UNLOCK[1]),
        (CID_CONTROL, CMD_LOCK_DOWN[0],     CMD_LOCK_DOWN[1]),
        (CID_CONTROL, CMD_HOVERING[0],      CMD_HOVERING[1]),
        (CID_CONTROL, CMD_TAKE_OFF[0],      CMD_TAKE_OFF[1]),
        (CID_CONTROL, CMD_LANDING[0],       CMD_LANDING[1]),
        (CID_CONTROL, CMD_ADJUST[0],        CMD_ADJUST[1]),
        (CID_CONTROL, CMD_BEEP[0],          CMD_BEEP[1]),
        (CID_CONTROL, CMD_RIGHT_YAW[0],     CMD_RIGHT_YAW[1]),
        (CID_CONTROL, CMD_LEFT_YAW[0],      CMD_LEFT_YAW[1]),
        (CID_CONTROL, CMD_DEST_HEIGHT[0],   CMD_DEST_HEIGHT[1]),
        (CID_CONTROL, CMD_TRANSLATION[0],   CMD_TRANSLATION[1]),
        (CID_CONTROL, CMD_QUERY_MODE[0],   CMD_QUERY_MODE[1]),
    )
)

"""

the param order in the table:

height
acceleration_x
acceleration_y
acceleration_z

"""