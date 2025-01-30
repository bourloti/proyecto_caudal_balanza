import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
from time import sleep

class Analisis_CSV:
    
    def __init__(self, directorio_archivo_csv):
        self.directorio_archivo_csv = directorio_archivo_csv
    
    def acondicionar_archivo_CSV(self):
        # Leer el archivo CSV
        df = pd.read_csv(self.directorio_archivo_csv, sep=',')  # Ajusta el nombre del archivo y el separador si es necesario

        nombre_columna_tiempo = 'fecha'
        nombre_columna_caudal = 'caudal'

        # Convertir la columna 'Fecha y Hora' a formato datetime
        df[nombre_columna_tiempo] = pd.to_datetime(df[nombre_columna_tiempo], format='%Y-%m-%d %H:%M:%S.%f')
        
        # Redondear las fechas a segundos (eliminando microsegundos)
        df[nombre_columna_tiempo] = df[nombre_columna_tiempo].dt.floor("s")
        
        # Convierte los datos de la columna caudal a valores numericos
        df[nombre_columna_caudal] = pd.to_numeric(df[nombre_columna_caudal])

        # Filtra los datos para que solo queden dentro del rango esperado
        df = df[df[nombre_columna_caudal].between(0,500)]

        # Crea un DataFrame con los valores deseados
        df = pd.DataFrame({'fecha': df[nombre_columna_tiempo], 'caudal': df[nombre_columna_caudal]})
        
        return df

    def calcular_toneladas_dia(self, df_dia, fecha):
        self.df = df_dia
        self.fecha = fecha
        
        lista_fecha_hora = []
        lista_prom_toneladas = []

       # Comparar con una cadena de texto (asegurándote de que ambas sean cadenas)
        if not (self.df.loc[self.df['fecha'].dt.strftime('%Y-%m-%d') == f"{self.fecha}"]).empty:
        
            # Iterar de 12 a 11 pm (24 horas)
            for i in range(24):

                # Verifica que existan las filas donde la hora es en punto (ej: 02:00:00, 09:00:00, etc), para poder hacer correcatmente el calcula de toneladas por hora
                fila_1 = self.df.loc[self.df["fecha"] == f"{self.fecha} {i:02d}:00:00"]
                
                if i < 23:
                    fila_2 = self.df.loc[self.df["fecha"] == f"{self.fecha} {(i+1):02d}:00:00"]

                # Verificar si se encontró la fecha
                if not fila_1.empty and not fila_2.empty:

                    if i < 23:
                        # Crear las horas de inicio y fin en formato 24 horas
                        hora_inicio = f'{self.fecha} {i:02d}:00:00'
                        hora_fin = f'{self.fecha} {(i+1)%24:02d}:00:00'
                    else:
                        # Crear las horas de inicio y fin en formato 24 horas
                        hora_inicio = f'{self.fecha} {i:02d}:00:00'
                        hora_fin = f'{self.fecha} 23:59:00'

                    # Filtrar el DataFrame para las filas que están entre hora_inicio y hora_fin
                    df_filtrado = self.df[self.df['fecha'].between(hora_inicio, hora_fin)]

                    # Calcular el promedio de las columnas numéricas en ese rango horario
                    promedio_por_hora = (df_filtrado['caudal'].mean() * 60) / 1000 # Esto devuelve una Serie con el promedio de cada columna numérica

                    lista_fecha_hora.append(pd.to_datetime(f'{self.fecha} {i:02d}:00:00', format='%Y-%m-%d %H:%M:%S'))
                    lista_prom_toneladas.append(promedio_por_hora)

                    #print(promedio_por_hora)

                    df_final = pd.DataFrame({'fecha': lista_fecha_hora, 'totalizador': lista_prom_toneladas})
        else: 
            return print('Fecha no encontrada')
        return df_final
    
    def graficar(self, df):
        self.df = df
        # Crear el gráfico de barras
        plt.figure(figsize=(10, 6))

        # Dibujar las barras en el gráfico, donde el eje X es la fecha de inicio de cada intervalo
        plt.bar(self.df['fecha'], self.df['totalizador'], width=0.02)  # width ajusta el tamaño de las barras

        # Configurar el formato de fecha en el eje X
        plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

        # Ajustar el formato de las etiquetas en el eje X para que no se solapen
        plt.xticks(rotation=45, ha='right')

        # Añadir etiquetas y título
        plt.xlabel(f'Fecha: {self.fecha}')
        plt.ylabel('Total por hora')
        toneladas = round(self.df['totalizador'].sum(), 2)
        plt.title(f'Toneladas totales: {toneladas} Ton')

        # Mostrar el gráfico
        plt.tight_layout()  # Ajusta los márgenes
        plt.show()

def main():
    balanza_final_mb = Analisis_CSV('D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_final_molino_blanco.csv')
    balanza_ingreso_mb = Analisis_CSV('D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_ingreso_molino_blanco.csv')
    balanza_integral_mb = Analisis_CSV('D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_integral_molino_blanco.csv')
    balanza_final_mp = Analisis_CSV('D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_final_molino_parboil.csv')
    balanza_ingreso_mp = Analisis_CSV('D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_ingreso_molino_parboil.csv')
    balanza_integral_mp = Analisis_CSV('D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_integral_molino_parboil.csv')
    balanza_silo_101 = Analisis_CSV('D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_silo_101.csv')
    balanza_tempering = Analisis_CSV('D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_tempering.csv')
    balanza_materia_prima = Analisis_CSV('D:\Mantenimiento\Bourlot Ignacio\GitHub repositorios\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_ingreso_materia_prima.csv')
        
    # balanza_final_mb.graficar(df_dia_balanza_final_mb)
    # balanza_ingreso_mb.graficar(df_dia_balanza_ingreso_mb)
   
    while True:
        
        if str(datetime.now().strftime("%H:%M:%S")) == '00:05:00':
            fecha_formateada = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            
            df_acondicionado_balanza_final_mb = balanza_final_mb.acondicionar_archivo_CSV()
            df_acondicionado_balanza_ingreso_mb = balanza_ingreso_mb.acondicionar_archivo_CSV()
            df_acondicionado_balanza_integral_mb = balanza_integral_mb.acondicionar_archivo_CSV()
            df_acondicionado_balanza_final_mp = balanza_final_mp.acondicionar_archivo_CSV()
            df_acondicionado_balanza_ingreso_mp = balanza_ingreso_mp.acondicionar_archivo_CSV()
            df_acondicionado_balanza_integral_mp = balanza_integral_mp.acondicionar_archivo_CSV()
            df_acondicionado_balanza_silo_101 = balanza_silo_101.acondicionar_archivo_CSV()
            df_acondicionado_balanza_tempering = balanza_tempering.acondicionar_archivo_CSV()
            df_acondicionado_balanza_materia_prima = balanza_materia_prima.acondicionar_archivo_CSV()
        
            df_dia_balanza_final_mb = balanza_final_mb.calcular_toneladas_dia(df_acondicionado_balanza_final_mb, fecha_formateada)
            df_dia_balanza_ingreso_mb = balanza_ingreso_mb.calcular_toneladas_dia(df_acondicionado_balanza_ingreso_mb, fecha_formateada)
            df_dia_balanza_integral_mbb = balanza_integral_mb.calcular_toneladas_dia(df_acondicionado_balanza_integral_mb, fecha_formateada)
            df_dia_balanza_final_mp = balanza_final_mp.calcular_toneladas_dia(df_acondicionado_balanza_final_mp, fecha_formateada)
            df_dia_balanza_ingreso_mp = balanza_ingreso_mp.calcular_toneladas_dia(df_acondicionado_balanza_ingreso_mp, fecha_formateada)
            df_dia_balanza_integral_mp = balanza_integral_mp.calcular_toneladas_dia(df_acondicionado_balanza_integral_mp, fecha_formateada)
            df_dia_balanza_silo_101 = balanza_silo_101.calcular_toneladas_dia(df_acondicionado_balanza_silo_101, fecha_formateada)
            df_dia_balanza_tempering = balanza_tempering.calcular_toneladas_dia(df_acondicionado_balanza_tempering, fecha_formateada)
            df_dia_balanza_materia_prima = balanza_materia_prima.calcular_toneladas_dia(df_acondicionado_balanza_materia_prima, fecha_formateada)
            
            # balanza_final_mb.graficar(df_dia_balanza_final_mb)
            # balanza_ingreso_mb.graficar(df_dia_balanza_ingreso_mb)
            
            sleep(1.5)
    
if __name__ == "__main__":
    main()
 