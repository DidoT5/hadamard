from tkinter import *
from tkinter import messagebox
from hadamard import Hadarmard
import numpy as np

class Calculo:
    hadamard = None
    t_value = None
    result = None

class App:

    def __init__(self):
        self.app = Tk()
        self.Calculo = Calculo()
        self.mainFrame = Frame(self.app)
        self.topFrame = Frame(self.mainFrame)
        self.part_text = StringVar()
        self.middleFrame = Frame(self.mainFrame)
        self.canvas = Canvas(self.middleFrame, width=200, height=100, bg="white")
        self.scrollbar = Scrollbar(self.middleFrame)
        self.bottomFrame = Frame(self.mainFrame)
        self.comb_var = StringVar()

    def draw_rectangles(self,t_value):
        canvas = self.canvas
        canvas.delete('all')
        for number in range(2,2*t_value):
            color = "red" if number-2 in self.Calculo.result[0] else "white"
            canvas.create_rectangle(50*(number-2), 0, 50*(number-1), 50, fill=color, outline = 'black')
            #canvas.create_text((50*(number-2)//2,  50*(number-1)//2), text=number)
        for number in range(2*t_value,4*t_value-1):
            color = "red" if number-2 in self.Calculo.result[1] else "white"
            canvas.create_rectangle(50*(number-2*t_value), 50, 50*(number-2*t_value+1), 100, fill=color, outline = 'black')
            #canvas.create_text((50*(number-2*t_value)//2, 50*(number-2*t_value+1)//2), anchor=W, text=number)
        canvas.config(scrollregion=canvas.bbox("all"))
        self.app.update()

    def execute_hadamard(self):
        try:
            t_value = int(self.part_text.get())
            if t_value > 1:
                self.Calculo.t_value = t_value
                self.Calculo.hadamard = Hadarmard(t_value)
                self.Calculo.result = self.Calculo.hadamard.main(t_value)
                self.draw_rectangles(t_value)
            else:
                messagebox.showerror('Value of t must be greater than 1')
        except ValueError:
            messagebox.showerror('A value for t is required', 'Must be an integer number')

    def next_hadamard(self):
        if not(self.Calculo.hadamard is None) :
            t_value = self.Calculo.t_value
            self.Calculo.result = self.Calculo.hadamard.main(t_value)
            if self.Calculo.result is None:
                messagebox.showerror('There is no more possible combinations for this value of t')
            else:
                self.draw_rectangles(t_value)
        else:
            messagebox.showerror('Hadarmard first search should be executed first')

    def prueba_comb(self):
        try:
            t_value = int(self.part_text.get())
            try:
                combinacion =(int(num) for num in comb_var.split(","))
                self.Calculo.t_value = t_value
                self.Calculo.hadamard = Hadarmard(t_value)
                self.Calculo.result = self.Calculo.hadamard.obtiene_matriz_hadamard(t_value, combinacion)
                if Calculo.result:
                    self.draw_rectangles(t_value)
            except ValueError:
                messagebox.showerror('Values for the combination must be all integers')
        except ValueError:
            messagebox.showerror('A value for t is required', 'Must be an integer number')

    def display_matrix(self):
        top = Toplevel()
        top.geometry('500x500')
        matrix = Canvas(top, width=500, height=500, bg="black")
        mat_sb_x = Scrollbar(top)
        mat_sb_y = Scrollbar(top)
        matrix.config(xscrollcommand=mat_sb_x.set, yscrollcommand=mat_sb_y.set, highlightthickness=0)
        mat_sb_x.config(orient=HORIZONTAL, command=matrix.xview)
        mat_sb_y.config(orient=VERTICAL, command=matrix.yview)
        t_value = self.Calculo.t_value
        final_mat = np.ones((4*t_value,4*t_value), dtype=np.int32)
        for mat in self.Calculo.result:
            if type(mat) is tuple:
                for c in mat:
                    final_mat = np.multiply(final_mat,self.Calculo.hadamard.cobordes[c])
            else:
                final_mat = np.multiply(final_mat,self.Calculo.hadamard.cobordes[mat])
        for i in range(4*t_value):
            for j in range(4*t_value):
                color = "red" if final_mat[i,j] == -1 else "white"
                matrix.create_rectangle(25*(i), 25*(j), 25*(i+1), 25*(j+1), fill=color, outline = 'blue')
        matrix.config(scrollregion=matrix.bbox("all"))
        mat_sb_x.pack(fill=X, side=BOTTOM, expand=FALSE)
        mat_sb_y.pack(fill=Y, side=RIGHT, expand=FALSE)
        matrix.pack(side=LEFT,expand=True,fill=BOTH)
        top.update()

    def __main__(self):

        self.mainFrame.grid(row=0, column=0, sticky="nswe")

        self.topFrame.grid(row=0, sticky="nswe")

        part_label = Label(self.topFrame, text='Variable T: ', font=('bold', 16), pady=20)
        part_entry = Entry(self.topFrame, textvariable=self.part_text)
        start_btn = Button(self.topFrame, text='Start calculation', width=20, command=self.execute_hadamard)

        part_label.grid(row=0, column=0)
        part_entry.grid(row=0, column=1)
        start_btn.grid(row = 0, column=2, pady=20)

        self.middleFrame.grid(row=1, sticky="nswe")

        self.canvas.config(xscrollcommand=self.scrollbar.set, highlightthickness=0)
        self.scrollbar.config(orient=HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)

        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

        self.bottomFrame.grid(row=3, sticky="nswe")

        start_btn = Button(self.bottomFrame, text='Next Combination', width=20, command=self.next_hadamard)
        start_btn.grid(row=0, column=1, pady=20, padx=10)
        start_btn = Button(self.bottomFrame, text='Draw Matrix', width=20, command=self.display_matrix)
        start_btn.grid(row=0, column=0, pady=20, padx=10)

        comb_text = Label(self.bottomFrame, text='Combinacion propuesta: ', font=('bold', 16), pady=20)
        comb_entry = Entry(self.bottomFrame, textvariable=self.comb_var, width=25)
        comb_text.grid(row=1, column=0)
        comb_entry.grid(row=1, column=1)

        self.mainFrame.place(relx=0.25, rely=0.15)
        self.app.title('Hadarmard App')
        self.app.geometry('800x400')

        self.app.mainloop()

app = App()
app.__main__()