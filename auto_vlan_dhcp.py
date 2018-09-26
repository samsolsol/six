#!/usr/local/bin/python3.7
# -*-coding:utf-8 -*

#Ce programme va permettre de calculer des plages d'adresses pour créer des VLAN.
#Il permettra également d'automatiser la fourniture d'adresses par DHCP.

#!! Ce programme est à utiliser sur le serveur DHCP !!

import os,sys,re,time
from fonctions import *
from operator import *

# Arrêt du programme si l'utilisateur n'est pas en root

#if not 'SUDO_UID' in os.environ.keys():
#  print("Vous devez posséder les droits root pour utiliser ce programme")
#  sys.exit(1)

#else:
print("\n## Bienvenue dans le programme d'automatisation de fourniture d'adresses ##\n")
	
choix_distrib = input("\n\nSur quelle type de serveur êtes-vous? Tapez d pour debian ou c pour centos/redhat\n>>>")

# Verification de l'installation du paquet "vlan"
if choix_distrib == "d":
	vlan_paquet = input("Avez-vous installé le paquet vlan 'o' ou 'n' (oui/non) ? \n>>>")

	if vlan_paquet == "n":
		print("Le paquet vlan va être installé dans quelques secondes !")

		time.sleep(5)

		os.system('apt-get install vlan')

# Validation de l'interface
ok_interface = ""

while ok_interface != "o":

	# Choix de l'interface
	interface = input("\nQuelle interface souhaitez-vous configurer?\n\n"+ get_all_interfaces() + "\n\n>>>")
	print("\n## Voici l'interface que vous avez renseigné: " + interface + " ##")
	ok_interface = input("\nVoulez-vous valider cette interface? Tapez o ou n (oui/non)\n>>>")

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
max_ip_address = 0

while ok_vlan != "o":

	# Demande du nombre de poste dans chaque VLAN
	nb_vlan = 1
	nb_ip_address = []
	netmask = []

	print("\nMerci de classer les vlans du plus grand au plus petit ! \n")
	time.sleep(5)

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


	for elt in nb_ip_address:
		max_ip_address += int(elt)

	if max_ip_address < 235:

		# Affichage de la liste des VLAN
		print("\n## Suite à l'application des masques de sous-réseaux, voici le nombre de postes disponibles pour chaques VLAN ##\n")

		# Tri du plus grand au plus petit VLAN
		#nb_ip_address = sorted(nb_ip_address, reverse=True)

		for i, elt in enumerate(nb_ip_address):
			print("Le VLAN {} sera composé de {} poste(s) de travail.".format((i+1), elt))
		

		# Confirmation de la liste de VLAN
		ok_vlan = input("\nVoulez-vous valider cette sélection? Tapez o ou n (oui/non)\n>>>")

	else:

		print("\n\n ! ! ! ! Le nombre de postes est trop élevé, merci de recommencer ! ! ! ! \n\n")
		ok_vlan = "n"

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

	# Ecriture de l'interface principale pour la distrib centos
	if choix_distrib == "c":
		write_main_interface(interface)

	# Ecriture du fichier /etc/network/interfaces
	if choix_distrib == "d":

		write_interfaces_debian(interface, i, octet_1, octet_2, octet_3, interface_address, network_address, broadcast_address, netmask)

	# Ecriture dans le dossier /etc/sysconfig/network-scripts
	else:

		write_interfaces_centos(i, interface, netmask, octet_1, octet_2, octet_3, interface_address, network_address)
		
	# Ecriture du fichier /etc/dhcp/dhcpd.conf
	if choix_distrib == "d":

		write_dhcpd_debian(i, octet_1,octet_2, octet_3,interface_address, network_address, broadcast_address, netmask)
	
	else:

		write_dhcpd_centos(i, octet_1,octet_2, octet_3,interface_address, network_address, broadcast_address, netmask)

	i += 1

# Ajout dconfig à dhcpd.conf
write_dhcpd_infos()

# Transformation de ma liste en str
str_list_subnet = " ".join(list_subnet)

# Ecriture du fichier /etc/default/isc-dhcp-server + restart network et dhcp
if choix_distrib == "d":

	write_isc_dhcp_server(str_list_subnet)

	print("La configuration est terminée !!")
	time.sleep(2)
	print("Vous devez maintenant relancer le réseau puis le service dhcp")
	time.sleep(4)
	print("\n#### Commande network: systemctl restart networking\n" + \
		"\n#### Commande dhcp: systemctl restart isc-dhcp-server.service\n")

else:

	print("La configuration est terminée !!")
	time.sleep(2)
	print("Vous devez maintenant relancer le réseau puis le service dhcp")
	time.sleep(4)
	print("\n#### Commande network: systemctl restart network\n" + \
		"\n#### Commande dhcp: systemctl restart dhcpd\n")
