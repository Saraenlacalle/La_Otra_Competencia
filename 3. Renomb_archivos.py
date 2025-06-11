import os
import pandas as pd

def renombrar_archivos_y_generar_excel(carpeta, prefijo="archivo_"):
    archivos = [f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))]
    
    datos = []
    for i, archivo in enumerate(archivos, start=1):
        ext = os.path.splitext(archivo)[1]  # Obtener la extensión
        nuevo_nombre = f"{prefijo}{i}{ext}"
        
        ruta_original = os.path.join(carpeta, archivo)
        ruta_nueva = os.path.join(carpeta, nuevo_nombre)
        
        os.rename(ruta_original, ruta_nueva)
        datos.append([archivo, nuevo_nombre])
    
    # Crear DataFrame y guardar en Excel
    df = pd.DataFrame(datos, columns=["Nombre Original", "Nuevo Nombre"])
    excel_path = os.path.join(carpeta, "renombrados.xlsx")
    df.to_excel(excel_path, index=False)
    
    print(f"Proceso completado. Archivo Excel generado en: {excel_path}")

# Ruta de la carpeta a procesar (modificar según sea necesario)
carpeta = "Incluir carpeta con archivos que requieren organización"
renombrar_archivos_y_generar_excel(carpeta)
