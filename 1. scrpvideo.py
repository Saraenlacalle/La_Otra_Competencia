import yt_dlp

# Nombre del archivo con las URLs
archivo_urls = "Incluir archivo txt con direcciónes de videos en YouTube"

# Leer las URLs desde el archivo
with open(archivo_urls, "r") as f:
    urls = [line.strip() for line in f if line.strip()]  # Elimina líneas vacías

# Configuración de descarga
opciones = {
    "outtmpl": "/Users/jwhan/Workspace/Compensar/Tesis/videos/Diario_As/%(title)s.%(ext)s",  # Usa el título del video
    "format": "best",  # Descarga la mejor calidad disponible
}

# Descargar los videos
with yt_dlp.YoutubeDL(opciones) as ydl:
    ydl.download(urls)

print("Descarga completada.")
