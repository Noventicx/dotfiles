#!/bin/sh
cover=$(playerctl metadata | sed "s/open\.spotify\.com/i.scdn.co/" | grep https://i.scdn.co/image | sed 's/^.*https/https/')
curl $cover --output /tmp/cover.png
info=$(playerctl metadata --format "{{ artist }} - {{ album }}")
song=$(playerctl metadata --format "{{ title }}")
notify-send "$song" "$info" --icon=/tmp/cover.png
