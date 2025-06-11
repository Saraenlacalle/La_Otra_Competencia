import os
import json
import csv

# Ruta raíz que contiene las subcarpetas por caso (Claro, Win, Diario_As)
carpeta_json = 'dirección de carpeta con archivos Json resultantes de transcripción'

# Archivo CSV de salida
archivo_csv = 'Establezca la direccion y el nombre del archivo de salida'

# Nuevos encabezados: caso, nombre_archivo, text, start, end
encabezados = ['caso', 'nombre_archivo', 'text', 'start', 'end']

# Función para buscar recursivamente 'text', 'start', y 'end' en un JSON anidado
def extraer_campos(json_data):
    resultados = []
    if isinstance(json_data, dict):
        if 'text' in json_data and 'start' in json_data and 'end' in json_data:
            resultados.append({
                'text': json_data['text'],
                'start': json_data['start'],
                'end': json_data['end']
            })
        for valor in json_data.values():
            resultados.extend(extraer_campos(valor))
    elif isinstance(json_data, list):
        for elemento in json_data:
            resultados.extend(extraer_campos(elemento))
    return resultados

# Abrir el archivo CSV para escribir los datos
with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo_salida:
    escritor_csv = csv.writer(archivo_salida)
    escritor_csv.writerow(encabezados)
    
    # Recorrer todos los subdirectorios y archivos
    for carpeta_caso in os.listdir(carpeta_json):
        ruta_caso = os.path.join(carpeta_json, carpeta_caso)
        if os.path.isdir(ruta_caso):
            for carpeta_archivo in os.listdir(ruta_caso):
                ruta_archivo_dir = os.path.join(ruta_caso, carpeta_archivo)
                if os.path.isdir(ruta_archivo_dir):
                    # Buscar un archivo .json dentro de esta carpeta
                    for archivo in os.listdir(ruta_archivo_dir):
                        if archivo.endswith('.json'):
                            ruta_json = os.path.join(ruta_archivo_dir, archivo)
                            with open(ruta_json, 'r', encoding='utf-8') as archivo_json:
                                datos = json.load(archivo_json)
                                campos_extraidos = extraer_campos(datos)
                                for campo in campos_extraidos:
                                    escritor_csv.writerow([
                                        carpeta_caso,           # nombre del caso (ej. Claro)
                                        carpeta_archivo,        # nombre del archivo (ej. archivo_112)
                                        campo['text'],
                                        campo['start'],
                                        campo['end']
                                    ])

print(f"Archivo CSV generado exitosamente: {archivo_csv}")
