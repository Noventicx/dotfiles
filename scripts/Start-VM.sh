#! /bin/sh
# call this script with domainname as param
# to start and open it

virsh start $1
#sudo /usr/bin/virt-viewer -w $1
virt-manager --connect qemu:///system --show-domain-console $1
