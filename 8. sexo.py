import pandas as pd

# === 1. Cargar archivo CSV ===
df = pd.read_csv("/Users/jwhan/Desktop/Sara/analisis_texto_sonido_etiquetado.csv")

# === 2. Diccionario de deportes basado en el corpus ===
deportes_olimpicos = {
    "natación": ["natación", "nadador", "nadadora"],
    "triatlón": ["triatlón", "triatleta"],
    "bicicleta": ["bicicleta", "ciclismo", "ciclista"],
    "gimnasia": ["gimnasia", "gimnasta"],
    "fútbol": ["fútbol", "futbolista"],
    "tenis": ["tenis", "tenista"],
    "boxeo": ["boxeo", "boxeador", "boxeadora"],
    "baloncesto": ["baloncesto", "basquetbolista"],
}

# === 3. Indicadores de género femenino y masculino ===
indicadores_femenino = [
    "ella", "jugadora", "campeona", "femenino", "femenina",
    "nadadora", "gimnasta", "triatleta"
]

indicadores_masculino = [
    "él", "jugador", "campeón", "masculino", "masculina",
    "nadador", "boxeador", "futbolista"
]

# === 4. Función para detectar deporte ===
def detectar_deporte(texto):
    texto = texto.lower()
    for deporte, palabras_clave in deportes_olimpicos.items():
        if any(palabra in texto for palabra in palabras_clave):
            return deporte
    return "ninguno"

# === 5. Función para inferir género del deporte ===
def detectar_genero_deporte(texto):
    texto = texto.lower()
    if any(pal in texto for pal in indicadores_femenino):
        return "femenino"
    elif any(pal in texto for pal in indicadores_masculino):
        return "masculino"
    else:
        return "no identificado"

# === 6. Aplicar las funciones al DataFrame ===
df['Deporte Mencionado'] = df['Texto'].apply(detectar_deporte)
df['Género Deporte'] = df['Texto'].apply(detectar_genero_deporte)

# === 7. Guardar archivo enriquecido ===
df.to_csv('/Users/jwhan/Desktop/Sara/analisis_texto_sonido_etiquetado.csv', index=False)
print("✅ Archivo guardado como 'analisis_texto_sonido_completo.csv'")
df.to_excel("/Users/jwhan/Desktop/Sara/BaseDatos.xlsx", index=False)
print("✅ También se guardó como 'BaseDatos.xlsx'")