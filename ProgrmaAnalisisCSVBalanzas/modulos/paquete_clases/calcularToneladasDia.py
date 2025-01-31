import pandas as pd

"""
Esta clase calcula el total de toneladas para cada hora en un día específico,
a partir de los datos acondicionados del archivo CSV.
"""

class CalculadorToneladasDia:

    def __init__(self, df):
        self.df = df

    def calcular_toneladas_dia(self, fecha):
        try:
            # Inicializa listas para almacenar las fechas y toneladas promedio por hora
            lista_fecha_hora = []
            lista_prom_toneladas = []

            if not (self.df.loc[self.df['fecha'].dt.strftime('%Y-%m-%d') == f"{fecha}"]).empty:
                # Iterar sobre las 24 horas del día
                for i in range(24):
                    # Buscar los datos de la hora exacta
                    fila_1 = self.df.loc[self.df["fecha"] == f"{fecha} {i:02d}:00:00"]
                    if i < 23:
                        fila_2 = self.df.loc[self.df["fecha"] == f"{fecha} {(i+1):02d}:00:00"]

                    # Si se encuentran datos para la hora y la siguiente hora
                    if not fila_1.empty and not fila_2.empty:
                        # Define las horas de inicio y fin para el rango de la hora
                        hora_inicio = f'{fecha} {i:02d}:00:00'
                        hora_fin = f'{fecha} {(i+1)%24:02d}:00:00' if i < 23 else f'{fecha} 23:59:00'
                        
                        # Filtra el DataFrame para obtener los registros dentro del rango de horas
                        df_filtrado = self.df[self.df['fecha'].between(hora_inicio, hora_fin)]
                        
                        # Calcular el promedio de caudal por hora y convertirlo a toneladas
                        promedio_por_hora = (df_filtrado['caudal'].mean() * 60) / 1000  # Toneladas por hora

                        # Añadir la hora y el promedio calculado a las listas
                        lista_fecha_hora.append(pd.to_datetime(f'{fecha} {i:02d}:00:00', format='%Y-%m-%d %H:%M:%S'))
                        lista_prom_toneladas.append(promedio_por_hora)

                # Crear un DataFrame con las fechas y toneladas calculadas
                df_final = pd.DataFrame({'fecha': lista_fecha_hora, 'totalizador': lista_prom_toneladas})
                return df_final
            else:
                print(f"Fecha {fecha} no encontrada en los datos.")
                return None
        except Exception as e:
            print(f"Error inesperado al calcular las toneladas: {e}")
            return None