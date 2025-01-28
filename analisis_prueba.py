import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Leer el archivo CSV
df = pd.read_csv('proyecto_caudal_balanza\\caudal_balanza_final_molino_blanco.csv', sep=',')  # Ajusta el nombre del archivo y el separador si es necesario
df_trending_mb = pd.read_csv('proyecto_caudal_balanza\\Trending_MB.csv', sep=';')  # Ajusta el nombre del archivo y el separador si es necesario

df['fecha'] = df['fecha'].replace({'-': '/'}, regex=True)
df_trending_mb['Terminado Time'] = df_trending_mb['Terminado Time'].replace({'a.m.': 'AM', 'p.m.': 'PM'}, regex=True)

# Convertir la columna 'Fecha y Hora' a formato datetime
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y/%m/%d %H:%M:%S.%f')
df_trending_mb['Terminado Time'] = pd.to_datetime(df_trending_mb['Terminado Time'], format='%d/%m/%Y %I:%M:%S %p')

df['caudal'] = pd.to_numeric(df['caudal'])
df_trending_mb['Terminado ValueY'] = df_trending_mb['Terminado ValueY'].replace({',': '.'}, regex=True)
df_trending_mb['Terminado ValueY'] = pd.to_numeric(df_trending_mb['Terminado ValueY'])

# Filtrar los datos para que solo queden dentro del rango esperado (por ejemplo, entre 0 y 50)
df = df[(df['caudal'] >= 0) & (df['caudal'] <= 500)]
df_trending_mb = df_trending_mb[(df_trending_mb['Terminado ValueY'] >= 0) & (df_trending_mb['Terminado ValueY'] <= 500)]

df_nuevo = pd.DataFrame({'fecha': df['fecha'], 'caudal': df['caudal']})
df_nuevo_trending_mb = pd.DataFrame({'fecha': df_trending_mb['Terminado Time'], 'caudal': df_trending_mb['Terminado ValueY']})

# Definir las fechas de inicio y fin que quieres filtrar
fecha_inicio = '2025-01-27 03:51:00'
fecha_fin = '2025-01-27 04:51:01'

# Filtrar el DataFrame entre esas fechas
df_filtrado = df_nuevo[(df_nuevo['fecha'] >= fecha_inicio) & (df_nuevo['fecha'] <= fecha_fin)]
df_filtrado_trending_mb = df_nuevo_trending_mb[(df_nuevo_trending_mb['fecha'] >= '27/01/2025 03:55:56 AM') & (df_nuevo_trending_mb['fecha'] <= '27/01/2025 04:55:56 AM')]

# Mostrar el DataFrame filtrado
print((df_filtrado['caudal'].mean()*59)/1000)
print(df_filtrado)

print(df_filtrado_trending_mb['caudal'].mean())
print(df_filtrado_trending_mb)

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