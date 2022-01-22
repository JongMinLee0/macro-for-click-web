import datetime
import queue
import logging
import signal
import time
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
import tkinter.messagebox as msgbox
from startCrawling import *


logger = logging.getLogger(__name__)


class Clock(threading.Thread):
    """Class to display the time every seconds
    Every 5 seconds, the time is displayed using the logging.ERROR level
    to show that different colors are associated to the log levels
    """

    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def run(self):
        logger.debug('Clock started')
        previous = -1
        while not self._stop_event.is_set():
            now = datetime.datetime.now()
            if previous != now.second:
                previous = now.second
                if now.second % 5 == 0:
                    level = logging.ERROR
                else:
                    level = logging.INFO
                logger.log(level, now)
            time.sleep(0.2)

    def stop(self):
        self._stop_event.set()


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue
    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):

        # Check every 100ms if there is a new messaeg in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


class FormUi:
    def __init__(self, frame):
        self.frame = frame
        # Create a text field 
        self.id = tk.StringVar()
        self.password = tk.StringVar()
        ttk.Label(self.frame, text='아이디:').grid(column=0, row=0, sticky=W)
        ttk.Label(self.frame, text='비밀번호:').grid(column=0, row=1, sticky=W)
        ttk.Entry(self.frame, textvariable=self.id, width=25).grid(column=1, row=0, sticky=(W, E))
        ttk.Entry(self.frame, textvariable=self.password, width=25).grid(column=1, row=1, sticky=(W, E))
        
        # Add a button to log the message
        self.button = ttk.Button(self.frame, text='시작', command=self.start_event)
        self.button.grid(column=1, row=2, sticky=W)
        self.button = ttk.Button(self.frame, text='중지', command=self.stop_event)
        self.button.grid(column=2, row=2, sticky=W)

    def start_event(self):
        # Get info
        id = self.id.get()
        password = self.password.get()
        if not id:
            msgbox.showwarning("주 의", "아이디를 입력해주세요.")
            return
        elif not password:
            msgbox.showwarning("주 의", "비밀번호를 입력해주세요.")
            return
        startCwal(id, password)
        # logger.log(lvl, self.message.get())

    def stop_event(self):
        #stop event
        id = self.id.get()


class ThirdUi:
    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame, text='아이디와 패스워드를 입력해주세요.').grid(column=0, row=1, sticky=W)
        # ttk.Label(self.frame, text='With another line here!').grid(column=0, row=4, sticky=W)



class App:
    # GUI
    def __init__(self, root):
        # Root Configuration
        self.root = root
        root.title('Auto Click')
        root.geometry("740x230+580+350")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.resizable(False, False)

        # Create the panes and frames
        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew")
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)
        form_frame = ttk.Labelframe(horizontal_pane, text="loginForm")
        form_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(form_frame, weight=1)
        console_frame = ttk.Labelframe(horizontal_pane, text="Console")
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        horizontal_pane.add(console_frame, weight=1)
        third_frame = ttk.Labelframe(vertical_pane, text="Info")
        vertical_pane.add(third_frame, weight=1)
        
        # Initialize all frames
        self.form = FormUi(form_frame)
        self.console = ConsoleUi(console_frame)
        self.third = ThirdUi(third_frame)
        self.clock = Clock()
        # self.clock.start()

        # close event
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)

    def quit(self, *args):
        self.clock.stop()
        self.root.destroy()


def main():
    logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()
