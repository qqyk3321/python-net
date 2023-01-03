import logging

'''
重构自定义接口

console

'''
class qqyk_debug():
    def __init__(self,console_level=2 ,file_name='./log.txt',file_mode='w',file_level=3):
        # 第一步，创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # Log等级总开关  此时是INFO
        
        # 第二步，创建一个handler，用于写入日志文件
        logfile = file_name
        fh = logging.FileHandler(logfile, mode=file_mode)  # open的打开模式这里可以进行参考
        fh.setLevel(console_level*10)  # 输出到file的log等级的开关

        # 第三步，再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(file_level*10)   # 输出到console的log等级的开关

        # 第四步，定义handler的输出格式（时间，文件，行数，错误级别，错误提示）
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 第五步，将logger添加到handler里面
        logger.addHandler(fh)
        logger.addHandler(ch)    
        self.logger=logger
    
    def debug(self,message):
        self.logger.debug(message)
    def info(self,message):
        self.logger.info(message)
    def warning(self,message):
        self.logger.warning(message)
    def error(self,message):
        self.logger.error(message)
    def critical(self,message):
        self.logger.critical(message)




# 日志级别
if __name__=="__main__":
    log=qqyk_debug()
    log.debug("DEBUG")
    log.info("INFO")
    log.warning("WARNING")
    log.critical("CRITICAL")
    log.error("ERROR")

#
# DEBUG：详细的信息,通常只出现在诊断问题上
# INFO：确认一切按预期运行
# WARNING（默认）：一个迹象表明,一些意想不到的事情发生了,或表明一些问题在不久的将来(例如。磁盘空间低”)。这个软件还能按预期工作。
# ERROR：更严重的问题,软件没能执行一些功能
# CRITICAL：一个严重的错误,这表明程序本身可能无法继续运行
