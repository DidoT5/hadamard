from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from hadamard import Hadarmard
import numpy as np

class Calculo:
    hadamard = None
    t_value = None
    result = None
    static_cob = 0
    prohibited_cob = 0

class App:

    def __init__(self):
        self.app = Tk()
        self.Calculo = Calculo()
        self.main_frame = Frame(self.app)
        self.top_frame = Frame(self.main_frame)
        self.part_text = StringVar()
        self.middle_frame = Frame(self.main_frame)
        self.canvas = Canvas(self.middle_frame, width=200, height=100, bg="white")
        self.scrollbar = Scrollbar(self.middle_frame)
        self.bottom_frame = Frame(self.main_frame)
        self.comb_var = StringVar()
        self.cobordes_canvas = []

    def clickedCob(self, button, number):

        color_actual =  button.cget('bg')
        valor = 2**number

        if color_actual== "blue":
            self.Calculo.static_cob -= valor
            self.Calculo.prohibited_cob += valor
            button.config(bg="yellow")
        elif color_actual=="yellow":
            self.Calculo.prohibited_cob += valor
            button.config(bg="white")
        else:
            self.Calculo.static_cob += valor
            button.config(bg="blue")
        self.app.update() 

    def draw_rectangles(self,t_value):
        canvas = self.canvas
        self.cobordes_canvas = []
        canvas.delete('all')
        for number in range(2,2*t_value+1):
            color = "red" if number-2 in self.Calculo.result else "white"
            button = Button(self.canvas, width=4, text=number)
            button.configure(bg=color, activebackground=color, command=lambda x=button, 
                num = number-2: self.clickedCob(x, num),relief="flat")
            self.cobordes_canvas.append(button)
            self.canvas.create_window((50*(number-2), 50), window=button, anchor=CENTER)

        for number in range(2*t_value+1,4*t_value-1):
            color = "red" if number-2 in self.Calculo.result else "white"
            button = Button(canvas, width=4, text=number)
            button.configure(bg=color, activebackground=color, command=lambda x=button, 
                num = number-2: self.clickedCob(x, num),relief="flat")
            self.cobordes_canvas.append(button)
            self.canvas.create_window((50*(number-2*t_value), 100), window=button, anchor=CENTER)

        canvas.config(scrollregion=canvas.bbox("all"))
        self.app.update()

    def execute_hadamard(self):
        try:
            t_value = int(self.part_text.get())
            if t_value > 1:
                self.Calculo.t_value = t_value
                self.Calculo.hadamard = Hadarmard(t_value)
                self.Calculo.result = self.Calculo.hadamard.__main__(t_value)
                self.draw_rectangles(t_value)
            else:
                messagebox.showerror('Value of t must be greater than 1')
        except ValueError as ex:
            print("Se produjo un error:", ex)
            messagebox.showerror('A value for t is required', 'Must be an integer number')

    def next_hadamard(self):
        if not(self.Calculo.hadamard is None) :
            t_value = self.Calculo.t_value
            self.Calculo.result = self.Calculo.hadamard.__main__(t_value)
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
                    final_mat = np.multiply(final_mat,self.Calculo.hadamard.cobordes[c].copy())
            else:
                final_mat = np.multiply(final_mat,self.Calculo.hadamard.cobordes[mat].copy())
        final_mat = np.multiply(final_mat, self.Calculo.hadamard.R.copy())
        for i in range(4*t_value):
            print('Fila i:',i,final_mat[i])
            print('Suma de fila i:',np.sum(final_mat[i]))
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

        self.main_frame.grid(row=0, column=0, sticky="nswe")

        self.top_frame.grid(row=0, sticky="nswe")

        part_label = Label(self.top_frame, text='Variable T: ', font=('bold', 16), pady=20)
        part_entry = Entry(self.top_frame, textvariable=self.part_text)
        start_btn = Button(self.top_frame, text='Start calculation', width=20, command=self.execute_hadamard)

        part_label.grid(row=0, column=0)
        part_entry.grid(row=0, column=1)
        start_btn.grid(row = 0, column=2, pady=20)

        self.middle_frame.grid(row=1, sticky="nswe")

        self.canvas.config(xscrollcommand=self.scrollbar.set, highlightthickness=0)
        self.scrollbar.config(orient=HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)

        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

        self.bottom_frame.grid(row=3, sticky="nswe")

        start_btn = Button(self.bottom_frame, text='Next Combination', width=20, command=self.next_hadamard)
        start_btn.grid(row=0, column=1, pady=20, padx=10)
        start_btn = Button(self.bottom_frame, text='Draw Matrix', width=20, command=self.display_matrix)
        start_btn.grid(row=0, column=0, pady=20, padx=10)

        comb_text = Label(self.bottom_frame, text='Combinacion propuesta: ', font=('bold', 16), pady=20)
        comb_entry = Entry(self.bottom_frame, textvariable=self.comb_var, width=25)
        comb_text.grid(row=1, column=0)
        comb_entry.grid(row=1, column=1)

        self.main_frame.place(relx=0.25, rely=0.15)

        self.app.title('Hadarmard App')
        self.app.geometry('800x400')

        self.app.mainloop()

app = App()
app.__main__()