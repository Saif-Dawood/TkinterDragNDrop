import tkinter as tk
from tkinter import ttk


class DragManager:
    x_diff = 0
    y_diff = 0
    cursors = dict()

    def add_dragable(self, widget):
        widget.bind("<ButtonPress-1>", self.on_start)
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        self.cursors[widget] = widget['cursor']
        widget.configure(cursor="hand1")
        
    def remove_dragable(self, widget: ttk.Widget):
        widget.unbind("<ButtonPress-1>")
        widget.unbind("<B1-Motion>")
        widget.unbind("<ButtonRelease-1>")
        widget.configure(cursor=self.cursors.get(widget) or "")

    def on_start(self, event):
        # you could use this method to create a floating window
        # that represents what is being dragged.
        # pass
        x, y = event.widget.winfo_pointerxy()
        self.target = event.widget.winfo_containing(x, y)
        # print(
        #     f"target master x, y: {self.target.master.winfo_rootx()}, "
        #     f"{self.target.master.winfo_rooty()}"
        # )
        self.x_diff = x - self.target.winfo_rootx()
        self.y_diff = y - self.target.winfo_rooty()
        # print(f"x_diff: {self.x_diff}, y_diff: {self.y_diff}")
        # print(f"target: {self.target}")

    def on_drag(self, event):
        # you could use this method to move a floating window that
        # represents what you're dragging
        x, y = event.widget.winfo_pointerxy()
        # target = event.widget.winfo_containing(x, y)
        # print(
        #     f"target master x, y: {self.target.master.winfo_rootx()}, "
        #     f"{self.target.master.winfo_rooty()}"
        # )
        # print(f"target: {self.target}")
        new_x = x - self.target.master.winfo_rootx()
        new_y = y - self.target.master.winfo_rooty()
        new_x -= self.x_diff
        new_y -= self.y_diff
        # print(f"new_ x: {new_x}, new_y: {new_y}")
        self.target.place(x=new_x, y=new_y)
        self.target.configure(cursor="fleur")

    def on_drop(self, event):
        # find the widget under the cursor
        # x, y = event.widget.winfo_pointerxy()
        # target = event.widget.winfo_containing(x, y)
        # print(f"x: {x}, y: {y}")
        # print(f"target: {target}")
        # try:
        #     target.configure(image=event.widget.cget("image"))
        # except:
        #     pass
        self.target.configure(cursor="hand1")
