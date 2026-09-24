import json
import os 
import customtkinter as ctk
import subprocess
import matplotlib.pyplot as plt

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
        carpeta_sctipt_actual = os.path.dirname(os.path.abspath(__file__))
        self.ruta_json = os.path.abspath(os.path.join(carpeta_sctipt_actual,"..","data_xml","reporte_analizado.json"))
        self.base_datos = self.cargar_base_datos()

        #Elemento 1:
        self.titulo = ctk.CTkLabel(
            self,
            text = "Analizador XBRLI",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.titulo.pack(padx=20, pady=20)
        
        #Boton que activará el Reporte.py o sea EL GRAFICO COMPARATIVO:
        self.btn_grafico = ctk.CTkButton(
            self, 
            text="📈 Generar Gráfico Comparativo Histórico", 
            command=self.lanzar_motor_grafico,
            fg_color="#1f77b4", 
            hover_color="#115584",
            font=ctk.CTkFont(weight="bold", size=14),
            height=40
        )
        #Se realiza una correción aquí para poder conectarse al .json
        self.btn_grafico.pack(padx=20, pady=10)


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

        #Elemento para exportar a Excel (nuevo)
        self.btn_excel = ctk.CTkButton(
            self, 
            text="📥 Exportar Base de Datos a Excel", 
            command=self.ejecutar_exportacion,
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_excel.pack(padx=20, pady=15)



    def cargar_base_datos(self):
            if os.path.exists(self.ruta_json):
                with open(self.ruta_json, "r", encoding="utf-8") as archivo:
                    return json.load(archivo)
            return None
    
    #Lanza o ejecuta al reporte.py:
    def lanzar_motor_grafico(self):
        try:
            self.lbl_estado.configure(text="⏳ Procesando datos y dibujando gráfico...", text_color="#ffb703")
            self.update() # Fuerza a la ventana a actualizar el texto de inmediato
            
            # Ejecutamos el comando 'python reporte.py'en la raiz inicial
            carpeta_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_reporte_py = os.path.abspath(os.path.join(carpeta_actual,"..","reporte.py"))
            subprocess.run(["python", ruta_reporte_py], check=True)
            
            self.lbl_estado.configure(text="✅ ¡Gráfico de Competidores Abierto!", text_color="#2ca02c")
        except Exception as e:
            self.lbl_estado.configure(text=f"❌ Error al lanzar report_engine.py: {str(e)}", text_color="#d32f2f")

    
    def ejecutar_exportacion(self):
        # Aquí reutilizamos la lógica exacta de tu archivo exporter.py
        try:
            ratios_a_exportar = ['Net Income', 'Margen Neto', 'ROE', 'ROA', 'Prueba ácida', 'Ratio Deuda/Activo']
            with pd.ExcelWriter(ruta_excel, engine='openpyxl') as writer:
                for empresa, datos_historicos in self.base_datos.items():
                    años_ordenados = sorted(list(datos_historicos.keys()))
                    matriz_excel = {}
                    for ratio in ratios_a_exportar:
                        matriz_excel[ratio] = [datos_historicos[año].get(ratio, 0) for año in años_ordenados]
                    df = pd.DataFrame(matriz_excel, index=años_ordenados).T
                    df.to_excel(writer, sheet_name=empresa, index_label="Ratio / Métrica")
            
            # Cambiamos el texto del estado para avisarle al usuario en tiempo real
            self.lbl_estado.configure(text=f"📊 ¡Excel generado con éxito en data_xml!", text_color="#2ca02c")
        except Exception as e:
            self.lbl_estado.configure(text=f"❌ Error al exportar: {str(e)}", text_color="#d32f2f")


# 3. Lanzador del bucle principal de la ventana
if __name__ == "__main__":
    app = AppFinanzas()
    app.mainloop()
