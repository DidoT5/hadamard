from tkinter import *
from tkinter import messagebox
from hadamard import Hadarmard

#Create Window object
app = Tk()
class Calculo:
    hadamard = None
    t_value = None

def execute_hadamard():
    t_value = part_text.get()
    try:
        Calculo.t_value = int(t_value)
        Calculo.hadamard = Hadarmard(Calculo.t_value)
        parts_list.delete(0, END)
        result = Calculo.hadamard.main(Calculo.t_value)
        for c in result:
            if type(c) is tuple:
                for valor in c:
                    parts_list.insert(END,valor+2)
            else:
                parts_list.insert(END,c+2)
    except ValueError:
        messagebox.showerror('A value for t is required', 'Must be an integer number')

def next_hadamard():
    if not(Calculo.hadamard is None) :
        parts_list.delete(0, END)
        result = Calculo.hadamard.main(Calculo.t_value)
        if result is None:
            messagebox.showerror('There is no more possible combinations for this value of t')
        else:
            for c in result:
                if type(c) is tuple:
                    for valor in c:
                        parts_list.insert(END,valor+2)
                else:
                    parts_list.insert(END,c+2)
    else:
        messagebox.showerror('Hadarmard first search should be executed first')

frame = Frame(app)

part_text = StringVar()
part_label = Label(frame, text='Variable T: ', font=('bold', 16), pady=20)
part_label.grid(column=0, row=0)
part_entry = Entry(frame, textvariable=part_text)
part_entry.grid(row=0, column=1)

parts_list = Listbox(frame, height=12, width=80)
parts_list.grid(row=2, column=2, pady=20, padx=20)

start_btn = Button(frame, text='Start calculation', width=20, command=execute_hadamard)
start_btn.grid(row=0, column=2, pady=20)
start_btn = Button(frame, text='Next Combination', width=20, command=next_hadamard)
start_btn.grid(row=3, column=2, pady=20)

app.title('Hadarmard App')
app.geometry('800x400')

frame.pack()

app.mainloop()