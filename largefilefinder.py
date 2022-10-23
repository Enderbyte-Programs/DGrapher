#!/usr/bin/env python3
import os
import curses
from curses.textpad import rectangle
import sys
import datetime
if len(sys.argv) > 1:
    ldir = sys.argv[1]
else:
    ldir = "/"
def parse_size(data: int) -> str:
    if data < 0:
        neg = True
        data = -data
    else:
        neg = False
    if data < 2000:
        result = f"{data} bytes"
    elif data > 2000000000:
        result = f"{round(data/1000000000,2)} GB"
    elif data > 2000000:
        result = f"{round(data/1000000,2)} MB"
    elif data > 2000:
        result = f"{round(data/1000,2)} KB"
    if neg:
        result = "-"+result
    return result

def displaymsg(stdscr,message: list):
    stdscr.clear()
    x,y = os.get_terminal_size()
    maxs = max([len(s) for s in message])
    rectangle(stdscr,y//2-(len(message)//2)-1, x//2-(maxs//2)-1, y//2+(len(message)//2)+2, x//2+(maxs//2+1)+1)
    stdscr.addstr(0,0,"Message: ")
    mi = -(len(message)/2)
    for msgl in message:
        mi += 1
        stdscr.addstr(int(y//2+mi),int(x//2-len(msgl)//2),msgl)
    stdscr.addstr(y-2,0,"Press any key to dismiss this message")
    stdscr.refresh()
    stdscr.getch()
def main(stdscr):
    
    refresh = True
    fileslist = {}
    selected = 0
    offset = 0
    stdscr.nodelay(False)
    curses.start_color()
    curses.init_pair(1,curses.COLOR_BLUE,curses.COLOR_BLACK)
    
    while True:
        fl = 0
        sx,sy = os.get_terminal_size()
        maxname = sx - 15
        if refresh:
            _stime = datetime.datetime.now()
            stdscr.addstr(0,0,"Calculating Files")
            stdscr.refresh()
            for subdir, dirs, files in os.walk(ldir):
                for file in files:
                    fl += 1
                    try:
                        stdscr.addstr(0,0," "*(sx-1))
                        stdscr.addstr(0,0,f"Calculating {os.path.join(subdir, file)}"[0:sx-1])
                        stdscr.refresh()
                        fileslist[os.path.join(subdir, file)] = os.path.getsize(os.path.join(subdir, file))
                        fileslist = {k: v for k, v in sorted(fileslist.items(), key=lambda item: item[1],reverse=True)[0:999]}#Only keeping top 1000 to save memory
                    except (PermissionError, FileNotFoundError, OSError):
                        pass
            _etime = datetime.datetime.now()
        refresh = False
        stdscr.addstr(0,0," "*(sx-1))
        stdscr.addstr(0,0,f"Calculated {fl} files in {_etime - _stime} | sel: {selected} | Press DEL to delete"[0:sx-1])
        rectangle(stdscr,1,0,sy-2,sx-1)
        yinc = 0
        for file in list(fileslist.items())[offset:offset+(sy-4)]:
            yinc += 1
            name, size = file
            if len(name) > maxname:
                name = name[0:maxname-3] + "..."
            else:
                name = name + ((maxname-len(name))*" ")
            size = parse_size(size)
            message = name + " " + size
            if yinc + offset -1 == selected:
                stdscr.addstr(yinc + 1,1,message,curses.color_pair(1))
            else:
                stdscr.addstr(yinc + 1,1,message)
        stdscr.addstr(sy-1,0,list(fileslist.keys())[selected][0:sx-1])
        stdscr.refresh()
        ch = stdscr.getch()
        if ch == 114:
            refresh = True#Refresh if R is pressed
        elif ch == curses.KEY_DOWN:
            if selected == len(fileslist)-1:
                pass
            else:
                selected += 1
                if selected > offset + (sy-5):
                    offset += 1# Page goes down
        elif ch == curses.KEY_UP:
            if selected > 0:
                selected -= 1
                if selected < offset and offset > 0:
                    offset -= 1
        elif ch == curses.KEY_DC:
            try:
                os.remove(list(fileslist.keys())[selected])
                del fileslist[list(fileslist.keys())[selected]]
            except Exception as e:
                displaymsg(stdscr,["Failed to remove file.",str(e)[0:sx-10]])
        stdscr.erase()

try:
    curses.wrapper(main)
except KeyboardInterrupt:#No traceback on ctrl-c
    sys.exit(0)