#!/usr/bin/python
import time, subprocess, os

# COLORS
BG_BLACK = "%{B#C8000000}%{-u}"
SELECTED = "%{B#BE09131A}%{+u}"
INIT     = "%{U#AA0C6FB6}"
WHITE    = "%{F#FFF}"
GRAY     = "%{F#555}"
RED      = "%{F#FF0000}"
CENTER   = "%{c}"
RIGHT    = "%{r}"
END      = u"\u00A0"u"\u00A0"+"\n"

# BATTERIES
B_CRITICAL = ""   #   5%
B_LOW      = ""   #  25%
B_HALF     = ""   #  50%
B_ALMOST   = ""   #  75%
B_FULL     = ""   # 100%
WIRED      = ""

# ICONS
VOLUME  = ""
WIFI    = ""

def run(arg):
  return subprocess.Popen(arg, stdout=subprocess.PIPE).stdout.read().decode(encoding="UTF-8")

def get_time():
  raw = run("date")[:16]
  return raw[:10] + "," + raw[10:]

def desknames():
  return run(["bspc", "query", "-D"]).replace("\n", "")

def windows():
  deskn  = -1
  names  = desknames()
  status = run(["bspc", "wm", "-g"])
  wins   = [0, 0, 0, 0, 0, 0]
  selec  = 0

  for i, e in enumerate(status.split(":")):
    if e[0] == "O":
      selec = i-1
      wins[i-1] = 1
    if e[0] == "F": selec = i-1
    if e[0] == "o": wins[i-1] = 1
  return selec, wins

def deskbar():
  selected, winds = windows()
  bar = ""
  if selected == 0: bar = SELECTED + bar
  for num, deskname in enumerate(desknames()):
    if winds[num] == 1:
      if num == selected: bar += SELECTED + "   " + WHITE + deskname + "   " + BG_BLACK
      else: bar += "   " + WHITE + deskname + "   "
    else:
      if num == selected: bar += SELECTED + "   " + GRAY  + deskname + "   " + BG_BLACK
      else: bar += "   " + GRAY  + deskname + "   "
  bar += WHITE + BG_BLACK
  return bar

def volume():
  raw   = run(["pactl", "list", "sinks"]).splitlines()[9:10][0]
  value = raw[raw.find("/ ")+2:raw.find("%")]
  return VOLUME + value + "%  "

def wifi():
  raw = run(["iwgetid"]).splitlines()[0][17:-1]
  if "ff" in raw: return ""
  return WIFI + " " + raw + "  "

def battery():
  raw     = run(["acpi"])[11:-1]
  icon    = ""
  if "until" in raw:
    if   percent <= 5:   icon = WIRED + " " +  B_CRITICAL
    elif percent <= 25:  icon = WIRED + " " + B_LOW
    elif percent <= 50:  icon = WIRED + " " + B_HALF
    elif percent <= 75:  icon = WIRED + " " + B_ALMOST
    elif percent <= 100: icon = WIRED + " " + B_FULL
  elif "Full" in raw:
    icon = WIRED
  elif "remaining" in raw:
    percent = int(raw[raw.find(" ")+1:raw.find("%")])
    if   percent <= 5:   icon = B_CRITICAL
    elif percent <= 25:  icon = B_LOW
    elif percent <= 50:  icon = B_HALF
    elif percent <= 75:  icon = B_ALMOST
    elif percent <= 100: icon = B_FULL
    icon += " "
    if icon == B_LOW + " ": return RED + icon
  return icon

def sysinfo():
  return "%s  %s%s%s" % (getlayout(), volume(), wifi(), battery())

def getlayout():
  return run(["setxkbmap", "-print"]).splitlines()[4][29:31]

while 1:
  f = open(".bar", "w")
  f.write(INIT + deskbar() + CENTER + get_time() + RIGHT + sysinfo() + END)
  time.sleep(.05)
