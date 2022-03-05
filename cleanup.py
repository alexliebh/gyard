import pandas as pd
import numpy as np

DATA_URL = ('./data.xlsx')
DATE_COLUMN = "décès"
BOOL_COLS = ["texte", "allemand", "hollandais", "reliquat", 
"alsacien-lorrain", "identitaire", "france", "élaborée", "belges", 
"citation", "épitaphe", "anglais", "translaté", "séputmult", "homme", "femme",
"dix neuf", "vingt", "enfant", "mort né"]

def load_data():
    data = pd.read_excel(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

def replace_oui(col_name):
    np.where(data[col_name] == "oui", "True", "False")

data = load_data()
data["concession"] = data["concession"].fillna(-1).astype(int)
data["âge"] = data["âge"].fillna(-1).astype(int)
data.loc[pd.isna(data['naissance']), 'âge'] = -1


# data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
data["section"] = data["section"].str.strip()

for c in BOOL_COLS:
    data[c] = np.where(data[c] == "oui", True, False)

# data.to_csv("./_cu.csv")
data.to_excel("./_cu.xlsx")
print(len(data["section"]))
