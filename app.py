from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from hadamard import Hadarmard
from GA import GA
import numpy as np

class Calculo:
    hadamard = None
    genetico = None
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
        self.t_text = StringVar()
        self.middle_frame = Frame(self.main_frame, pady=5)
        self.canvas = Canvas(self.middle_frame, width=200, height=100, bg="white")
        self.scrollbar = Scrollbar(self.middle_frame)
        self.bottom_frame = Frame(self.main_frame)
        self.comb_var = StringVar()
        self.max_cob_var = StringVar()
        self.num_gen_var = StringVar()
        self.num_sel_var = StringVar()
        self.num_ind_var = StringVar()
        self.mut_rate_var = StringVar()
        self.cobordes_canvas = []
        self.comb_encontradas = []

    def clickedCob(self, number):

        (button,color) =  self.cobordes_canvas[number]
        color_actual =  button.cget('bg')
        valor = 2**number

        if color == "blue":
            self.Calculo.static_cob -= valor
            self.Calculo.prohibited_cob += valor
            button.config(bg="yellow")
            color = "yellow"
        elif color=="yellow":
            self.Calculo.prohibited_cob -= valor
            button.config(bg="white")
            color = "white"
        else:
            self.Calculo.static_cob += valor
            button.config(bg="blue")
            color = "blue"
        self.cobordes_canvas[number] = ((button,color))
        self.app.update() 

    def draw_rectangles(self,t_value):
        canvas = self.canvas
        self.cobordes_canvas = []
        canvas.delete('all')
        resultado = [] if self.Calculo.result is None else self.Calculo.result
        for number in range(2,2*t_value+1):
            button = Button(self.canvas, width=4, text=number)
            button.configure(bg="white", activebackground="white", command=lambda 
                num = number-2: self.clickedCob(num),relief="flat")
            self.cobordes_canvas.append((button,"white"))
            self.canvas.create_window((50*(number-2), 50), window=button, anchor=CENTER)

        for number in range(2*t_value+1,4*t_value-1):
            button = Button(canvas, width=4, text=number)
            button.configure(bg="white", activebackground="white", command=lambda 
                num = number-2: self.clickedCob(num),relief="flat")
            self.cobordes_canvas.append((button,"white"))
            self.canvas.create_window((50*(number-2*t_value), 100), window=button, anchor=CENTER)
        canvas.config(scrollregion=canvas.bbox("all"))
        self.app.update()

    def update_rectangles(self,t_value):
        canvas = self.canvas
        canvas.delete('all')
        resultado = [] if self.Calculo.result is None else self.Calculo.result
        for number in range(2,2*t_value+1):
            (button,color) =  self.cobordes_canvas[number-2]
            if number-2 in resultado:
                if color=="white":
                    color = "red"
            else:
                if color =="red":
                    color = "white"
            button.configure(bg=color, activebackground=color, command=lambda
                num = number-2: self.clickedCob(num),relief="flat")
            self.cobordes_canvas[number-2] = (button,color)
            self.cobordes_canvas.append(button)
            self.canvas.create_window((50*(number-2), 50), window=button, anchor=CENTER)

        for number in range(2*t_value+1,4*t_value-1):
            (button,color) =  self.cobordes_canvas[number-2]
            if number-2 in resultado:
                if color=="white":
                    color = "red"
            else:
                if color =="red":
                    color = "white"
            button.configure(bg=color, activebackground=color, command=lambda 
                num = number-2: self.clickedCob(num),relief="flat")
            self.cobordes_canvas[number-2] = (button,color)
            self.canvas.create_window((50*(number-2*t_value), 100), window=button, anchor=CENTER)

        canvas.config(scrollregion=canvas.bbox("all"))
        self.app.update()

    def init_hadamard(self):
        t_value = int(self.t_text.get())
        self.comb_encontradas = []
        max = self.max_cob_var.get()
        if len(max)>0:
            try:
                max = int(max)
                t_value = int(self.t_text.get())
                if max > t_value-1 and max < 3*t_value-2:
                    if t_value > 1:
                        self.Calculo.t_value = t_value
                        self.Calculo.hadamard = Hadarmard(t_value,max=max)
                        self.draw_rectangles(t_value)
                    else:
                        messagebox.showerror('T Value error','Value of t must be greater than 1')
                else:
                    messagebox.showerror('Max configuration error','Value of max must be greater than t-1 and minor than 3*t-2')
            except ValueError as ex:
                print("Se produjo un error:", ex)
                messagebox.showerror('A value for t is required', 'Must be an integer number')
        else:
            try:
                t_value = int(self.t_text.get())
                if t_value > 1:
                    self.Calculo.t_value = t_value
                    self.Calculo.hadamard = Hadarmard(t_value)
                    self.draw_rectangles(t_value)
                else:
                    messagebox.showerror('Value of t must be greater than 1')
            except ValueError as ex:
                messagebox.showerror('Wrong max value', 'Must be an integer number')


    def next_hadamard(self):
        if not(self.Calculo.hadamard is None) :
            t_value = self.Calculo.t_value
            self.Calculo.result = np.sort(self.Calculo.hadamard.__main__(t_value, fijos=self.Calculo.static_cob, prohibidos= self.Calculo.prohibited_cob))
            if self.Calculo.result is None:
                messagebox.showerror('There is no more possible combinations for this value of t')
            else:
                self.comb_encontradas.append(self.Calculo.result)
                self.update_rectangles(t_value)
        else:
            messagebox.showerror('Hadarmard first search should be executed first')
    
    def genetic_algorithm(self):
        try:
            t_value = int(self.t_text.get())
            num_gen = int(self.num_gen_var.get())
            sel_var = int(self.num_sel_var.get())
            num_ind = int(self.num_ind_var.get())
            mut_rate = float(self.mut_rate_var.get())
            if t_value > 1:
                self.Calculo.t_value = t_value
                self.draw_rectangles(t_value)
                self.Calculo.genetico = GA(t_value, num_ind, sel_var, num_gen, mut_rate)
                self.Calculo.result = self.Calculo.genetico.__main__()
                if self.Calculo.result is None:
                    messagebox.showerror('There is no solution found')
                else:
                    self.comb_encontradas.append(self.Calculo.result)
                    self.update_rectangles(t_value)
            else:
                messagebox.showerror('Value of t must be greater than 1')
        except ValueError as ex:
            print(ex)
            messagebox.showerror('Bad format of numbers', 'T value, Num Generations, Num Individuos and Num Selecciones must be integers numbers \n And mutation rate a decimal between 0 and 1')

    def display_matrix(self):
        top = Toplevel()
        top.geometry('500x500')
        top.title('Representación de la combinación: {}'.format(self.Calculo.result+2))
        matrix = Canvas(top, width=500, height=500, bg="black")
        mat_sb_x = Scrollbar(top)
        mat_sb_y = Scrollbar(top)
        matrix.config(xscrollcommand=mat_sb_x.set, yscrollcommand=mat_sb_y.set, highlightthickness=0)
        mat_sb_x.config(orient=HORIZONTAL, command=matrix.xview)
        mat_sb_y.config(orient=VERTICAL, command=matrix.yview)
        t_value = self.Calculo.t_value
        final_mat = np.ones((4*t_value,4*t_value), dtype=np.int32)
        for mat in self.Calculo.result:
            final_mat = np.multiply(final_mat,self.Calculo.hadamard.cobordes[mat].copy())
        final_mat = np.multiply(final_mat, self.Calculo.hadamard.R.copy())
        for i in range(4*t_value):
            for j in range(4*t_value):
                color = "red" if final_mat[j][i] == -1 else "white"
                matrix.create_rectangle(25*i, 25*j, 25*(i+1), 25*(j+1), fill=color, outline = 'blue')
        matrix.config(scrollregion=matrix.bbox("all"))
        mat_sb_x.pack(fill=X, side=BOTTOM, expand=FALSE)
        mat_sb_y.pack(fill=Y, side=RIGHT, expand=FALSE)
        matrix.pack(side=LEFT,expand=True,fill=BOTH)
        top.update()

    def display_encountered_comb(self):
        top = Toplevel()
        top.geometry('700x500')
        top.title("Matrices encontradas")
        texto_inicial = 'Se encontraron un total de {} combinacion/es\n'.format(len(self.comb_encontradas))
        Label(top, text=texto_inicial, font= ('Helvetica bold',14)).pack(anchor=CENTER)
        v = Scrollbar(top)
        v.pack(side = RIGHT, fill = Y)
        t = Text(top, width = 15, wrap = NONE,
                 yscrollcommand = v.set)
        for comb in self.comb_encontradas:
            t.insert(END,'Combinación:{} \n'.format(comb+2))
        t.pack(side=TOP, fill=X)
        v.config(command=t.yview)

        top.update()


    def __main__(self):

        self.main_frame.place(relx=0.5, rely=0.5,anchor=CENTER)

        self.top_frame.grid(row=0, sticky="s")

        t_label = Label(self.top_frame, text='Variable T: ', font=('bold', 8))
        t_entry = Entry(self.top_frame, textvariable=self.t_text, width=5)
        max_cob_label = Label(self.top_frame, text='Maximo Cobordes: ', font=('bold', 8))
        max_cob_entry = Entry(self.top_frame, textvariable=self.max_cob_var, width=5)
        start_btn = Button(self.top_frame, text='Configurar', width=15, command=self.init_hadamard)

        start_btn.grid(row=0, column=2, pady=5)
        t_label.grid(row=1, column=0)
        t_entry.grid(row=1, column=1)
        max_cob_label.grid(row=1, column=3)
        max_cob_entry.grid(row=1, column=4)

        self.middle_frame.grid(row=1, sticky=NSEW)

        self.canvas.config(xscrollcommand=self.scrollbar.set, highlightthickness=0)
        self.scrollbar.config(orient=HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)

        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)

        self.bottom_frame.grid(row=2)

        siguiente_comb_btn = Button(self.bottom_frame, text='Calcula', width=15, command=self.next_hadamard)
        siguiente_comb_btn.grid(row=0, column=2)
        dibuja_btn = Button(self.bottom_frame, text='Dibuja Matriz', width=15, command=self.display_matrix)
        dibuja_btn.grid(row=0, column=0)

        muestra_encontradas_btn = Button(self.bottom_frame, text='Matrices Encontradas ', width=18, command=self.display_encountered_comb)
        muestra_encontradas_btn.grid(row=0, column=1, pady=5, padx=5)

        num_gen_label = Label(self.bottom_frame, text='Num Generaciones: ', font=('bold', 8))
        num_gen_entry = Entry(self.bottom_frame, textvariable=self.num_gen_var, width=5)
        num_gen_label.grid(row=1, column=0)
        num_gen_entry.grid(row=1, column=1)

        num_sel_label = Label(self.bottom_frame, text='Num Selecciones: ', font=('bold', 8))
        num_sel_entry = Entry(self.bottom_frame, textvariable=self.num_sel_var, width=5)
        num_sel_label.grid(row=1, column=2)
        num_sel_entry.grid(row=1, column=3)

        num_ind_label = Label(self.bottom_frame, text='Num Individuos: ', font=('bold', 8))
        num_ind_entry = Entry(self.bottom_frame, textvariable=self.num_ind_var, width=5)
        num_ind_label.grid(row=2, column=0)
        num_ind_entry.grid(row=2, column=1)

        mut_rate_label = Label(self.bottom_frame, text='Tasa de mutación: ', font=('bold', 8))
        mut_rate_entry = Entry(self.bottom_frame, textvariable=self.mut_rate_var, width=5)
        mut_rate_label.grid(row=2, column=2)
        mut_rate_entry.grid(row=2, column=3)

        muestra_encontradas_btn = Button(self.bottom_frame, text='Algoritmo Genetico', width=15, command=self.genetic_algorithm)
        muestra_encontradas_btn.grid(row=3, column=1, pady=5, padx=5)

        self.app.title('Hadarmard App')
        self.app.geometry('800x400')

        self.app.mainloop()

app = App()
app.__main__()