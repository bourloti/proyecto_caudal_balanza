import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Leer el archivo CSV
df_1 = pd.read_csv('caudal_balanza_integral_molino_blanco.csv', sep=',')  # Ajusta el nombre del archivo y el separador si es necesario
df_2 = pd.read_csv('Trending_MB.csv', sep=';')  # Ajusta el nombre del archivo y el separador si es necesario

nombre_columna_tiempo_df_1 = 'fecha'
nombre_columna_tiempo_df_2 = 'Integral Time'

nombre_columna_caudal_df_1 = 'caudal'
nombre_columna_caudal_df_2 = 'Integral ValueY'

df_1[nombre_columna_tiempo_df_1] = df_1[nombre_columna_tiempo_df_1].replace({'-': '/'}, regex=True)
df_2[nombre_columna_tiempo_df_2] = df_2[nombre_columna_tiempo_df_2].replace({'a.m.': 'AM', 'p.m.': 'PM'}, regex=True)

# Convertir la columna 'Fecha y Hora' a formato datetime
df_1[nombre_columna_tiempo_df_1] = pd.to_datetime(df_1[nombre_columna_tiempo_df_1], format='%Y/%m/%d %H:%M:%S.%f')
df_2[nombre_columna_tiempo_df_2] = pd.to_datetime(df_2[nombre_columna_tiempo_df_2], format='%d/%m/%Y %I:%M:%S %p')

df_1[nombre_columna_caudal_df_1] = pd.to_numeric(df_1[nombre_columna_caudal_df_1])
df_2[nombre_columna_caudal_df_2] = df_2[nombre_columna_caudal_df_2].replace({',': '.'}, regex=True)
df_2[nombre_columna_caudal_df_2] = pd.to_numeric(df_2[nombre_columna_caudal_df_2])

# Filtrar los datos para que solo queden dentro del rango esperado (por ejemplo, entre 0 y 50)
df_1 = df_1[(df_1[nombre_columna_caudal_df_1] >= 0) & (df_1[nombre_columna_caudal_df_1] <= 500)]
df_2 = df_2[(df_2[nombre_columna_caudal_df_2] >= 0) & (df_2[nombre_columna_caudal_df_2] <= 500)]

df_nuevo = pd.DataFrame({'fecha': df_1['fecha'], 'caudal': df_1['caudal']})
df_nuevo_trending_mb = pd.DataFrame({'fecha': df_2[nombre_columna_tiempo_df_2], 'caudal': df_2[nombre_columna_caudal_df_2]})

# Definir las fechas de inicio y fin que quieres filtrar
fecha_inicio = '2025-01-29 00:00:00'
fecha_fin = '2025-01-29 02:00:00'

# Filtrar el DataFrame entre esas fechas
df_filtrado_1 = df_nuevo[df_nuevo['fecha'].between(fecha_inicio, fecha_fin)]
df_filtrado_2 = df_nuevo_trending_mb[df_nuevo_trending_mb['fecha'].between('29-01-2025 00:03:00', '29-01-2025 02:03:00')]

# Mostrar el DataFrame filtrado
print((df_filtrado_1['caudal'].mean()*59)/1000)
# print(df_filtrado_1['caudal'].count())

print(df_filtrado_2['caudal'].mean())
# print(df_filtrado_2['caudal'].count())

'''
# Graficar la temperatura en función de la fecha y hora
plt.figure(figsize=(10, 6))
#plt.plot(df['Ingreso Silo 101 Time'], df['Ingreso Silo 101'], marker='o', linestyle='-', color='b')
plt.plot(df_filtrado['fecha'],df_filtrado['caudal'], marker='o', linestyle='-', color='b')

# Personalizar la gráfica
plt.title('Serie Temporal de Temperaturas', fontsize=10)
plt.xlabel('Fecha y Hora', fontsize=8)
plt.ylabel('Temperatura (°C)', fontsize=12)

# Ajustar el formato de las fechas en el eje X (incluir la hora)
date_format = DateFormatter('%d/%m/%Y %H:%M')  # Día/Mes/Año Hora:Minuto:Segundo
plt.gca().xaxis.set_major_formatter(date_format)

plt.xticks(rotation=45)  # Rotar las etiquetas del eje X para mejor visibilidad
plt.grid(True)

# Mostrar la gráfica
plt.tight_layout()
plt.show()
'''
'''
import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo CSV
df = pd.read_csv('./Curso_De_Python/analisis_trending/datos_temperatura.csv', sep=';')  # Ajusta el nombre del archivo y el separador si es necesario

# Convertir la columna 'Fecha y Hora' a formato datetime
df['Fecha y Hora'] = pd.to_datetime(df['Fecha y Hora'], format='%d/%m/%Y %I:%M:%S %p')

# Graficar la temperatura en función de la fecha y hora
plt.figure(figsize=(10, 6))
plt.plot(df['Fecha y Hora'][50:100], df['Temperatura (°C)'][50:100], marker='o', linestyle='-', color='b')

# Personalizar la gráfica
plt.title('Serie Temporal de Temperaturas', fontsize=14)
plt.xlabel('Fecha y Hora', fontsize=12)
plt.ylabel('Temperatura (°C)', fontsize=12)
plt.xticks(rotation=45)  # Rotar las etiquetas del eje X para mejor visibilidad
plt.grid(True)

# Mostrar la gráfica
plt.tight_layout()
plt.show()
print(df['Temperatura (°C)'][50:100])'''