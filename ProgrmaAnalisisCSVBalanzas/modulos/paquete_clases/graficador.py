import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

"""
Esta clase se encarga de generar los gráficos de barras con los datos de toneladas.
"""

class Graficador:

    def __init__(self, df, titulo):
        self.df = df
        self.titulo = titulo

    def graficar(self, fecha):
        try:
            # Verifica que el DataFrame no esté vacío
            if self.df is None or self.df.empty:
                print("No hay datos para graficar.")
                return
            
            # Crear el gráfico de barras
            plt.figure(figsize=(10, 6))
            plt.bar(self.df['fecha'], self.df['totalizador'], width=0.02)
            
            # Formato de fecha en el eje X (mostrando solo la hora y minutos)
            plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))
            
            # Ajustar la posición de las etiquetas en el eje X para evitar solapamientos
            plt.xticks(rotation=45, ha='right')
            
            # Etiquetas y título del gráfico
            plt.xlabel(f'Fecha: {fecha}')
            plt.ylabel('Total por hora')
            
            # Calcular el total de toneladas en el día y mostrarlo en el título
            toneladas = round(self.df['totalizador'].sum(), 2)
            plt.title(f'{self.titulo} - Toneladas totales: {toneladas} Ton')

            # Mostrar el gráfico ajustando el layout para que se vea bien
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Error al generar el gráfico: {e}")