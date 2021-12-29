import tkinter as tk
import random
from tkinter import *


# Function to swap two bars that will be animated

def swap(pos0, pos1):
    bar11, _, bar12, _ = canvas.coords(pos0) # set coordinates for pos0
    bar21, _, bar22, _ = canvas.coords(pos1) # set coordinates for pos0
    canvas.move(pos0, bar21 - bar11, 0)
    canvas.move(pos1, bar12 - bar22, 0)

worker = None


# Function to do Insertion Sort
def _insertion_sort():
    global barList
    global lengthList

    # Outer loop to Traverse through len(LengthList)
    for i in range(len(lengthList)):
        cursor = lengthList[i]
        cursorBar = barList[i]
        pos = i

        # move elements of lenghtlist[pos-1], that are greater than cursor , to one position ahead of their current  position
        while pos > 0 and lengthList[pos - 1] > cursor:
            lengthList[pos] = lengthList[pos - 1]
            barList[pos], barList[pos - 1] = barList[pos - 1], barList[pos]
            swap(barList[pos], barList[pos - 1])
            yield
            pos -= 1

        lengthList[pos] = cursor
        barList[pos] = cursorBar
        swap(barList[pos], cursorBar)


# Bubble Sort
def _bubble_sort():
    global barList
    global lengthList

    # Traverse through array elements
    # len(lengthList) also work but outer loop will reapeat one time more than needed
    for i in range(len(lengthList) - 1):
        # Traverse the array through len(lengthList) - i - 1
        for j in range(len(lengthList) - i - 1):
            # Swap if the element found is greater than the next element
            if lengthList[j] > lengthList[j + 1]:
                lengthList[j], lengthList[j + 1] = lengthList[j + 1], lengthList[j]
                barList[j], barList[j + 1] = barList[j + 1], barList[j]
                swap(barList[j + 1], barList[j])
                yield


# Selection Sort
def _selection_sort():
    global barList
    global lengthList

    # Traverse through all array element
    for i in range(len(lengthList)):
        # find the minimum element in remaining unsorted array
        min = i
        for j in range(i + 1, len(lengthList)):
            if lengthList[j] < lengthList[min]:
                min = j
        # swap the found minimum element with the first element
        lengthList[min], lengthList[i] = lengthList[i], lengthList[min]
        barList[min], barList[i] = barList[i], barList[min]
        swap(barList[min], barList[i])
        yield


# Triggering Fuctions

def insertion_sort():
    global worker
    worker = _insertion_sort()
    animate()


def selection_sort():
    global worker
    worker = _selection_sort()
    animate()


def bubble_sort():
    global worker
    worker = _bubble_sort()
    animate()


# Animation Function
def animate():
    global worker
    if worker is not None:
        try:
            next(worker)
            root.after(10, animate)
        except StopIteration:
            worker = None
        finally:
            root.after_cancel(animate)


# Generator function for generating data
def generate():
    global barList
    global lengthList
    canvas.delete('all')
    barstart = 5
    barend = 15
    barList = []
    lengthList = []

    # Creating a rectangle
    for bar in range(1, 25):
        randomY = random.randint(1, 360)
        bar = canvas.create_rectangle(barstart + 30, randomY, barend, 365, fill='plum3')
        barList.append(bar)
        barstart += 23
        barend += 23

    # Getting length of the bar and appending into length list
    for bar in barList:
        bar = canvas.coords(bar)
        length = bar[3] - bar[1]
        lengthList.append(length)

    # Maximum is colored Red
    # Minimum is colored Black
    for i in range(len(lengthList) - 1):
        if lengthList[i] == min(lengthList):
            canvas.itemconfig(barList[i], fill='red')
        elif lengthList[i] == max(lengthList):
            canvas.itemconfig(barList[i], fill='grey10')


# Making a window using the Tk widget

root = Tk()  # to initialize tkinter, we have to create a Tk root widget , which is a window with a title bar and other decoration rovided by window manager
root.geometry("1350x700+0+0")  # to set dimension of Tkinter window and is used to set position of main window on the user's desktop
root.title('Sorting Algorithm Visualiser')  # to set title of the window
root.maxsize(1350, 750)  # to set maximum size of root window
root.config(bg='lightyellow2')  # to set root window background

# Arranging the position of group widget

mainframe = Frame(root, width=1200, height=300, bg='lightyellow2')  # main frame of the window
mainframe.grid(row=0, column=0, padx=8, pady=0)  # to organise widget in a table-structure in the parent widget

TitleFrame = Frame(mainframe, width=500, padx=8, bd=20, relief=RIDGE)  # Title frame for the window
TitleFrame.pack(side=TOP)  # to organise widgets in block before placing them in the parent widget
lblTitle = Label(TitleFrame, width=39, font=('Times New Roman', 40, 'bold'), text="\tSorting Algorithm Visualiser\t",
                 bg="pink3", fg='black', padx=8)  # to set label for title frame
lblTitle.grid()

DataFrame = Frame(mainframe, bd=12, width=1300, height=600, padx=5, relief=RIDGE)

FrameTOP = LabelFrame(DataFrame, bd=10, width=450, height=300, padx=5, relief=RIDGE, font=('Times New Roman', 18),
                      text="Visualiser", fg="black")  # frame , at right
canvas = Canvas(FrameTOP, width=600, height=380,
                bg='darkseagreen')  # Making a Canvas within the top frame to  display contents
canvas.grid(row=0, column=0, padx=20, pady=0)
FrameTOP.pack(side=TOP)

FrameBOTTOM = Frame(DataFrame, bd=12, width=1250, height=800, padx=5, relief=RIDGE)

# Creating Buttons within bottom frame for different sorting technique
insert = tk.Button(FrameBOTTOM, text='Insertion Sort', command=insertion_sort, font=('Times New Roman', 18), bg='pink3')
select = tk.Button(FrameBOTTOM, text='Selection Sort', command=selection_sort, font=('Times New Roman', 18), bg='pink3')
bubble = tk.Button(FrameBOTTOM, text='Bubble Sort', command=bubble_sort, font=('Times New Roman', 18), bg='pink3')
shuf = tk.Button(FrameBOTTOM, text='Shuffle', command=generate, font=('Times New Roman', 18), bg='skyblue1')
insert.grid(column=2, row=0)
select.grid(column=3, row=0)
bubble.grid(column=4, row=0)
shuf.grid(column=1, row=0)

FrameBOTTOM.pack(side=BOTTOM)

DataFrame.pack(side=BOTTOM)

generate()

root.mainloop()  # This method will loop forever, waiting for events from the users, until the user exits the program
