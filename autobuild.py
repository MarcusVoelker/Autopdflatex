#!/usr/bin/python

import os
import sys
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import call

class LaTeXRunner(FileSystemEventHandler):
    def on_any_event(self,event):
        ext = os.path.splitext(event.src_path)[1]
        if ext == '.tex':
            e = call(["pdflatex", "-interaction nonstopmode", "-halt-on-error","-file-line-error","-output-directory=./.autobuild", mainfile])
            if e == 0:
                shutil.copy("./.autobuild/" + fname + ".pdf", ".")

if len(sys.argv) < 2 :
    print("Missing arguments filename!")
    sys.exit(1)

global mainfile
mainfile = sys.argv[1]
global fname
fname = os.path.splitext(mainfile)[0]
if not os.path.exists("./.autobuild"):
    os.makedirs("./.autobuild")
observer = Observer()
runner = LaTeXRunner()
observer.schedule(runner,".",recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

