from tkinter import *
import time
import solver
import generator

# ------------------------------F U N C T I O N S----------------------------- #

def mouseClick(event, canvas, data):  # left mouse click
    print("Mouse click @(" + str(event.x) + "," + str(event.y) + ")")
    # check if it lands in any clickable spot.
    for i in range(len(data.buttons_positions)):
        if (data.buttons_positions[i][0] < event.x) and (data.buttons_positions[i][2] > event.x)\
        and (data.buttons_positions[i][1] < event.y) and (data.buttons_positions[i][3] > event.y):
            checkButton(event, data, canvas, i)
            break

def checkButton(event, data, canvas, button):
    # check if the button exists at the moment, and if so, then preform the right action.

    # if it's the reset button
    if button == 0:
        # change image to pressed
        data.IMG_reset_button = data.IMG_reset_button_pressed
        # reset line info
        for i in range(10):
            data.linesinfo[i][0] = 0
            data.linesinfo[i][1] = 0
            data.linesinfo[i][2] = 0
        # reset hint boxes
        for i in range(10):
            data.hintboxes[i] = 0
        # reset Lock
        data.lockinfo = ["?", "?", "?"]
        # reset the metal piece if it's lifted
        data.metal_y = 0
        # reset dialogue massage
        data.dialogue = ""

        redrawAll(canvas, data)  # redraw all

    # if it's the generate button
    if button == 1:
        data.IMG_generate_button = data.IMG_generate_button_pressed
        result = generator.generate()

        data.linesinfo = result[0]
        data.hintboxes = result[1]
        data.lines = result[2]
        # complete linesinfo and hintboxes to 10 lines, as its original format
        for i in range(10 - data.lines):
            data.linesinfo.append([0, 0, 0])
            data.hintboxes.append(0)

        # reset Lock
        data.lockinfo = ["?", "?", "?"]
        # reset the metal piece if it's lifted
        data.metal_y = 0
        # reset dialogue massage
        data.dialogue = ""
        # update highlighter
        data.highlighter_y = data.lines

        redrawAll(canvas, data)  # redraw all

    # if it's the solve button
    if button == 2:
        # change image to pressed
        data.IMG_solve_button = data.IMG_solve_button_pressed
        data.metal_y = 0  # im not sure ur supposed to put this here
        result = solver.solve(data.lines, data.linesinfo, data.hintboxes)  # execute the great script. It returns an array with 4 element.
        data.lockinfo[0] = result[0]
        data.lockinfo[1] = result[1]
        data.lockinfo[2] = result[2]
        data.dialogue = result[3]
        redrawAll(canvas, data)

        if data.dialogue == "Puzzle Solved!":
            animateMetal(root, canvas, data)

    if button == 3:  # if it's the plus/minus button
        # check 1st line, last line, any in between.
        if data.lines == 1 and event.x < (data.line_x + 32):  # if its 1st line and clicked on the positive
            # create a Line and redraw everything
            data.lines += 1
            redrawAll(canvas, data)
        elif data.lines == 10 and event.x > (data.line_x + 32):  # if its 10th line and clicked on the negative
            data.lines -= 1  # delete a line
            data.hintboxes[data.lines] = 0  # reset the hint box of the line you deleted
            if data.highlighter_y > data.lines:  # if you deleted a line that had the highlighter,
                data.highlighter_y -= 1  # then move the highlighter up.
            resetAline(data, data.lines)  # let's reset the info in that line we just deleted
            redrawAll(canvas, data)  # redraw everything
        elif (data.lines > 1) and (data.lines < 10):  # if neither the 1st or last line, but somewhere in between
            if event.x > (data.line_x + 32):  # delete a line if it's the minus button
                data.lines -= 1
                data.hintboxes[data.lines] = 0  # reset the hint box of the line you deleted
                if data.highlighter_y > data.lines:  # if you deleted a line that had the highlighter,
                    data.highlighter_y -= 1  # then move the highlighter up.
                resetAline(data, data.lines)  # lets reset the info in that line we just deleted
                redrawAll(canvas, data)
            elif event.x < (data.line_x + 32):  # add a line if its the plus button
                data.lines += 1
                redrawAll(canvas, data)

    # if it's a line
    if (button >= 4) and (button <= 13):
        if data.lines >= (button - 4 + 1):  # if it exists atm
            data.highlighter_y = button - 3  # set the Y to the appropriate line
            # set the x to the appropriate line
            if event.x < data.line_x + data.line_height:
                data.highlighter_x = 1
            elif (event.x > data.line_x + data.line_height) and (event.x < data.line_x + 2*data.line_height):
                data.highlighter_x = 2
            elif event.x > data.line_x + 2*data.line_height:
                data.highlighter_x = 3
            redrawAll(canvas, data)  # redraw all

    # if its a hint box
    if (button >= 14) and (button <= 23):
        if data.lines >= (button - 14):  # if it exists atm
            data.hintboxes[button - 14] += 1  # increase the hint box by 1 so it moves to the next hint
            if data.hintboxes[button - 14] > 6:  # if the hint exceeds 6, then recycle
                data.hintboxes[button - 14] = 0
            redrawAll(canvas, data)

def animateMetal(root, canvas, data):
    while data.metal_y < 20:
            canvas.move(data.animatedMetal, 0, -1)
            root.update()
            data.metal_y += 1
            time.sleep(0.01)


def redrawAll(canvas, data):
    canvas.delete(ALL)

    # draw the background color
    canvas.create_rectangle(0, 0, data.window_width, data.window_height, fill='#{:02x}{:02x}{:02x}'.format(43, 43, 43))

    # draw the buttons
    canvas.create_image(20, 20, image=data.IMG_reset_button, anchor=NW)
    canvas.create_image(20, 60, image=data.IMG_generate_button, anchor=NW)
    canvas.create_image(20, 120, image=data.IMG_solve_button, anchor=NW)

    # the lock and its components
    # we assign this to a variable so it becomes an object and we can move it on the canvas when we want to animate it
    data.animatedMetal = canvas.create_image(200 + 200, 60 - data.metal_y + 85, image=data.IMG_metal, anchor=NW)
    canvas.create_image(200 + 200, 225, image=data.IMG_lock, anchor=NW)
    canvas.create_text(209 + 200, 216 + 85, text=data.lockinfo[0], anchor="nw", fill="black", font="Times 20 bold")
    canvas.create_text(242 + 200, 216 + 85, text=data.lockinfo[1], anchor="nw", fill="black", font="Times 20 bold")
    canvas.create_text(277 + 200, 216 + 85, text=data.lockinfo[2], anchor="nw", fill="black", font="Times 20 bold")
    # draw the dialogue message
    canvas.create_text(260 + 200 - 10, 300 + 85, text=data.dialogue, anchor="n", fill='#{:02x}{:02x}{:02x}'.format(90, 90, 90), font="Verdana 14")

    # draw the lines
    for i in range(data.lines):
        canvas.create_text(data.line_x-10 + 6, (data.line_y+(i*data.line_height)+((i-1)*data.line_distance)),  # line number
                           text=str(i+1) + ".", anchor="ne", fill='#{:02x}{:02x}{:02x}'.format(90, 90, 90), font="Verdana 15")
        canvas.create_image(data.line_x, (data.line_y+(i*data.line_height)+((i-1)*data.line_distance)), image=data.IMG_line, anchor=NW)

    # draw the line information
    color = '#{:02x}{:02x}{:02x}'.format(195, 195, 195)
    for i in range(data.lines):
        canvas.create_text(data.line_x + 8 - 1, (data.line_y + (i*data.line_height)+((i-1)*data.line_distance)),
                           text=data.linesinfo[i][0], anchor="nw", fill=color, font="Verdana 20")
        canvas.create_text(data.line_x + 32 + 8 - 1, (data.line_y + (i*data.line_height)+((i-1)*data.line_distance)),
                           text=data.linesinfo[i][1], anchor="nw", fill=color, font="Verdana 20")
        canvas.create_text(data.line_x + 64 + 8 - 1, (data.line_y + (i*data.line_height)+((i-1)*data.line_distance)),
                           text=data.linesinfo[i][2], anchor="nw", fill=color, font="Verdana 20")

    # draw the hint boxes
    for i in range(data.lines):
        canvas.create_image(data.line_x + 100, data.line_y + (i * data.line_height) + ((i-1) * data.line_distance),
                            image=data.IMG_hintboxes[data.hintboxes[i]], anchor=NW)

    # draw the plus/minus
    if data.lines == 1:
        canvas.create_image(data.line_x, 20, image=data.IMG_plus, anchor=NW)
    elif data.lines == 10:
        canvas.create_image(data.line_x, 20, image=data.IMG_minus, anchor=NW)
    else:
        canvas.create_image(data.line_x, 20, image=data.IMG_plus_minus, anchor=NW)


    # draw highlighter
    # draw highlighter's outline
    canvas.create_rectangle(data.line_x + (data.line_height * (data.highlighter_x-1)),
    (data.line_y + ((data.highlighter_y - 1) * data.line_height) + ((data.highlighter_y - 1 - 1) * data.line_distance)),
     data.line_x + (data.line_height * data.highlighter_x),
    (data.line_y + ((data.highlighter_y-1) * data.line_height) + ((data.highlighter_y-1-1)*data.line_distance)) + data.line_height,
    outline='#{:02x}{:02x}{:02x}'.format(100, 100, 0), width=5)
    # draw highlighter yellow color
    canvas.create_rectangle(data.line_x + (data.line_height * (data.highlighter_x-1)),
    (data.line_y + ((data.highlighter_y - 1) * data.line_height) + ((data.highlighter_y - 1 - 1) * data.line_distance)),
     data.line_x + (data.line_height * data.highlighter_x),
    (data.line_y + ((data.highlighter_y-1) * data.line_height) + ((data.highlighter_y-1-1)*data.line_distance)) + data.line_height,
    outline='#{:02x}{:02x}{:02x}'.format(192, 192, 0), width=3)
    # Note: the "-1-1" one is for the highlighter being 1 up, the other '-1' is because.....
    # .....there are less space between lines than actual lines by one

    # draw program information
    canvas.create_rectangle(20, 515, 218, 608, fill='#{:02x}{:02x}{:02x}'.format(50, 50, 50), width=0)
    canvas.create_text(25, 520, text="Crack The Code", anchor="nw",
                       fill='#{:02x}{:02x}{:02x}'.format(90, 90, 90), font="Verdana 13 bold")
    canvas.create_text(25, 540, text="Version 1.0\nDeveloped by I.S\nMade with Python 3.6", anchor="nw", fill='#{:02x}{:02x}{:02x}'.format(90, 90, 90), font="Verdana 13")

def initialize(data):
    data.buttons_positions = [
    # [x1,y1,x2,y2] (x1,y1) is the top-left corner, (x2,y2) is the bottom-right corner.
    [20, 20, 138, 52],  # reset button
    [20, 60, 138, 92],  # generate button
    [20, 120, 138, 152],  # solve button
    [data.line_x, 20, data.line_x + 65, 20 + 32],  # plus/minus button
    # locations of the 10 different lines, let's initialize them here and adjust the values next.
    [0, 0, 0, 0],  # 1st line
    [0, 0, 0, 0],  # 2nd line
    [0, 0, 0, 0],  # 3rd line
    [0, 0, 0, 0],  # 4th line
    [0, 0, 0, 0],  # 5th line
    [0, 0, 0, 0],  # 6th line
    [0, 0, 0, 0],  # 7th line
    [0, 0, 0, 0],  # 8th line
    [0, 0, 0, 0],  # 9th line
    [0, 0, 0, 0],  # 10th line
    # location of the 10 different hint boxes, let's initialize them here and adjust the values next.
    [0, 0, 0, 0],  # 1st hint box
    [0, 0, 0, 0],  # 2nd hint box
    [0, 0, 0, 0],  # 3rd hint box
    [0, 0, 0, 0],  # 4th hint box
    [0, 0, 0, 0],  # 5th hint box
    [0, 0, 0, 0],  # 6th hint box
    [0, 0, 0, 0],  # 7th hint box
    [0, 0, 0, 0],  # 8th hint box
    [0, 0, 0, 0],  # 9th hint box
    [0, 0, 0, 0],  # 10th hint box
    ]

    # lets adjust the values for the lines
    for index in range(10):  # runs 10 times. index will be [0-9]
        data.buttons_positions[4 + index] = [
            data.line_x,
            data.line_y + (data.line_height*index) + (data.line_distance*(index-1)),
            data.line_x + data.line_width,
            data.line_y + (data.line_height*index) + (data.line_distance*(index-1)) + data.line_height
        ]
    # lets adjust the values for the hint boxes
    for index in range(10):  # runs 10 times. index will be [0-9]
        data.buttons_positions[14 + index] = [
            data.line_x + 100,
            data.line_y + (data.line_height * index) + (data.line_distance * (index-1)),
            data.line_x + 100 + 201,  # plus the width of the hint box
            data.line_y + (data.line_height*index) + (data.line_distance*(index-1)) + 51  # the height of the hint box
        ]

    # this array stores the what hint goes for each of the 10 boxes. Because there are 10 lines total, there are...
    # 10 elements here, and those elements' values ranges [0,6] because there are 7 possible hints to be shown. Thus ..
    # this keeps track what each box hold what type of hint.
    data.hintboxes = [1, 1, 1, 2, 2, 0, 0, 0, 0, 0]

    data.linesinfo = [
        [1, 0, 4],
        [4, 1, 0],
        [4, 0, 1],
        [5, 7, 0],
        [2, 8, 6],
        [0, 6, 0],
        [0, 0, 7],
        [0, 8, 0],
        [9, 0, 0],
        [1, 0, 0],
    ]

    data.lockinfo = ["?", "?", "?"]


def moveHighlighter(movey, movex, canvas, data):
    # So this will be like the grid in the original program.
    # as you go right, x increases. As you go down, y increases.
    data.highlighter_x += movex
    data.highlighter_y += movey

    if data.highlighter_x > 3:
        data.highlighter_x = 1
    if data.highlighter_x < 1:
        data.highlighter_x = 3
    if data.highlighter_y < 1:
        data.highlighter_y = data.lines
    if data.highlighter_y > data.lines:
        data.highlighter_y = 1

    # print("(" + str(data.highlighter_x) + "," + str(data.highlighter_y) + ")")
    redrawAll(canvas, data)

def updateLines(data, num):
    # print("You entered the number " + str(num))
    data.linesinfo[data.highlighter_y - 1][data.highlighter_x - 1] = num
    redrawAll(canvas, data)

def resetAline(data, num):
    # this function is for if I delete a line by the minus, i want that line to reset it values to...
    # ..zeros. So that when i get it back, I don't want it to keep its previous values. I am making this
    # simple function purely to avoid clustering. its either like this.
    data.linesinfo[num][0] = 0
    data.linesinfo[num][1] = 0
    data.linesinfo[num][2] = 0

def unpress(canvas, data):
    data.IMG_reset_button = data.IMG_reset_button_unpressed
    data.IMG_solve_button = data.IMG_solve_button_unpressed
    data.IMG_generate_button = data.IMG_generate_button_unpressed
    redrawAll(canvas, data)



# ---------------------------M A I N   P R O G R A M------------------------ #


# ---------------------data structure object--------------------- #
# a class that we will use to create data object
# we will store all data in this object so we can access and modify it from any function
class Structure(object):
    pass

# create the data object
data = Structure()

# ---------------------root & canvas--------------------- #
# Window's height and width
data.window_width = 1080
data.window_height = 628

# create root
root = Tk()
root.resizable(width=False, height=False)  # prevents resizing window
root.title("")

# create canvas
canvas = Canvas(root, width=data.window_width, height=data.window_height)
canvas.configure(bd=0, highlightthickness=0)
canvas.pack()

# ---------------------essential variables and data initialization--------------------- #

# lines
# we will use this information to manage the design layout on the canvas.
data.lines = 5  # amount of the initial(and current) lines
data.line_x = 759  # top left corner of the 1st line
data.line_y = 85  # top left corner of the 1st line
data.line_distance = 23  # the distance between each line
data.line_height = 32  # the height of the line image
data.line_width = 94  # the width of the line image


# highlighter
# the highlighter will have coordinates(x,y) to locate its position
data.highlighter_x = 1  # [1-3]
data.highlighter_y = 1  # [1-10(depends on how many lines you currently have)]

# images
data.IMG_reset_button_unpressed = PhotoImage(file="IMG_resetButton.png")
data.IMG_reset_button_pressed = PhotoImage(file="IMG_resetButtonPressed.png")
data.IMG_reset_button = data.IMG_reset_button_unpressed
data.IMG_solve_button_unpressed = PhotoImage(file="IMG_solveButton.png")
data.IMG_solve_button_pressed = PhotoImage(file="IMG_solveButtonPressed.png")
data.IMG_solve_button = data.IMG_solve_button_unpressed
data.IMG_generate_button_unpressed = PhotoImage(file="IMG_generate.png")
data.IMG_generate_button_pressed = PhotoImage(file="IMG_generatepressed.png")
data.IMG_generate_button = data.IMG_generate_button_unpressed
data.IMG_lock = PhotoImage(file="IMG_lock.png")
data.IMG_metal = PhotoImage(file="IMG_metal.png")
data.IMG_plus = PhotoImage(file="IMG_plus.png")
data.IMG_plus_minus = PhotoImage(file="IMG_plusMinus.png")
data.IMG_minus = PhotoImage(file="IMG_minus.png")
data.IMG_line = PhotoImage(file="IMG_line.png")
data.IMG_hintboxes = [  # the images of the hint boxes are being stored here.
PhotoImage(file="IMG_hint0.png"),
PhotoImage(file="IMG_hint1.png"),
PhotoImage(file="IMG_hint2.png"),  # 195 x 42
PhotoImage(file="IMG_hint3.png"),  # 195 x 42
PhotoImage(file="IMG_hint4.png"),  # 195 x 42
PhotoImage(file="IMG_hint5.png"),  # 195 x 42
PhotoImage(file="IMG_hint6.png"),  # 195 x 42
                      ]

# other
data.dialogue = ""  # the message shown after the user hit the 'run' button. It's one of the three:
# Puzzle Solved!
# Error: Information Provided is not enough!
# Error: Information provided has no solution!


''' 
This variable serves 2 things:
1st) When redrawAll method is called, and the metal is
supposed to be up, it will draw it up instead of resetting it to default position.
2nd) There is a bug that I don't understand for the life of me. When you
call on the metal animation function, it will activate the loop that moves the metal one
pixel at each iteration. The problem is, sometimes the metal goes above and beyond where it 
supposed to. So it floats upwards. What seems to be is that when you call the metal animation
while the animation is already taking place, it stops the process, and takes the remaining iterations 
and adds them up to the next method call that you just did. So it preform the animation as it supposed to
PLUS the remaining iterations from the previous call to the function. So this help keep track of the metal 
position and use this information to keep it straight and not bugs out. It didn't solve the problem 100% it seems,
but good enough and it's not noticeable. '''
data.metal_y = 0


initialize(data)  # send it to the initialization function. It will be given the rest of the necessary information

# ---------- now that we have all data, let's draw
redrawAll(canvas, data)

# ---------------------events--------------------- #
# Mouse Click
root.bind("<Button-1>", lambda event: mouseClick(event, canvas, data))
root.bind("<ButtonRelease-1>", lambda event: unpress(canvas, data))

# highlighter movement
root.bind('<Left>', lambda event: moveHighlighter(0, -1, canvas, data))
root.bind('<Right>', lambda event: moveHighlighter(0, 1, canvas, data))
root.bind('<Up>', lambda event: moveHighlighter(-1, 0, canvas, data))
root.bind('<Down>', lambda event: moveHighlighter(1, 0, canvas, data))
root.bind('a', lambda event: moveHighlighter(0, -1, canvas, data))
root.bind('d', lambda event: moveHighlighter(0, 1, canvas, data))
root.bind('w', lambda event: moveHighlighter(-1, 0, canvas, data))
root.bind('s', lambda event: moveHighlighter(1, 0, canvas, data))
root.bind('A', lambda event: moveHighlighter(0, -1, canvas, data))
root.bind('D', lambda event: moveHighlighter(0, 1, canvas, data))
root.bind('W', lambda event: moveHighlighter(-1, 0, canvas, data))
root.bind('S', lambda event: moveHighlighter(1, 0, canvas, data))
# root.bind('<Shift_L>', lambda event: moveHighlighter(0, 1, canvas, data))
# Note that besides these, the highlighter also moves to where you Mouse click

# entering numbers
root.bind('0', lambda event: updateLines(data, 0))
root.bind('1', lambda event: updateLines(data, 1))
root.bind('2', lambda event: updateLines(data, 2))
root.bind('3', lambda event: updateLines(data, 3))
root.bind('4', lambda event: updateLines(data, 4))
root.bind('5', lambda event: updateLines(data, 5))
root.bind('6', lambda event: updateLines(data, 6))
root.bind('7', lambda event: updateLines(data, 7))
root.bind('8', lambda event: updateLines(data, 8))
root.bind('9', lambda event: updateLines(data, 9))


root.mainloop()
print("Program over!")
