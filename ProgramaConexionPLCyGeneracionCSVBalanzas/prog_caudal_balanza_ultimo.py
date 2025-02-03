from snap7.util import get_real, get_bool, get_byte
from time import sleep
from datetime import datetime
import os

from modulos.paquetes_funciones.conexion_plc import connect_to_plc
from modulos.paquete_clases.archivoCSV import GenerarArchivoCSV
from modulos.paquete_clases.caudalBalanza import CaudalBalanzas

def main():
    try:
        plc_molino = connect_to_plc("10.100.100.10", 0, 3)
        
        # Diccionario con los nombre de las balanzas y las rutas con archivos CSV
        archivos = {
            'balanza_final_mb': 'C:\ProyectoIIOT\Repositorio GitHub\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_final_molino_blanco.csv',
            'balanza_ingreso_mb': 'C:\ProyectoIIOT\Repositorio GitHub\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_ingreso_molino_blanco.csv',
            'balanza_integral_mb': 'C:\ProyectoIIOT\Repositorio GitHub\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_integral_molino_blanco.csv',
            'balanza_final_mp': 'C:\ProyectoIIOT\Repositorio GitHub\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_final_molino_parboil.csv',
            'balanza_ingreso_mp': 'C:\ProyectoIIOT\Repositorio GitHub\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_ingreso_molino_parboil.csv',
            'balanza_integral_mp': 'C:\ProyectoIIOT\Repositorio GitHub\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_integral_molino_parboil.csv',
            'balanza_silo_101': 'C:\ProyectoIIOT\Repositorio GitHub\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_silo_101.csv',
            'balanza_tempering': 'C:\ProyectoIIOT\Repositorio GitHub\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_tempering.csv',
            'balanza_materia_prima': 'C:\ProyectoIIOT\Repositorio GitHub\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_ingreso_materia_prima.csv'
        }
        # Crea un diccionariob a partir del diccionario "archivo", donde el key es el nombre de la balanza y el value es un dataFrame con los objetos de la clase "CaudalBalanzas"
        objetos_caudal_balanzas = {nombre_balanza: CaudalBalanzas() for nombre_balanza in archivos.keys()}

        
        # Crea un diccionariob a partir del diccionario "archivo", donde el key es el nombre de la balanza y el value es un dataFrame con los objetos de la clase "GenerarArchivoCSV"
        # La funcion os.path.split(ruta), se le pasa la ruta de un archivo y devuelve una tupla con dos valores: uno el directorio del archivo y el otro el nombre, 
        objetos_genera_CSV_balanzas = {nombre_balanza: GenerarArchivoCSV(os.path.split(ruta)[1], os.path.split(ruta)[0]) for nombre_balanza, ruta in archivos.items()}
        
        while True:
            try:
                # Verificar si el PLC sigue conectado
                if not plc_molino.get_connected():
                    print("Se perdió la conexión con el PLC. Reintentando...")
                    plc_molino = connect_to_plc("10.100.100.10", 0, 3)

                '''
                    Leo los datos del PLC de las balanzas, y los guardo en un diccionario donde los nombres de las balanzas deben ser iguales a los generados arriba
                    Con db_read obtengo el numero real, le paso 3 parametros: numeroDB,direccionDeArranque,cuantosByteLee
                '''
              
                datos_leidos_plc = {
                    'balanza_final_mb': round(get_real(plc_molino.db_read(153,8,4),0),1),
                    'balanza_ingreso_mb': round(get_real(plc_molino.db_read(152,8,4),0),1),
                    'balanza_integral_mb': round(get_real(plc_molino.db_read(159,8,4),0),1),
                    'balanza_final_mp': (round(get_real(plc_molino.db_read(158,8,4),0),1)) / 10,
                    'balanza_ingreso_mp': round(get_real(plc_molino.db_read(163,8,4),0),1),
                    'balanza_integral_mp': round(get_real(plc_molino.db_read(161,8,4),0),1),
                    'balanza_silo_101': round(get_real(plc_molino.db_read(157,8,4),0),1),
                    'balanza_tempering': round(get_real(plc_molino.db_read(164,8,4),0),1),
                    'balanza_materia_prima': round(get_real(plc_molino.db_read(150,8,4),0),1)
                }
                
#-------------------------------------------------------------------------------------------------------------------------------
                # Para obtener los kilogramos por minuto de las balanzas, este if se debe ejecutar cada 1 min
                if datetime.now().second == 00:

                    #-------------------------------------------------------------------------
                    # Crear un diccionario vacío antes de empezar la iteración
                    diccionario_balanzas = {}
                    # Iterar sobre el diccionario "objetos_caudal_balanzas" para obtener un df con hora y caudal (kg/min)
                    for balanzas_nombre, balanzas_objeto in objetos_caudal_balanzas.items():
                        if balanzas_nombre in datos_leidos_plc.keys():
                            # Añadir el nombre_balanzas como clave y balanzas_objeto como valor al diccionario
                            diccionario_balanzas[balanzas_nombre] = balanzas_objeto.obtiene_caudal(datos_leidos_plc[balanzas_nombre])
                        else:
                            print(f'No se encontro la {balanzas_nombre}')
                    #-------------------------------------------------------------------------
                    # Iterar sobre el diccionario "objetos_genera_CSV_balanzas" cargar los valores obtenidos en un CSV  
                    for balanzas_nombre, balanzas_objetos in objetos_genera_CSV_balanzas.items():
                        if balanzas_nombre in diccionario_balanzas.keys():
                            balanzas_objetos.crear_csv(diccionario_balanzas[balanzas_nombre])
                    #-------------------------------------------------------------------------
                    
                    sleep(1.5)
#-------------------------------------------------------------------------------------------------------------------------------
                sleep(0.1)

            except Exception as e:
                print(f"Error durante la operación: {e}")
                print("Intentando reconectar...")
                plc_molino = connect_to_plc("10.100.100.10", 0, 3)

    except KeyboardInterrupt:
        print("Comunicación Snap7 finalizada.")
        plc_molino.disconnect()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()