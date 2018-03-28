import re
import os
from vlan_work import *
from common_functions import *
from name_work import *
			
def pull_cdp_output(ip,username,password,file_name):
	net_connect = make_connection (ip,username,password)
	to_doc_w (file_name, net_connect.send_command_expect('show cdp entry *'))
	net_connect.disconnect()
	

def pull_int_status	(ip,username,password,file_name):
	net_connect = make_connection (ip,username,password)
	to_doc_w (file_name, net_connect.send_command_expect('show int status'))
	int_status = normalize_sh_int_status(file_name)
	to_doc_w (file_name,"")
	for line in int_status:
		to_doc_a (file_name,line)
	net_connect.disconnect()
	
def pull_show_int(ip,username,password,file_name):
	net_connect = make_connection (ip,username,password)
	to_doc_w (file_name, net_connect.send_command_expect('show int'))
	net_connect.disconnect()

def pull_run(ip,username,password,file_name):
	net_connect = make_connection (ip,username,password)
	to_doc_w (file_name, net_connect.send_command_expect('show run'))
	net_connect.disconnect()

def get_main_uplink(ip,username,password):
	net_connect = make_connection (ip,username,password)
	try:
		gatway = get_ip (net_connect.send_command_expect("show run | i gateway"))[0]
	except:
		#"This is a Layer 3 switch, i can't handel that yet"
		return None
	command = "ping "+ gatway
	net_connect.send_command_expect(command)
	command = "show ip arp "+ gatway
	arp_table = net_connect.send_command_expect(command)
	mac = get_mac (arp_table)
	command = "show mac address-table address " + mac[0] + " | i 0"
	mac_table = net_connect.send_command_expect(command)
	mac_table = mac_table.split("\n")
	for line in mac_table:
		line = line.split(" ")
		return line[-1]

def pull_run_int(ip,username,password,interface):
	net_connect = make_connection (ip,username,password)
	command = "show run int "+interface
	int_config = net_connect.send_command_expect(command)
	return int_config

def pull_switch_int_info(show_run_file):
	all_interfaces = []
	interfaces = []
	tmp_interfaces = find_child_text (show_run_file, "interface ")
	for interface in tmp_interfaces:
	#	print (interface)
	#	print (type(interface))
		try:
			line_search = re.search('^interface',interface[0])
			if line_search != None:
				interfaces.append(interface)
		except:
			print ('\n')
			print (interface)
			print ('\n')
		
		
	
	for interface in interfaces:
		#try:
			each_interface = {}
			vlans_allowed = get_vlans_from_config_already_list(interface)
			each_interface["vlans_allowed"] = vlans_allowed
			for line in interface:
			#	print (line)
				if "interface " in line:
					line = line.lstrip(' ')
					line_search = re.search('^interface',line)
					if line_search != None:
						temp_name = remove_start(line,"interface ")
						temp_name=normalize_interface_names(temp_name)
						each_interface["name"]= temp_name
					else:
						continue
				#	print (each_interface["name"])
				if "description" in line:
					each_interface["old_description"]= remove_start(line,"description ")
				if "speed" in line:
					each_interface["speed_set"] = "True"
				if "duplex" in line:
					each_interface["duplex_set"] = "True"
				if "switchport mode trunk" in line:
					each_interface["int_type"] = "Trunk"
				if "switchport mode access" in line:
					each_interface["int_type"] = "Access"
				if "switchport access vlan" in line:
					tmp = line.split(" ")
					each_interface["access_vlan"] = tmp[-1]
				if "switchport access vlan" in line:
					each_interface['access_vlan'] = line.split(" ")[-1]
				if "switchport voice vlan" in line:
					each_interface['voice_vlan'] = line.split(" ")[-1]
				if "ip address" in line:
					if "no ip address" not in line:
						each_interface['ip'] = line.split(" ")[-2]
				if "ip address" in line:
					if "no ip address" not in line:
						each_interface['snm'] = line.split(" ")[-1]
			all_interfaces.append(each_interface)
		#except:
		#	pass
	return all_interfaces
			
		
def pull_status(line):
	#print (line)
	line = line[0]
	#print [line]
	line = line.split("is")[-1]
	#print (line)
	return (line)

					
					
	
				
	
	
	