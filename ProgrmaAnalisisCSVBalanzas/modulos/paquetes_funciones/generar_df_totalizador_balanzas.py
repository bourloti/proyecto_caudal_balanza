import pandas as pd

def generar_df_totalizadores_balanzas(df_dia, titulo):
    '''
    Genera un dataframe con los valores por hora de todas las balanzas, y lo convierte a CSV
    df_dia: lista donde cada elementeo es un dataframe con columna1 (fecha) y columna 2 (totalizador)
    titulo: lista con los nombres de cada una de las balanzas
    '''
    
    # Inicializa el diccionario vacío
    diccionario_balanzas = {}

    # Itera sobre las filas de df_dia_graficos
    for i in range(len(df_dia)):
        # Genera un nombre para la balanza (puedes personalizar esto si tienes nombres específicos)
        nombre_balanza = f'{titulo[i]}'  # Nombres como 'balanza_1', 'balanza_2', etc.
        
        # Crea las listas de toneladas y fechas
        lista_toneladas_totales = list(df_dia[i]['totalizador'])
        lista_fechas = list(df_dia[i]['fecha'])

        # Agregar las fechas y toneladas al diccionario
        diccionario_balanzas[f'fecha_{nombre_balanza}'] = lista_fechas
        diccionario_balanzas[f'toneladas_{nombre_balanza}'] = lista_toneladas_totales
        
        df = pd.DataFrame(diccionario_balanzas)
        
    return df