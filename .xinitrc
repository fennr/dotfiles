export XCURSOR_THEME=FlatbedCursors.Green.Regular &
xsetroot -cursor_name left_ptr &
xrdb ~/.Xresources &

sxhkd -f 100 &
feh --bg-scale ~/dotfiles/scrot.jpg &
compton &
exec bspwm