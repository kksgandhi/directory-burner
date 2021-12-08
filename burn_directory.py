#!/usr/bin/python3

import curses, random, sys, os, math
from os import path

DROP_SPEED          = 45
MAX_FILES_ON_SCREEN = 15

class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-30:])
    def get_text(self):
        return '\n'.join(self.text.split('\n'))

class FileOnScreen:

    # coordinates of the file
    y = 0
    x = 0

    screen_width = 100

    # increasing counter. Counts up each loop until internal_drop_threshold is hit, then this file moves down one line.
    drop_counter = 0
    internal_drop_threshold = 100

    # list of booleans describing whether each character in the filename are "burnt" or not (and whether they should be drawn)
    unburnt_characters = [True]

    def __init__(self, filename, screen_width):
        self.filename                = filename
        n                            = len(filename)
        self.unburnt_characters      = [True] * n
        self.screen_width            = screen_width
        self.internal_drop_threshold = random.randint(50, 150)
        self.x                       = random.randint(n + 5, screen_width - n - 5)

    def __handle_dropping_lower(self):
        """
        Increase the drop counter, 
        if it is over the drop threshold, lower this file's y coordinate by 1
        """
        self.drop_counter += random.random() * DROP_SPEED
        if self.drop_counter > self.internal_drop_threshold:
            self.drop_counter = 0
            self.y += 1

    def __handle_burning(self, b):
        """
        Look at the b array (which describes how 'on fire' each pixel is)
        and set the unburnt_characters array appropriately
        """
        for offset in range(len(self.filename)):
            i = self.y * self.screen_width + self.x + offset
            if b[i] > 4:
                self.unburnt_characters[offset] = False

    def __draw(self, screen):
        """Draw unburnt_characters to the screen"""
        for idx, char in enumerate(self.filename):
            if self.unburnt_characters[idx]:
                screen.addstr(self.y, self.x + idx, char)

    def __delete_file_if_entirely_burnt(self):
        if not dry_run and self.is_fully_burnt():
            os.remove(path.join(directory, self.filename))

    def handle_main_loop(self, screen, b):
        self.__handle_dropping_lower()
        self.__handle_burning(b)
        self.__draw(screen)
        self.__delete_file_if_entirely_burnt()

    def is_fully_burnt(self):
        # self does not have any unburnt_characters, aka all characters are burnt
        return not any(self.unburnt_characters)

def main(screen):
    # get everything that is a simple file
    filenames = [f for f in os.listdir(directory) if path.isfile(path.join(directory, f))]
    width       = screen.getmaxyx()[1]
    height      = screen.getmaxyx()[0]
    size        = width * height
    char        = [" ", ".", ":", "^", "*", "x", "s", "S", "#", "$"]
    b           = [0] * (size + width + 1)
    files_on_screen = []

    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1,0,0)
    curses.init_pair(2,1,0)
    curses.init_pair(3,3,0)
    curses.init_pair(4,4,0)
    screen.clear

    while 1:
        # remove any files that are fully burnt
        files_on_screen = list(filter(lambda files_on_screen: not file_on_screen.is_fully_burnt(), files_on_screen))
        print(list(map(lambda fil: fil.filename, files_on_screen)))
        do_files_remain = len(filenames) > 0
        # The next two lines are just some magic numbers and arbitrary formulas to decide whether a new file should be dropped
        # Basically the fewer files are on screen, the more likely it is for a new file to be dropped.
        files_fill_ratio  = (MAX_FILES_ON_SCREEN * 0.5 - len(files_on_screen)) / MAX_FILES_ON_SCREEN
        should_drop = math.pow(random.random(), 0.3) < files_fill_ratio
        if do_files_remain and should_drop:
            files_on_screen.append(FileOnScreen(filenames.pop(), width))

        # Fire code, see README for link to original code
        for i in range(int(width/9)): b[int((random.random()*width)+width*(height-1))]=min(height * 3, 65)
        for i in range(size):
            b[i]=int((b[i]+b[i+1]+b[i+width]+b[i+width+1])/4)
            color=(4 if b[i]>15 else (3 if b[i]>9 else (2 if b[i]>4 else 1)))
            if(i<size-1):   
                screen.addstr(int(i/width),
                              i%width,
                              char[(9 if b[i]>9 else b[i])],
                              curses.color_pair(color) | curses.A_BOLD )

        for file_on_screen in files_on_screen: 
            file_on_screen.handle_main_loop(screen, b)
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

    mystdout = StdOutWrapper()
    sys.stdout = mystdout
    sys.stderr = mystdout

    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Hope that burning your files was cathartic!")
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdout.write(mystdout.get_text())
