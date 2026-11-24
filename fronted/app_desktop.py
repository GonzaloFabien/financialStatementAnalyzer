import json
import os 
import customtkinter as ctk
import subprocess
import matplotlib.pyplot as plt
import pandas as pd

#Variables básicas:
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#Configuración Frontend para los colores:
COLORES = {
    "color_fondo_app" : "#0B0E14",
    "color_fondo_panel" : "#131722",
    "color_borde" : "#FF9800",
    "empresa_1" :  "#FF9800",
    "empresa_1_hover": "#7A4F0E",
    "empresa_2": "#2A2E39",       
    "empresa_2_hover": "#292727",
    "exito": "#00C805",           
    "exito_hover": "#009E04",
    "texto_principal": "#E0E3EB",
    "texto_secundario": "#787B86"

}


#--------------------------------Valores a mostrar--------------------------------
#Para ver los tag disponibles, ver lo último de analyzer.py 

valores_a_mostrar = [
    "Revenue",
    "CostOfSales",
    "Gross Margin",
    "Administrative Expenses",
    "Selling Expenses",
    "Operating Margin",
    "Finance Income",
    "Finance Expense",
    "Net Income",

    "Equity",
    "Assets",
    "ROA",
    "ROE"
]

#---------------------------------------------------------------------------------

#Iniciación de la aplicación de escritorio:
class AppFinanzas(ctk.CTk):
    def __init__(self):
        super().__init__()

        #Títulos y otros:
        self.title("SMV Equity Analytics - Desktop Edition")
        self.geometry("1200x720")
        self.configure(fb_color=COLORES["color_fondo_app"])


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
            fg_color= COLORES["empresa_2"], 
            hover_color= COLORES["empresa_2_hover"],
            font=ctk.CTkFont(weight="bold", size=14),
            height=40
        )
        #Se realiza una correción aquí para poder conectarse al .json
        self.btn_grafico.pack(padx=20, pady=10)


        #Elemento visual 2: Etiqueta de estado de la base de datos 
        if self.base_datos:
            empresas = list(self.base_datos.keys())
            mensaje = f"(Base de datos concetada con las Empresas:{', '.join(empresas)})"

            #Extraermos los ratios dinamicamente :
            nombre_emprecita =  list(self.base_datos.keys())[0]
            primer_año = list(self.base_datos[nombre_emprecita].keys())[0]
            
            #Extraemos todos los datos posibles 
            self.ratios_disponibles = list(self.base_datos[nombre_emprecita ][primer_año].keys())
            
            
        else:
            self.empresas = ["No disponible"]
            self.ratios_disponibles = ["No disponible"]
            mensaje = "Error en cargar el reporte_analizado.json "


        self.lbl_estado = ctk.CTkLabel(self, text=mensaje, text_color= COLORES["texto_principal"])
        self.lbl_estado.pack(padx=20, pady=10)

        # --- CONTENEDOR DE CONTROLES (FRAME INTERACTIVO) ---
        # Creamos una "caja" interna para agrupar los desplegables
        self.frame_controles = ctk.CTkFrame(self)
        self.frame_controles.pack(padx=20, pady=15, fill="x")

        #Configuramos la figura 1, para que absorba el espacio disponible:
        self.frame_controles.grid_columnconfigure(1, weight=1)

        #------ Row 0: Empresa 1 ------
        self.lbl_empresa = ctk.CTkLabel(self.frame_controles, text="Empresa 1 :", font=ctk.CTkFont(size=13, weight='bold'))
        self.lbl_empresa.grid(row=0, column=0, padx=15, pady=8, sticky="w")
        
        # CORRECCIÓN: Se cambió self.empresas por empresas (o una lista vacía si falla la carga)
        self.combo_empresa = ctk.CTkComboBox(
            self.frame_controles,
            values = empresas if self.base_datos else [],
            width= 220,
            border_color= COLORES["empresa_1"],
            button_color= COLORES["empresa_1"],
            button_hover_color= COLORES["empresa_1_hover"]
        )
        #Agregamos sticky="ew" para alinearlos perfectamente
        self.combo_empresa.grid(row=0, column=1, padx=15, pady=8, sticky="w")

        #------ ROW 1: Emprea 2 ------
        #Combobox de la segunda empresa a anlizar:
        self.lbl_empresa2 = ctk.CTkLabel(self.frame_controles, text="Empresa 2", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_empresa2.grid(row=1, column=0, padx=15, pady=8, sticky="w") # <-- Corregido pady a 10
        
        self.combo_empresa2 = ctk.CTkComboBox(
            self.frame_controles, 
            values=empresas if self.base_datos else [],
            width=220,
            border_color= COLORES["empresa_2"],
            button_color= COLORES["empresa_2"],
            button_hover_color= COLORES["empresa_2_hover"]
        )
        self.combo_empresa2.grid(row=1, column=1, padx=15, pady=8, sticky="w")
        if self.base_datos and len(empresas) > 1: 
            self.combo_empresa2.set(empresas[1]) # Protegido si falla la BD

        # Selector 2: Ratio / Métrica
        
        
        self.lbl_ratio = ctk.CTkLabel(self.frame_controles, text="Seleccionar Ratio:", font=ctk.CTkFont(size=13))
        self.lbl_ratio.grid(row=2, column=0, padx=15, pady=10, sticky="w")
        
        self.combo_ratio = ctk.CTkComboBox(
            self.frame_controles, 
            values=self.ratios_disponibles,
            width= 220,
            border_color= COLORES["color_borde"],
            button_color=COLORES["empresa_1"],
            button_hover_color= COLORES["empresa_1_hover"]
        )
        self.combo_ratio.grid(row=2, column=1, padx=15, pady=10, sticky="w")

        #Esta configuración del botón de aquí fue mala idea, la eliminé.

            
        # Botón secundario para activar la Tabla Numérica Histórica (Empresa 1)
        self.btn_tabla = ctk.CTkButton(
            self, 
            text="📊 Mostrar Tabla Histórica (Empresa 1)", 
            command=self.mostrar_tabla_numerica,
            fg_color= COLORES["color_fondo_panel"], # Color verde para diferenciarlo del gráfico azul
            hover_color= COLORES["color_borde"],
            border_color= COLORES["empresa_1"],
            font=ctk.CTkFont(weight="bold", size=14),
            height=40
        )
        self.btn_tabla.pack(padx=20, pady=10)
        #Self ruta excel
        #Declaramos FRAME_TABLA y tambien esto permite hacer Scroll para mostrar la empresa en su selección:
        self.frame_tabla = ctk.CTkScrollableFrame(self, height=180)
        
        #Elemento para exportar a Excel (nuevo)
        self.btn_excel = ctk.CTkButton(
            self, 
            text="📥 Exportar Base de Datos a Excel", 
            command=self.abrir_pestaña_modal,
            fg_color = COLORES["exito_hover"],
            text_color = "#000000",
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
            self.lbl_estado.configure(text="⏳ Procesando datos y dibujando gráfico...", text_color= COLORES["empresa_1"])
            self.update() # Fuerza a la ventana a actualizar el texto de inmediato

            #Segmentamos en dos empresas: 
            empresa_1 = self.combo_empresa.get()
            empresa_2 = self.combo_empresa2.get()
            ratio_a_analizar = self.combo_ratio.get()

            # Ejecutamos el comando 'python reporte.py'en la raiz inicial
            carpeta_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_reporte_py = os.path.abspath(os.path.join(carpeta_actual,"..","reporte.py"))
            subprocess.run(["python", ruta_reporte_py, empresa_1, empresa_2, ratio_a_analizar], check=True)
            
            self.lbl_estado.configure(text="🗸 ¡Gráfico de Competidores Abierto!", text_color="#2ca02c")
        except Exception as e:
            self.lbl_estado.configure(text=f"❌ Error al lanzar report_engine.py: {str(e)}", text_color="#d32f2f")

    
    def mostrar_tabla_numerica(self):
        try:
            # 0- Se limpia cualquier consulta previa
            for widget in self.frame_tabla.winfo_children():
                widget.destroy()
                
            # 1- Seleccionamos la empresa usando el Combobox de empresa 1: 
            empresa_activa = self.combo_empresa.get()
            datos_empresa = self.base_datos.get(empresa_activa, {})

            if not datos_empresa:
                self.lbl_estado.configure(text=f"No se encuentran datos para {empresa_activa}", text_color="#d32f2f")
                return
            
            # 2- Ordenamos cronológicamente los años de la empresa actual
            #print(datos_empresa.values()) #Datos empresa es donde están todos los datos absolutos de la empresa:------------
            años_ordenados = sorted(list(datos_empresa.keys()))
            self.frame_tabla.pack(padx=20, pady=10, fill="both", expand=True)

            # CORRECCIÓN CLAVE: Extraer los ratios dinámicamente usando el primer año YA ORDENADO de esta empresa
            año_referencia = años_ordenados[0]
            ratios_actuales = list(datos_empresa[año_referencia].keys())

            # 3- Mostramos el encabezado de la tabla: título/ratio/años
            lbl_head_ratio_date = ctk.CTkLabel(self.frame_tabla, text="Métrica/Ratio", font=ctk.CTkFont(weight="bold"), anchor="w")
            lbl_head_ratio_date.grid(row=0, column=0, padx=0, pady=5, sticky="w")

            for col_idx, año in enumerate(años_ordenados, start=1):
                lbl_hdr_año = ctk.CTkLabel(self.frame_tabla, text=str(año), font=ctk.CTkFont(weight="bold"))
                lbl_hdr_año.grid(row=0, column=col_idx, padx=15, pady=5)
            
            # 4- CUERPO DE LA TABLA:
            """ 
                Renderizamos usando 'valores_a_mostrar' en vez de 'ratios_actuales',
                si quieres mostrar TODOS los tags disponibles puedes utilizar 'valores_a_mostrar'
                el cual es una lista de diccionario con todo los datos del JSON para el primera año
                de la empresa.
            """
            for row_idx, ratio in enumerate(ratios_actuales, start=1):
                lbl_nombre_ratio = ctk.CTkLabel(self.frame_tabla, text=ratio, anchor="w")
                lbl_nombre_ratio.grid(row=row_idx, column=0, padx=10, pady=2, sticky="w")

                for col_idx, año in enumerate(años_ordenados, start=1):
                    # Buscamos de forma segura en el año correspondiente
                    valor = datos_empresa[año].get(ratio, 0)

                    # Formateo de datos corregido para decimales y millones
                    if abs(valor) <= 4.0 and valor != 0:
                        valor_texto = f"{valor:.1%}"
                    elif abs(valor) < 300:
                        valor_texto = f"{valor:.1f}%" if valor != 0 else "0.0%"
                    else:
                        valor_texto = f"{valor/1_000_000:.1f}M" if valor != 0 else "0.0M"
                    
                    lbl_valor = ctk.CTkLabel(self.frame_tabla, text=valor_texto)
                    lbl_valor.grid(row=row_idx, column=col_idx, padx=15, pady=2)

            self.lbl_estado.configure(text=f"🗸, Tabla histórica de {empresa_activa} cargada con éxito", text_color="#2ca02c")

        except Exception as e:
            self.lbl_estado.configure(text=f"Error al cargar la tabla: {str(e)}", text_color="#d32f2f")

    def abrir_pestaña_modal(self):

        #1-Configuración basica de la pestaña modal:
        pestaña_modal = ctk.CTkToplevel(self)
        pestaña_modal.title("Configuraciones:")
        pestaña_modal.geometry("400x200")
        pestaña_modal.configure(fb_color=COLORES["color_fondo_app"])

        #2-La volvemos Modal
        pestaña_modal.transient(self)
        pestaña_modal.grab_set()

        #3-Contenido de la pestaña modal:
        titulo_modal = ctk.CTkLabel(pestaña_modal, text="Exportar excel:", font=ctk.CTkFont(size=18), text_color=COLORES["texto_principal"])
        titulo_modal.pack(pady=(15,5))

        entrada_nombre = ctk.CTkEntry(pestaña_modal, placeholder_text="nombre de archivo")
        entrada_nombre.insert(0, "excel_BD")
        entrada_nombre.pack(pady=5)

        #4- Guardar y salir boton:
        boton_modal = ctk.CTkButton(
            pestaña_modal, text="Guardar excel", width=120,
            command=lambda: self.ejecutar_exportacion(entrada_nombre.get(), pestaña_modal),
            text_color=COLORES["texto_principal"],
            font=ctk.CTkFont(size=16),
            fg_color = COLORES["empresa_1"],
            hover_color= COLORES["empresa_1_hover"]
            )
        boton_modal.pack(pady=10)

        return None

    def ejecutar_exportacion(self, nombre, pestaña_m):
        # Aquí reutilizamos la lógica exacta de tu archivo exporter.py
        try:
            #--- Área en mantenimiento: 
            primer_año = list(self.base_datos['Casa Grande'].keys())[0]
            """ratios_a_exportar =  list(self.base_datos['Casa Grande'][primer_año].keys())"""

            #--- Fin del área en mantenimiento:
            ruta_excel = f"{nombre}.xlsx"
            with pd.ExcelWriter(ruta_excel, engine='openpyxl') as writer:
                for empresa, datos_historicos in self.base_datos.items():
                    #print(f"empresa |{empresa}| dato historico|{datos_historicos}|")
                    años_ordenados = sorted(list(datos_historicos.keys()))
                    matriz_excel = {}
                    print(matriz_excel)
                    for ratio in valores_a_mostrar: #Cambiar aquí la varaible
                        matriz_excel[ratio] = [datos_historicos[año].get(ratio, 0) for año in años_ordenados]
                    df = pd.DataFrame(matriz_excel, index=años_ordenados).T
                    df.to_excel(writer, sheet_name=empresa, index_label="Ratio / Métrica")
            
            # Cambiamos el texto del estado para avisarle al usuario en tiempo real
            self.lbl_estado.configure(text=f"📊 ¡Excel {ruta_excel} geneardo correctamente!", text_color=COLORES["exito"])
            pestaña_m.destroy()
        except Exception as e:
            self.lbl_estado.configure(text=f"❌ Error al exportar: {str(e)}", text_color="#d32f2f")


# 3. Lanzador del bucle principal de la ventana
if __name__ == "__main__":
    app = AppFinanzas()
    app.mainloop()