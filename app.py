from tkinter import *
from tkinter import messagebox
from hadamard import Hadarmard

#Create Window object
app = Tk()
hadamard = Hadarmard()

def execute_hadamard():
    t_value = part_text.get()
    try:
        t_value = int(t_value)
        parts_list.delete(0, END)
        result = hadamard.main(t_value)
        for c in result:
            if type(c) is tuple:
                for valor in c:
                    parts_list.insert(END,valor+2)
            else:
                parts_list.insert(END,c+2)
    except ValueError:
        messagebox.showerror('A value for t is required', 'Must be an integer number')


part_text = StringVar()
part_label = Label(app, text='Variable T: ', font=('bold', 16), pady=20)
part_label.grid(column=0, row=0)
part_entry = Entry(app, textvariable=part_text)
part_entry.grid(row=0, column=1)

parts_list = Listbox(app, height=8, width=50)
parts_list.grid(row=2, column=2, pady=20, padx=20)

start_btn = Button(app, text='Start calculation', width=20, command=execute_hadamard)
start_btn.grid(row=0, column=2, pady=20)

app.title('Hadarmard App')
app.geometry('800x400')

app.mainloop()