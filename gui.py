import os
import tkinter as tk
from tkinter import Tk, ttk
from drag_manager import DragManager

root = Tk()

windows = dict()


class GUI:
    windows_folder = "windows"
    cur_window = None

    def __init__(
        self,
        master: Tk,
        windows: dict,
        cur_window="",
        view_type="normal",
        title=""
    ):
        # Create the windows folder if not exists
        root_dir = os.getcwd()
        # print(root_dir)
        self.windows_folder = f"{root_dir}/{self.windows_folder}"
        if not os.path.exists(self.windows_folder):
            os.makedirs(self.windows_folder)

        # The master window
        self.master = master
        self.windows = windows
        self.view_type = view_type

        # For editing the view
        if self.view_type == "edit":
            self.drag_mgr = DragManager()
            for window in windows.values():
                window["edit"] = ttk.Button(self.master, text="Edit", command=self.edit)
                window["save"] = ttk.Button(self.master, text="Save", command=self.save)
                window["cancel"] = ttk.Button(
                    self.master, text="Cancel", command=self.cancel
                )
        elif self.view_type == "normal":
            pass
        else:
            raise ValueError(
                "Invalid view type. It should be either 'normal' or 'edit'"
            )

        # View the current window
        self.view_window(cur_window, title=title)

    def view_window(self, window_name="", title=""):
        # Delete cur_window
        if self.cur_window:
            for name, widget in self.cur_window.items():
                widget.place_forget()

        # Rename root title
        if title == "":
            title = window_name.capitalize()
        self.master.title(f"{title}")

        # Change cur_window
        if not self.windows.get(window_name):
            raise ValueError(f"Window {window_name} does not exist.")
        self.cur_window = self.windows[window_name]
        self.path = f"{self.windows_folder}/{window_name}.txt"
        if not os.path.isfile(self.path):
            # put items in grid
            if self.view_type == "edit":
                self.cur_window["edit"].place(x=1, y=1)
            for name, widget in self.cur_window.items():
                if not name in ["edit", "save", "cancel"]:
                    widget.pack()
        else:
            # get new items from cur_window
            # assign cur_window to temp and leave only new items
            temp: dict = self.cur_window.copy()
            # get positions
            with open(self.path, "r") as file:
                if self.view_type == "edit":
                    temp["edit"].place(x=1, y=1)
                    temp.pop("edit")
                for line in file:
                    # print(line.strip())
                    [name, coord] = line.split("=")
                    coord = coord.strip().split(",")
                    # print(name)
                    # print(coord)
                    # place them
                    if temp.get(name):
                        temp[name].place(x=int(coord[0]), y=int(coord[1]))
                        temp.pop(name)
            # pack new items (left ones)
            for name, widget in temp.items():
                if not name in ["edit", "save", "cancel"]:
                    widget.pack()

    def edit(self):
        if self.view_type == "edit":
            # remove edit button
            self.cur_window["edit"].place_forget()

            # put save, cancel buttons
            self.cur_window["save"].place(x=1, y=1, anchor=tk.NW)
            self.cur_window["cancel"].place(rely=1, x=1, y=1, anchor=tk.SW)

        # make all widgets draggable and disabled
        for name, widget in self.cur_window.items():
            if not name in ["edit", "save", "cancel"]:
                self.drag_mgr.add_dragable(widget)
                widget.configure(state="disabled")
                widget.bind("<Enter>", self.print_name)

    def save(self):
        if self.view_type == "edit":
            # remove save, cancel buttons
            self.cur_window["save"].place_forget()
            self.cur_window["cancel"].place_forget()

            # put edit button
            self.cur_window["edit"].place(x=1, y=1)

        with open(self.path, "w") as file:
            for name, widget in self.cur_window.items():
                if not name in ["edit", "save", "cancel"]:
                    # enable all widgets and stop draggability
                    self.drag_mgr.remove_dragable(widget)
                    widget.configure(state="enabled")
                    widget.unbind("<Enter>")

                    # save current positions
                    x = widget.winfo_rootx() - self.master.winfo_rootx()
                    y = widget.winfo_rooty() - self.master.winfo_rooty()
                    file.write(f"{name}={x},{y}\n")

    def cancel(self):
        if self.view_type == "edit":
            # remove save, cancel buttons
            self.cur_window["save"].place_forget()
            self.cur_window["cancel"].place_forget()

            # put edit button
            self.cur_window["edit"].place(x=1, y=1)

        if not os.path.isfile(self.path):
            # put items in grid
            for name, widget in self.cur_window.items():
                if not name in ["edit", "save", "cancel"]:
                    # enable all widgets and stop draggability
                    self.drag_mgr.remove_dragable(widget)
                    widget.configure(state="enabled")
                    widget.unbind("<Enter>")

                    widget.place_forget()
                    widget.pack_forget()
                    widget.pack()
        else:
            # get positions
            with open(self.path, "r") as file:
                for line in file:
                    # print(line.strip())
                    [name, coord] = line.split("=")
                    coord = coord.strip().split(",")
                    # print(name)
                    # print(coord)
                    # place them
                    if self.cur_window.get(name):
                        self.cur_window[name].place(x=int(coord[0]), y=int(coord[1]))
                        # enable all widgets and stop draggability
                        self.drag_mgr.remove_dragable(self.cur_window[name])
                        self.cur_window[name].configure(state="enabled")
                        self.cur_window[name].unbind("<Enter>")

    def get_positions(self):
        self.view_now = dict()

    def print_name(self, event):
        x, y = event.widget.winfo_pointerxy()
        self.target = event.widget.winfo_containing(x, y)
        print(self.target.winfo_name())
