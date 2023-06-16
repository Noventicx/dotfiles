#!/bin/sh
#if playerctl -l | grep "spotifyd"
#then
#	if gdbus introspect --session --dest org.mpris.MediaPlayer2.spotifyd --object-path /org/mpris/MediaPlayer2 | grep PlaybackStatus | grep Paused
#	then
#		playerctl --player spotifyd play
#	elif gdbus introspect --session --dest org.mpris.MediaPlayer2.spotifyd --object-path /org/mpris/MediaPlayer2 | grep PlaybackStatus
#	then
#		playerctl --player spotifyd pause
#	else
#		echo test
#	fi
#else
#	playerctl play-pause
#fi

if playerctl status | grep -q Paused
then
	playerctl --player=playerctld play
elif playerctl status | grep -q Playing
then
	playerctl --player=playerctld pause
elif playerctl status | grep -q Stopped
then
	if spt pb -s -f '%d %s' | grep -q "Stereo Anlage"
	then
		spt pb -t
	fi
fi
