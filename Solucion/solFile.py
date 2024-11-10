import pandas as pd
from datetime import datetime

#Leer el archivo
df = pd.read_csv('C:\\Users\\rosem\\Downloads\\Cuadrodepagos_aws.csv')

# Mostrar las primeras filas
print(df.head())
# Mostrar los nombres de las columnas
print(df.columns)

# Convertir las columnas de fechas a formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha']) # Corresponde a la fecha de vencimiento
df['Fecha_de_Pago_Aplicado'] = pd.to_datetime(df['Fecha de Pago Aplicado']) #Corresponde a la fecha de pago

# Verificar que las conversiones se realizaron correctamente
print(df[['Fecha', 'Fecha_de_Pago_Aplicado']].head())


#1) Cálculo de días mora con la fecha corte

#fecha_str = input("Ingresa una fecha (YYYY-MM-DD): ")
fecha_actual = datetime.today()

# Función para calcular los días de mora
def calcular_dias_mora(Fecha, Fecha_de_Pago_Aplicado):
    if pd.isna(Fecha_de_Pago_Aplicado) or Fecha_de_Pago_Aplicado > fecha_actual:  # No ha pagado o está por pagar
        dias_mora = (fecha_actual - Fecha).days
        return max(dias_mora, 0)  # No debe haber valores negativos
    else:
        return 0  # No hay mora si ya pagó

df['dias_mora'] = df.apply(lambda row: calcular_dias_mora(row['Fecha'], row['Fecha_de_Pago_Aplicado']), axis=1)

print(df[['ID Contrato', 'Fecha', 'Fecha_de_Pago_Aplicado', 'dias_mora']].head())

#2) Calculo del saldo insoluto en la fecha corte

# Convertir las columnas de fechas a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Fecha_de_Pago_Aplicado'] = pd.to_datetime(df['Fecha_de_Pago_Aplicado'], errors='coerce')  # 'coerce' para valores inválidos

print(df[['Fecha', 'Fecha_de_Pago_Aplicado']].head())

# Definir la fecha de corte
fecha_corte = datetime(2024, 10, 15)

# Filtrar las filas hasta la fecha de corte
df_filtrado = df[df['Fecha_de_Pago_Aplicado'] <= fecha_corte]

# Agrupar por ID_contrato y obtener el saldo insoluto
saldo_insoluto = df_filtrado.groupby('ID Contrato').agg(saldo_insoluto=('Saldo Final', 'last') ) # Tomamos el último saldo insoluto registrado por cada cliente

# Ver los resultados
print(saldo_insoluto.head())




