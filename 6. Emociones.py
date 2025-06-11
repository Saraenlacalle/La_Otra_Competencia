import pandas as pd
import ast

# === 1. Cargar archivos ===
df_textura = pd.read_csv("incluya la direccion del archivo con los resultados de sonido")
df_transcripciones = pd.read_csv("Incluya la direccion del archivo con los resultados de las transcripciones")

# === 2. Corregir columna 'Tempo' (de string tipo "[120.0]" a float) ===
def limpiar_tempo(valor):
    try:
        lista = ast.literal_eval(valor)
        if isinstance(lista, list) and len(lista) > 0:
            return float(lista[0])
    except:
        return None
    return None

df_textura['Tempo'] = df_textura['Tempo'].apply(limpiar_tempo)

# === 3. Unificar nombres de columnas ===
df_transcripciones.rename(columns={
    'caso': 'Caso',
    'nombre_archivo': 'Archivo',
    'start': 'start_text',
    'end': 'end_text',
    'text': 'Texto'
}, inplace=True)

# === 4. Asegurar tipos numéricos para tiempo ===
df_textura['Inicio'] = df_textura['Inicio'].astype(float)
df_textura['Fin'] = df_textura['Fin'].astype(float)
df_transcripciones['start_text'] = df_transcripciones['start_text'].astype(float)
df_transcripciones['end_text'] = df_transcripciones['end_text'].astype(float)

# === 5. Columnas de audio a promediar ===
columnas_sonoras = [
    'Pitch Mean', 'Intensity Mean', 'Tempo', 'Pausa Total (s)'
] + [f'MFCC_{i}' for i in range(1, 14)]

# === 6. Función para etiquetar emocionalidad ===
def etiquetar_emocion(fila):
    pitch = fila.get('Pitch Mean', 0)
    intensidad = fila.get('Intensity Mean', 0)
    pausa = fila.get('Pausa Total (s)', 0)
    tempo = fila.get('Tempo', 0)

    if pitch > 300 and intensidad > 0.05:
        return 'emocional'
    elif pausa > 1.0:
        return 'reflexivo'
    elif tempo > 150:
        return 'enérgico'
    else:
        return 'neutro'

# === 7. Recorrer transcripciones y calcular promedios ===
resultados = []

for _, fila in df_transcripciones.iterrows():
    caso = fila['Caso']
    archivo = fila['Archivo']
    start = fila['start_text']
    end = fila['end_text']

    segmento = df_textura[
        (df_textura['Caso'] == caso) &
        (df_textura['Archivo'] == archivo) &
        (df_textura['Inicio'] >= start) &
        (df_textura['Inicio'] <= end)
    ]

    if not segmento.empty:
        promedio = segmento[columnas_sonoras].mean()
        nueva_fila = {
            'Caso': caso,
            'Archivo': archivo,
            'Texto': fila['Texto'],
            'start_text': start,
            'end_text': end
        }
        nueva_fila.update(promedio.to_dict())
        nueva_fila['Etiqueta Sonora'] = etiquetar_emocion(promedio)
        resultados.append(nueva_fila)

# === 8. Crear DataFrame final ===
df_sonido_por_texto = pd.DataFrame(resultados)

# === 9. (Opcional) Guardar a CSV ===
df_sonido_por_texto.to_csv("Incluya direccion y nombre de archivo de salida de este proceso", index=False)
