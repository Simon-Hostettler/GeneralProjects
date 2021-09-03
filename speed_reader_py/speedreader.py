import argparse
import curses
import time

parser = argparse.ArgumentParser(
    description="Command line speedreading tool, specify a file to be read and the desired WPM.")
parser.add_argument("Path", metavar="path", type=str, help="File to be read")
parser.add_argument("WPM", nargs="?", metavar="wpm", type=int,
                    help="Speed at which words are displayed", default=350)
args = parser.parse_args()
path, WPM = args.Path, args.WPM

content = ""
with open(path, "r") as f:
    content = f.read().split()

scr = curses.initscr()
curses.curs_set(0)
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_RED, -1)
scrh, scrw = scr.getmaxyx()
win = curses.newwin(scrh, scrw, 0, 0)
midh = scrh//2

for word in content:
    middle = len(word)//2
    # splitting word to color middle char red
    split_word = [word[:middle], word[middle:middle+1], word[middle+1:]]
    # centering the word
    midw = scrw//2 - len(word)//2
    win.erase()
    # drawing word
    win.addstr(midh, midw, split_word[0])
    win.addstr(split_word[1], curses.color_pair(1))
    win.addstr(split_word[2])
    win.refresh()
    time.sleep(60/WPM)
