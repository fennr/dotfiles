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

# LANG RULES
En = ["", "Termite", "Subl3", "Nautilus", "Wine"]
Ru = ["Firefox"]

def run(arg):
  return subprocess.Popen(arg, stdout=subprocess.PIPE).stdout.read().decode(encoding="UTF-8")

def get_time():
  raw = run("date")[:15]
  return raw[:9] + "," + raw[9:]

def desknames():
  return run(["bspc", "query", "-D"]).replace("\n", "")

def windows():
  deskn  = -1
  names  = desknames()
  status = run(["bspc", "query", "-T"])
  wins   = [[], [], [], [], [], []]
  selec  = 0

  for line in status.splitlines()[1:]:
    if line[1:].find("V m") != -1:
      continue
    if line[1:].find("0,0,0,0") != -1:
      deskn += 1
      if line.endswith("*"): selec = deskn
      continue
    wins[deskn].append(line)
  return selec, wins

def deskbar():
  selected, winds = windows()
  bar = ""
  if selected == 0: bar = SELECTED + bar
  for num, deskname in enumerate(desknames()):
    if len(winds[num]) != 0:
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
  raw = run(["iwconfig"]).splitlines()[0][33:-3]
  if "ff" in raw: return ""
  return WIFI + " " + raw + "  "

def battery():
  raw     = run(["acpi"])[11:-1]
  icon    = ""
  time    = ""
  time = raw[raw.find("%,")+4:raw.find("%,")+8]
  if "until" in raw:
    icon = WIRED + " "
    if time == "unti": time = ""
  elif "Full" in raw:
    icon = WIRED
    time = ""
  elif "remaining" in raw:
    percent = int(raw[raw.find(" ")+1:raw.find("%")])
    if   percent <= 5:   icon = B_CRITICAL
    elif percent <= 25:  icon = B_LOW
    elif percent <= 50:  icon = B_HALF
    elif percent <= 75:  icon = B_ALMOST
    elif percent <= 100: icon = B_FULL
    icon += " "
    if icon == B_LOW + " ": return RED + icon + time
  return icon + time

def sysinfo():
  return "%s  %s%s%s" % (getlayout(), volume(), wifi(), battery())

def stats():
  f         = open(".toggle", "r")
  state     = f.read()[0]
  if state == "1":
    space   = "  "
    offset  = " " * 30
    rawmem  = run(["free", "-m"]).splitlines()[1]
    mem     = int(rawmem[26:32])
    cpuraw  = run(["top", "-bn2", "u1"]).splitlines()[13:17]
    cpu     = 0
    for c in cpuraw: cpu += int(c[c.find(":")+1:c.find(".")])
    cpu     = cpu // 4
    rawtemp = run("sensors").splitlines()[2:3][0]
    temp    = rawtemp[rawtemp.find("+")+1:rawtemp.find(".")]
    return "mem:" + space + str(mem) + space + "cpu:" + space + str(cpu) + "%" + space + "t:" + space + temp + "°" + offset
  else: return ""

def getlayout():
  return run(["setxkbmap", "-print"]).splitlines()[4][29:31]

def setlayout(lang):
  start = "setxkbmap -layout "
  end   = ' -option "grp:caps_toggle"'
  en    = '"us,ru"'
  ru    = '"ru,us"'
  if lang == 1: os.system(start + en + end)
  else: os.system(start + ru + end)

last = ""
focused = ""

while 1:
  f = open(".bar", "w")
  f.write(INIT + deskbar() + CENTER + get_time() + RIGHT + stats() + sysinfo() + END)

  selected, winarray = windows()
  for win in winarray[selected]:
    if win.endswith("*"): focused = win[win.find(" ")+1:]
  focused = focused[:focused.find(" ")]
  if last != focused:
    if   focused in En: setlayout(1)
    elif focused in Ru: setlayout(0)
    last = focused

  time.sleep(.05)