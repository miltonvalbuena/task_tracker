#!/usr/bin/env python3
"""
Script para analizar los archivos Excel y entender la estructura de datos
"""

import pandas as pd
import os

def analyze_excel_file(file_path):
    print(f"\n{'='*60}")
    print(f"ANALIZANDO: {os.path.basename(file_path)}")
    print(f"{'='*60}")
    
    try:
        # Leer el archivo Excel
        df = pd.read_excel(file_path)
        
        print(f"📊 Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
        print(f"\n📋 Columnas encontradas:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        print(f"\n📝 Primeras 3 filas de datos:")
        print(df.head(3).to_string())
        
        print(f"\n🔍 Tipos de datos:")
        print(df.dtypes.to_string())
        
        print(f"\n📈 Valores únicos por columna:")
        for col in df.columns:
            unique_count = df[col].nunique()
            print(f"   {col}: {unique_count} valores únicos")
            if unique_count <= 10:  # Mostrar valores únicos si son pocos
                unique_values = df[col].dropna().unique()
                print(f"      Valores: {list(unique_values)}")
        
        return df
        
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return None

def main():
    files_dir = "Files"
    
    if not os.path.exists(files_dir):
        print(f"❌ Directorio {files_dir} no encontrado")
        return
    
    excel_files = [f for f in os.listdir(files_dir) if f.endswith('.xlsx')]
    
    if not excel_files:
        print(f"❌ No se encontraron archivos Excel en {files_dir}")
        return
    
    print(f"🔍 Encontrados {len(excel_files)} archivos Excel:")
    for file in excel_files:
        print(f"   - {file}")
    
    all_dataframes = {}
    
    for file in excel_files:
        file_path = os.path.join(files_dir, file)
        df = analyze_excel_file(file_path)
        if df is not None:
            all_dataframes[file] = df
    
    # Análisis comparativo
    if len(all_dataframes) > 1:
        print(f"\n{'='*60}")
        print("ANÁLISIS COMPARATIVO")
        print(f"{'='*60}")
        
        files = list(all_dataframes.keys())
        df1, df2 = all_dataframes[files[0]], all_dataframes[files[1]]
        
        print(f"\n📊 Comparación de columnas:")
        cols1 = set(df1.columns)
        cols2 = set(df2.columns)
        
        print(f"   Columnas en {files[0]}: {len(cols1)}")
        print(f"   Columnas en {files[1]}: {len(cols2)}")
        print(f"   Columnas comunes: {len(cols1 & cols2)}")
        print(f"   Columnas únicas en {files[0]}: {cols1 - cols2}")
        print(f"   Columnas únicas en {files[1]}: {cols2 - cols1}")

if __name__ == "__main__":
    main()
