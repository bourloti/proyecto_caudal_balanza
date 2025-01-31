import snap7
from time import sleep

# Intentar conectar en un bucle hasta tener éxito
def connect_to_plc(ip, rack, slot):
    while True:
        try:
            plc = snap7.client.Client()
            print("Intentando conectar al PLC...")
            plc.connect(ip, rack, slot)

            # Verificar si la conexión es exitosa
            if plc.get_connected():
                print("Conexión establecida con éxito.")
                return plc

        except Exception as e:
            print(f"Error al intentar conectar: {e}")
    
        # Esperar antes de volver a intentar
        print("Reintentando en 5 segundos...")
        sleep(5)
