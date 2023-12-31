"""Describe a rectangle shape object."""
import tkinter as tk

import shape

class Rectangle(shape.Shape):
    def __init__(self, x0=0, y0=0, x1=0, y1=0, fill="red", outline="blue", canvas_id=0):
        super().__init__(x0, y0, x1, y1, fill, outline)
        self.canvas_id = canvas_id

    def get_area(self):
        """Calculate and return are aof rectangle."""
        width = self.x1 - self.x0
        height = self.y1 - self.y0

        area = width * height

        return area
    
    def draw_yo_self(self, canvas: tk.Canvas):
        """Draw yourself on a given canvas and return the index of that newly created rectangle item of the canvas."""
        return canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.fill, outline=self.outline)
