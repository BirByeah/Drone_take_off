from utility.log import *

logger = Logger("setup")
try:
    from control.ControlCore import TaskImplementation
    
    taskimplementation = TaskImplementation()
    taskimplementation.task_arrangement()
    
except Exception as e:
    logger.critical_log(f"{e}")