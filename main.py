import random
import sys
import tkinter as tk
import os
from SwSpotify import spotify, SpotifyNotRunning

class UnsupportedPlatform(Exception):
    def __init__(self, message="This program can only run on Windows.") -> None:
        super().__init__(message)

class Pigeon(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.x = self.winfo_screenwidth() - 300
        self.y = self.winfo_screenheight() - 150
        self.cycle = 0
        self.check = 1
        self.idle_num = [1, 2, 3, 4]
        self.sleep_num = [11, 12, 13, 15, 16]
        self.walk_left = [6, 7]
        self.walk_right = [8, 9]
        self.event_number = random.randrange(1, 3, 1)
        self.go_eat = False

        self.idle = [tk.PhotoImage(file=self.resource_path("assets/idle.gif"), format='gif -index %i' %(i)) for i in range(5)] #idle gif
        self.idle_to_sleep = [tk.PhotoImage(file=self.resource_path("assets/idle_to_sleep.gif"), format='gif -index %i' %(i)) for i in range(8)] #idle to sleep gif
        self.sleep = [tk.PhotoImage(file=self.resource_path("assets/sleep.gif"), format='gif -index %i' %(i)) for i in range(3)] #sleep gif
        self.sleep_to_idle = [tk.PhotoImage(file=self.resource_path("assets/sleep_to_idle.gif"), format='gif -index %i' %(i)) for i in range(8)] #sleep to idle gif
        self.walk_positive = [tk.PhotoImage(file=self.resource_path("assets/walking_positive.gif"), format='gif -index %i' %(i)) for i in range(8)] #walk to left gif
        self.walk_negative = [tk.PhotoImage(file=self.resource_path("assets/walking_negative.gif"), format='gif -index %i' %(i)) for i in range(8)] #walk to right gif
        self.eat = [tk.PhotoImage(file=self.resource_path("assets/eat.gif"), format='gif -index %i' %(i)) for i in range(8)] #eat
        self.sing = [tk.PhotoImage(file=self.resource_path("assets/sing.gif"), format='gif -index %i' %(i)) for i in range(16)] #sing

        self.config(highlightbackground='black')
        self.overrideredirect(True)
        self.wm_attributes('-transparentcolor','black')
        self.wm_attributes("-topmost", True)
        self.label = tk.Label(self, bd=0, bg='black')
        self.label.pack()
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Exit", command=self.quit)
        menu.add_separator()
        menu.add_command(label="Created by liamdj23", state="disabled")
        def do_popup(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
        self.bind("<Button-3>", do_popup)
        def do_eat(event):
            self.go_eat = True
        self.bind("<Double-Button-1>", do_eat)

        self._offsetx = 0
        self._offsety = 0
        self.bind('<Button-1>', self.clickwin)
        self.bind('<B1-Motion>', self.dragwin)

    def dragwin(self, event):
        self.x = self.winfo_pointerx() - self._offsetx
        self.y = self.winfo_pointery() - self._offsety
        self.geometry(f'+{self.x}+{self.y}')

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def event(self, cycle: int, check: int, event_number: int) -> None:
        if self.go_eat:
            check = 6
            print('eat')
            self.after(300, self.update, cycle, check, event_number)#no. 17 = eat
            return
        if event_number in self.idle_num:
            check = 0
            print('idle')
            self.after(400, self.update, cycle, check, event_number) #no. 1,2,3,4 = idle
        elif event_number == 5:
            check = 1
            print('from idle to sleep')
            self.after(100, self.update, cycle, check, event_number) #no. 5 = idle to sleep
        elif event_number in self.walk_left:
            check = 4
            print('walking towards left')
            self.after(100, self.update, cycle, check, event_number) #no. 6,7 = walk towards left
        elif event_number in self.walk_right:
            check = 5
            print('walking towards right')
            self.after(100, self.update, cycle, check, event_number) #no 8,9 = walk towards right
        elif event_number in self.sleep_num:
            check = 2
            print('sleep')
            self.after(1000, self.update, cycle, check, event_number)#no. 11,12,13,15,16 = sleep
        elif event_number == 14:
            check = 3
            print('from sleep to idle')
            self.after(100, self.update, cycle, check, event_number)#no. 14 = sleep to idle
        elif event_number == 10:
            check = 7
            print('sing')
            self.after(600, self.update, cycle, check, event_number)#no. 10 = sing
    
    def gif_work(self, cycle: int, frames: int, event_number: int, first_num: int, last_num: int) -> tuple[int, int]:
        if cycle < len(frames) - 1:
            cycle += 1
        else:
            cycle = 0
            event_number = random.randrange(first_num, last_num+1, 1)
            self.go_eat = False
        return cycle, event_number

    def update(self, cycle: int, check: int, event_number: int) -> None:
        #idle
        if check == 0:
            frame = self.idle[cycle]
            cycle, event_number = self.gif_work(cycle, self.idle, event_number, 1, 10)
        #idle to sleep
        elif check == 1:
            frame = self.idle_to_sleep[cycle]
            cycle, event_number = self.gif_work(cycle, self.idle_to_sleep, event_number, 11, 11)
        #sleep
        elif check == 2:
            frame = self.sleep[cycle]
            cycle, event_number = self.gif_work(cycle, self.sleep, event_number, 11, 16)
        #sleep to idle
        elif check == 3:
            frame = self.sleep_to_idle[cycle]
            cycle, event_number = self.gif_work(cycle, self.sleep_to_idle, event_number, 1, 1)
        #walk toward left
        elif check == 4:
            frame = self.walk_positive[cycle]
            cycle, event_number = self.gif_work(cycle, self.walk_positive, event_number, 1, 10)
            self.x -= 3 if self.x - 3 > 0 else 0
        #walk towards right
        elif check == 5:
            frame = self.walk_negative[cycle]
            cycle, event_number = self.gif_work(cycle, self.walk_negative, event_number, 1, 10)
            self.x += 3 if self.x < self.winfo_screenwidth() - 100 else 0
        #eat
        elif check == 6:
            frame = self.eat[cycle]
            cycle, event_number = self.gif_work(cycle, self.eat, event_number, 1, 10)
        #sing
        elif check == 7:
            try:
                spotify.get_info_windows()
                frame = self.sing[cycle]
                cycle, event_number = self.gif_work(cycle, self.sing, event_number, 1, 10)
            except SpotifyNotRunning as e:
                if cycle > 0:
                    cycle = 0
                frame = self.idle[cycle]
                cycle, event_number = self.gif_work(cycle, self.idle, 1, 1, 10)
        self.geometry(f'100x100+{self.x}+{self.y}')
        self.label.configure(image=frame)
        self.after(1, self.event, cycle, check, event_number)

    def resource_path(self, relative_path: str) -> str:
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def start(self) -> None:
        self.after(1, self.update, self.cycle, self.check, self.event_number)
        self.mainloop()

if sys.platform.startswith("win"):
    app = Pigeon()
    app.start()
else:
    raise UnsupportedPlatform
