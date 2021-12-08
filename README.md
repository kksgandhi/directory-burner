Is `rm -rf` too boring for you? `burn_directory.py` lets you watch as your files are slowly and cathartically burnt away.

![Example gif of burn_directory](example.gif)

#### Usage

`python3 directory_burn.py <directory> --dry-run` (To test out the program without deleting any files)

or

`python3 directory_burn.py <directory> --burn-it` (To actually delete the files in said directory)

Or you can run `test.sh` to create a test folder and then burn the files inside it.

#### Other info

[Fire code taken from here](https://gist.github.com/msimpson/1096950)

This program is simplistic in that it doesn't support recursively deleting directories, etc. This is because I didn't want to be responsible for deleting someone's entire file system. Either way though, use this program with caution, I made it as a joke.
