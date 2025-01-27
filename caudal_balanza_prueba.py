import snap7
from snap7.util import get_real, get_bool, get_byte
from time import sleep
from datetime import datetime
import pandas as pd
import os

# Completa los archvos csv pasandole un diccionario con las keys que son nombres de balanzas y los values son dataframe

class ArchivoCSV:
    def __init__(self, nombre_archivo = str):
        self.nombre_archivo = nombre_archivo
    
    # Guardar el DataFrame en el archivo correspondiente
    def crear_csv(self, df):

        # Verifica si el archivo existe
        if not os.path.exists(self.nombre_archivo):
            # Si el archivo no existe, crea uno nuevo con los datos
            pd.DataFrame({'fecha': [], 'caudal': []}).to_csv(self.nombre_archivo, index=False)
            print(f"El archivo {self.nombre_archivo} fue creado y los datos fueron agregados.")
        else:
            # Si el archivo ya existe, agrega los nuevos datos al final
            df.to_csv(self.nombre_archivo, mode='a', header=False, index=False)
            print(f"Guardado en {self.nombre_archivo}")
        
class CaudalBalanzas:
    def __init__(self):
        self.acumulado_anterior = 0

    def obtiene_caudal(self, acumulado):

        # Calcula los kilogramas entre un llamado y el otro
        kilos = acumulado - self.acumulado_anterior
        self.acumulado_anterior = acumulado  # Actualizar el valor de acumulado_anterior

        # Crea un DataFrame con la fecha y los kilos
        df = pd.DataFrame({'fecha': [datetime.now()], 'caudal': [kilos]})

        return df

# Intentar conectar en un bucle hasta tener éxito
def connect_to_plc(ip, rack, slot):
    while True:
        try:
            plc = snap7.client.Client()
            print("Intentando conectar al PLC...")
            plc.connect(ip, rack, slot)

            # Verificar si la conexión es exitosa
            if plc.get_connected():
                print("Conexión establecida con éxito.")
                return plc

        except Exception as e:
            print(f"Error al intentar conectar: {e}")
    
        # Esperar antes de volver a intentar
        print("Reintentando en 5 segundos...")
        sleep(5)

def main():
    try:
        plc_molino = connect_to_plc("10.100.100.10", 0, 3)
        #Diccionario con balanzas que se estan leyendo

        caudal_ingreso_matreia_prima = CaudalBalanzas()
        caudal_tempering = CaudalBalanzas()
        
        csv_balanza_ingreso_materia_prima = ArchivoCSV('caudal_balanza_ingreso_materia_prima.csv')
        csv_balanza_tempering = ArchivoCSV('caudal_balanza_tempering.csv')

        while True:
            try:
                # Verificar si el PLC sigue conectado
                if not plc_molino.get_connected():
                    print("Se perdió la conexión con el PLC. Reintentando...")
                    plc_molino = connect_to_plc("10.100.100.10", 0, 3)

                #Leo los datos del PLC de las balanzas
                '''
                    Con db_read obtengo el numero real, le paso 3 parametros: numeroDB,direccionDeArranque,cuantosByteLee
                '''
                kilos_acumulados_balanza_ingreso_materia_prima = round(get_real(plc_molino.db_read(150,8,4),0),1)
                # kilos_acumulado_balanza_silo_101 = round(get_real(plc_molino.db_read(157,8,4),0),1)
                kilos_acumulado_balanza_tempering = round(get_real(plc_molino.db_read(164,8,4),0),1)
                # kilos_acumulado_balanza_tempering_dudoso = round(get_real(plc_molino.db_read(158,8,4),0),1)

#-------------------------------------------------------------------------------------------------------------------------------
                # Para obtener el caudal por minuto de las balanzas, este if se debe ejecutar cada 1 min
                if datetime.now().second == 00:
                    caudal_ingreso_maetria_prima = caudal_ingreso_matreia_prima.obtiene_caudal(kilos_acumulados_balanza_ingreso_materia_prima)
                    csv_balanza_ingreso_materia_prima.crear_csv(caudal_ingreso_maetria_prima)
                    
                    csv_balanza_tempering.crear_csv(caudal_tempering.obtiene_caudal(kilos_acumulado_balanza_tempering))

                    sleep(1.5)
#-------------------------------------------------------------------------------------------------------------------------------
                sleep(0.1)

            except Exception as e:
                print(f"Error durante la operación: {e}")
                print("Intentando reconectar...")
                plc_molino = connect_to_plc("10.100.100.10", 0, 3)

    except KeyboardInterrupt:
        # print("Comunicación Snap7 finalizada.")
        plc_molino.disconnect()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()