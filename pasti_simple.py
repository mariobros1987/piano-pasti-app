import pandas as pd

# Create the data
data = [
    {"Giorno": "Mercoledì", "Pasto": "Colazione", "Categoria": "Cereali", "Alimento": "Fiocchi d'avena", "Quantità_Mario": "40g", "Quantità_Mariantonietta": "30g"},
    {"Giorno": "Mercoledì", "Pasto": "Colazione", "Categoria": "Proteine", "Alimento": "Yogurt greco", "Quantità_Mario": "150g", "Quantità_Mariantonietta": "125g"},
    {"Giorno": "Mercoledì", "Pasto": "Colazione", "Categoria": "Frutta", "Alimento": "Fragole", "Quantità_Mario": "50g", "Quantità_Mariantonietta": "50g"},
    {"Giorno": "Mercoledì", "Pasto": "Spuntino", "Categoria": "Frutta", "Alimento": "Kiwi", "Quantità_Mario": "1 medio", "Quantità_Mariantonietta": "1 medio"},
    {"Giorno": "Mercoledì", "Pasto": "Pranzo", "Categoria": "Cereali", "Alimento": "Pasta integrale", "Quantità_Mario": "60g", "Quantità_Mariantonietta": "50g"},
    {"Giorno": "Mercoledì", "Pasto": "Pranzo", "Categoria": "Proteine", "Alimento": "Merluzzo", "Quantità_Mario": "150g", "Quantità_Mariantonietta": "120g"},
    {"Giorno": "Mercoledì", "Pasto": "Pranzo", "Categoria": "Verdura", "Alimento": "Broccoli", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"},
    {"Giorno": "Mercoledì", "Pasto": "Pranzo", "Categoria": "Grassi", "Alimento": "Olio EVO", "Quantità_Mario": "10g", "Quantità_Mariantonietta": "10g"},
    {"Giorno": "Mercoledì", "Pasto": "Merenda", "Categoria": "Cereali/Grassi", "Alimento": "Gallette + burro arachidi", "Quantità_Mario": "2 + 10g", "Quantità_Mariantonietta": "2 + 10g"},
    {"Giorno": "Mercoledì", "Pasto": "Cena", "Categoria": "Proteine", "Alimento": "Bresaola", "Quantità_Mario": "120g", "Quantità_Mariantonietta": "80g"},
    {"Giorno": "Mercoledì", "Pasto": "Cena", "Categoria": "Verdura", "Alimento": "Insalata", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"},
    {"Giorno": "Mercoledì", "Pasto": "Cena", "Categoria": "Cereali", "Alimento": "Pane integrale", "Quantità_Mario": "40g", "Quantità_Mariantonietta": "40g"},
    {"Giorno": "Mercoledì", "Pasto": "Cena", "Categoria": "Grassi", "Alimento": "Olio EVO", "Quantità_Mario": "10g", "Quantità_Mariantonietta": "10g"},
]

# Create DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel("pasti_settimanali.xlsx", index=False)
print("File Excel creato con successo: pasti_settimanali.xlsx") 