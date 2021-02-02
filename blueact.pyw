from PIL import Image, ImageEnhance, ImageTk
import tkinter
from tkinter import filedialog, Button, Canvas
import os

def get_redact_color(image):
    image = image.convert('RGBA')
    pixels = image.load()
    width, height = image.size
    pixels_count = [(None), 0]
    row_pixel = None
    prev = [None, 0]
    redact_color = None
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            if pixel == pixels_count[0]:
                pixels_count[1] += 1
            elif pixels_count[1] > 30 and pixel[0] + pixel[1] + pixel[3]<300:
                row_pixel = pixels[x, y]
            else:
                pixels_count[0] = pixels[x, y]
        prev_sum = 255
        if prev[0] != None: 
            prev_sum = prev[0][0] + prev[0][1] + prev[0][2]
        if prev[1] > 20 and prev[0]!=None:
            return(prev[0])
        if prev[0] == row_pixel:
            prev[1]+=1
        else:
            prev[0] = row_pixel
            prev[1] = 0

def overwrite_redact_color(redact_color, image):
    image = image.convert('RGBA')
    pixels = image.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            if pixel == redact_color:
                image.putpixel((x, y), (255, 255, 255))
    return(image)

def main(path):
    image = Image.open(path)
    redact_color = get_redact_color(image)
    print(redact_color)
    new_image = overwrite_redact_color(redact_color, image)
    new_image.save("output.png")
    return(new_image)

def gui():
    def ask_for_file():
        win.sourceFile = filedialog.askopenfilename(parent=win, initialdir= os.getcwd(), title='Please select an image')
        print(win.sourceFile)
        main(win.sourceFile).show()
    win = tkinter.Tk()
    win.geometry("500x200")
    win.configure(bg='darkgrey')
    image_btn = Button(text="Select an image",bg="blue", command=ask_for_file)
    image_btn.pack()
    win.mainloop()
gui()
