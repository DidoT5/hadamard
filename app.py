from tkinter import *
from tkinter import messagebox
from hadamard import Hadarmard

#Create Window object
app = Tk()

global canvas

class Calculo:
    hadamard = None
    t_value = None

def execute_hadamard():
    global canvas
    try:
        t_value = int(part_text.get())
        Calculo.t_value = t_value
        Calculo.hadamard = Hadarmard(Calculo.t_value)
        result = Calculo.hadamard.main(t_value)
        canvas.delete()
        for number in range(2,2*t_value):
            color = "red" if number-2 in result[0] else "white"
            canvas.create_rectangle(50*(number-2), 0, 50*(number-1), 50, fill=color, outline = 'black')
            #canvas.create_text((50*(number-2)//2,  50*(number-1)//2), text=number)
        for number in range(2*t_value,4*t_value-1):
            color = "red" if number-2 in result[1] else "white"
            canvas.create_rectangle(50*(number-2*t_value), 50, 50*(number-2*t_value+1), 100, fill=color, outline = 'black')
            #canvas.create_text((50*(number-2*t_value)//2, 50*(number-2*t_value+1)//2), anchor=W, text=number)
        canvas.config(scrollregion=canvas.bbox("all"))
        app.update()
    except ValueError:
        messagebox.showerror('A value for t is required', 'Must be an integer number')

def next_hadamard():
    if not(Calculo.hadamard is None) :
        result = Calculo.hadamard.main(Calculo.t_value)
        if result is None:
            messagebox.showerror('There is no more possible combinations for this value of t')
    else:
        messagebox.showerror('Hadarmard first search should be executed first')

def createScrollableContainer():
	canvas.config(xscrollcommand=scrollbar.set, highlightthickness=0)
	scrollbar.config(orient=HORIZONTAL, command=canvas.xview)

	scrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)
	canvas.pack(fill=BOTH, side=LEFT, expand=TRUE)

mainFrame = Frame(app)
mainFrame.grid(row=0, column=0, sticky="nswe")


topFrame = Frame(mainFrame)
topFrame.grid(row=0, sticky="nswe")

part_text = StringVar()
part_label = Label(topFrame, text='Variable T: ', font=('bold', 16), pady=20)
part_entry = Entry(topFrame, textvariable=part_text)
start_btn = Button(topFrame, text='Start calculation', width=20, command=execute_hadamard)

part_label.grid(row=0, column=0)
part_entry.grid(row=0, column=1)
start_btn.grid(row = 0, column=2, pady=20)

middleFrame = Frame(mainFrame)
middleFrame.grid(row=1, sticky="nswe")

canvas = Canvas(middleFrame, width=200, height=100, bg="white")
scrollbar = Scrollbar(middleFrame)
createScrollableContainer()
canvas.pack(side=LEFT,expand=True,fill=BOTH)

bottomFrame = Frame(mainFrame)
bottomFrame.grid(row=3, sticky="nswe")
start_btn = Button(bottomFrame, text='Next Combination', width=20, command=next_hadamard)
start_btn.grid(column=2, pady=20)

mainFrame.place(relx=0.25, rely=0.15)
app.title('Hadarmard App')
app.geometry('800x400')

app.mainloop()