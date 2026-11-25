#!/usr/bin/env bash

xrandr --auto
widths=$(xrandr | grep connected | grep -v disconnected | rev | cut -d\  -f3 | rev | sort -n)
echo $widths
vmon=$(xrandr | grep "$(echo "$widths" | head -n 1)" | cut -d\  -f1)
hmon=$(xrandr | grep "$(echo "$widths" | tail -n 1)" | cut -d\  -f1)
echo vmon=$vmon hmon=$hmon
xrandr | grep "$hmon connected" && xrandr --output $hmon --primary
xrandr | grep "$vmon connected" && xrandr --output $vmon --left-of $hmon --rotate right
xsetroot -solid "#222222"

# === same
do_vol() {
    if command -v wpctl >/dev/null 2>&1; then
        wpctl get-volume @DEFAULT_AUDIO_SINK@ 2>/dev/null | awk '{printf "%d%%", $2 * 100}'
    elif command -v amixer >/dev/null 2>&1; then
        amixer get Master 2>/dev/null | awk -F'[][]' '/%/ {print $2; exit}'
    elif command -v pactl >/dev/null 2>&1; then
        pactl get-sink-volume @DEFAULT_SINK@ 2>/dev/null | awk '/Volume:/ {print $5; exit}'
    else
        echo "--"
    fi
}


pgrep dwm || {
    while true; do
    bat_a=$(cat /sys/class/power_supply/BAT0/capacity)
    bat_s=$(cat /sys/class/power_supply/BAT0/status | cut -c1)
        xsetroot -name "$bat_s$bat_a | VOL:$(do_vol) | $(date '+%Y-%m-%d %H:%M')"
        sleep 60
    done &

    xset s off &
    xset -dpms &
    xset s noblank &
    exec dwm
}
