import pandas as pd
import os

# Rutas
RUTA_MATCHES = "datos/matches_1930_2022.csv"
CARPETA_SALIDA = "datos_limpios"
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# 🏆 DICCIONARIO OFICIAL DE ARGENTINA EN MUNDIALES (1930-2026) - GOLEADORES COMPARTIDOS DETALLADOS
DATOS_OFICIALES = {
    1930: {"partidos": 5,  "goles": 18, "gc": 9,  "instancia": "🥈 Subcampeón",     "goleador": "Guillermo Stábile (8)"},
    1934: {"partidos": 1,  "goles": 2,  "gc": 3,  "instancia": "Fase Eliminatoria",  "goleador": "Ernesto Belis y Alberto Galateo (1 c/u)"},
    1958: {"partidos": 3,  "goles": 5,  "gc": 10, "instancia": "Fase Eliminatoria",  "goleador": "Oreste Corbatta (3)"},
    1962: {"partidos": 3,  "goles": 2,  "gc": 3,  "instancia": "Fase Eliminatoria",  "goleador": "José Sanfilippo y Héctor Facundo (1 c/u)"},
    1966: {"partidos": 4,  "goles": 4,  "gc": 2,  "instancia": "Fase Eliminatoria",  "goleador": "Luis Artime (3)"},
    1974: {"partidos": 6,  "goles": 9,  "gc": 12, "instancia": "Fase Eliminatoria",  "goleador": "René Houseman (3)"},
    1978: {"partidos": 7,  "goles": 15, "gc": 4,  "instancia": "🏆 Campeón",          "goleador": "Mario Kempes (6)"},
    1982: {"partidos": 5,  "goles": 8,  "gc": 7,  "instancia": "Fase Eliminatoria",  "goleador": "Daniel Bertoni, Daniel Passarella y Diego Maradona (2 c/u)"},
    1986: {"partidos": 7,  "goles": 14, "gc": 5,  "instancia": "🏆 Campeón",          "goleador": "Diego Maradona (5)"},
    1990: {"partidos": 7,  "goles": 5,  "gc": 4,  "instancia": "🥈 Subcampeón",     "goleador": "Claudio Caniggia (2)"},
    1994: {"partidos": 4,  "goles": 8,  "gc": 6,  "instancia": "Fase Eliminatoria",  "goleador": "Gabriel Batistuta (4)"},
    1998: {"partidos": 5,  "goles": 10, "gc": 4,  "instancia": "Fase Eliminatoria",  "goleador": "Gabriel Batistuta (5)"},
    2002: {"partidos": 3,  "goles": 2,  "gc": 2,  "instancia": "Fase Eliminatoria",  "goleador": "Gabriel Batistuta y Hernán Crespo (1 c/u)"},
    2006: {"partidos": 5,  "goles": 11, "gc": 3,  "instancia": "Fase Eliminatoria",  "goleador": "Hernán Crespo y Maxi Rodríguez (3 c/u)"},
    2010: {"partidos": 5,  "goles": 10, "gc": 6,  "instancia": "Fase Eliminatoria",  "goleador": "Gonzalo Higuaín (4)"},
    2014: {"partidos": 7,  "goles": 8,  "gc": 4,  "instancia": "🥈 Subcampeón",     "goleador": "Lionel Messi (4)"},
    2018: {"partidos": 4,  "goles": 6,  "gc": 9,  "instancia": "Fase Eliminatoria",  "goleador": "Sergio Agüero (2)"},
    2022: {"partidos": 7,  "goles": 15, "gc": 8,  "instancia": "🏆 Campeón",          "goleador": "Lionel Messi (7)"},
    2026: {"partidos": 8,  "goles": 19, "gc": 8,  "instancia": "🥈 Subcampeón",     "goleador": "Lionel Messi (8)"},
}

def limpiar_datos_argentina():
    print("Iniciando limpieza enfocada en ARGENTINA...")
    
    if os.path.exists(RUTA_MATCHES):
        df = pd.read_csv(RUTA_MATCHES, encoding="utf-8")
        df_arg = df[df['home_team'].str.contains('Argentina', case=False, na=False) | 
                    df['away_team'].str.contains('Argentina', case=False, na=False)].copy()
        
        df_arg["Date"] = pd.to_datetime(df_arg["Date"], errors="coerce")
        df_arg["Year"] = pd.to_numeric(df_arg["Year"], errors="coerce").fillna(0).astype(int)
        df_arg["home_score"] = pd.to_numeric(df_arg["home_score"], errors="coerce").fillna(0).astype(int)
        df_arg["away_score"] = pd.to_numeric(df_arg["away_score"], errors="coerce").fillna(0).astype(int)
        
        df_arg["Goles_Arg"] = df_arg.apply(lambda r: r["home_score"] if "Argentina" in r["home_team"] else r["away_score"], axis=1)
        df_arg["Goles_Rival"] = df_arg.apply(lambda r: r["away_score"] if "Argentina" in r["home_team"] else r["home_score"], axis=1)
        df_arg["Rival"] = df_arg.apply(lambda r: r["away_team"] if "Argentina" in r["home_team"] else r["home_team"], axis=1)
        
        def get_resultado(row):
            g_arg = row["Goles_Arg"]
            g_riv = row["Goles_Rival"]
            if g_arg > g_riv: 
                return "Victoria"
            elif g_arg < g_riv: 
                return "Derrota"
            else:
                h_pen = row.get("home_penalty", pd.NA)
                a_pen = row.get("away_penalty", pd.NA)
                if pd.notna(h_pen) and pd.notna(a_pen):
                    is_home = "Argentina" in str(row["home_team"])
                    arg_won = (is_home and h_pen > a_pen) or (not is_home and a_pen > h_pen)
                    return "Victoria" if arg_won else "Derrota"
                return "Empate"

        df_arg["Resultado"] = df_arg.apply(get_resultado, axis=1)
    else:
        df_arg = pd.DataFrame()

    partidos_2026 = [
        {"Year": 2026, "Date": "2026-06-16", "Round": "Fase de Grupos", "Rival": "Argelia", "Goles_Arg": 3, "Goles_Rival": 0, "Resultado": "Victoria"},
        {"Year": 2026, "Date": "2026-06-22", "Round": "Fase de Grupos", "Rival": "Austria", "Goles_Arg": 2, "Goles_Rival": 0, "Resultado": "Victoria"},
        {"Year": 2026, "Date": "2026-06-27", "Round": "Fase de Grupos", "Rival": "Jordania", "Goles_Arg": 3, "Goles_Rival": 1, "Resultado": "Victoria"},
        {"Year": 2026, "Date": "2026-07-03", "Round": "Dieciseisavos", "Rival": "Cabo Verde", "Goles_Arg": 3, "Goles_Rival": 2, "Resultado": "Victoria"},
        {"Year": 2026, "Date": "2026-07-07", "Round": "Octavos de Final", "Rival": "Egipto", "Goles_Arg": 3, "Goles_Rival": 2, "Resultado": "Victoria"},
        {"Year": 2026, "Date": "2026-07-11", "Round": "Cuartos de Final", "Rival": "Suiza", "Goles_Arg": 3, "Goles_Rival": 1, "Resultado": "Victoria"},
        {"Year": 2026, "Date": "2026-07-15", "Round": "Semifinal", "Rival": "Inglaterra", "Goles_Arg": 2, "Goles_Rival": 1, "Resultado": "Victoria"},
        {"Year": 2026, "Date": "2026-07-19", "Round": "Final", "Rival": "España", "Goles_Arg": 0, "Goles_Rival": 1, "Resultado": "Derrota"},
    ]
    
    df_2026 = pd.DataFrame(partidos_2026)
    df_arg = pd.concat([df_arg, df_2026], ignore_index=True)
    
    resumen_mundiales = []
    for year, datos in sorted(DATOS_OFICIALES.items()):
        resumen_mundiales.append({
            "Año": year,
            "Partidos_Jugados": datos["partidos"],
            "Goles_Arg": datos["goles"],
            "Goles_Rival": datos["gc"],
            "Goleador_Arg": datos["goleador"],
            "Instancia": datos["instancia"]
        })
        
    df_resumen = pd.DataFrame(resumen_mundiales).sort_values("Año")
    
    df_arg.to_csv(f"{CARPETA_SALIDA}/partidos_argentina.csv", index=False, date_format='%Y-%m-%d')
    df_resumen.to_csv(f"{CARPETA_SALIDA}/resumen_argentina.csv", index=False)
    
    print("✅ ¡Limpieza completada con goleadores detallados!")

if __name__ == "__main__":
    limpiar_datos_argentina()
