import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
from time import sleep

def analisis(directorio_archivo_csv, dia_a_analizar):
    # Leer el archivo CSV
    df_1 = pd.read_csv(directorio_archivo_csv, sep=',')  # Ajusta el nombre del archivo y el separador si es necesario

    nombre_columna_tiempo = 'fecha'
    nombre_columna_caudal = 'caudal'

    df_1[nombre_columna_tiempo] = df_1[nombre_columna_tiempo].replace({'-': '/'}, regex=True)

    # Convertir la columna 'Fecha y Hora' a formato datetime
    df_1[nombre_columna_tiempo] = pd.to_datetime(df_1[nombre_columna_tiempo], format='%Y/%m/%d %H:%M:%S.%f')
    # Redondear las fechas a segundos (eliminando microsegundos)
    df_1["fecha"] = df_1["fecha"].dt.floor("s")

    df_1[nombre_columna_caudal] = pd.to_numeric(df_1[nombre_columna_caudal])

    # Filtrar los datos para que solo queden dentro del rango esperado (por ejemplo, entre 0 y 50)
    df = df_1[df_1[nombre_columna_caudal].between(0,500)]

    df_nuevo = pd.DataFrame({'fecha': df[nombre_columna_tiempo], 'caudal': df[nombre_columna_caudal]})

    lista_1 = []
    lista_2 = []
    toneladas_en_dia = 0

    # Iterar de 12 a 11 pm (24 horas)
    for i in range(24):

        # Definir la fecha a buscar (ajustando al mismo formato)
        if i < 23:
            fecha_buscar = pd.Timestamp(f"2025-01-29 {(i+1):02d}:00:00")

        # Buscar la fila donde la fecha sea igual a la que buscamos
        fila = df.loc[df["fecha"] == fecha_buscar]

        # Verificar si se encontró la fecha
        if not fila.empty:

            if i < 23:
                # Crear las horas de inicio y fin en formato 24 horas
                hora_inicio = f'{dia_a_analizar} {i:02d}:00:00'
                hora_fin = f'{dia_a_analizar} {(i+1)%24:02d}:00:00'
            else:
                # Crear las horas de inicio y fin en formato 24 horas
                hora_inicio = f'{dia_a_analizar} {i:02d}:00:00'
                hora_fin = f'{dia_a_analizar} 23:59:00'

            # Filtrar el DataFrame para las filas que están entre hora_inicio y hora_fin
            df_filtrado = df_nuevo[df_nuevo['fecha'].between(hora_inicio, hora_fin)]

            # Calcular el promedio de las columnas numéricas en ese rango horario
            promedio_por_hora = (df_filtrado['caudal'].mean() * 60) / 1000 # Esto devuelve una Serie con el promedio de cada columna numérica

            lista_1.append(pd.to_datetime(f'{dia_a_analizar} {i:02d}:00:00', format='%d/%m/%Y %H:%M:%S'))
            lista_2.append(promedio_por_hora)

            toneladas_en_dia = toneladas_en_dia + promedio_por_hora

            #print(promedio_por_hora)

            df_final = pd.DataFrame({'fecha': lista_1, 'totalizador': lista_2})

    return df_final, toneladas_en_dia

def graficar(df, toneladas_totales):
    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))

    # Dibujar las barras en el gráfico, donde el eje X es la fecha de inicio de cada intervalo
    plt.bar(df['fecha'], df['totalizador'], width=0.02)  # width ajusta el tamaño de las barras

    # Configurar el formato de fecha en el eje X
    plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

    # Ajustar el formato de las etiquetas en el eje X para que no se solapen
    plt.xticks(rotation=90, ha='right')

    # Añadir etiquetas y título
    plt.xlabel('Fecha: 17/12/2024')
    plt.ylabel('Total por hora')
    plt.title(f'Caudal entre Intervalos de Tiempo. Toneladas totales en el dia {toneladas_totales}')

    # Mostrar el gráfico
    plt.tight_layout()  # Ajusta los márgenes
    plt.show()

if __name__ == "__main__":
    df,ton = analisis('C:\Python Nacho\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_integral_molino_blanco.csv', '29/01/2025')
    graficar(df,ton)
    # while True:
    #     if str(datetime.now().strftime("%H:%M:%S")) == '05:13:30':
    #         fecha_formateada = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
    #         df,ton = analisis('C:\ProyectoIIOT\Repositorio GitHub\caudal_balanzas\proyecto_caudal_balanza\caudal_balanza_final_molino_blanco.csv', str(fecha_formateada))
    #         graficar(df,ton)
    #         sleep(1.5)