#import os
from lib.qqyklog import qqyk_debug
import telnetlib
import time
import json

class ensp_telnet():
    '''
    基类,添加最普通的参数
    '''
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.__connect()
    def __enter__(self):
        '''
        already finished in __connect
        '''
        return self
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        # 通过exc_type参数接收到的值，来判断程序执行是否出现异常
        # 如果是None,说明没有异常
        if exc_type == None:
            print('正常执行')
        else:
            # 否则出现异常，可以选择怎么处理异常
            print('Type: ', exc_type)
            print('Value:', exc_val)
            print('TreacBack:', exc_tb)
        # 返回值决定了捕获的异常是否继续向外抛出
        # 如果是False那么就会继续向外抛出，程序会看到系统提示的异常信息
        # 如果是True不会向外抛出,程序看不到系统提示信息，只能看到else中的输出
        return True

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
    def close(self):
        self.tn.close()
class ar_add_ssh_by_telnet(ensp_telnet):
    '''
    GigabitEthernet 0/0/0
    '''
    def __init__(self,telnet_host,telnet_port,device_port,ssh_ip,usr,passwd):
        super().__init__(telnet_host, telnet_port)
        self.device_port=device_port
        self.ssh_ip=ssh_ip
        self.usr=usr
        self.passwd=passwd
        self.__generate_cmd()
        self.send_cmd(self.cmd)
    def __generate_cmd(self):
        '''
        读取参数并导入
        '''
        cmd='''system-view
interface {device_port}
ip address {ssh_ip} 24
quit
stelnet server enable
rsa local-key-pair create
y


aaa
local-user {usr} password cipher {passwd}
local-user {usr} privilege level 15
local-user {usr} service-type ssh
quit
user-interface vty 0 4
authentication-mode aaa
protocol inbound all

quit
ssh user {usr} authentication-type all
quit
        '''.format(device_port=self.device_port,ssh_ip=self.ssh_ip,usr=self.usr,passwd=self.passwd)
    
        #print(repr(cmd))
        self.cmd=cmd

class ar_add_ssh_by_telnet_json(ar_add_ssh_by_telnet):
    '''
    load para by json
    example json file: ar_ssh_para_example.json
    '''
    def __init__(self,json_file):
        with open(json_file,'r+') as fp:
            para_list=json.load(fp)
        super().__init__(**para_list)


class switch_add_ssh_by_telnet(ensp_telnet):
    '''
    和AR的区别在于ip是绑定在VLAN上的,不是绑定在port上的
    vlan 10
    GigabitEthernet 0/0/1
    '''
    def __init__(self,telnet_host,telnet_port,device_port,ssh_ip,usr,passwd,vlan):
        super().__init__(telnet_host, telnet_port)
        self.device_port=device_port
        self.ssh_ip=ssh_ip
        self.usr=usr
        self.passwd=passwd
        self.vlan=vlan
        self.__generate_cmd()
        self.send_cmd(self.cmd)
    def __generate_cmd(self):
        '''
        读取参数并导入
        '''
        cmd='''system-view
vlan batch {vlan}
interface vlan {vlan}
ip address {ssh_ip} 24
quit
interface {device_port}
port link-type access 
port default vlan {vlan}
quit
stelnet server enable
rsa local-key-pair create
y

aaa
local-user {usr} password cipher {passwd}
local-user {usr} privilege level 15
local-user {usr} service-type ssh
quit
user-interface vty 0 4
authentication-mode aaa
protocol inbound all

quit
ssh  authentication-type  default password

quit
        '''.format(vlan=self.vlan,device_port=self.device_port,ssh_ip=self.ssh_ip,usr=self.usr,passwd=self.passwd)
    
        #print(repr(cmd))
        self.cmd=cmd       
class switch_add_ssh_by_telnet_json(switch_add_ssh_by_telnet):
    '''
    load para by json
    example json file: ar_ssh_para_example.json
    '''
    def __init__(self,json_file):
        with open(json_file,'r+') as fp:
            para_list=json.load(fp)
        super().__init__(**para_list)
if __name__ == "__main__":

    '''
    可以从json读取参数
    '''
    
    ssh_para={}
    ssh_para['telnet_host']="127.0.0.1"
    ssh_para['telnet_port']=2004
    ssh_para['device_port']="GigabitEthernet 0/0/1"
    ssh_para['ssh_ip']="192.168.56.9"
    ssh_para['usr']="python"
    ssh_para['passwd']="qqyk3321"
    ssh_para['vlan']=10
    with open('switch_ssh_para_example.json',"w+") as fp:

        json.dump(ssh_para,indent=4,fp=fp)
 



    with switch_add_ssh_by_telnet(**ssh_para) as tn:
        out=tn.get_result()
        print(out)
'''
    tn.send_cmd('system-view')
    tn.send_cmd('interface GigabitEthernet 0/0/0')
    tn.send_cmd('ip address 192.168.56.8 24')
    tn.send_cmd('quit')
    tn.send_cmd('stelnet server enable')
    tn.send_cmd('rsa local-key-pair create')
    tn.send_cmd('\n')
    tn.send_cmd('\n')
    tn.send_cmd('\n')
    tn.send_cmd('aaa')
    tn.send_cmd('local-user python password cipher qqyk3321')
    tn.send_cmd('local-user python privilege level 15')
    tn.send_cmd('local-user python service-type ssh')
    tn.send_cmd('quit')
    tn.send_cmd('user-interface vty 0 4')
    tn.send_cmd('protocol inbound ssh')
    tn.send_cmd('authentication-mode aaa')
    tn.send_cmd('quit')
    tn.send_cmd('ssh user python authentication-type all')
    tn.send_cmd('quit')
'''
    
    

        
    #tn.write('at'.encode('utf-8') + b'\n')

    # time.sleep(1)

    # res=tn.read_all()
    #res = tn.read_very_eager().decode('utf-8')

    