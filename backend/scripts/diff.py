from backend.config import settings
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()

import os, sys

# conexões
engine_raw = create_engine(settings.RAW_DATABASE_URL)
engine_dw = create_engine(settings.DW_DATABASE_URL)

df_raw = pd.read_sql("SELECT id FROM resultados_itens", engine_raw)
df_dw = pd.read_sql("SELECT id_staging FROM f_resultado_item", engine_dw)

faltantes = df_raw[~df_raw["id"].isin(df_dw["id_staging"])]

print("IDs faltando no DW:")
print(faltantes if not faltantes.empty else "Nenhum! 🎉")