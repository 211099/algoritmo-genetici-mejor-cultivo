import tkinter as tk
from tkinter import simpledialog

class ConfigWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Configuración')
        self.geometry("800x600")  # Ajusta el tamaño de la ventana emergente a tu preferencia.
        self.inputs = []

        titulo_labels = ["quecultivo quieres sembrar?","algun tipo de cultivo en especifico","tipo de suelo","nutrientes del suelo","clima del area","riesgos conocidos","mes de la siembra"]

        for i in range(6):
            tk.Label(self, text=titulo_labels[i], font=('Arial', 20)).grid(row=i, column=0, sticky='w', padx=(20, 10), pady=10)
            entry = tk.Entry(self, font=('Arial', 20))
            entry.grid(row=i, column=1, padx=(10, 20), pady=10)
            self.inputs.append(entry)

        tk.Button(self, text="Recopilar datos", command=self.collect_data, font=('Arial', 20)).grid(row=7, columnspan=2, padx=20, pady=20)

    def collect_data(self):
        data = [entry.get() for entry in self.inputs]
        print(data)  # Aquí puedes hacer lo que necesites con los datos.

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

        tk.Label(self, text='proyectoc3', font=('Arial', 25)).grid(row=0, columnspan=3, pady=20)

        self.entries = []
        titulo_labels = ["quecultivo quieres sembrar?","algun tipo de cultivo en especifico","tipo de suelo","nutrientes del suelo","clima del area","riesgos conocidos","mes de la siembra"]
        titulo_labels_configuracion = ["cantidad poblacion inicial","poblacion Maxima","posibilidad de cruza","probabilidad de mutacion del individuo","probabilidad de mutacion del gen","cantidad de iteraciones"]
        
        for i in range(len(titulo_labels)):
            tk.Label(self, text=titulo_labels[i], font=('Arial', 20)).grid(row=i+1, column=0, sticky='w', padx=(20, 10), pady=10)
            entry = tk.Entry(self, font=('Arial', 20))
            entry.grid(row=i+1, column=1, padx=(10, 20), pady=10)
            self.entries.append(entry)

        tk.Button(self, text="Recopilar datos", command=self.collect_data, font=('Arial', 20)).grid(row=len(titulo_labels_configuracion)+2, columnspan=3, padx=20, pady=20)

        # Asegúrate de cambiar 'icono_tuerca.png' a la ruta de tu icono.
        config_icon = tk.PhotoImage(file='icono.png')
        config_button = tk.Button(self, image=config_icon, command=self.open_config)
        config_button.image = config_icon
        config_button.grid(row=1, column=2, sticky='nsew', padx=(50, 0), pady=10)  # Padding de 50 pixels a la izquierda

    def collect_data(self):
        data = [entry.get() for entry in self.entries]
        print(data)  # Aquí puedes hacer lo que necesites con los datos.

    def open_config(self):
        ConfigWindow(self)

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
