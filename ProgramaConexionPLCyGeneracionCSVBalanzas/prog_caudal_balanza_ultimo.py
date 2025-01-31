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
        #Diccionario con balanzas que se estan leyendo
        
        # Diccionario con las rutas de los archivos CSV
        archivos = {
            'balanza_final_mb': 'D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_final_molino_blanco.csv',
            'balanza_ingreso_mb': 'D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_ingreso_molino_blanco.csv',
            'balanza_integral_mb': 'D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_integral_molino_blanco.csv',
            'balanza_final_mp': 'D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_final_molino_parboil.csv',
            'balanza_ingreso_mp': 'D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_ingreso_molino_parboil.csv',
            'balanza_integral_mp': 'D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_integral_molino_parboil.csv',
            'balanza_silo_101': 'D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_silo_101.csv',
            'balanza_tempering': 'D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_tempering.csv',
            'balanza_materia_prima': 'D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_ingreso_materia_prima.csv'
        }
                
        objetos_caudal_balanzas = {nombre_balanza: CaudalBalanzas() for nombre_balanza in archivos.keys()}

        objetos_genera_CSV_balanzas = {nombre_balanza: GenerarArchivoCSV(os.path.split(directorio)) for nombre_balanza, directorio in archivos.items()}
        
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
                # Para obtener el caudal por minuto de las balanzas, este if se debe ejecutar cada 1 min
                if datetime.now().second == 00:
                    
                    for nombre_balanzas, balanzas_objeto in objetos_caudal_balanzas.items():
                        caudal_balanzas = {f'{nombre_balanzas}': balanzas_objeto.obtiene_caudal(datos_leidos_plc[nombre_balanzas])}
                        
                    for balanzas_objetos in objetos_genera_CSV_balanzas.values():
                        balanzas_objetos.crearCSV(caudal_balanzas[nombre_balanzas])
                   
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