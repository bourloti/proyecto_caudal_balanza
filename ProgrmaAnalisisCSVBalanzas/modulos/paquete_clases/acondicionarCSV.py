import pandas as pd

"""
Esta clase se encarga de acondicionar (limpiar y preparar) el archivo CSV,
realizando tareas como la conversión de tipos de datos y filtrado de valores.
Devuelve un DataFrame con los valores leidos del CSV
"""

class AcondicionadorCSV:
    
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