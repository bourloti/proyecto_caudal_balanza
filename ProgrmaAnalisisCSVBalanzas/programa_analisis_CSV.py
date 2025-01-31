import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
from time import sleep
import os

from modulos.paquete_clases.acondicionarCSV import AcondicionadorCSV
from modulos.paquete_clases.archivoCSV import GenerarArchivoCSV
from modulos.paquete_clases.calcularToneladasDia import CalculadorToneladasDia
from modulos.paquete_clases.graficador import Graficador

from modulos.paquetes_funciones.generar_df_totalizador_balanzas import generar_df_totalizadores_balanzas

def main():
    """
    Función principal que ejecuta el procesamiento de datos y la generación de gráficos
    de toneladas por hora para cada uno de los archivos CSV.
    """
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
                    df_dia_graficos.append(calculador.calcular_toneladas_dia('2025-01-29'))

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
                totalizadores_por_hora = GenerarArchivoCSV('totalizadores_todas_balanzas.csv', 'D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza')
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
