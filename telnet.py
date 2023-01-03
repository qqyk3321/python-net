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
    def continuous_send(self,cmd_list):
        for cmd in cmd_list:
            self.send_cmd(cmd)


if __name__ == "__main__":

    ip = "127.0.0.1"
    port = 2002
    tn=ensp_telnet(ip,port)
    tn.send_cmd('system-view')
    tn.send_cmd('interface GigabitEthernet 0/0/0')
    tn.send_cmd('ip address 192.168.56.7 24')
    tn.send_cmd('quit')
    tn.send_cmd('stelnet server enable')
    tn.send_cmd('rsa local-key-pair create')
    tn.send_cmd('y')
    tn.send_cmd('\n')
    tn.send_cmd('aaa')
    tn.send_cmd('local-user python password cipher qqyk3321')
    tn.send_cmd('local-user python privilege level 15')
    tn.send_cmd('local-user python service-type ssh')
    tn.send_cmd('quit')
    tn.send_cmd('user-interface vty 0 4')
    tn.send_cmd('protocol inbound ssh')
    tn.send_cmd('quit')
    tn.send_cmd('ssh user python authentication-type all')
    

    out=tn.get_result()
    print(out)
    #tn.write('at'.encode('utf-8') + b'\n')

    # time.sleep(1)

    # res=tn.read_all()
    #res = tn.read_very_eager().decode('utf-8')

    