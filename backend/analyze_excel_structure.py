#!/usr/bin/env python3
import pandas as pd
import sys

def analyze_excel_file(file_path, arl_name):
    print(f"\n=== {arl_name} ===")
    try:
        df = pd.read_excel(file_path)
        print(f"Archivo: {file_path}")
        print(f"Columnas: {df.columns.tolist()}")
        print(f"Número de filas: {len(df)}")
        print("\nPrimeras 3 filas:")
        print(df.head(3))
        
        # Buscar columnas que puedan indicar clientes/empresas
        client_columns = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['empresa', 'cliente', 'company', 'client', 'razon', 'social']):
                client_columns.append(col)
        
        if client_columns:
            print(f"\nColumnas que podrían ser clientes: {client_columns}")
            for col in client_columns:
                unique_values = df[col].dropna().unique()
                print(f"  {col}: {len(unique_values)} valores únicos")
                if len(unique_values) <= 10:
                    print(f"    Valores: {list(unique_values)}")
                else:
                    print(f"    Primeros 5 valores: {list(unique_values[:5])}")
        
        return df
    except Exception as e:
        print(f"Error al leer {file_path}: {e}")
        return None

if __name__ == "__main__":
    # Analizar archivos Excel
    colmena_file = "Files/Estado de Tareas_COLMENA ARL.xlsx"
    positiva_file = "Files/Estado de Tareas_POSITIVA ARL.xlsx"
    
    df_colmena = analyze_excel_file(colmena_file, "COLMENA ARL")
    df_positiva = analyze_excel_file(positiva_file, "POSITIVA ARL")
    
    # Comparar estructuras
    if df_colmena is not None and df_positiva is not None:
        print("\n=== COMPARACIÓN ===")
        print(f"Columnas COLMENA: {set(df_colmena.columns)}")
        print(f"Columnas POSITIVA: {set(df_positiva.columns)}")
        print(f"Columnas comunes: {set(df_colmena.columns) & set(df_positiva.columns)}")
        print(f"Columnas diferentes: {set(df_colmena.columns) ^ set(df_positiva.columns)}")
