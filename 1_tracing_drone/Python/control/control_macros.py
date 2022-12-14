import platform

TASK_NUM                = 7

POS_CRTL_ROL            = 0
POS_CRTL_PIT            = 1
POS_CRTL_THR            = 2
POS_CRTL_YAWDPS         = 3
POS_CRTL_SPD_X          = 4
POS_CRTL_SPD_Y          = 5
POS_CRTL_SPD_Z          = 6

CMD_FLY_MODE    = (0x01, 0x01)
CMD_UNLOCK      = (0x00, 0x02)
CMD_LOCK_DOWN   = (0x00, 0x02)
CMD_HOVERING    = (0x00, 0x04)
CMD_TAKE_OFF    = (0x00, 0x05)
CMD_LANDING     = (0x00, 0x06)
CMD_GO_UP       = (0x02, 0x01)
CMD_GO_DOWN     = (0x02, 0x02)
CMD_ADJUST      = (0x02, 0x04)
CMD_BEEP        = (0x02, 0x05)
CMD_QUERY_MODE  = (0x02, 0x06)
CMD_LEFT_YAW    = (0X02, 0X07)
CMD_RIGHT_YAW   = (0X02, 0X08)
CMD_DEST_HEIGHT = (0x01, 0x02)
CMD_TRANSLATION = (0x02, 0x03)

# Fly mode
FLY_MODE_POS        = 0
FLY_MODE_POS_HIGH   = 1
FLY_MODE_FIX_POINT  = 2
FLY_MODE_PRO_CONTR  = 3

TASK_INDEX_TAKE_OFF = 0
TASK_INDEX_ADJUST   = 1
TASK_INDEX_FORWARD  = 2
TASK_INDEX_BEEP     = 3
TASK_INDEX_BACKWARD = 4
TASK_INDEX_LANDING  = 5

SYS = platform.platform(terse=True)