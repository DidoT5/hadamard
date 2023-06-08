from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import os
from hadamard import Hadarmard
import threading
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
        self.is_running_bf = False
        self.is_running_ga = False

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
        self.comb_encontradas = []
        max = self.max_cob_var.get()
        if len(max)>0:
            try:
                max = int(max)
                t_value = int(self.t_text.get())
                self.num_ind_var.set(t_value*8)
                if max >= t_value-1 and max < 3*t_value-2:
                    if t_value > 1:
                        self.Calculo.t_value = t_value
                        self.Calculo.hadamard = Hadarmard(t_value,max=max)
                        self.draw_rectangles(t_value)
                    else:
                        messagebox.showerror('Valor de t','Valor de t tiene que ser mayor que 1')
                else:
                    messagebox.showerror('Mala configuración de máximos','El valor de máximos cobordes debe ser mayor o igual que t-1 y menor que 3t-2')
            except ValueError as ex:
                messagebox.showerror('Valor de t', 'Se necesita un valor entero para t')
        else:
            try:
                t_value = int(self.t_text.get())
                self.num_ind_var.set(t_value*8)
                if t_value > 1:
                    self.Calculo.t_value = t_value
                    self.Calculo.hadamard = Hadarmard(t_value)
                    self.draw_rectangles(t_value)
                else:
                    messagebox.showerror('Valor de t','Valor de t tiene que ser mayor que 1')
            except ValueError as ex:
               messagebox.showerror('Valor de t', 'Se necesita un valor entero para t')


    def next_hadamard(self):
        while self.is_running_bf:
            if not(self.Calculo.hadamard is None) :
                t_value = self.Calculo.t_value
                self.Calculo.result = np.sort(self.Calculo.hadamard.__main__(t_value, fijos=self.Calculo.static_cob, prohibidos= self.Calculo.prohibited_cob))
                if self.Calculo.result is None:
                    messagebox.showerror('No hay más combinaciones posibles para este valor de t')
                else:
                    self.comb_encontradas.append(self.Calculo.result)
                    self.update_rectangles(t_value)
            else:
                messagebox.showerror('Confiuración Previa', 'Antes de empezar a buscar hay que establecer un valor para t')
            self.siguiente_comb_btn.config(text='Calcula', command=self.start_brute_force_thread)
            self.app.update()
            self.is_running_bf = False

    def start_brute_force_thread(self):
        if not self.is_running_bf:
            self.is_running_bf = True
            self.siguiente_comb_btn.config(text='Para', command=self.stop_brute_force_thread)
            self.app.update()
            thread = threading.Thread(target=self.next_hadamard)
            thread.start()

    def stop_brute_force_thread(self):
        self.siguiente_comb_btn.config(text='Calcula', command=self.start_brute_force_thread)
        self.app.update()
        self.is_running_bf = False
    
    def genetic_algorithm(self):
        try:
            while self.is_running_ga:
                if self.Calculo.t_value is None:
                    messagebox.showerror('No hay valor de t configurado')
                num_gen = int(self.num_gen_var.get())
                sel_var = int(self.num_sel_var.get())
                num_ind = int(self.num_ind_var.get())
                mut_rate = float(self.mut_rate_var.get())
                if self.Calculo.t_value > 1:
                    self.Calculo.genetico = GA(self.Calculo.t_value, num_ind, sel_var, num_gen, mut_rate)
                    self.Calculo.result = self.Calculo.genetico.__main__()
                    if self.Calculo.result is None:
                        messagebox.showerror('Algoritmo Genético','No se ha encontrado solución')
                    else:
                        self.comb_encontradas.append(self.Calculo.result)
                        self.update_rectangles(self.Calculo.t_value)
                self.algoritmo_genetico_btn.config(text='Algoritmo Genetico', command=self.start_ga_thread)
                self.is_running_ga = False
                self.app.update()
        except ValueError as ex:
            messagebox.showerror('Mal formato en las variables', 'Num Generaciones, Num Individuos y Num Selecciones tienen que ser enteros \n Y la tasa de mutación un número decimal entre 0 y 1')
            self.is_running_ga = False
    
    def start_ga_thread(self):
        if not self.is_running_ga:
            self.is_running_ga = True
            self.algoritmo_genetico_btn.config(text='Para AG', command=self.stop_ga_thread)
            self.app.update()
            thread = threading.Thread(target=self.genetic_algorithm)
            thread.start()

    def stop_ga_thread(self):
        self.algoritmo_genetico_btn.config(text='Algoritmo Genetico', command=self.start_ga_thread)
        self.app.update()
        self.is_running_ga = False

    def display_matrix(self):
        if self.Calculo.result is None:
            messagebox.showerror('No hay matriz encontrada', 'No se ha encontrado ninguna matriz y por lo tanto no puede ser representada ninguna')
            return
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

    def display_help(self):
        top = Toplevel()
        top.geometry('700x500')
        top.title("Guía de la App")
        texto_inicial = 'Cómo usar la App'
        Label(top, text=texto_inicial, font= ('Helvetica bold',14)).pack(anchor=CENTER)
        v = Scrollbar(top)
        y = Scrollbar(top, orient=HORIZONTAL)
        v.pack(side = RIGHT, fill = Y)
        y.pack(side = BOTTOM, fill = X)
        t = Text(top, width = 15, wrap = NONE, xscrollcommand = y.set, yscrollcommand = v.set)
        t.insert(END,'Primer paso (obligatorio):Es necesario darle un valor a la variable "Variable T", este valor debe ser entero y mayor que 1 \n\n'+
                'Segundo paso (obligatorio): Pulsar el botón "Configurar" para establecer el valor de la variable t y el máximo de cobordes en caso de tener valor \n\n'+
                'Una vez realizados los dos pasos obligatorios anteriores se verán unos números correspondientes a los cobordes, estos números te permiten \n' +
                'fijar un coborde (1 click o color azul) o prohibirlo (2 clicks o color amarillo), si un número es seleccionado por tercera vez este vuelve al estado normal \n\n'+
                'Por otro lado, tenemos la opción de elegir un número máximo de cobordes en el valor introducible "Máximo Cobordes", este valor debe ser entero además de mayor o igual que t-1 y menor que 3t-2\n'+
                'Cabe destacar que éstas últimas dos opciones por motivos lógicos sólo están disponibles para el algoritmo de búsqueda exhaustiva \n\n'+
                'Debajo de la ventana en la que son mostrados los cobordes encontramos un total de tres botones con distintos usos:\n'+
                '"Dibuja Matriz": Este botón muestra la forma que tiene la matriz resultante de la última combinación de Hadamard encontrada, señalando en rojo los "-1" y en blanco los "1"\n'+
                '"Matrices Encontradas:" Este botón muestra un listado de todas las combinaciones resultantes en matrices de Hadamard que han sido encontradas con cualquiera de los algoritmos disponibles\n'+
                '"Calcula": Este botón pone en marcha el algoritmo de búsqueda exhaustiva que recorre de principio a fin todo el espacio de búsqueda\n\n'+
                'A continuación encontramos la sección del Algoritmo Genético, por defecto este viene con un valor (recomendado) de 8t para la variable "Num Individuos",\n'+
                'Tenemos otras tres variables personalizabes "Num Generaciones","Num Selecciones" y "Tasa de Mutación", de estas cuatro variables \n'+
                '"Num Individuos", "Num Generaciones" y "Num Selecciones" tienen que tener valores enteros y "Tasa de mutación" un valor decimal \n'+
                'entre 0 y 1, aunque no se aconseja subirlo a más del 0.5.\n'+
                'Una vez que se les ha dado valor a todas estas variables se puede ejecutar el algoritmo genético pulsando el botón que está justo debajo "Algoritmo Genético"')
        t.pack(side=TOP, fill=BOTH)
        v.config(command=t.yview)
        y.config(command=t.xview)

        top.update()


    def __main__(self):

        self.main_frame.place(relx=0.5, rely=0.5,anchor=CENTER)

        self.top_frame.grid(row=0, sticky="s")

        t_label = Label(self.top_frame, text='Variable T: ', font=('bold', 8))
        t_entry = Entry(self.top_frame, textvariable=self.t_text, width=5)
        max_cob_label = Label(self.top_frame, text='Maximo Cobordes: ', font=('bold', 8))
        max_cob_entry = Entry(self.top_frame, textvariable=self.max_cob_var, width=5)
        start_btn = Button(self.top_frame, text='Configurar', width=15, command=self.init_hadamard)
        current_directory = os.path.dirname(os.path.abspath("app.py"))
        img_path = os.path.join(current_directory, "help.png")
        help_img = Image.open(img_path)
        img_width, img_heigth = help_img.size
        help_img_resize = help_img.resize((int(25*(img_width/img_heigth)),25))
        help_bttn_img = ImageTk.PhotoImage(help_img_resize)
        help_btn = Button(self.top_frame, image=help_bttn_img, borderwidth=0, command=self.display_help)

        help_btn.grid(row=0,column=0, pady=5)
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

        self.siguiente_comb_btn = Button(self.bottom_frame, text='Calcula', width=15, command=self.start_brute_force_thread)
        self.siguiente_comb_btn.grid(row=0, column=2)
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

        self.algoritmo_genetico_btn = Button(self.bottom_frame, text='Algoritmo Genetico', width=15, command=self.start_ga_thread)
        self.algoritmo_genetico_btn.grid(row=3, column=1, pady=5, padx=5)

        self.app.title('Hadarmard App')
        self.app.geometry('800x400')

        self.app.mainloop()

app = App()
thread = threading.Thread(target=app.__main__)
thread.run()