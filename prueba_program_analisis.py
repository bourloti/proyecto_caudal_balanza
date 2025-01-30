import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
from time import sleep
import os

class AcondicionadorCSV:
    """
    Esta clase se encarga de acondicionar (limpiar y preparar) el archivo CSV,
    realizando tareas como la conversión de tipos de datos y filtrado de valores.
    Devuelve un DataFrame con los valores leidos del CSV
    """
    def __init__(self, directorio_archivo_csv):
        self.directorio_archivo_csv = directorio_archivo_csv

    def acondicionar_archivo_CSV(self):
        try:
            # Leer el archivo CSV con el separador por comas
            df = pd.read_csv(self.directorio_archivo_csv, sep=',')  
        except FileNotFoundError:
            print(f"Error: El archivo {self.directorio_archivo_csv} no se encuentra.")
            return None
        except pd.errors.ParserError:
            print(f"Error: Hubo un problema al leer el archivo CSV {self.directorio_archivo_csv}.")
            return None
        except Exception as e:
            print(f"Error inesperado al leer el archivo CSV: {e}")
            return None

        try:
            # Realizar el acondicionamiento de los datos
            nombre_columna_tiempo = 'fecha'
            nombre_columna_caudal = 'caudal'

            # Convertir la columna 'fecha' a formato datetime
            df[nombre_columna_tiempo] = pd.to_datetime(df[nombre_columna_tiempo], format='%Y-%m-%d %H:%M:%S.%f')
            df[nombre_columna_tiempo] = df[nombre_columna_tiempo].dt.floor("s")
            
            # Convertir los valores de la columna 'caudal' a valores numéricos
            df[nombre_columna_caudal] = pd.to_numeric(df[nombre_columna_caudal])

            # Filtrar solo los registros cuyo caudal esté entre 0 y 500
            df = df[df[nombre_columna_caudal].between(0,500)]

        except KeyError as e:
            print(f"Error: Columna no encontrada en el archivo CSV: {e}")
            return None
        except ValueError as e:
            print(f"Error al convertir datos: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado durante el acondicionamiento de datos: {e}")
            return None

        return df

class CalculadorToneladasDia:
    """
    Esta clase calcula el total de toneladas para cada hora en un día específico,
    a partir de los datos acondicionados del archivo CSV.
    """
    def __init__(self, df):
        self.df = df

    def calcular_toneladas_dia(self, fecha):
        try:
            # Inicializa listas para almacenar las fechas y toneladas promedio por hora
            lista_fecha_hora = []
            lista_prom_toneladas = []

            if not (self.df.loc[self.df['fecha'].dt.strftime('%Y-%m-%d') == f"{fecha}"]).empty:
                # Iterar sobre las 24 horas del día
                for i in range(24):
                    # Buscar los datos de la hora exacta
                    fila_1 = self.df.loc[self.df["fecha"] == f"{fecha} {i:02d}:00:00"]
                    if i < 23:
                        fila_2 = self.df.loc[self.df["fecha"] == f"{fecha} {(i+1):02d}:00:00"]

                    # Si se encuentran datos para la hora y la siguiente hora
                    if not fila_1.empty and not fila_2.empty:
                        # Define las horas de inicio y fin para el rango de la hora
                        hora_inicio = f'{fecha} {i:02d}:00:00'
                        hora_fin = f'{fecha} {(i+1)%24:02d}:00:00' if i < 23 else f'{fecha} 23:59:00'
                        
                        # Filtra el DataFrame para obtener los registros dentro del rango de horas
                        df_filtrado = self.df[self.df['fecha'].between(hora_inicio, hora_fin)]
                        
                        # Calcular el promedio de caudal por hora y convertirlo a toneladas
                        promedio_por_hora = (df_filtrado['caudal'].mean() * 60) / 1000  # Toneladas por hora

                        # Añadir la hora y el promedio calculado a las listas
                        lista_fecha_hora.append(pd.to_datetime(f'{fecha} {i:02d}:00:00', format='%Y-%m-%d %H:%M:%S'))
                        lista_prom_toneladas.append(promedio_por_hora)

                # Crear un DataFrame con las fechas y toneladas calculadas
                df_final = pd.DataFrame({'fecha': lista_fecha_hora, 'totalizador': lista_prom_toneladas})
                return df_final
            else:
                print(f"Fecha {fecha} no encontrada en los datos.")
                return None
        except Exception as e:
            print(f"Error inesperado al calcular las toneladas: {e}")
            return None

class Graficador:
    """
    Esta clase se encarga de generar los gráficos de barras con los datos de toneladas.
    """
    def __init__(self, df, titulo):
        self.df = df
        self.titulo = titulo

    def graficar(self, fecha):
        try:
            # Verifica que el DataFrame no esté vacío
            if self.df is None or self.df.empty:
                print("No hay datos para graficar.")
                return
            
            # Crear el gráfico de barras
            plt.figure(figsize=(10, 6))
            plt.bar(self.df['fecha'], self.df['totalizador'], width=0.02)
            
            # Formato de fecha en el eje X (mostrando solo la hora y minutos)
            plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))
            
            # Ajustar la posición de las etiquetas en el eje X para evitar solapamientos
            plt.xticks(rotation=45, ha='right')
            
            # Etiquetas y título del gráfico
            plt.xlabel(f'Fecha: {fecha}')
            plt.ylabel('Total por hora')
            
            # Calcular el total de toneladas en el día y mostrarlo en el título
            toneladas = round(self.df['totalizador'].sum(), 2)
            plt.title(f'{self.titulo} - Toneladas totales: {toneladas} Ton')

            # Mostrar el gráfico ajustando el layout para que se vea bien
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error al generar el gráfico: {e}")

class GeneraArchivoCSV:
    def __init__(self, nombre_archivo, directorio):
        self.nombre_archivo = nombre_archivo
        self.directorio = directorio
    
    # Guardar el DataFrame en el archivo correspondiente
    def crear_csv(self, df):

        # Verifica si el archivo existe
        if not os.path.exists(f'{self.directorio}/{self.nombre_archivo}'):
            # Si el archivo no existe, crea uno nuevo con los datos
            df.to_csv(f'{self.directorio}/{self.nombre_archivo}', index=False)
            print(f"El archivo {self.nombre_archivo} fue creado y los datos fueron agregados.")
        else:
            # Si el archivo ya existe, agrega los nuevos datos al final
            df.to_csv(f'{self.directorio}/{self.nombre_archivo}', mode='a', header=False, index=False)
            print(f"Guardado en {self.nombre_archivo}")

def generar_df_totalizadores_balanzas(df_dia, titulo):
    '''
    Genera un dataframe con los valores por hora de todas las balanzas, y lo convierte a CSV
    df_dia: lista donde cada elementeo es un dataframe con columna1 (fecha) y columna 2 (totalizador)
    titulo: lista con los nombres de cada una de las balanzas
    '''
    
    # Inicializa el diccionario vacío
    diccionario_balanzas = {}

    # Itera sobre las filas de df_dia_graficos
    for i in range(len(df_dia)):
        # Genera un nombre para la balanza (puedes personalizar esto si tienes nombres específicos)
        nombre_balanza = f'{titulo[i]}'  # Nombres como 'balanza_1', 'balanza_2', etc.
        
        # Crea las listas de toneladas y fechas
        lista_toneladas_totales = list(df_dia[i]['totalizador'])
        lista_fechas = list(df_dia[i]['fecha'])

        # Agregar las fechas y toneladas al diccionario
        diccionario_balanzas[f'fecha_{nombre_balanza}'] = lista_fechas
        diccionario_balanzas[f'toneladas_{nombre_balanza}'] = lista_toneladas_totales
        
        df = pd.DataFrame(diccionario_balanzas)
        
    return df

def main():
    """
    Función principal que ejecuta el procesamiento de datos y la generación de gráficos
    de toneladas por hora para cada uno de los archivos CSV.
    """
    # Diccionario con las rutas de los archivos CSV
    archivos = {
        'balanza_final_mb': 'C:\progrmasPython\proyecto_caudal_balanza\proyecto_caudal_balanza\caudal_balanza_final_molino_blanco.csv',
        'balanza_ingreso_mb': 'C:\progrmasPython\proyecto_caudal_balanza\proyecto_caudal_balanza\caudal_balanza_ingreso_molino_blanco.csv',
        'balanza_integral_mb': 'C:\progrmasPython\proyecto_caudal_balanza\proyecto_caudal_balanza\caudal_balanza_integral_molino_blanco.csv',
        'balanza_final_mp': 'C:\progrmasPython\proyecto_caudal_balanza\proyecto_caudal_balanza\caudal_balanza_final_molino_parboil.csv',
        'balanza_ingreso_mp': 'C:\progrmasPython\proyecto_caudal_balanza\proyecto_caudal_balanza\caudal_balanza_ingreso_molino_parboil.csv',
        'balanza_integral_mp': 'C:\progrmasPython\proyecto_caudal_balanza\proyecto_caudal_balanza\caudal_balanza_integral_molino_parboil.csv',
        'balanza_silo_101': 'C:\progrmasPython\proyecto_caudal_balanza\proyecto_caudal_balanza\caudal_balanza_silo_101.csv',
        'balanza_tempering': 'C:\progrmasPython\proyecto_caudal_balanza\proyecto_caudal_balanza\caudal_balanza_tempering.csv',
        'balanza_materia_prima': 'C:\progrmasPython\proyecto_caudal_balanza\proyecto_caudal_balanza\caudal_balanza_ingreso_materia_prima.csv'
    }

    # Crear una instancia para cada archivo CSV usando AcondicionadorCSV, el keys es el nombre de la balanza y el value es el objeto creado
    objetos_balanzas = {nombre: AcondicionadorCSV(ruta) for nombre, ruta in archivos.items()}
    
    titulos_graficos = [titulo for titulo in archivos.keys()]
    

    while True:
        try:
            df_dia_graficos = []
            # Ejecutar el proceso a las 00:05:00
            if input('Enter') == '1':
            #if str(datetime.now().strftime("%H:%M:%S")) == '03:23:00':
                # Obtener la fecha de ayer para usarla en la búsqueda de datos
                fecha_formateada = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

                # Acondicionar los datos de cada archivo CSV, recorro el diccionario creado con los objetos, y la variable balanza va tomando los objetos en cada iteracion
                for balanza in objetos_balanzas.values():
                    df_acondicionado = balanza.acondicionar_archivo_CSV()

                    if df_acondicionado is None:
                        df_dia_graficos.append(0)
                        continue

                    # Crear objeto de calculador para calcular las toneladas por día, crea un DataFrame con fecha y caudal por hora. Guarda el df en una lista, para luego poder graficarlos
                    calculador = CalculadorToneladasDia(df_acondicionado)
                    df_dia_graficos.append(calculador.calcular_toneladas_dia(fecha_formateada))

                    # if df_dia_graficos is None:
                    #     continue

                #-------------------------------------------------------------------------------------------------------
                # Si los datos fueron calculados correctamente, graficar los resultados
                # for i in range(len(df_dia_graficos)):
                #     graficador = Graficador(df_dia_graficos[i], titulos_graficos[i].upper())
                #     graficador.graficar(fecha_formateada)
                #-------------------------------------------------------------------------------------------------------

                #-------------------------------------------------------------------------------------------------------
                # Crea un archivo CSV con los datos de fecha y totalizador balanza por hora
                df_totalizadores_balanzas = generar_df_totalizadores_balanzas(df_dia_graficos, titulos_graficos)
                totalizadores_por_hora = GeneraArchivoCSV('totalizadores_todas_balanzas.csv', 'C:\progrmasPython\proyecto_caudal_balanza\proyecto_caudal_balanza')
                totalizadores_por_hora.crear_csv(df_totalizadores_balanzas) 

                df = pd.read_csv("totalizadores_todas_balanzas.csv")
                # Eliminar filas duplicadas (mantiene la primera ocurrencia por defecto)
                df_sin_duplicados = df.drop_duplicates()
                # Guardar el nuevo CSV sin duplicados
                df_sin_duplicados.to_csv("totalizadores_todas_balanzas.csv", index=False)
                #-------------------------------------------------------------------------------------------------------

        except KeyboardInterrupt:
            print("Proceso interrumpido por el usuario.")
            break
        except Exception as e:
            print(f"Error inesperado en el proceso principal: {e}")
            sleep(5)

if __name__ == "__main__":
    main()
