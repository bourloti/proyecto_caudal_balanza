import pandas as pd
from datetime import datetime 

# Obtiene el caudal de las balanzas , pasandole el valor acumulado proveniente del PLC 
class CaudalBalanzas:
    def __init__(self):
        self.acumulado_anterior = 0

    def obtiene_caudal(self, acumulado):

        # Calcula los kilogramas entre un llamado y el otro
        kilos = acumulado - self.acumulado_anterior
        self.acumulado_anterior = acumulado  # Actualizar el valor de acumulado_anterior

        # Crea un DataFrame con la fecha y los kilos
        df = pd.DataFrame({'fecha': [datetime.now()], 'caudal': [kilos]})

        return df