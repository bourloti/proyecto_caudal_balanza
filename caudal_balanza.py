import snap7
from snap7.util import get_real, get_bool, get_byte
from time import sleep
from datetime import datetime
import pandas as pd

# Variable global para mantener el valor de acumulado_anterior se utiliza en la funcion "obtiene_caudal_kilos_por_minuto"
acumulado_anterior = {}

# Funcion que le paso el acumulado del PLC y devuelve un dataframe con el dato de kg en 1 minuto
def obtiene_caudal_kilos_por_minuto(acumulado, id_balanza):

    # Usar la variable global para almacenar el acumulado anterior
    global acumulado_anterior

    # Si la balanza no tiene un acumulado anterior, lo inicializamos
    if id_balanza not in acumulado_anterior:
        acumulado_anterior[id_balanza] = acumulado
        
    kilos = acumulado - acumulado_anterior[id_balanza]
    acumulado_anterior[id_balanza] = acumulado  # Actualizar el valor de acumulado_anterior

    df = pd.DataFrame({'fecha': [datetime.now()], 'caudal': [kilos]})
    return df 

# Completa los archvos csv pasandole un diccionario con las keys que son nombres de balanzas y los values son dataframe
def crear_archivos_csv(diccionario):

    # Iterar sobre el diccionario para guardar cada DataFrame en un archivo CSV
    for key, df in diccionario.items():
        # Crear el nombre del archivo usando la clave
        nombre_archivo = f"caudal_{key}.csv"
        
        # Guardar el DataFrame en el archivo correspondiente
        df.to_csv(nombre_archivo, mode='a', header=False, index=False)
        print(f"Guardado en {nombre_archivo}")

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
        id_balanza = {'balanza_1': 0,'balanza_2': 0,'balanza_3': 0,'balanza_4': 0}

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
                kilos_acumulado_balanza_silo_101 = round(get_real(plc_molino.db_read(157,8,4),0),1)
                kilos_acumulado_balanza_tempering = round(get_real(plc_molino.db_read(164,8,4),0),1)
                kilos_acumulado_balanza_tempering_dudoso = round(get_real(plc_molino.db_read(158,8,4),0),1)

#-------------------------------------------------------------------------------------------------------------------------------
                #Cada 1 minuto ejecuta lo que hay dentro del if
                if datetime.now().second == 00:
                    id_balanza['balanza_1'] = obtiene_caudal_kilos_por_minuto(kilos_acumulados_balanza_ingreso_materia_prima, 'balanza_1')
                    id_balanza['balanza_2'] = obtiene_caudal_kilos_por_minuto(kilos_acumulado_balanza_tempering, 'balanza_2')
                    id_balanza['balanza_3'] = obtiene_caudal_kilos_por_minuto(kilos_acumulado_balanza_silo_101, 'balanza_3')
                    id_balanza['balanza_4'] = obtiene_caudal_kilos_por_minuto(kilos_acumulado_balanza_tempering_dudoso, 'balanza_4')
                    crear_archivos_csv(id_balanza)
                    sleep(1.5)
#-------------------------------------------------------------------------------------------------------------------------------
                sleep(0.1)

            except Exception as e:
                print(f"Error durante la operación: {e}")
                print("Intentando reconectar...")
                #plc_molino = connect_to_plc("10.100.100.10", 0, 3)

    except KeyboardInterrupt:
        print("Comunicación Snap7 finalizada.")
        plc_molino.disconnect()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()