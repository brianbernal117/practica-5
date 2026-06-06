from supabase import create_client
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

sb = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))

# 1. Descargar tabla productos
response = sb.table('productos').select('*').execute()
df = pd.DataFrame(response.data)
print("=== TABLA ORIGINAL ===")
print(df[['id', 'nombre', 'precio', 'stock']])

# 2. Aplicar descuento del 10% a productos con stock > 10
df['precio_nuevo'] = df.apply(
    lambda row: round(row['precio'] * 0.90, 2) if row['stock'] > 10 else row['precio'],
    axis=1
)
print("\n=== CON DESCUENTO APLICADO ===")
print(df[['id', 'nombre', 'precio', 'precio_nuevo', 'stock']])

# 3. Subir cambios a Supabase
for _, row in df[df['stock'] > 10].iterrows():
    sb.table('productos').update(
        {'precio': row['precio_nuevo']}
    ).eq('id', row['id']).execute()

print("\n Descuentos aplicados correctamente en Supabase!")