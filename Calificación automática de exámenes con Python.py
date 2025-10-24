import pandas as pd

# === PRIMER BLOQUE: CARGA Y VALIDACIÓN DE DATOS ===
def cargar_datos(ruta_estudiantes, ruta_clave):
    try:
        df_estudiantes = pd.read_csv(ruta_estudiantes)
    except:
        df_estudiantes = pd.read_excel(ruta_estudiantes.replace('.csv', '.xlsx'))

    try:
        df_correctas = pd.read_csv(ruta_clave)
    except:
        df_correctas = pd.read_excel(ruta_clave.replace('.csv', '.xlsx'))

    return df_estudiantes, df_correctas


# === SEGUNDO BLOQUE: PROCESAMIENTO CENTRAL ===
def calcular_puntuaciones(df_estudiantes, df_correctas):
    preguntas = df_correctas['Pregunta'].values
    clave_respuestas = {}

    for i in range(df_correctas.shape[0]):
        pregunta = df_correctas['Pregunta'].iloc[i]
        respuesta = df_correctas['Respuesta'].iloc[i]
        clave_respuestas[pregunta] = respuesta

    df_estudiantes['Puntuación'] = 0
    for p in preguntas:
        respuesta_correcta = clave_respuestas[p]
        df_estudiantes['Puntuación'] = df_estudiantes['Puntuación'].add(
            (df_estudiantes[p] == respuesta_correcta).astype(int)
        )
    
    df_estudiantes['Puntuación'] = (df_estudiantes['Puntuación'] / len(preguntas)) * 10
    return df_estudiantes, clave_respuestas, preguntas


# === TERCER BLOQUE: GENERACIÓN DE REPORTES ===
def generar_reportes(df_estudiantes, clave_respuestas, preguntas):
    df_detalle = df_estudiantes.copy()

    for p in preguntas:
        df_detalle[p] = df_detalle[p].where(
            df_detalle[p] == clave_respuestas[p],
            df_detalle[p] + 'X'
        )

    df_detalle = df_detalle.sort_values('Puntuación', ascending=False)
    print("Leyenda: RespuestaX = Incorrecta")
    print(df_detalle.to_string(index=False))

    print("\n ==== RESULTADOS DE LOS ESTUDIANTES ====")
    print(df_estudiantes[['Nombre','Puntuación']].sort_values('Puntuación', ascending=False).to_string(index=False))

    df_estudiantes.to_csv("resultados_examen.csv", index=False)
    print("\nResultados guardados en 'resultados_examen.csv'")

# === EJECUCIÓN DEL PROGRAMA ===
def main():
    ruta_estudiantes = "C:/Users/Liliana/OneDrive/Documentos/Proyectos_Python/respuestas_estudiantes.csv"
    ruta_clave = "C:/Users/Liliana/OneDrive/Documentos/Proyectos_Python/respuestas_correctas.csv"

    df_estudiantes, df_correctas = cargar_datos(ruta_estudiantes, ruta_clave)
    df_estudiantes, clave_respuestas, preguntas = calcular_puntuaciones(df_estudiantes, df_correctas)
    generar_reportes(df_estudiantes, clave_respuestas, preguntas)


if __name__ == "__main__":
    main()

