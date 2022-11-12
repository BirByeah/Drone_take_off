import logging

class Logger:
    def __init__(self,
                 logger_name:str,
                 filename:str = "drone_rasp_serial.log",
                 logger_level:int = logging.DEBUG) -> None:
        self.filename = filename
        sh = logging.StreamHandler(stream=None)
        fh = logging.FileHandler(filename,mode='a',encoding="UTF-8",delay=False)
        fmt = logging.Formatter(fmt="%(asctime)s - %(name)-5s - %(levelname)-4s - %(message)s"
                                ,datefmt="%Y/%m/%d %H:%M:%S")

        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logger_level)
        self.logger.addHandler(fh)
        self.logger.debug("#")

        fh.setFormatter(fmt)
        sh.setFormatter(fmt)
        self.logger.addHandler(sh)

    def debug_log(self,
                 message):
        self.logger.debug(f"{message}")

    def info_log(self,
                 message):
        self.logger.info(f"{message}")
        
    def warning_log(self,
                    message):
        self.logger.warning(f"{message}")
        
    def error_log(self,
                  message):
        self.logger.error(f"{message}")  
        
    def exception_log(self,
                      message):
        self.logger.exception(f"{message}")
        raise Exception(f"Please see the details in {self.filename}.")
        
    def critical_log(self,
                     message):
        self.logger.critical(f"{message}")
        raise Exception(f"Please see the details in {self.filename}.")
        