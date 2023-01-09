from lib import *
import socket
import paramiko
json_lib=example_json()
ensp_para_path=json_lib.get_json_path(1)
with open(ensp_para_path,"r+") as fp:
    ensp_para=json.load(fp=fp)
print(ensp_para)
switch_with_authentication_issue=[]
ssh_channel_list=[""]*10
for nu in range(3,7+1):
    device_name=f"LSW{nu}"
    try:
        with paramiko_ssh(ip=ensp_para[device_name]['ssh_ip'],usr=ensp_para[device_name]['usr'],passwd=ensp_para[device_name]['passwd']) as ensp_para[device_name]['ssh_channel']:
            ssh:paramiko_ssh=ensp_para[device_name]['ssh_channel']
            ssh.channel_send("display vlan\n")
            time.sleep(1)
            output=ssh.channel_recv(1)
    except paramiko.ssh_exception.AuthenticationException:
        print(ensp_para[device_name]['ssh_ip'] + "用户验证失败！")
        switch_with_authentication_issue.append(ensp_para[device_name]['ssh_ip'])
    except socket.error:
        print(ensp_para[device_name]['ssh_ip'] + "目标不可达！")
        switch_with_authentication_issue.append(ensp_para[device_name]['ssh_ip'])