#!/usr/bin/python3

import curses, random, sys, os, math
from os import path

DROP_SPEED          = 45
MAX_FILES_ON_SCREEN = 15


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
        for idx, char in enumerate(self.mainStr):
            if self.toDraw[idx]:
                screen.addstr(self.y, self.x + idx, char)
        if not dry_run and not self.isValid():
            os.remove(path.join(directory, self.mainStr))

    def isValid(self):
        return any(self.toDraw)

def main(screen):
    filenames = [f for f in os.listdir(directory) if path.isfile(path.join(directory, f))]
    width       = screen.getmaxyx()[1]
    height      = screen.getmaxyx()[0]
    size        = width * height
    char        = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
    b           = [0] * (size + width + 1)
    dropstrings = []

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1,0,0)
    curses.init_pair(2,1,0)
    curses.init_pair(3,3,0)
    curses.init_pair(4,4,0)
    screen.clear

    while 1:
        dropstrings = list(filter(lambda dropStr: dropStr.isValid(), dropstrings))
        files_remain = len(filenames) > 0
        files_fill_ratio  = (MAX_FILES_ON_SCREEN * 0.5 - len(dropstrings)) / MAX_FILES_ON_SCREEN
        should_drop = math.pow(random.random(), 0.3) < files_fill_ratio
        if files_remain and should_drop:
            dropstrings.append(DropStr(filenames.pop(), width))

        for i in range(int(width/9)): b[int((random.random()*width)+width*(height-1))]=min(height * 3, 65)
        for i in range(size):
            b[i]=int((b[i]+b[i+1]+b[i+width]+b[i+width+1])/4)
            color=(4 if b[i]>15 else (3 if b[i]>9 else (2 if b[i]>4 else 1)))
            if(i<size-1):   
                screen.addstr(int(i/width),
                              i%width,
                              char[(9 if b[i]>9 else b[i])],
                              curses.color_pair(color) | curses.A_BOLD )

        for dropstr in dropstrings: dropstr.draw(screen, b)
        screen.refresh()
        screen.timeout(30)
        screen.getch()

if __name__ == "__main__":
    global dry_run, directory
    usage = "\nUsage:\n\npython3 directory_burn.py <directory> --dry-run\n\n(to test out the program)\n\npython3 directory_burn.py <directory> --burn-it\n\n(to actually delete the files in a directory)"
    def error_out(error):
        print()
        print(error)
        print(usage)
        exit(1)

    if len(sys.argv) < 3:
        error_out("Not enough arguments")
    directory = sys.argv[1]
    if not path.isdir(directory):
        error_out("First argument is not a directory")
    if sys.argv[2] == "--dry-run":
        dry_run = True
    elif sys.argv[2] == "--burn-it":
        dry_run = False
    else:
        error_out("Second argument must be --dry-run or --burn-it")

    curses.wrapper(main)
