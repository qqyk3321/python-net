import paramiko
import time
import json




class paramiko_ssh():
    '''
    
    '''

    def __init__(self,ip="192.168.1.176",usr="qqyk321",passwd="qqyk3321",para_json=None):
        if(para_json==None):
            self.__init_para__(ip,usr,passwd)
        else:
            with open(para_json,"r+") as fd:
                para=json.load(fd)
            self.__init_para__(**para)
        self.__paramiko_init_sshclient()
        
        self.__paramiko_ssh_channel()
    def __enter__(self):
        '''
        already finished in __connect
        '''
        return self
        pass
    def close(self):
        print(f"{self.ip} channel of ssh close")
        self.channel.close()
        self.ssh_client.close()
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
    def __close_show__(self,):
        print(f"{self.ip} channel of ssh close")
    def __init_para__(self,ip,usr,passwd):
        self.ip=ip
        self.usr=usr
        self.passwd=passwd
    def __paramiko_init_sshclient(self):
        self.ssh_client=paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=self.ip, username=self.usr,  \
                    password=self.passwd, look_for_keys=False)
    def __paramiko_ssh_channel(self,):
        self.channel = self.ssh_client.invoke_shell()
    def channel_send(self,cmd):
        '''
        cmd need endwith \\n
        '''
        self.channel.send(cmd)

    def channel_recv(self,show=None):
        output = self.channel.recv(65535).decode('utf-8')
        output=self.__display_with_ip(output)
        if(show!=None):
            print(output)
        return output
    def __display_with_ip(self,output:str):
        output_list=output.split('\n')
        for nu in range(len(output_list)):
            output_list[nu]=f"{self.ip}>>  "+output_list[nu]
        return ('\n').join(output_list)



if __name__=="__main__":
        
    import lib.ensp_telnet as ensp_telnet
    if 1:
        with ensp_telnet.switch_add_ssh_by_telnet_json("example_switch_ssh_para.json") as tn:
            out=tn.get_result()
            print(out)




    with paramiko_ssh(para_json="example_ssh_para.json") as ssh:
        ssh.channel_send("sys\n")
        ssh.channel_send("interface LoopBack 0\n")
        ssh.channel_send("ip address 1.1.1.1 255.255.255.255\n")
        ssh.channel_send("return\n")

        time.sleep(3)
        ssh.channel_send("display current-configuration interface LoopBack 0\n")
        time.sleep(1)
        output=ssh.channel_recv(1)
        

'''
    # paramiko 联机“套路”
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, username=username,  \
                    password=password, look_for_keys=False)
    print("Successfully connected to ",ip)

    # 注：这些代码中间，我们可以随时加插 print(xx) 进行测试，术语叫“调试”。

    command = ssh_client.invoke_shell()
    command.send("sys\n")
    command.send("interface LoopBack 0\n")
    command.send("ip address 1.1.1.1 255.255.255.255\n")
    command.send("return\n")
    command.send("save\n")
    command.send("y\n")

    # 这种场景，paramiko 模块模仿人工进行联机操作。

    time.sleep(3)
    command.send("display this\n")    # 这里的 dis this 查询意义不大，也可以修改为如下命令，去掉注释即可执行。
    # command.send("display current-configuration interface LoopBack 0\n")
    time.sleep(1)

    # 调用延迟的目的也是等待设备响应和回显信息，否则执行太快，回显信息会“捞”不全。
    output = command.recv(65535)
    print(output.decode("ascii"))   # 回显信息涉及到编解码。

    # 操作完成后，需要断开 SSH 连接。

    # 关闭 invoke_shell。
    command.close()
    # 关闭 ssh 客户端。
    ssh_client.close()
'''