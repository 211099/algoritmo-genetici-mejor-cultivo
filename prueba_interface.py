import tkinter as tk
from main_clase import AlgoritmoGenetico
class ConfigWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Configuración')
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.hide)  # Sobrescribe el evento de cierre de la ventana.
        self.withdraw()  # Oculta la ventana hasta que se necesite.

        self.inputs = []
        titulo_labels = ["cantidad poblacion inicial","poblacion Maxima","posibilidad de cruza","probabilidad de mutacion del individuo","probabilidad de mutacion del gen","cantidad de iteraciones"]
        default_values = ["37", "93", "68", "37", "22", "112"]

        for i in range(6):
            tk.Label(self, text=titulo_labels[i], font=('Arial', 20), anchor='w').grid(row=i, column=0, sticky='w', padx=(20, 10), pady=10)
            entry = tk.Entry(self, font=('Arial', 20))
            entry.insert(0, default_values[i])
            entry.grid(row=i, column=1, padx=(10, 20), pady=10)
            self.inputs.append(entry)

        tk.Button(self, text="Recopilar datos", command=self.collect_data, font=('Arial', 20)).grid(row=7, columnspan=2, padx=20, pady=20)

    def collect_data(self):
        return [entry.get() for entry in self.inputs]

    def hide(self):
        """Oculta la ventana en lugar de destruirla."""
        self.withdraw()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.config_window = ConfigWindow(self)
        

        tk.Label(self, text='proyectoc3', font=('Arial', 25)).grid(row=0, columnspan=3, pady=20)

        self.inputs = []
        titulo_labels = ["quecultivo quieres sembrar?","algun tipo de cultivo en especifico","tipo de suelo","nutrientes del suelo","clima del area","riesgos conocidos","mes de la siembra","cantidad de cultivos","PH del suelo"]

        for i in range(len(titulo_labels)):
            tk.Label(self, text=titulo_labels[i], font=('Arial', 20), anchor='w').grid(row=i+1, column=0, sticky='w', padx=(20, 10), pady=10)
            entry = tk.Entry(self, font=('Arial', 20))
            entry.grid(row=i+1, column=1, padx=(10, 20), pady=10)
            self.inputs.append(entry)

        tk.Button(self, text="Recopilar datos", command=self.collect_all_data, font=('Arial', 20)).grid(row=len(titulo_labels)+1, columnspan=3, padx=20, pady=20)

        # Asegúrate de tener la imagen correcta para este botón.
        config_icon = tk.PhotoImage(file='icono.png')
        config_button = tk.Button(self, image=config_icon, command=self.open_config)
        config_button.image = config_icon
        config_button.grid(row=1, column=2, sticky='nsew', padx=(50, 20), pady=10)

    def open_config(self):
        self.config_window.deiconify()

    def collect_all_data(self):
        main_data = [entry.get() for entry in self.inputs]
        config_data = self.config_window.collect_data()
        print("Datos de MainApp:", main_data)
        print("Datos de ConfigWindow:", config_data)
        
        print("Antes de llamar a AlgoritmoGenetico.main()")
    
        
        cultivo_requerido_sin_espacios = main_data[0].replace(' ', '')  # Eliminar los espacios
        cultivo_requerido = cultivo_requerido_sin_espacios.split(',') 
        tipo_cultivo_sin_espacios = main_data[1].replace(' ','')
        tipo_cultivo =  tipo_cultivo_sin_espacios.split(',')
        tipo_suelo = main_data[2].replace(" ","")
        nutrientes_suelo_sin_espacios = main_data[3].replace(' ','')
        nutrientes_suelo = nutrientes_suelo_sin_espacios.split(',')
        riesgo_conocido_sin_espacios = main_data[5].replace(' ','')
        riesgo_conocido = riesgo_conocido_sin_espacios.split(',')
        self.algoritmo = AlgoritmoGenetico(arreglo_data_algoritmo=config_data,cultivo_requerido=cultivo_requerido,tipo_cultivo=tipo_cultivo,tipo_suelo=tipo_suelo,nutrientes_suelo=nutrientes_suelo,arreglo_data_main=main_data,riesgo_conocido=riesgo_conocido)
        self.algoritmo.main()
        print("Después de llamar a AlgoritmoGenetico.main()")



if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
