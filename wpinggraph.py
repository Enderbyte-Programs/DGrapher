
import curses
from curses.textpad import rectangle
import os
from time import sleep
from subprocess import check_output
import sys
import libcurses
blocklist = [" "," "," ","-","-","█","█","█"]
#blocklist = [str(s) for s in [0,1,2,3,4,5,6,7]]#for testing

def ceil(a,b):
    return -(a // -b)
def average(data: list):
    a = 0
    for d in data:
        a += d
    return a/len(data)

def main(stdscr) :
    libcurses.load_colours()
    IP = libcurses.cursesinput(stdscr,"Welcome to Ping Graph. What is the IP or website you wish to monitor?")
    stdscr.erase()
    useoutfile = libcurses.askyesno(stdscr,"Do you want to save statistics to a file?")
    if useoutfile:
        outfile = libcurses.cursesinput(stdscr,"What is the file path to the save file? (Saved in CSV format)")
    stdscr.nodelay(1)
    s = 0
    graph = [1]
    graphxpoint = 0
    lostpackets = 0
    tick = 0
    try:
        if useoutfile:
            try:
                with open(outfile,"w+") as f:
                    f.write("IP,Ping,Max Ping, Min Ping, Average Ping, Packet Loss\n")
            except:
                libcurses.displaymsg(stdscr,["Error","The provided statistics file could not be created","Press any key to continue"])
                useoutfile = False
        while True:      
            sx, sy = os.get_terminal_size()
            try:
                rectangle(stdscr,4,0,sy-1,sx-2)
            except:
                pass
            try:
                _s = check_output(["ping","-n","1",IP.strip()])
            except Exception as e:
                _s = f"dsfdfstime=5000 ms".encode()
                stdscr.addstr(sy-1,0,f"ERROR: Ping get failed: {str(e)}"[0:sx-1])
                lostpackets += 1
            s = round(float(_s.decode().split("time=")[1].split(" ")[0].replace("ms","").replace("s","")))
            
            graphy = sy-7
            graphx = sx-3
            tick += 1
            maxgraphy = max(graph[graphxpoint:])
            graphyinc = (maxgraphy/graphy)
            stdscr.addstr(0,0,f"Watching {IP}")
            stdscr.addstr(1,0,f"Current Ping: {s} ms")
            stdscr.addstr(0,30,f"Max Ping: {max(graph[graphxpoint:])} ms")#Using difft to 1s
            stdscr.addstr(1,30,f"Minimum Ping: {min(graph[graphxpoint:])} ms")#Using difft to 1s
            stdscr.addstr(3,0,f"Graph Y Increment: {round(graphyinc)} ms")
            stdscr.addstr(2,0,f"Average Ping: {round(average(graph[graphxpoint:]),3)} ms")
            stdscr.addstr(2,30,f"Packet Loss: {round(lostpackets/len(graph)*100,3)}%")

            #stdscr.addstr(0,20,f"CPU Cores: {psutil.cpu_count()}")
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
                    stdscr.addstr(sy-2,ginc,blocklist[0])
                else:
                    stdscr.addstr(sy-2-gy,ginc,blocklist[round((gyf/gyfmax*8)//1-1)])
                if gy > 0:
                    for i in range(gy):
                        stdscr.addstr(sy-2-(gy-i)+1,ginc,blocklist[7])
            stdscr.refresh()
            stdscr.getch()
            if useoutfile:
                with open(outfile,"a+") as f:
                    f.write(f"{IP},{s},{max(graph)},{min(graph)},{average(graph)},{round(lostpackets/len(graph)*100,3)}\n")
            sleep(1)# Limiting to 1FPS to increase accuracy
            stdscr.erase()
            graph.append(s)
            if len(graph) > graphx - 1:
                graphxpoint += 1 
    except KeyboardInterrupt:
        sys.exit()
    except Exception:
        libcurses.displayerror(stdscr,Exception,"An error occured.")
curses.wrapper(main)