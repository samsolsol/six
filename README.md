- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

- - - - - - - - - - - - - - - - - - - - - - - - - DOCUMENTATION - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



Documentation du script auto_vlan_dhcp.py

IT COMPANY

Version 1.0
Auteur samsolsol
Date 28/09/2018


Informations générales

- - - - - - - - - - - - - - - - - - - - - - - - - Le rôle - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Le rôle de ce script est de créer des vlans et de fournir les adresses de ces vlans par dhcp.

- - - - - - - - - - - - - - - - - - - - - - - - - Les avantages - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Ce script va permettre d’éviter:
les erreurs de calcul de masque de sous-réseau;
les erreurs d’écriture dans les fichiers de configuration.

Ce script va également nous permettre un gain de temps considérable lors de la mise en place de vlans.
Les caractéristiques
Le script est écrit en langage python, il utilise la version “3.7.0” du langage.
Il est utilisable sur des serveurs Debian/Ubuntu et Centos/Redhat.

Il est composé de 2 fichiers:

“auto_vlan_dhcp.py” qui correspond au script à proprement parlé
“fonctions” qui représente les fonctions utilisées dans le script

- - - - - - - - - - - - - - - - - - - - - - - - - Prérequis - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


Ce script est à utiliser sur un serveur (Debian/Ubuntu - Centos/Redhat) qui jouera le rôle de serveur DHCP.

Vérifier que les 2 fichiers sont bien exécutables avec la commande:

root@localhost /]# ls -l

S’il n’y a pas de “x” à gauche des 2 fichiers, lancer les commandes: 

root@localhost /]# chmod +x auto_vlan_dhcp.py
root@localhost /]# chmod +x fonctions.py

Le script doit être exécuté en tant que super-utilisateur (root). Si ce n’est pas le cas, le script ne se lancera pas.


- - - - - - - - - - - - - - - - - - - - - - - - - Utilisation - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


Le script va échanger avec l’utilisateur afin de recueillir des informations pour écrire dans le fichiers de configuration.

## Vérification de la distribution

Dans un premier temps, le script va déterminer quel distribution est installée sur le serveur. Tout est automatique vous n’avez rien à faire.


Vérification de la configuration
Ensuite, le script va rechercher si le paquet “isc-dhcp-server” et le paquet “vlan” ont été installés (pour une distribution Debian). Si ce n’est pas le cas l’installation va se lancer automatiquement.



Si vous êtes sous Centos, cela concerne uniquement le paquet “dhcp”.


## Choix de l’interface

Maintenant il va falloir choisir l’interface sur laquelle vous souhaitez créer vos vlans.
Toutes les interfaces présentent sur votre serveur seront listées, il vous faudra en choisir une et la réécrire après les “>>>”

Tapez “o” pour confirmer ou “n” pour choisir de nouveau une interface.

## Choix de l’adresse réseau
Vous devez ici sélectionner l’adresse ip sur laquelle vous souhaitez que vos vlans soient créés. Si l’adresse rentrée n’est pas valide, il faudra la réécrire de nouveau.

Il faut ensuite valider cette adresse avec “o” ou “n”:

## Composition des VLANS

Important: Les vlans doivent être classés du plus grand au plus petit pour que le script fonctionne !

Vous devez maintenant dire combien de postes de travail vous voulez sur le premier vlan.

Dans notre exemple, le premier fera 25 postes.


Il faut ensuite indiquer si nous voulons ajouter un vlan supplémentaire. 
Tapez “o” pour oui et “n” pour non:


Vous devez répéter cette opération autant de fois que vous voulez de vlan.

Pour notre exemple, nous avons fait 3 vlans.

Il faut maintenant confirmer la liste des vlans, “o” pour oui et “n” pour non. Si vous avez commis une erreur, tapez “n” et vous pourrez de nouveau configurer vos vlans.

Comme indiqué, les masques sont appliqués au nombre de postes désirés, ce qui vous attribuera la plupart du temps quelques adresses ip supplémentaires. Ces adresses seront disponibles pour l’ajout éventuel de postes supplémentaires.

## Ecriture des fichiers de configuration

Maintenant que les vlans ont été validés, le script va écrire dans les fichiers de configuration suivants:

Pour Ubuntu/Debian:

/etc/network/interfaces (création des sous-réseaux)
/etc/dhcp/dhcpd.conf (création des vlans)
/etc/default/isc-dhcp-server (correspondance interfaces/vlan)

Pour Centos/Redhat:

/etc/sysconfig/network-scripts/ (création des sous-réseaux)
/etc/dhcp/dhcpd.conf (création des vlans)

La configuration est terminée !

Le réseau et le service dhcp vont être relancés automatiquement.



A noter, dans le fichier dhcpd.conf une configuration standard a été appliquée. 
La voici:

max-lease-time 7200;
default-lease-time 600;
option domain-name-servers 8.8.8.8, 8.8.4.4;
ddns-update-style none;


Une fois le script exécuté, vous pourrez vous rendre dans ce fichier pour le modifier.

