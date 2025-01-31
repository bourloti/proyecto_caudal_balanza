import os

# Crea un archivo CSV, pasandole un nombre y en el metodo se le pasa un dataframe con los valores
class GenerarArchivoCSV:
    def __init__(self, nombre_archivo, directorio):
        self.nombre_archivo = nombre_archivo
        self.directorio = directorio
    
    # Guardar el DataFrame en el archivo correspondiente
    def crear_csv(self, df):

        # Verifica si el archivo existe
        if not os.path.exists(f'{self.directorio}/{self.nombre_archivo}'):
            # Si el archivo no existe, crea uno nuevo con los datos
            #pd.DataFrame({'fecha': [], 'caudal': []}).to_csv(f'{self.directorio}/{self.nombre_archivo}', index=False)
            df.to_csv(f'{self.directorio}/{self.nombre_archivo}', index=False)
            print(f"El archivo {self.nombre_archivo} fue creado y los datos fueron agregados.")
        else:
            # Si el archivo ya existe, agrega los nuevos datos al final
            df.to_csv(f'{self.directorio}/{self.nombre_archivo}', mode='a', header=False, index=False)
            print(f"Guardado en {self.nombre_archivo}")