import os
import subprocess
from tqdm import tqdm

# Definir las carpetas de entrada y salida
carpeta_entrada = "Incluir carpeta con videos para procesamiento"
carpeta_salida = "Incluir carpeta de salida de resultados"

# Crear la carpeta de salida si no existe
os.makedirs(carpeta_salida, exist_ok=True)

# Obtener la lista de archivos en la carpeta de entrada
archivos = [f for f in os.listdir(carpeta_entrada) if f.lower().endswith((".mp4", ".m4a", ".mov"))]

# Verificar si hay archivos para procesar
if not archivos:
    print("No se encontraron archivos MP4 en la carpeta de entrada.")
    exit()

# Proceso de conversión
for archivo in tqdm(archivos, desc="Convirtiendo archivos"):
    ruta_entrada = os.path.join(carpeta_entrada, archivo)
    nombre_salida = os.path.splitext(archivo)[0] + ".wav"
    ruta_salida = os.path.join(carpeta_salida, nombre_salida)

    # Comando FFmpeg para extraer el audio con calidad óptima para IA
    comando = [
        "ffmpeg",
        "-i", ruta_entrada,  # Archivo de entrada
        "-ac", "1",  # Convertir a mono (mejora la transcripción)
        "-ar", "16000",  # Frecuencia de muestreo 16kHz (recomendado para Whisper)
        "-ab", "256k",  # Tasa de bits alta para mejorar calidad
        "-vn",  # Remover el video
        "-y",  # Sobrescribir si ya existe
        ruta_salida
    ]

    # Ejecutar el comando FFmpeg
    subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print(f"Conversión completada. Archivos WAV guardados en: {carpeta_salida}")
