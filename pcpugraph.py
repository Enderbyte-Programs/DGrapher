#!/usr/bin/env python3
import psutil
import curses
from curses.textpad import rectangle
import os
import sys
if len(sys.argv) < 2:
    print("Please provide a PID. For overall memory, run command mgraph")
prid = int(sys.argv[1])
blocklist = ["▁","▂","▃","▄","▅","▆","▇","█"]
#blocklist = [str(s) for s in [0,1,2,3,4,5,6,7]]#for testing
def ceil(a,b):
    return -(a // -b)
def main(stdscr) :
    stdscr.nodelay(1)
    s = 0
    graph = [1]
    graphxpoint = 0
    stdscr.addstr(0,0,"Loading...")
    stdscr.refresh()
    while True:           
        sx, sy = os.get_terminal_size()
        
        s = round(psutil.Process(prid).cpu_percent(1) / psutil.cpu_count(),1)
        try:
            rectangle(stdscr,2,0,sy-1,sx-2)
        except:
            pass
        graphy = sy-4
        graphx = sx-4
        maxgraphy = max(graph[graphxpoint:])
        graphyinc = (maxgraphy/graphy)
        stdscr.addstr(0,0,f"CPU Percent: {s}")
        stdscr.addstr(1,0,f"Max Usage: {maxgraphy}")#Using difft to 1s
        stdscr.addstr(1,20,f"Graph Y Increment: {round(graphyinc)}")
        stdscr.addstr(0,20,f"CPU Cores: {psutil.cpu_count()}")
        if graphyinc == 0:
            graphxpoint = 0
            graph = [1]
            graphyinc = 0.2
        ginc = 0
        for g in graph[graphxpoint:]:
            ginc += 1
            gy = round(g/graphyinc)
            gyf = g/graphyinc
            gyfmax = ceil(g,graphyinc)
            if g == 0:
                stdscr.addstr(sy-2,ginc+1,blocklist[0])
            else:
                stdscr.addstr(sy-2-gy,ginc+1,blocklist[round((gyf/gyfmax*8)//1-1)])
            if gy > 0:
                for i in range(gy):
                    stdscr.addstr(sy-2-(gy-i)+1,ginc+1,blocklist[7])
        stdscr.refresh()
        stdscr.getch()
        #sleep(1)# Limiting to 1FPS to increase accuracy
        stdscr.erase()
        graph.append(s)
        if len(graph) > graphx - 1:
            graphxpoint += 1 
curses.wrapper(main)