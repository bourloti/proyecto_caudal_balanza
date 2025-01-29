import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Leer el archivo CSV
df_1 = pd.read_csv('caudal_balanza_ingreso_materia_prima.csv', sep=',')  # Ajusta el nombre del archivo y el separador si es necesario

nombre_columna_tiempo = 'fecha'
nombre_columna_caudal = 'caudal'

df_1[nombre_columna_tiempo] = df_1[nombre_columna_tiempo].replace({'-': '/'}, regex=True)

# Convertir la columna 'Fecha y Hora' a formato datetime
df_1[nombre_columna_tiempo] = pd.to_datetime(df_1[nombre_columna_tiempo], format='%Y/%m/%d %H:%M:%S.%f')

df_1[nombre_columna_caudal] = pd.to_numeric(df_1[nombre_columna_caudal])

# Filtrar los datos para que solo queden dentro del rango esperado (por ejemplo, entre 0 y 50)
df = df_1[df_1[nombre_columna_caudal].between(0,500)]

df_nuevo = pd.DataFrame({'fecha': df[nombre_columna_tiempo], 'caudal': df[nombre_columna_caudal]})

# # Definir las fechas de inicio y fin que quieres filtrar
# fecha_inicio = '2025-01-29 01:00:00'
# fecha_fin = '2025-01-29 02:00:00'

# # Filtrar el DataFrame entre esas fechas
# df_filtrado_1 = df_nuevo[(df_nuevo['fecha'].between(fecha_inicio,fecha_fin))]

# # Mostrar el DataFrame filtrado
# print((df_filtrado_1['caudal'].mean()*60)/1000)
# print(df_filtrado_1['caudal'].count())

#-------------------------------------------------------------------------------------------------
lista_1 = []
lista_2 = []
dia = '29/01/2025'

# Iterar de 12 a 11 pm (24 horas)
for i in range(2):
    
    if i < 23:
        # Crear las horas de inicio y fin en formato 24 horas
        hora_inicio = f'{dia} {i:02d}:00:00'
        hora_fin = f'{dia} {(i+1)%24:02d}:00:00'
    else:
        # Crear las horas de inicio y fin en formato 24 horas
        hora_inicio = f'{dia} {i:02d}:00:00'
        hora_fin = f'{dia} 23:59:00'

    # Filtrar el DataFrame para las filas que están entre hora_inicio y hora_fin
    df_filtrado = df_nuevo[df_nuevo['fecha'].between(hora_inicio, hora_fin)]

    # Calcular el promedio de las columnas numéricas en ese rango horario
    promedio_por_hora = (df_filtrado['caudal'].mean() * 60) / 1000 # Esto devuelve una Serie con el promedio de cada columna numérica

    lista_1.append(pd.to_datetime(f'{dia} {i:02d}:00:00', format='%d/%m/%Y %H:%M:%S'))
    lista_2.append(promedio_por_hora)

    # Acumular los promedios por hora
    if i == 0:
        toneladas_en_dia = promedio_por_hora
    else:
        toneladas_en_dia = toneladas_en_dia + promedio_por_hora
        
    if i == 1:
        df_final = pd.DataFrame({'fecha': lista_1, 'totalizador': lista_2})
        print(df_final)


# Crear el gráfico de barras
plt.figure(figsize=(10, 6))

# Dibujar las barras en el gráfico, donde el eje X es la fecha de inicio de cada intervalo
plt.bar(df_final['fecha'], df_final['totalizador'], width=0.02)  # width ajusta el tamaño de las barras

# Configurar el formato de fecha en el eje X
plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

# Ajustar el formato de las etiquetas en el eje X para que no se solapen
plt.xticks(rotation=90, ha='right')

# Añadir etiquetas y título
plt.xlabel('Fecha: 17/12/2024')
plt.ylabel('Total por hora')
plt.title(f'Caudal entre Intervalos de Tiempo. Toneladas totales en el dia {toneladas_en_dia}')

# Mostrar el gráfico
plt.tight_layout()  # Ajusta los márgenes
plt.show()
