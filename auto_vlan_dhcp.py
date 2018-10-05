#!/usr/local/bin/python3.7
# -*-coding:utf-8 -*

#Ce programme va permettre de calculer des plages d'adresses pour créer des VLAN.
#Il permettra également d'automatiser la fourniture d'adresses par DHCP.

#!! Ce programme est à utiliser sur le serveur DHCP !!

import os,sys,re,time
from fonctions import *
from operator import *

# Arrêt du programme si l'utilisateur n'est pas en root
if os.geteuid() != 0:
	print("Vous devez posséder les droits root pour utiliser ce programme !")
	sys.exit(1)

print("\n## Bienvenue dans le programme d'automatisation de fourniture d'adresses ##\n")

choix_distrib = ""

# Vérification de la distribution linux
print("Nous allons vérifier sur quelle distribution est votre serveur...\n")

time.sleep(2)

choix_distrib = check_distrib(choix_distrib)

time.sleep(2)

# Verification de l'installation du paquet "isc-dhcp-server" et du paquet "vlan"
if choix_distrib == "d":
	
	print("\nVérification de la présence des paquets 'vlan' et 'isc-dhcp-server'.\n\nS'il ne sont pas installés, cela sera fait automatiquement!")

	time.sleep(5)

	check_packet("isc-dhcp-server", choix_distrib)
	check_packet("vlan", choix_distrib)

# Verification de l'installation du paquet dhcpd
else:
	
	print("\nVérification de la présence du paquet 'dhcp'.\n\nS'il n'est pas installé, cela sera fait automatiquement!")

	time.sleep(5)

	check_packet("dhcp", choix_distrib)

time.sleep(2)

# Validation de l'interface
ok_interface = ""

while ok_interface != "o":

	# Choix de l'interface
	interface = input("\nQuelle interface souhaitez-vous configurer?\n\n"+ get_all_interfaces() + "\n\n>>>")
	print("\n## Voici l'interface que vous avez renseigné: " + interface + " ##")

	# Demande de validation de l'interface
	ok_interface = input("\nVoulez-vous valider cette interface? Tapez o ou n (oui/non)\n>>>")

# Validation de l'adresse réseau
ok_network_address = ""

# La boucle s'arretera quand l'utilisateur ne voudra plus ajouter de VLAN
while ok_network_address != "o":

	# Demande puis vérification de l'adresse du réseau à l'utilisateur
	main_network_address = ""
	expression = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"

	while re.search(expression,main_network_address) is None:
		main_network_address = input("Saisissez l'adresse de votre réseau (ipv4):\n>>>")

		# Affichage de l'adresse à l'utilisateur
		print("\n## Voici l'adresse de réseau que vous avez renseigné: " + main_network_address + " ##")

	# Demande de validation de l'adresse réseau
	ok_network_address = input("\nVoulez-vous valider cette adresse de réseau? Tapez o ou n (oui/non)\n>>>")


# Validation de la liste de VLAN
ok_vlan = ""

max_ip_address = 0

while ok_vlan != "o":

	another_vlan = "o"
	nb_vlan = 0
	nb_ip_address = []
	netmask = []

	print("\nMerci de classer les vlans du plus grand au plus petit ! \n")

	time.sleep(4)

	# Ajout d'un nouveau VLAN
	while another_vlan == "o":
		nb_vlan = str(int(nb_vlan) + 1)

		# Demande du nombre de poste dans chaque VLAN
		nb_ip_addresses = input("Combien de poste de travail souhaitez-vous configurer dans le VLAN " + nb_vlan + "?\n>>>")
		nb_ip_addresses = int(nb_ip_addresses)

		# Convertion du nombre de poste "utilisateur" en postes réels après l'application du masque de sous-réseau
		check_nb_ip_address = test_nb_ip_address(nb_ip_addresses)
		check_netmask = test_netmask(check_nb_ip_address)

		nb_ip_address.append(check_nb_ip_address)
		netmask.append(check_netmask)

		another_vlan = input("Voulez-vous configurer un autre VLAN? Tapez o ou n (oui/non)?\n>>>")

	# Calcul du nombre total de poste (hors adresses de réseau et de broadcast)
	for elt in nb_ip_address:
		max_ip_address += int(elt)

	# Vérification du nombre de poste à configurer
	if max_ip_address < 235:

		# Affichage de la liste des VLAN
		print("\n## Suite à l'application des masques de sous-réseaux, voici le nombre de postes disponibles pour chaques VLAN ##\n")

		for i, elt in enumerate(nb_ip_address):
			print("Le VLAN {} sera composé de {} poste(s) de travail.".format((i+1), elt))
		
		# Demande de confirmation de la liste de VLAN
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

	# Calcul des différentes adresses
	interface_address.append(octet_4 + 1)
	network_address.append(interface_address[i] - 1)
	user_address.append(interface_address[i] + int(nb_ip_address[i]))
	broadcast_address.append(user_address[i] + 1)
	octet_4 = broadcast_address[i] + 1

	# Fabrication d'une liste des interfaces pour éditer le fichier isc-dhcp-server (Debian)
	list_subnet.append(interface + "." + str(i + 1))
		

	# Ecriture du fichier /etc/network/interfaces
	if choix_distrib == "d":

		write_interfaces_debian(interface, i, octet_1, octet_2, octet_3, interface_address, network_address, broadcast_address, netmask)

	# Ecriture dans le dossier /etc/sysconfig/network-scripts
	else:

		write_main_interface(interface)
		write_interfaces_centos(i, interface, netmask, octet_1, octet_2, octet_3, interface_address, network_address)
		
	# Ecriture du fichier /etc/dhcp/dhcpd.conf
	if choix_distrib == "d":

		write_dhcpd_debian(i, octet_1,octet_2, octet_3,interface_address, network_address, broadcast_address, netmask)
	
	else:

		write_dhcpd_centos(i, octet_1,octet_2, octet_3,interface_address, network_address, broadcast_address, netmask)

	i += 1

# Ajout d'information générales à dhcpd.conf
write_dhcpd_infos()

# Ecriture du fichier /etc/default/isc-dhcp-server + affichage restart network et dhcp
if choix_distrib == "d":

	write_isc_dhcp_server(list_subnet)

	time.sleep(2)

	print("\n\nLe réseau puis le service dhcp vont maintenant être relancés")

	os.system('systemctl restart networking')
	os.system('systemctl restart isc-dhcp-server.service')

	time.sleep(2)

	print("La configuration est maintenant terminée !!")

else:

	time.sleep(2)

	print("\n\nLe réseau puis le service dhcp vont maintenant être relancés")

	os.system('systemctl restart network')
	os.system('systemctl restart dhcpd')

	time.sleep(2)

	print("La configuration est maintenant terminée !!")