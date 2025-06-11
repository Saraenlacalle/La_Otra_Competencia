import os
import librosa
import numpy as np
import pandas as pd

def cargar_audio(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    return y, sr

def extraer_caracteristicas(segment, sr):
    if len(segment) < 2048:
        return None

    try:
        pitch, magnitudes = librosa.piptrack(y=segment, sr=sr)
        pitch_values = pitch[pitch > 0]
        pitch_mean = np.mean(pitch_values) if len(pitch_values) > 0 else 0

        intensity = librosa.feature.rms(y=segment).mean()
        tempo, _ = librosa.beat.beat_track(y=segment, sr=sr)
        mfccs = librosa.feature.mfcc(y=segment, sr=sr, n_mfcc=13).mean(axis=1)

        non_silent_intervals = librosa.effects.split(segment, top_db=20)
        pausa_total = 0
        for j in range(1, len(non_silent_intervals)):
            pausa = non_silent_intervals[j][0] - non_silent_intervals[j-1][1]
            pausa_total += pausa / sr

        return {
            'Pitch Mean': pitch_mean,
            'Intensity Mean': intensity,
            'Tempo': tempo,
            'Pausa Total (s)': pausa_total,
            **{f'MFCC_{j+1}': mfccs[j] for j in range(13)}
        }
    except Exception as e:
        print(f"⚠️ Error al procesar un segmento: {e}")
        return None

def procesar_audio_por_segmentos(audio_path, caso, nombre_archivo, duracion_segmento=1.0):
    print(f"Iniciando procesamiento del archivo: {nombre_archivo} (caso: {caso})")
    
    y, sr = cargar_audio(audio_path)
    duracion_total = len(y) / sr
    datos_completos = []

    for seg_inicio in np.arange(0, duracion_total, duracion_segmento):
        seg_fin = min(seg_inicio + duracion_segmento, duracion_total)
        segmento = y[int(seg_inicio * sr):int(seg_fin * sr)]

        caracteristicas = extraer_caracteristicas(segmento, sr)
        if caracteristicas:
            caracteristicas['Caso'] = caso
            caracteristicas['Archivo'] = nombre_archivo
            caracteristicas['Inicio'] = seg_inicio
            caracteristicas['Fin'] = seg_fin
            datos_completos.append(caracteristicas)

    return datos_completos

def procesar_todos_los_archivos(carpeta_raiz, salida_csv_final, duracion_segmento=1.0):
    todos_los_datos = []

    for carpeta_caso in os.listdir(carpeta_raiz):
        ruta_caso = os.path.join(carpeta_raiz, carpeta_caso)
        if os.path.isdir(ruta_caso):
            for carpeta_archivo in os.listdir(ruta_caso):
                ruta_archivo_dir = os.path.join(ruta_caso, carpeta_archivo)
                if os.path.isdir(ruta_archivo_dir):
                    for archivo in os.listdir(ruta_archivo_dir):
                        if archivo.endswith('.wav'):
                            ruta_audio = os.path.join(ruta_archivo_dir, archivo)
                            datos = procesar_audio_por_segmentos(
                                audio_path=ruta_audio,
                                caso=carpeta_caso,
                                nombre_archivo=carpeta_archivo,
                                duracion_segmento=duracion_segmento
                            )
                            todos_los_datos.extend(datos)

    if todos_los_datos:
        df = pd.DataFrame(todos_los_datos)
        os.makedirs(os.path.dirname(salida_csv_final), exist_ok=True)
        df.to_csv(salida_csv_final, index=False, encoding='utf-8', sep=',')
        print(f"\n✅ Todos los resultados se guardaron en:\n{salida_csv_final}")
    else:
        print("⚠️ No se generaron datos. Revisa los archivos de entrada.")

# === PARÁMETROS ===
carpeta_audio = '/Users/jwhan/Documents/superwhisper/recordings'
salida_csv_final = '/Users/jwhan/Desktop/Sara/textura_sonora.csv'

procesar_todos_los_archivos(carpeta_audio, salida_csv_final)