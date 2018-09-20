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