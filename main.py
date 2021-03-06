import random
import sys
import tkinter as tk
import os
from tkinter import messagebox
import shutil
from SwSpotify import spotify, SpotifyNotRunning
import winreg
import subprocess

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
        self.sleep_num = [12, 13, 15, 16, 17]
        self.walk_left = [6, 7]
        self.walk_right = [8, 9]
        self.event_number = random.randrange(1, 3, 1)
        self.go_eat = False
        self.path = os.getenv("APPDATA") + "\\Pigeon"
        
        self.autostart = tk.BooleanVar(value=True)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
        try:
            winreg.QueryValueEx(registry_key, "Pigeon")
        except FileNotFoundError:
            self.autostart.set(False)
        winreg.CloseKey(registry_key)

        self.idle = [tk.PhotoImage(file=self.resource_path("assets/idle.gif"), format='gif -index %i' %(i)) for i in range(5)] #idle gif
        self.idle_to_sleep = [tk.PhotoImage(file=self.resource_path("assets/idle_to_sleep.gif"), format='gif -index %i' %(i)) for i in range(8)] #idle to sleep gif
        self.sleep = [tk.PhotoImage(file=self.resource_path("assets/sleep.gif"), format='gif -index %i' %(i)) for i in range(3)] #sleep gif
        self.sleep_to_idle = [tk.PhotoImage(file=self.resource_path("assets/sleep_to_idle.gif"), format='gif -index %i' %(i)) for i in range(8)] #sleep to idle gif
        self.walk_positive = [tk.PhotoImage(file=self.resource_path("assets/walking_positive.gif"), format='gif -index %i' %(i)) for i in range(8)] #walk to left gif
        self.walk_negative = [tk.PhotoImage(file=self.resource_path("assets/walking_negative.gif"), format='gif -index %i' %(i)) for i in range(8)] #walk to right gif
        self.eat = [tk.PhotoImage(file=self.resource_path("assets/eat.gif"), format='gif -index %i' %(i)) for i in range(8)] #eat
        self.sing = [tk.PhotoImage(file=self.resource_path("assets/sing.gif"), format='gif -index %i' %(i)) for i in range(16)] #sing
        self.dance = [tk.PhotoImage(file=self.resource_path("assets/dance.gif"), format='gif -index %i' %(i)) for i in range(8)] #dance

        self.config(highlightbackground='black')
        self.overrideredirect(True)
        self.wm_attributes('-transparentcolor','black')
        self.hide_under_apps = tk.BooleanVar(value=False)
        self.wm_attributes("-topmost", not self.hide_under_apps.get())
        self.label = tk.Label(self, bd=0, bg='black')
        self.label.pack()

        menu = tk.Menu(self, tearoff=0)
        def switch_hide_under_apps():
            self.wm_attributes("-topmost", not self.hide_under_apps.get())
        menu.add_checkbutton(label="Hide under apps", command=switch_hide_under_apps, onvalue=True, offvalue=False, variable=self.hide_under_apps)
        if self.is_installed():
            menu.add_checkbutton(label="Autostart", command=self.switch_autostart, onvalue=True, offvalue=False, variable=self.autostart)
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

    def is_installed(self) -> bool:
        if os.path.isdir(self.path):
            if os.path.isfile(self.path + "\\pigeon.exe"):
                return True
        return False

    def switch_autostart(self) -> None:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
        if not self.autostart.get():
            winreg.SetValueEx(registry_key, "Pigeon", 0, winreg.REG_SZ, self.path + "\\pigeon.exe")
            winreg.CloseKey(registry_key)
            self.autostart.set(True)
        else:
            winreg.DeleteValue(registry_key, "Pigeon")
            winreg.CloseKey(registry_key)
            self.autostart.set(False)

    def event(self, cycle: int, check: int, event_number: int) -> None:
        if self.go_eat:
            check = 6
            print('eat')
            self.after(300, self.update, cycle, check, event_number)
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
            self.after(1000, self.update, cycle, check, event_number)#no. 12,13,15,16,17 = sleep
        elif event_number == 14:
            check = 3
            print('from sleep to idle')
            self.after(100, self.update, cycle, check, event_number)#no. 14 = sleep to idle
        elif event_number == 10:
            check = 7
            print('sing')
            self.after(600, self.update, cycle, check, event_number)#no. 10 = sing
        elif event_number == 11:
            check = 8
            print('dance')
            self.after(600, self.update, cycle, check, event_number)#no. 11 = dance
    
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
            cycle, event_number = self.gif_work(cycle, self.idle, event_number, 1, 11)
        #idle to sleep
        elif check == 1:
            frame = self.idle_to_sleep[cycle]
            cycle, event_number = self.gif_work(cycle, self.idle_to_sleep, event_number, 12, 12)
        #sleep
        elif check == 2:
            frame = self.sleep[cycle]
            cycle, event_number = self.gif_work(cycle, self.sleep, event_number, 12, 17)
        #sleep to idle
        elif check == 3:
            frame = self.sleep_to_idle[cycle]
            cycle, event_number = self.gif_work(cycle, self.sleep_to_idle, event_number, 1, 1)
        #walk toward left
        elif check == 4:
            frame = self.walk_positive[cycle]
            cycle, event_number = self.gif_work(cycle, self.walk_positive, event_number, 1, 11)
            self.x -= 3 if self.x - 3 > 0 else 0
        #walk towards right
        elif check == 5:
            frame = self.walk_negative[cycle]
            cycle, event_number = self.gif_work(cycle, self.walk_negative, event_number, 1, 11)
            self.x += 3 if self.x < self.winfo_screenwidth() - 100 else 0
        #eat
        elif check == 6:
            cycle = 0
            frame = self.eat[cycle]
            cycle, event_number = self.gif_work(cycle, self.eat, event_number, 1, 11)
        #sing
        elif check == 7:
            try:
                spotify.get_info_windows()
                frame = self.sing[cycle]
                cycle, event_number = self.gif_work(cycle, self.sing, event_number, 1, 11)
            except SpotifyNotRunning as e:
                if cycle > 0:
                    cycle = 0
                frame = self.idle[cycle]
                cycle, event_number = self.gif_work(cycle, self.idle, 1, 1, 11)
        #dance
        elif check == 8:
            try:
                spotify.get_info_windows()
                frame = self.dance[cycle]
                cycle, event_number = self.gif_work(cycle, self.dance, event_number, 1, 11)
            except SpotifyNotRunning as e:
                if cycle > 0:
                    cycle = 0
                frame = self.idle[cycle]
                cycle, event_number = self.gif_work(cycle, self.idle, 1, 1, 11)
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

    def install(self) -> None:
        answer = messagebox.askyesno("Pigeon Installer", "Do you want to install Pigeon?")
        if answer is False:
            return
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        shutil.copyfile(os.path.realpath(sys.executable), self.path + "\\pigeon.exe")
        os.system(self.path + "\\pigeon.exe")
        sys.exit(0)

if sys.platform.startswith("win"):
    app = Pigeon()
    if not app.is_installed():
        app.install()
    app.start()
else:
    raise UnsupportedPlatform
