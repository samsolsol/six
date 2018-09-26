#!/usr/local/bin/python3.7
# -*-coding:utf-8 -*

import os

# Fonctions

def get_all_interfaces():

    list = os.listdir('/sys/class/net/')
   
    return " ".join(list)


def test_nb_ip_address(nb_ip_address):

	if nb_ip_address > 0 and nb_ip_address < 6:
		return 5

	if nb_ip_address >= 6 and nb_ip_address < 14:
		return 13

	if nb_ip_address >= 14 and nb_ip_address < 30:
		return 29

	if nb_ip_address >= 30 and nb_ip_address < 62:
		return 61

	if nb_ip_address >= 62 and nb_ip_address < 126:
		return 125

	if nb_ip_address >= 126 and nb_ip_address < 254:
		return 253


def test_netmask(nb_ip_address):
	
	if nb_ip_address == 5:
		return "255.255.255.248"

	if nb_ip_address == 13:
		return "255.255.255.240"

	if nb_ip_address == 29:
		return "255.255.255.224"

	if nb_ip_address == 61:
		return "255.255.255.192"

	if nb_ip_address == 125:
		return "255.255.255.128"

	if nb_ip_address == 253:
		return "255.255.255.0"

# Ecriture du fichier /etc/network/interfaces
def write_interfaces_debian(interface, i, octet_1, octet_2, octet_3, interface_address, network_address, broadcast_address, netmask):

	interfaces_file = open("/etc/network/interfaces","a")
	interfaces_file.write("\nauto " + interface + "." + str(i + 1) + \
		"\niface " + interface + "." + str(i + 1) + " inet static" + \
		"\n    address " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i]) + \
		"\n    netmask " + netmask[i] + \
		"\n    network " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + \
		"\n    broadcast " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i]) + \
		"\n    vlan_raw_device " + interface + "\n")

	interfaces_file.close()

# def display_interfaces_debian(interface, i, octet_1, octet_2, octet_3, interface_address, network_address, broadcast_address, netmask):

# 	print("\nauto " + interface + "." + str(i + 1) + \
# 		"\niface " + interface + "." + str(i + 1) + " inet static" + \
# 		"\n    address " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i]) + \
# 		"\n    netmask " + netmask[i] + \
# 		"\n    network " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + \
# 		"\n    broadcast " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i]) + \
# 		"\n    vlan_raw_device " + interface + "\n")

# Ecriture dans le dossier /etc/sysconfig/network-scripts/
def write_main_interface(interface):
	
	interface_file = open("/etc/sysconfig/network-scripts/ifcfg-" + interface, "w")
	interface_file.write("\nDEVICE=" + interface + \
		"\nTYPE=Ethernet" + \
		"\nBOOTPROTO=none" + \
		"\nONBOOT=yes")
	
	interface_file.close()


def write_interfaces_centos(i, interface, netmask, octet_1, octet_2, octet_3, interface_address, network_address):
	
	interfaces_file = open("/etc/sysconfig/network-scripts/ifcfg-" + interface + "." + str(i + 1) , "a")
	interfaces_file.write("\nDEVICE=" + interface + "." + str(i + 1) + \
		"\nBOOTPROTO=none" + \
		"\nONBOOT=yes" + \
		"\nIPADDR=" + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(interface_address[i]) + \
		"\nNETMASK=" + netmask[i] + \
		"\nNETWORK=" + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + \
		"\nVLAN=yes")

	interfaces_file.close()

# def display_interfaces_centos(i, interface, netmask, octet_1, octet_2, octet_3, interface_address, network_address):

# 	print("\nDEVICE=" + interface + "." + str(i + 1) + \
# 		"\nBOOTPROTO=none" + \
# 		"\nONBOOT=yes" + \
# 		"\nIPADDR=" + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(interface_address[i]) + \
# 		"\nNETMASK=" + netmask[i] + \
# 		"\nNETWORK=" + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + \
# 		"\nVLAN=yes")

# Ecriture du fichier /etc/dhcp/dhcpd.conf
def write_dhcpd_debian(i, octet_1, octet_2, octet_3, interface_address, network_address, broadcast_address, netmask):
	
	dhcpd_files = open("/etc/dhcp/dhcpd.conf","a")
	dhcpd_files.write("\n# VLAN " + str(i + 1) + \
		"\nsubnet " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + " netmask " + netmask[i] + " {" + \
		"\n    option routers " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i]) + ";" + \
		"\n    option broadcast-address " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i]) + ";" + \
		"\n    range " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i] + 1) + " " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i] - 1) + ";" + \
		"\n}\n")

	dhcpd_files.close()

# def display_dhcpd_debian(i, octet_1, octet_2, octet_3, interface_address, network_address, broadcast_address, netmask):

# 	print("\n# VLAN " + str(i + 1) + \
# 		"\nsubnet " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + " netmask " + netmask[i] + " {" + \
# 		"\n    option routers " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i]) + ";" + \
# 		"\n    option broadcast-address " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i]) + ";" + \
# 		"\n    range " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i] + 1) + " " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i] - 1) + ";" + \
# 		"\n}\n")

# Ecriture du fichier /etc/dhcp/dhcpd.conf
def write_dhcpd_centos(i, octet_1, octet_2, octet_3, interface_address, network_address, broadcast_address, netmask):
	
	dhcpd_files = open("/etc/dhcp/dhcpd.conf","a")
	dhcpd_files.write("\n\n# VLAN " + str(i + 1) + \
		"\nsubnet " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + " netmask " + netmask[i] + " {" + \
		"\n    option routers " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i]) + ";" + \
		"\n    option broadcast-address " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i]) + ";" + \
		"\n    range " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i] + 1) + " " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i] - 1) + ";" + \
		"\n}\n")

	dhcpd_files.close()

# def display_dhcpd_centos(i, octet_1, octet_2, octet_3, interface_address, network_address, broadcast_address, netmask):

# 	print("\n\n# VLAN " + str(i + 1) + \
# 		"\nsubnet " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + " netmask " + netmask[i] + " {" + \
# 		"\n    option routers " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i]) + ";" + \
# 		"\n    option broadcast-address " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i]) + ";" + \
# 		"\n    range " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i] + 1) + " " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i] - 1) + ";" + \
# 		"\n}\n")

# Ajout config à dhcpd.conf
def write_dhcpd_infos():
	
	dhcpd_files = open("/etc/dhcp/dhcpd.conf","a")
	dhcpd_files.write("\noption domain-name-servers 8.8.8.8, 8.8.4.4;\nauthoritative;\nddns-update-style none;\nmax-lease-time 7200;\ndefault-lease-time 600;")
	
	dhcpd_files.close()


# Ecriture du fichier /etc/default/isc-dhcp-server
def write_isc_dhcp_server(str_list_subnet):
	
	isc_dhcp_server_files = open("/etc/default/isc-dhcp-server","w")
	isc_dhcp_server_files.write("INTERFACES=\"" + str_list_subnet + "\"")
	
	isc_dhcp_server_files.close()

