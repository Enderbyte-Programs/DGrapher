#!/usr/bin/env python3
import shutil
import curses
from curses.textpad import rectangle
import os
import sys
from time import sleep
blocklist = ["▁","▂","▃","▄","▅","▆","▇","█"]
#blocklist = [str(s) for s in [0,1,2,3,4,5,6,7]]#for testing
def ceil(a,b):
    return -(a // -b)
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
def main(stdscr) :
    tick =0
    stdscr.nodelay(1)
    s = shutil.disk_usage("/").free
    osz = s
    xdifft = 0
    difft = 0
    difftx = 0
    xdifftx = 0
    difftxa = 0
    xdifftxa = 0
    graph = [1]
    graphxpoint = 0
    try:
        while True:
            
            tick += 1
            if tick == 20:           
                xdifftx = xdifft
                xdifft = 0
                difftx = difft
                difftxa += difftx
                xdifftxa += xdifftx
                difft = 0
                if len(graph) > graphx - 1:
                    graphxpoint += 1
            sx, sy = os.get_terminal_size()
            s = shutil.disk_usage("/").free
            try:
                rectangle(stdscr,5,0,sy-1,sx-2)
            except:
                pass
            graphy = sy-7
            graphx = sx-4
            maxgraphy = max(graph[graphxpoint:])
            graphyinc = (maxgraphy/graphy)
            diff = osz - s
            if diff < 0:
                xdiff = -diff
            else:
                xdiff = diff
            xdifft += xdiff
            difft += diff
            stdscr.addstr(0,0,f"Total Space: {shutil.disk_usage('/').total} bytes")
            stdscr.addstr(1,0,f"Used Space: {shutil.disk_usage('/').used} bytes")
            stdscr.addstr(2,0,f"Free Space: {shutil.disk_usage('/').free} bytes")
            stdscr.addstr(3,0,f"Used percent: {round(shutil.disk_usage('/').used/shutil.disk_usage('/').total*100,3)}%")
            stdscr.addstr(1,40,f"Disk Change: {parse_size(difftx)}")#Using difft to 1s
            stdscr.addstr(0,40,f"Disk Speed: {parse_size(xdifftx)}/sec")#Using difft to 1s
            stdscr.addstr(2,40,f"Total Change: {parse_size(difftxa)}")#Using difft to 1s
            stdscr.addstr(3,40,f"Total written: {parse_size(xdifftxa)}")#Using difft to 1s
            stdscr.addstr(4,0,f"Graph Y Increment: {parse_size(round(graphyinc))}")
            stdscr.addstr(4,40,f"Maximum write: {parse_size(round(graphyinc*graphy))}")
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
            sleep(0.05)# Limiting to 20FPS
            stdscr.erase()
            if tick == 20:
                graph.append(xdifftx)
                tick = 0#Waiting until later
            osz = s  
    except KeyboardInterrupt:
        sys.exit(0)
curses.wrapper(main)