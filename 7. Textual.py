import pandas as pd
import spacy
from textblob import TextBlob

# === 1. Cargar el archivo CSV original ===
df = pd.read_csv("Incluya dirección de archivo con procesamiento de texto y sonido (último crado proceso 6)")

# === 2. Cargar modelo de spaCy en español ===
nlp = spacy.load("es_core_news_sm")

# === 3. Análisis de sentimiento (TextBlob trabaja en inglés, pero puede funcionar si el texto es simple) ===
def analizar_sentimiento(texto):
    blob = TextBlob(texto)
    polaridad = blob.sentiment.polarity
    if polaridad > 0.1:
        return 'positivo', polaridad
    elif polaridad < -0.1:
        return 'negativo', polaridad
    else:
        return 'neutro', polaridad

# === 4. Análisis de tiempo verbal ===
def detectar_tiempo(texto):
    doc = nlp(texto)
    tiempos = {'presente': 0, 'pasado': 0, 'futuro': 0}
    for token in doc:
        if token.pos_ == 'VERB':
            if 'Tense=Pres' in token.morph:
                tiempos['presente'] += 1
            elif 'Tense=Past' in token.morph:
                tiempos['pasado'] += 1
            elif 'Tense=Fut' in token.morph:
                tiempos['futuro'] += 1
    if not any(tiempos.values()):
        return 'indefinido'
    return max(tiempos, key=tiempos.get)

# === 5. Clasificación del uso del lenguaje ===
def clasificar_lenguaje(texto):
    texto_lower = texto.lower()
    if any(pal in texto_lower for pal in ['yo creo', 'pienso que', 'me parece', 'desde mi perspectiva']):
        return 'perspectiva'
    elif any(pal in texto_lower for pal in ['bueno', 'malo', 'excelente', 'terrible', 'importante', 'grave']):
        return 'evaluativo'
    else:
        return 'informativo'

# === 6. Aplicar las funciones ===
sentimientos = df['Texto'].apply(analizar_sentimiento)
df['Sentimiento'] = sentimientos.apply(lambda x: x[0])
df['Valor Sentimiento'] = sentimientos.apply(lambda x: x[1])

df['Tiempo Verbal'] = df['Texto'].apply(detectar_tiempo)
df['Tipo de Lenguaje'] = df['Texto'].apply(clasificar_lenguaje)

# === 7. Guardar resultado ===
df.to_csv("direccion y n ombre de archivo del resultado de este proceso.", index=False)
print("✅ Archivo enriquecido guardado como 'analisis_texto_sonido_enriquecido.csv'")
