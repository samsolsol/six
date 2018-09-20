#!/usr/local/bin/python3.7
# -*-coding:utf-8 -*

#Ce programme va permettre de calculer des plages d'adresses pour créer des VLAN.
#Il permettra également d'automatiser la fourniture d'adresses par DHCP.

#!! Ce programme est à utiliser sur le serveur DHCP !!

import os,sys,re
from fonctions import *

# Arrêt du programme si l'utilisateur n'est pas en root

if not 'SUDO_UID' in os.environ.keys():
  print("Vous devez posséder les droits root pour utiliser ce programme")
  sys.exit(1)

else:
	print("\n## Bienvenue dans le programme d'automatisation de fourniture d'adresses ##\n")

# Validation de l'interface

ok_interface = ""

while ok_interface != "o":

	# Choix de l'interface

	interface = input("\nQuelle interface souhaitez-vous configurer?\n\n"+ get_all_interfaces() + "\n\n>>>")
	print("\n## Voici l'interface que vous avez renseigné: " + interface + " ##")
	ok_interface = input("\nVoulez-vous valider cette interface? Tapez o ou n (oui/non)\n")

# Validation de l'adresse réseau

ok_network_address = ""

while ok_network_address != "o":

	# Demande de l'adresse du réseau à l'utilisateur

	main_network_address = ""
	expression = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"

	while re.search(expression,main_network_address) is None:
		main_network_address = input("Saisissez l'adresse de votre réseau (ipv4):\n>>>")
		print("\n## Voici l'adresse de réseau que vous avez renseigné: " + main_network_address + " ##")

	ok_network_address = input("\nVoulez-vous valider cette adresse de réseau? Tapez o ou n (oui/non)\n>>>")


# Validation de la liste de VLAN

ok_vlan = ""

while ok_vlan != "o":


	# Demande du nombre de poste dans chaque VLAN

	nb_vlan = 1
	nb_ip_address = []
	netmask = []

	nb_ip_addresses = input("\nCombien de poste de travail souhaitez-vous configurer dans le VLAN 1?\n>>>")
	nb_ip_addresses = int(nb_ip_addresses)
	check_nb_ip_address = test_nb_ip_address(nb_ip_addresses)
	check_netmask = test_netmask(check_nb_ip_address)

	nb_ip_address.append(check_nb_ip_address)
	netmask.append(check_netmask)

	another_vlan = input("Voulez-vous configurer un autre VLAN? Tapez o ou n (oui/non)?\n>>>")


	# Ajout d'un nouveau VLAN

	while another_vlan == "o":
		nb_vlan = int(nb_vlan)
		nb_vlan += 1
		nb_vlan = str(nb_vlan)

		nb_ip_addresses = input("Combien de poste de travail souhaitez-vous configurer dans le VLAN " + nb_vlan + "?\n>>>")
		nb_ip_addresses = int(nb_ip_addresses)
		check_nb_ip_address = test_nb_ip_address(nb_ip_addresses)
		check_netmask = test_netmask(check_nb_ip_address)

		nb_ip_address.append(check_nb_ip_address)
		netmask.append(check_netmask)

		another_vlan = input("Voulez-vous configurer un autre VLAN? Tapez o ou n (oui/non)?\n>>>")


	# Affichage de la liste des VLAN

	print("\n## Suite à l'application des masques de sous-réseaux, voici le nombre de postes disponibles pour chaques VLAN ##\n")

	for i, elt in enumerate(nb_ip_address):
		print("Le VLAN {} sera composé de {} poste(s) de travail.".format((i+1), elt))


	# Confirmation de la liste de VLAN
	
	ok_vlan = input("\nVoulez-vous valider cette sélection? Tapez o ou n (oui/non)\n>>>")


# Insertion de l'adresse de réseau dans une liste pour séparer les octets

split_network_address = main_network_address.split(".")

# Convertion des octets en int

octet_1 = int(split_network_address[0])
octet_2 = int(split_network_address[1])
octet_3 = int(split_network_address[2])
octet_4 = int(split_network_address[3])


# Création des tableaux pour les interfaces de sous-réseau

i = 0
list_subnet = []
network_address = []
interface_address = []
user_address = []
broadcast_address = []
interface = str(interface)

nb_vlan = int(nb_vlan)

# Remplissage des tableaux pour les interfaces de sous-réseau

while i < nb_vlan:

	interface_address.append(octet_4 + 1)
	network_address.append(interface_address[i] - 1)
	user_address.append(interface_address[i] + int(nb_ip_address[i]))
	broadcast_address.append(user_address[i] + 1)
	octet_4 = broadcast_address[i] + 1

	# Fabrication d'une liste des interfaces pour éditer le fichier isc-dhcp-server

	list_subnet.append(interface + "." + str(i + 1))

	# print("auto " + interface + "." + str(i) + \
	# 	"\niface " + interface + "." + str(i) + " inet static" + \
	# 	"\naddress " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i]) + \
	# 	"\nnetmask " + netmask[i] + \
	# 	"\nnetwork " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + \
	# 	"\nbroadcast " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i]) + \
	# 	"\nvlan_raw_device " + interface + "\n")

	# Ecriture du fichier /etc/network/interfaces

	interfaces_file = open("/etc/network/interfaces","a")

	interfaces_file.write("\nauto " + interface + "." + str(i + 1) + \
		"\niface " + interface + "." + str(i + 1) + " inet static" + \
		"\n    address " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i]) + \
		"\n    netmask " + netmask[i] + \
		"\n    network " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + \
		"\n    broadcast " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i]) + \
		"\n    vlan_raw_device " + interface + "\n")

	interfaces_file.close()

	# Ecriture du fichier /etc/dhcp/dhcpd.conf

	dhcpd_files = open("/etc/dhcp/dhcpd.conf","a")

	dhcpd_files.write("\n# VLAN " + str(i + 1) + \
		"\nsubnet " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + " netmask " + netmask[i] + " {" + \
		"\n    option routers " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i]) + ";" + \
		"\n    option broadcast-address " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i]) + ";" + \
		"\n    range " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i] + 1) + " " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i] - 1) + ";" + \
		"\n}\n")

	dhcpd_files.close()

	# print("\n# VLAN " + str(i + 1) + \
	# 	"\nsubnet " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(network_address[i]) + " netmask " + netmask[i] + " {" + \
	# 	"\n    option routers " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i]) + ";" + \
	# 	"\n    option broadcast-address " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i]) + ";" + \
	# 	"\n    range " + str(octet_1) + "." + str(octet_2)+ "." + str(octet_3) + "." + str(interface_address[i] + 1) + " " + str(octet_1) + "." + str(octet_2) + "." + str(octet_3) + "." + str(broadcast_address[i] - 1) + ";" + \
	# 	"\n}")

	i += 1

# Ajout de Authoritative

dhcpd_files = open("/etc/dhcp/dhcpd.conf","a")
dhcpd_files.write("\nauthoritative")
dhcpd_files.close()

# Transformation de ma liste en str

str_list_subnet = " ".join(list_subnet)

# Ecriture du fichier /etc/default/isc-dhcp-server

isc_dhcp_server_files = open("/etc/default/isc-dhcp-server","w")
isc_dhcp_server_files.write("INTERFACES=\"" + str_list_subnet + "\"")
isc_dhcp_server_files.close()

