import json
import os 
import customtkinter as ctk

#Variables básicas:
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#Iniciación de la aplicación de escritorio:
class AppFinanzas(ctk.CTk):
    def __init__(self):
        super().__init__()

        #Títulos y otros:
        self.title("SMV Equity Analytics - Desktop Edition")
        self.geometry("600x400")

        #Conexión segura a la BD NoSQL Json:
        self.ruta_json = "../data_xml/reporte_analizado.json"
        self.base_datos = self.cargar_base_datos()

        #Elemento 1:
        self.titulo = ctk.CTkLabel(
            self,
            text = "Analizador XBRLI",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.titulo.pack(padx=20, pady=20)
        

        #Elemento visual 2: Etiqueta de estado de la base de datos 
        if self.base_datos:
            empresas = list(self.base_datos.keys())
            mensaje = f"(Base de datos concetada con las Empresas:{', '.join(empresas)})"
        else:
            mensaje = "Error en cargar el reporte_analizado.json "

        self.lbl_estado = ctk.CTkLabel(self, text=mensaje, text_color="#2ca02c")
        self.lbl_estado.pack(padx=20, pady=10)

        # --- CONTENEDOR DE CONTROLES (FRAME INTERACTIVO) ---
        # Creamos una "caja" interna para agrupar los desplegables
        self.frame_controles = ctk.CTkFrame(self)
        self.frame_controles.pack(padx=20, pady=20, fill="x")
        
        # Selector 1: Empresa
        self.lbl_empresa = ctk.CTkLabel(self.frame_controles, text="Seleccionar Empresa:", font=ctk.CTkFont(size=13))
        self.lbl_empresa.grid(row=0, column=0, padx=15, pady=10, sticky="w")
        
        # CORRECCIÓN: Se cambió self.empresas por empresas (o una lista vacía si falla la carga)
        self.combo_empresa = ctk.CTkComboBox(self.frame_controles, values=empresas if self.base_datos else [])
        self.combo_empresa.grid(row=0, column=1, padx=15, pady=10)
        
        # Selector 2: Ratio / Métrica
        self.ratios_disponibles = ['Net Income', 'Margen Neto', 'ROE', 'ROA']
        
        self.lbl_ratio = ctk.CTkLabel(self.frame_controles, text="Seleccionar Ratio:", font=ctk.CTkFont(size=13))
        self.lbl_ratio.grid(row=1, column=0, padx=15, pady=10, sticky="w")
        
        self.combo_ratio = ctk.CTkComboBox(self.frame_controles, values=self.ratios_disponibles)
        self.combo_ratio.grid(row=1, column=1, padx=15, pady=10)


    def cargar_base_datos(self):
            if os.path.exists(self.ruta_json):
                with open(self.ruta_json, "r", encoding="utf-8") as archivo:
                    return json.load(archivo)
            return None

# 3. Lanzador del bucle principal de la ventana
if __name__ == "__main__":
    app = AppFinanzas()
    app.mainloop()
