killall spotifyd && killall spt

spotifyd &

spt &

while pgrep -x "spt"
do
	wait
	echo "wating ..."
done

killall spotifyd
