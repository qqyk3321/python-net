import os 
import sys 
sys.path.append(os.getcwd())
from lib import *


old_json=example_json()
new_path=old_json.new_json_path("example_ensp.json")
ensp_para={}
for nu in range(3,7+1):
    device_name=f"LSW{nu}"
    ensp_para[device_name]=dict()
    ensp_para[device_name]['telnet_host']="127.0.0.1"
    ensp_para[device_name]['telnet_port']=2000+nu
    ensp_para[device_name]['device_port']="GigabitEthernet 0/0/1"
    ensp_para[device_name]['ssh_ip']=f"192.168.56.{nu}"
    ensp_para[device_name]['usr']="python"
    ensp_para[device_name]['passwd']="qqyk3321"
    ensp_para[device_name]['vlan']=10
with open(new_path,"w+") as fp:
    json.dump(obj=ensp_para,indent=4,fp=fp)



ssh_para={}
for nu in range(3,7+1):
    device_name=f"LSW{nu}"
    ensp_para[device_name]['telnet_host']="127.0.0.1"
    ensp_para[device_name]['telnet_port']=2000+nu
    ensp_para[device_name]['device_port']="GigabitEthernet 0/0/1"
    ensp_para[device_name]['ssh_ip']=f"192.168.56.{nu}"
    ensp_para[device_name]['usr']="python"
    ensp_para[device_name]['passwd']="qqyk3321"
    ensp_para[device_name]['vlan']=10
    '''
    for _ in range(3):
        with switch_add_ssh_by_telnet(**ssh_para) as tn:
            out=tn.get_result()
            print(out)
    '''
    




    with paramiko_ssh(ip=ensp_para[device_name]['ssh_ip'],usr=ensp_para[device_name]['usr'],passwd=ensp_para[device_name]['passwd']) as ssh:
        ssh.channel_send("sys\n")
        ssh.channel_send("interface LoopBack 0\n")
        ssh.channel_send("ip address 1.1.1.1 255.255.255.255\n")
        ssh.channel_send("return\n")

        time.sleep(3)
        ssh.channel_send("display current-configuration interface LoopBack 0\n")
        ssh.channel_send("save\n")
        ssh.channel_send("y\n")
        ssh.channel_send("\n")
        ssh.channel_send("\n")
        time.sleep(1)
        output=ssh.channel_recv(1)