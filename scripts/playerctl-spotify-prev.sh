#!/bin/sh

if spt pb -s -f '%d %s' | grep -q "Stereo Anlage" && playerctl status | grep "Stopped"
then
	spt pb -p
else
	playerctl previous
fi
