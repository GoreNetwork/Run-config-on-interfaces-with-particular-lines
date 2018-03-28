from common_functions import *
from build_conn_base import *
from pprint import pprint

config_file = "config_lines.txt"


for ip in ips:
    print (ip)
    net_connect = make_connection(ip, username, password)
    running_conf = run_command_on_net_connect(net_connect,'show run')
    running_conf = running_conf.split("\n")
    #Finds 'interface' lines with 'ip helper-address 116.113.64.89' children
    interfaces = find_parent_with_child("interface", "ip helper-address 116.113.64.89", running_conf)
    for interface in interfaces:
        conf_list = [interface]
        config_data = read_doc_list(config_file)
        for line in config_data:
            line = line.strip()
            conf_list.append(line)
        net_connect.send_config_set(conf_list)

        pprint (conf_list)
    print (run_command_on_net_connect(net_connect, 'write mem'))