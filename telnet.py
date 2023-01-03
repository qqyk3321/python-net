#import os
from qqyklog import qqyk_debug
import telnetlib
import time


class ensp_telnet():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__connect()
    def __connect(self,):
        self.tn = telnetlib.Telnet(host=self.host, port=self.port)
    def send_cmd(self, cmd:str):
        self.tn.write(cmd.encode('utf-8') + b'\n')
    def get_result(self,wait_time=1):
        time.sleep(wait_time)   # 针对单条回显过多，添加等待时间
        out = self.tn.read_very_eager().decode('utf-8')
        # 回显处理，只保留查询到的结果，过滤掉查询输入字符
        return out
class setup_ssh(ensp_telnet):
    def __init__(self,host,port,eth_ip,eth_port,usrname,passwd,):
        super().__init__(host,port)
        self.eth_ip=eth_ip
        self.eth_port=eth_port
        self.usrname=usrname
        self.passwd=passwd
        self.cmd_list=['']
    def write_cmd

if __name__ == "__main__":

    ip = "127.0.0.1"
    port = 2000
    tn=ensp_telnet()
    
    tn.read_until
    #tn.write('at'.encode('utf-8') + b'\n')

    # time.sleep(1)

    # res=tn.read_all()
    #res = tn.read_very_eager().decode('utf-8')

    