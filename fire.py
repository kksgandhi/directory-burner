#!/usr/bin/python
import curses, random, sys
def debug_write(string): 
    with open("aa.txt", "a") as fil: fil.write(f"{string}\n")

DROP_SPEED = 15

class DropStr:
    y = 0

    drop_counter = 0

    def __init__(self, initstr, width):
        self.mainStr = initstr
        n = len(initstr)
        self.toDraw  = [True] * n
        self.width = width
        self.internal_drop_threshold = random.randint(50, 150)
        self.x = random.randint(n + 5, width - n - 5)

    def draw(self, screen, b):
        self.drop_counter += random.random() * DROP_SPEED
        if self.drop_counter > self.internal_drop_threshold:
            self.drop_counter = 0
            self.y += 1
        for offset in range(len(self.mainStr)):
            i = self.y * self.width + self.x + offset
            if b[i] > 4:
                self.toDraw[offset] = False
        debug_write(self.mainStr)
        debug_write(self.toDraw)
        for idx, char in enumerate(self.mainStr):
            if self.toDraw[idx]:
                screen.addstr(self.y, self.x + idx, char)


def main(screen):
    # screen  = curses.initscr()
    width   = screen.getmaxyx()[1]
    height  = screen.getmaxyx()[0]
    size    = width*height
    char    = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
    b       = []
    dropstr = DropStr("hello", width)

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1,0,0)
    curses.init_pair(2,1,0)
    curses.init_pair(3,3,0)
    curses.init_pair(4,4,0)
    screen.clear
    for i in range(size+width+1): b.append(0)

    while 1:

        for i in range(int(width/9)): b[int((random.random()*width)+width*(height-1))]=min(height * 3, 65)
        for i in range(size):
            b[i]=int((b[i]+b[i+1]+b[i+width]+b[i+width+1])/4)
            color=(4 if b[i]>15 else (3 if b[i]>9 else (2 if b[i]>4 else 1)))
            if(i<size-1):   
                screen.addstr(int(i/width),
                              i%width,
                              char[(9 if b[i]>9 else b[i])],
                              curses.color_pair(color) | curses.A_BOLD )

        dropstr.draw(screen, b)
        screen.refresh()
        screen.timeout(30)
        if (screen.getch()!=-1): break

curses.wrapper(main)
