import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(page_title="Piano Pasti Settimanale", layout="wide")

# Sezione per la lista della spesa e ricette
st.sidebar.title("Lista della Spesa e Ricette")

# Funzione per generare lista della spesa
def genera_lista_spesa(df):
    # Raggruppa per alimento e somma le quantità
    lista_spesa = df.groupby('Alimento').agg({
        'Quantità_Mario': 'sum',
        'Quantità_Mariantonietta': 'sum'
    }).reset_index()
    return lista_spesa

# Funzione per visualizzare ricette per giorno e pasto
def visualizza_ricette(df):
    # Filtra solo pranzi e cene
    ricette = df[df['Pasto'].isin(['Pranzo', 'Cena'])]
    return ricette

# Funzione per visualizzare ricette di verdure e contorni
def visualizza_ricette_verdure():
    ricette_verdure = {
        "Insalata mista": {
            "ingredienti": ["Lattuga", "Rucola", "Pomodorini", "Carote", "Cetrioli"],
            "preparazione": "Lavare e tagliare tutte le verdure. Condire con olio EVO, sale e aceto balsamico a piacere."
        },
        "Verdure grigliate": {
            "ingredienti": ["Zucchine", "Melanzane", "Peperoni", "Radicchio"],
            "preparazione": "Tagliare le verdure a fette, spennellare con olio EVO e grigliare fino a doratura. Condire con sale e erbe aromatiche."
        },
        "Caponata di verdure": {
            "ingredienti": ["Melanzane", "Sedano", "Cipolla", "Pomodori", "Olive verdi"],
            "preparazione": "Tagliare le verdure a cubetti, soffriggere la cipolla, aggiungere le altre verdure e cuocere per 20-25 minuti. Condire con sale e basilico."
        },
        "Insalata di finocchi": {
            "ingredienti": ["Finocchi", "Arance", "Olive nere"],
            "preparazione": "Affettare finemente i finocchi, aggiungere spicchi d'arancia e olive. Condire con olio EVO e sale."
        },
        "Verdure al vapore": {
            "ingredienti": ["Broccoli", "Cavolfiori", "Carote", "Fagiolini"],
            "preparazione": "Cuocere le verdure al vapore per 10-15 minuti. Condire con olio EVO, sale e limone."
        }
    }
    return ricette_verdure

# Funzione per visualizzare ricette per pranzo e cena
def visualizza_ricette_pasti():
    ricette_pasti = {
        "Pranzo": {
            "Pasta integrale con merluzzo": {
                "ingredienti": ["Pasta integrale (90g/70g)", "Merluzzo (150g/120g)", "Verdure miste (200g)", "Olio EVO (10g)", "Aglio", "Prezzemolo"],
                "preparazione": "1. Cuocere la pasta in acqua bollente salata\n2. In una padella, rosolare l'aglio in olio EVO\n3. Aggiungere il merluzzo a pezzetti e cuocere per 5-6 minuti\n4. Unire le verdure miste e cuocere per altri 3-4 minuti\n5. Scolare la pasta e saltarla nel condimento\n6. Completare con prezzemolo fresco"
            },
            "Pasta integrale con pollo": {
                "ingredienti": ["Pasta integrale (90g/70g)", "Petto di pollo (120g/100g)", "Verdure miste (200g)", "Olio EVO (10g)", "Rosmarino", "Salvia"],
                "preparazione": "1. Cuocere la pasta in acqua bollente salata\n2. Tagliare il pollo a strisce e condirlo con erbe aromatiche\n3. In una padella, scaldare l'olio e cuocere il pollo\n4. Aggiungere le verdure e cuocere per 5-6 minuti\n5. Scolare la pasta e unirla al condimento\n6. Saltare il tutto per un minuto"
            }
        },
        "Cena": {
            "Tacchino con patate": {
                "ingredienti": ["Fettine di tacchino (150g/180g)", "Patate (200g/80g)", "Verdure cotte-crude (200g)", "Olio EVO (10g)", "Origano", "Rosmarino"],
                "preparazione": "1. Tagliare le patate a spicchi e condirle con olio e rosmarino\n2. Infornare le patate a 200°C per 20-25 minuti\n3. Grigliare le fettine di tacchino 3-4 minuti per lato\n4. Preparare le verdure cotte-crude\n5. Servire con un filo d'olio e origano"
            },
            "Pesce magro al forno": {
                "ingredienti": ["Pesce magro (200g)", "Pangrattato (q.b.)", "Verdura cotta-cruda (200g)", "Olio EVO (10g)", "Limone", "Prezzemolo"],
                "preparazione": "1. Pulire il pesce e asciugarlo\n2. Condire con olio, sale e pangrattato\n3. Infornare a 180°C per 15-20 minuti\n4. Preparare le verdure come contorno\n5. Servire con succo di limone e prezzemolo fresco"
            },
            "Carne magra alla griglia": {
                "ingredienti": ["Carne magra (150g)", "Verdure cotte-crude (200g)", "Olio EVO (10g)", "Rosmarino", "Salvia"],
                "preparazione": "1. Marinare la carne con erbe aromatiche\n2. Grigliare la carne secondo la cottura desiderata\n3. Preparare le verdure come contorno\n4. Servire con un filo d'olio a crudo"
            }
        }
    }
    return ricette_pasti

# Funzione per caricare i dati
def carica_dati():
    if os.path.exists("pasti_settimanali.xlsx"):
        return pd.read_excel("pasti_settimanali.xlsx")
    else:
        return pd.DataFrame(columns=["Giorno", "Pasto", "Categoria", "Alimento", "Quantità_Mario", "Quantità_Mariantonietta"])

# Funzione per salvare i dati
def salva_dati(df):
    df.to_excel("pasti_settimanali.xlsx", index=False)
    st.success("Dati salvati con successo!")

# Funzione per generare pasti per tutta la settimana
def genera_pasti_settimana():
    # Definizione piano pasti settimanale
    piano_pasti = []
    
    # Giorni della settimana
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    
    # Giorni di allenamento calcetto
    giorni_allenamento = ["Martedì", "Giovedì", "Sabato"]
    
    for giorno in giorni:
        # COLAZIONE (uguale per tutti i giorni)
        piano_pasti.append({
            "Giorno": giorno, "Pasto": "Colazione", "Categoria": "Cereali",
            "Alimento": "Fiocchi d'avena", "Quantità_Mario": "40g", "Quantità_Mariantonietta": "30g"
        })
        piano_pasti.append({
            "Giorno": giorno, "Pasto": "Colazione", "Categoria": "Proteine",
            "Alimento": "Yogurt greco", "Quantità_Mario": "150g", "Quantità_Mariantonietta": "125g"
        })
        piano_pasti.append({
            "Giorno": giorno, "Pasto": "Colazione", "Categoria": "Frutta",
            "Alimento": "Fragole", "Quantità_Mario": "50g", "Quantità_Mariantonietta": "50g"
        })
        
        # SPUNTINO METÀ MATTINA
        if giorno in giorni_allenamento:
            # Giorni di allenamento
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Spuntino", "Categoria": "Cereali",
                "Alimento": "Pane", "Quantità_Mario": "40g", "Quantità_Mariantonietta": "30g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Spuntino", "Categoria": "Grassi",
                "Alimento": "Burro d'arachidi", "Quantità_Mario": "20g", "Quantità_Mariantonietta": "15g"
            })
        else:
            # Giorni normali
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Spuntino", "Categoria": "Grassi",
                "Alimento": "Olive verdi", "Quantità_Mario": "80g", "Quantità_Mariantonietta": "60g"
            })
        
        # PRANZO
        if giorno in giorni_allenamento:
            # Giorni di allenamento
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Pranzo", "Categoria": "Cereali",
                "Alimento": "Pasta integrale", "Quantità_Mario": "90g", "Quantità_Mariantonietta": "70g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Pranzo", "Categoria": "Proteine",
                "Alimento": "Pesce (merluzzo)", "Quantità_Mario": "150g", "Quantità_Mariantonietta": "120g"
            })
        else:
            # Giorni normali
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Pranzo", "Categoria": "Cereali",
                "Alimento": "Pasta integrale", "Quantità_Mario": "90g", "Quantità_Mariantonietta": "70g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Pranzo", "Categoria": "Proteine",
                "Alimento": "Carne magra (pollo)", "Quantità_Mario": "120g", "Quantità_Mariantonietta": "100g"
            })
        
        # Comune per tutti i pranzi
        piano_pasti.append({
            "Giorno": giorno, "Pasto": "Pranzo", "Categoria": "Verdura",
            "Alimento": "Verdure miste", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"
        })
        piano_pasti.append({
            "Giorno": giorno, "Pasto": "Pranzo", "Categoria": "Grassi",
            "Alimento": "Olio EVO", "Quantità_Mario": "10g", "Quantità_Mariantonietta": "10g"
        })
        
        # MERENDA POMERIGGIO
        if giorno in giorni_allenamento:
            # Giorni di allenamento (1.5-2h prima dell'allenamento)
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Merenda", "Categoria": "Cereali",
                "Alimento": "Panino", "Quantità_Mario": "50g", "Quantità_Mariantonietta": "40g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Merenda", "Categoria": "Proteine",
                "Alimento": "Affettato magro", "Quantità_Mario": "40g", "Quantità_Mariantonietta": "30g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Merenda", "Categoria": "Frutta",
                "Alimento": "Banana (10 min prima)", "Quantità_Mario": "1 media", "Quantità_Mariantonietta": "1 piccola"
            })
        else:
            # Giorni normali
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Merenda", "Categoria": "Proteine",
                "Alimento": "Yogurt greco", "Quantità_Mario": "150g", "Quantità_Mariantonietta": "125g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Merenda", "Categoria": "Grassi",
                "Alimento": "Burro d'arachidi", "Quantità_Mario": "20g", "Quantità_Mariantonietta": "15g"
            })
        
        # CENA - seguendo la tabella di Mariantonietta e facendo coincidere gli alimenti
        if giorno == "Lunedì":
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Cereali",
                "Alimento": "Pane tostato/Patate", "Quantità_Mario": "70g/200g", "Quantità_Mariantonietta": "40g/80g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Proteine",
                "Alimento": "Carne magra (tacchino)", "Quantità_Mario": "150g", "Quantità_Mariantonietta": "180g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Verdura",
                "Alimento": "Verdure cotte-crude", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"
            })
        elif giorno == "Martedì":
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Cereali",
                "Alimento": "Pane/Pangrattato", "Quantità_Mario": "70g", "Quantità_Mariantonietta": "40g/4 cucchiai"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Proteine",
                "Alimento": "Pesce magro", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Verdura",
                "Alimento": "Verdura cotta-cruda", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"
            })
        elif giorno == "Mercoledì":
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Proteine",
                "Alimento": "Carne magra", "Quantità_Mario": "150g", "Quantità_Mariantonietta": "150g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Verdura",
                "Alimento": "Insalata valeriana e finocchi", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"
            })
        elif giorno == "Giovedì":
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Proteine",
                "Alimento": "Affettato magro", "Quantità_Mario": "120g", "Quantità_Mariantonietta": "120g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Verdura",
                "Alimento": "Verdura cotta-cruda", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"
            })
        elif giorno == "Venerdì":
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Cereali",
                "Alimento": "Pane tostato/Patate", "Quantità_Mario": "70g/200g", "Quantità_Mariantonietta": "40g/80g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Proteine",
                "Alimento": "Carne magra", "Quantità_Mario": "150g", "Quantità_Mariantonietta": "180g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Verdura",
                "Alimento": "Verdure cotte-crude", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"
            })
        elif giorno == "Sabato":
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Proteine",
                "Alimento": "Carne magra o Pesce magro", "Quantità_Mario": "150g/200g", "Quantità_Mariantonietta": "150g/200g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Verdura",
                "Alimento": "Verdura cotta", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Note",
                "Alimento": "Dopo 2 settimane: CENA LIBERA", "Quantità_Mario": "", "Quantità_Mariantonietta": ""
            })
        else:  # Domenica
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Proteine",
                "Alimento": "Carne magra o Pesce magro", "Quantità_Mario": "150g/200g", "Quantità_Mariantonietta": "150g/200g"
            })
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Verdura",
                "Alimento": "Verdura cotta", "Quantità_Mario": "200g", "Quantità_Mariantonietta": "200g"
            })
        
        # Olio per tutte le cene
        piano_pasti.append({
            "Giorno": giorno, "Pasto": "Cena", "Categoria": "Grassi",
            "Alimento": "Olio EVO", "Quantità_Mario": "10g", "Quantità_Mariantonietta": "10g"
        })
        
        # Condimento per alcune cene
        if giorno in ["Lunedì", "Venerdì"]:
            piano_pasti.append({
                "Giorno": giorno, "Pasto": "Cena", "Categoria": "Condimento",
                "Alimento": "Origano e/o spezie", "Quantità_Mario": "q.b.", "Quantità_Mariantonietta": "q.b."
            })
    
    # Crea il DataFrame
    nuovo_df = pd.DataFrame(piano_pasti)
    return nuovo_df

# Inizializza le statistiche nutrizionali (esempio)
categorie_nutrizionali = {
    "Cereali": {"calorie": 120, "proteine": 3, "carboidrati": 25, "grassi": 1},
    "Proteine": {"calorie": 150, "proteine": 20, "carboidrati": 2, "grassi": 8},
    "Frutta": {"calorie": 80, "proteine": 1, "carboidrati": 20, "grassi": 0},
    "Verdura": {"calorie": 40, "proteine": 2, "carboidrati": 8, "grassi": 0},
    "Grassi": {"calorie": 90, "proteine": 0, "carboidrati": 0, "grassi": 10},
    "Cereali/Grassi": {"calorie": 200, "proteine": 5, "carboidrati": 20, "grassi": 12},
    "Altro": {"calorie": 100, "proteine": 5, "carboidrati": 15, "grassi": 5},
}

# Funzione per calcolare statistiche nutrizionali
def calcola_statistiche(df_day, persona):
    stats = {"calorie": 0, "proteine": 0, "carboidrati": 0, "grassi": 0}
    
    for _, row in df_day.iterrows():
        categoria = row["Categoria"]
        quantita = row[f"Quantità_{persona}"]
        
        # Calcola un fattore di scala basato sulla quantità (semplificato)
        fattore = 1.0
        if isinstance(quantita, str) and "g" in quantita:
            try:
                grammi = float(quantita.replace("g", ""))
                if categoria in ["Cereali", "Proteine", "Frutta", "Verdura", "Grassi"]:
                    fattore = grammi / 100.0
            except:
                pass # Keep as pass to avoid errors on non-gram values like "q.b."
        
        # Aggiungi i valori nutrizionali
        if categoria in categorie_nutrizionali:
            for nutriente in stats:
                stats[nutriente] += categorie_nutrizionali[categoria][nutriente] * fattore
    
    return stats

# Carica dati esistenti
df = carica_dati()

# Visualizza lista della spesa e ricette
with st.expander("Lista della Spesa"):
    lista_spesa = genera_lista_spesa(df)
    st.dataframe(lista_spesa)

with st.expander("Ricette per Pranzo e Cena"):
    ricette = visualizza_ricette(df)
    for giorno in ricette['Giorno'].unique():
        st.subheader(giorno)
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Pranzo:**")
            st.dataframe(ricette[(ricette['Giorno'] == giorno) & (ricette['Pasto'] == 'Pranzo')])
        with col2:
            st.write("**Cena:**")
            st.dataframe(ricette[(ricette['Giorno'] == giorno) & (ricette['Pasto'] == 'Cena')])

with st.expander("Ricette di Verdure e Contorni", expanded=True):
    ricette_verdure = visualizza_ricette_verdure()
    for nome_ricetta, dettagli in ricette_verdure.items():
        st.subheader(nome_ricetta)
        st.write("**Ingredienti:**")
        for ingrediente in dettagli['ingredienti']:
            st.write(f"- {ingrediente}")
        st.write("**Preparazione:**")
        st.write(dettagli['preparazione'])
        st.markdown("---")

with st.expander("Ricette per Pranzo e Cena", expanded=True):
    ricette_pasti = visualizza_ricette_pasti()
    
    st.header("Ricette per il Pranzo")
    for nome_ricetta, dettagli in ricette_pasti['Pranzo'].items():
        st.subheader(nome_ricetta)
        st.write("**Ingredienti:**")
        for ingrediente in dettagli['ingredienti']:
            st.write(f"- {ingrediente}")
        st.write("**Preparazione:**")
        st.write(dettagli['preparazione'])
        st.markdown("---")
    
    st.header("Ricette per la Cena")
    for nome_ricetta, dettagli in ricette_pasti['Cena'].items():
        st.subheader(nome_ricetta)
        st.write("**Ingredienti:**")
        for ingrediente in dettagli['ingredienti']:
            st.write(f"- {ingrediente}")
        st.write("**Preparazione:**")
        st.write(dettagli['preparazione'])
        st.markdown("---")

# Crea tabs per diverse sezioni
tab1, tab2, tab3, tab4 = st.tabs(["Piano Pasti", "Statistiche Nutrizionali", "Gestione Dati", "Info Dieta"])

with tab1:
    st.title("Piano Pasti Settimanale")

    # Sidebar per filtrare e aggiungere pasti
    with st.sidebar:
        st.header("Filtri e Operazioni")
        
        # Filtra per giorno
        giorni_options = ["Tutti"] + sorted(df["Giorno"].unique().tolist()) if not df.empty else ["Tutti"]
        giorno_selezionato = st.selectbox("Seleziona giorno", giorni_options)
        
        st.markdown("---")
        
        # Aggiungi nuovo pasto
        with st.expander("Aggiungi Nuovo Pasto", expanded=False):
            giorni_settimana = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
            nuovo_giorno = st.selectbox("Giorno", giorni_settimana, key="new_day")
            
            pasti_options = ["Colazione", "Spuntino", "Pranzo", "Merenda", "Cena"]
            nuovo_pasto = st.selectbox("Pasto", pasti_options, key="new_meal")
            
            categorie_options = ["Cereali", "Proteine", "Frutta", "Verdura", "Grassi", "Cereali/Grassi", "Altro"]
            nuova_categoria = st.selectbox("Categoria", categorie_options, key="new_category")
            
            nuovo_alimento = st.text_input("Alimento", key="new_food")
            nuova_quantita_mario = st.text_input("Quantità Mario", key="new_qty_mario")
            nuova_quantita_mariantonietta = st.text_input("Quantità Mariantonietta", key="new_qty_mariantonietta")
            
            if st.button("Aggiungi Pasto", key="add_meal_button"):
                nuovo_pasto_dict = {
                    "Giorno": nuovo_giorno,
                    "Pasto": nuovo_pasto,
                    "Categoria": nuova_categoria,
                    "Alimento": nuovo_alimento,
                    "Quantità_Mario": nuova_quantita_mario,
                    "Quantità_Mariantonietta": nuova_quantita_mariantonietta
                }
                df = pd.concat([df, pd.DataFrame([nuovo_pasto_dict])], ignore_index=True)
                salva_dati(df)
                st.experimental_rerun()

    # Filtra il dataframe in base al giorno selezionato
    if not df.empty and giorno_selezionato != "Tutti":
        df_filtrato = df[df["Giorno"] == giorno_selezionato]
    else:
        df_filtrato = df

    # Mostra il piano pasti per ogni giorno della settimana
    giorni_settimana_display = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    if giorno_selezionato != "Tutti":
        giorni_da_mostrare = [giorno_selezionato]
    else:
        giorni_da_mostrare = [g for g in giorni_settimana_display if not df.empty and g in df["Giorno"].unique()]

    for giorno_iter in giorni_da_mostrare: # Renamed to avoid conflict
        st.header(giorno_iter)
        df_giorno = df_filtrato[df_filtrato["Giorno"] == giorno_iter]
        
        # Verifica se è giorno di allenamento
        if giorno_iter in ["Martedì", "Giovedì", "Sabato"]:
            st.markdown("**🏃‍♂️ Giorno di allenamento calcetto**")
        
        # Organizza per pasto
        for pasto_iter in ["Colazione", "Spuntino", "Pranzo", "Merenda", "Cena"]: # Renamed to avoid conflict
            df_pasto = df_giorno[df_giorno["Pasto"] == pasto_iter]
            if not df_pasto.empty:
                with st.expander(f"{pasto_iter}", expanded=True):
                    # Crea colonne per le tabelle
                    cols = st.columns([2, 1, 1, 1])
                    cols[0].write("**Alimento**")
                    cols[1].write("**Categoria**")
                    cols[2].write("**Mario**")
                    cols[3].write("**Mariantonietta**")
                    
                    for _, row in df_pasto.iterrows():
                        cols_data = st.columns([2, 1, 1, 1]) # Renamed to avoid conflict
                        cols_data[0].write(row["Alimento"])
                        cols_data[1].write(row["Categoria"])
                        cols_data[2].write(row["Quantità_Mario"])
                        cols_data[3].write(row["Quantità_Mariantonietta"])

with tab2:
    st.title("Statistiche Nutrizionali")
    
    # Seleziona giorno e persona per le statistiche
    col_stats1, col_stats2 = st.columns(2) # Renamed to avoid conflict
    
    with col_stats1:
        giorno_stats_options = sorted(df["Giorno"].unique().tolist()) if not df.empty else []
        giorno_stats = st.selectbox("Seleziona giorno per statistiche", 
                                   giorno_stats_options, key="stats_day_select")
    
    with col_stats2:
        persona_stats = st.radio("Seleziona persona", ["Mario", "Mariantonietta"], key="stats_person_select") # Renamed
    
    # Filtra per il giorno selezionato
    if giorno_stats: # Check if a day is selected
        df_day_stats = df[df["Giorno"] == giorno_stats] # Renamed
        
        if not df_day_stats.empty:
            # Calcola statistiche
            stats = calcola_statistiche(df_day_stats, persona_stats)
            
            # Mostra statistiche
            st.subheader(f"Valori nutrizionali approssimativi per {persona_stats} - {giorno_stats}")
            
            col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4) # Renamed
            col_metric1.metric("Calorie", f"{int(stats['calorie'])} kcal")
            col_metric2.metric("Proteine", f"{int(stats['proteine'])} g")
            col_metric3.metric("Carboidrati", f"{int(stats['carboidrati'])} g")
            col_metric4.metric("Grassi", f"{int(stats['grassi'])} g")
            
            # Crea un grafico a torta per i macronutrienti
            st.subheader("Distribuzione Macronutrienti")
            fig_macros, ax_macros = plt.subplots() # Renamed
            labels_macros = ['Proteine', 'Carboidrati', 'Grassi'] # Renamed
            values_macros = [stats['proteine'] * 4, stats['carboidrati'] * 4, stats['grassi'] * 9]  # Calorie per grammo
            ax_macros.pie(values_macros, labels=labels_macros, autopct='%1.1f%%')
            ax_macros.axis('equal')
            st.pyplot(fig_macros)
            
            # Crea un grafico per le calorie per pasto
            st.subheader("Calorie per Pasto")
            pasti_calorie = {}
            for pasto_calorie_iter in ["Colazione", "Spuntino", "Pranzo", "Merenda", "Cena"]: # Renamed
                df_pasto_calorie = df_day_stats[df_day_stats["Pasto"] == pasto_calorie_iter] # Renamed
                if not df_pasto_calorie.empty:
                    pasto_stats_calorie = calcola_statistiche(df_pasto_calorie, persona_stats) # Renamed
                    pasti_calorie[pasto_calorie_iter] = pasto_stats_calorie["calorie"]
            
            if pasti_calorie: # Check if dictionary is not empty
                pasti_df_calorie = pd.DataFrame({ # Renamed
                    'Pasto': list(pasti_calorie.keys()),
                    'Calorie': list(pasti_calorie.values())
                })
                
                chart_calories = alt.Chart(pasti_df_calorie).mark_bar().encode( # Renamed
                    x='Pasto',
                    y='Calorie',
                    color='Pasto'
                ).properties(
                    width=600
                )
                st.altair_chart(chart_calories)
            else:
                st.write("Nessun dato calorico per i pasti selezionati.")

        else:
            st.warning(f"Nessun dato disponibile per {giorno_stats}")
    else:
        st.info("Seleziona un giorno per visualizzare le statistiche.")


with tab3:
    st.title("Gestione Dati")
    
    col_gest1, col_gest2 = st.columns(2) # Renamed
    
    with col_gest1:
        st.subheader("Genera Piano per tutta la Settimana")
        st.markdown("""
        Questa funzione genera un piano alimentare settimanale completo per Mario e Mariantonietta,
        rispettando le indicazioni del nutrizionista e considerando i giorni di allenamento calcetto.
        """)
        
        if st.button("Genera Piano Settimanale Personalizzato", key="generate_plan_button"):
            nuovo_df_generated = genera_pasti_settimana() # Renamed
            df = nuovo_df_generated # Update main df
            salva_dati(df)
            st.success("Piano settimanale personalizzato generato con successo!")
            st.experimental_rerun()
    
    with col_gest2:
        st.subheader("Eliminazione Pasti")
        
        if st.checkbox("Mostra opzioni di eliminazione", key="show_delete_options_checkbox"):
            st.warning("Seleziona i pasti da eliminare:")
            delete_rows_indices = [] # Renamed
            
            for i_del, row_del in df.iterrows(): # Renamed iterators
                label_del = f"{row_del['Giorno']} - {row_del['Pasto']} - {row_del['Alimento']}" # Renamed
                if st.checkbox(label_del, key=f"del_row_{i_del}"):
                    delete_rows_indices.append(i_del)
            
            if delete_rows_indices and st.button("Elimina Selezionati", key="delete_selected_button"):
                df = df.drop(delete_rows_indices).reset_index(drop=True)
                salva_dati(df)
                st.experimental_rerun()
    
    st.markdown("---")
    
    st.subheader("Esporta Dati")
    if st.button("Esporta Excel", key="export_excel_button"):
        salva_dati(df)
        st.success(f"File Excel salvato come: pasti_settimanali.xlsx")
        
    # Mostra anteprima dati
    st.subheader("Anteprima Dati")
    st.dataframe(df)

with tab4:
    st.title("Informazioni sulla Dieta")
    
    # Aggiungo un selettore per scegliere la persona
    persona_dieta_select = st.radio("Seleziona persona", ["Informazioni Generali", "Mario", "Mariantonietta"], horizontal=True, key="diet_info_person_select") # Renamed
    
    if persona_dieta_select == "Informazioni Generali":
        st.header("Piano Alimentare Personalizzato")
        
        st.markdown("""
        ### Avvertenze generali
        
        - Il peso degli alimenti si riferisce a crudo e al netto degli scarti
        - Masticare con cura gli alimenti. Una buona e lenta masticazione consente di digerire e assimilare meglio gli alimenti
        - Non saltare i pasti
        - Aggiungere l'olio EVO a crudo a cottura ultimata
        - Non limitare l'uso del sale, alternarlo con diversi tipi: rosso, rosa, blu, affumicato
        - Utilizzare sale marino integrale, rosa dell'Himalaya o sale alle erbe
        - Preferire l'utilizzo di spezie secche e fresche (curcuma, cumino, zenzero, erbe aromatiche)
        - Evitare il consumo di aceto di vino e preferire quello di mele o succo di limone
        - Le grammature non devono essere intese alla lettera; possono variare leggermente
        
        ### Giorni di allenamento calcetto
        
        - **Martedì, Giovedì, Sabato**
        - In questi giorni è previsto uno spuntino specifico e una merenda pre-allenamento circa 1.5-2 ore prima
        
        ### Dieta anti-infiammatoria
        
        Questo piano alimentare si prefigge l'obiettivo di promuovere un'alimentazione personalizzata, normocalorica e mirata a favorire il miglioramento del profilo lipidico ematico, ed è basata sul potere antinfiammatorio degli alimenti.
        """)
        
        st.header("Modalità di cottura consigliate")
        
        st.markdown("""
        - **Verdure**: in padella, al forno o al vapore e ripassate in padella
        - **Carne**: al vapore, alla griglia, al forno, al cartoccio o a bagnomaria
        - **Riso**: lessato al dente e ripassato sotto l'acqua corrente, poi mantecato in padella
        - **Pasta**: cottura al dente, ripassata poi in padella con olio caldo
        - **Pane**: se fresco, tostarlo
        - **Patate**: bollite, lasciate raffreddare e conservate in frigo per abbassare il carico glicemico
        - **Uova**: alla coque, occhio di bue o frittatina (no sode)
        
        ### Integrazione consigliata
        
        - Colex Mu: 1 compressa al giorno, la sera dopo cena per 3 mesi
        """)
        
        st.header("Alimenti da ridurre")
        
        col_reduce1, col_reduce2 = st.columns(2) # Renamed
        
        with col_reduce1:
            st.markdown("""
            ### Da limitare
            
            - Prodotti confezionati ricchi di sale e zuccheri
            - Crackers, fette biscottate, cereali da prima colazione
            - Yogurt con frutta e confetture con zuccheri
            - Creme spalmabili tipo nutella e dolciumi vari
            - Ogni forma di alcool
            - Prodotti industriali per celiaci
            - Acidi grassi saturi animali (latte, formaggi, burro normale, salumi)
            """)
        
        with col_reduce2:
            st.markdown("""
            ### Da preferire
            
            - Tisane, camomilla senza zucchero (boldo, betulla, ortica, tarassaco)
            - Verdura cotta in olio di cocco/EVO ripassata in padella
            - Vellutate di verdure
            - Pesce fresco (5-6 volte a settimana)
            - Verdure e frutta biologiche a km 0
            - Carne da macelleria locale (non allevamenti intensivi)
            - Pesci piccoli, possibilmente pescati
            - Uova di galline locali
            """)
    
    elif persona_dieta_select == "Mario":
        st.header("Piano Alimentare Personalizzato di Mario")
        
        st.markdown("""
        ### Dieta anti-infiammatoria per Mario
        
        Questo piano alimentare si prefigge l'obiettivo di promuovere un'alimentazione personalizzata, normocalorica e mirata a favorire il miglioramento del profilo lipidico ematico, ed è basata sul potere antinfiammatorio degli alimenti.
        
        ### Giorni di allenamento calcetto (Martedì, Giovedì, Sabato)
        
        #### Colazione
        - Yogurt greco 0% bianco o Fage trublend o Hipro Danone (150g)
        - 40g di fiocchi di avena o fiocchi di riso
        - Un frutto fresco (150g)
        - 15g di burro d'arachidi o frutta secca
        
        #### Spuntino metà mattina
        - 40g di pane + 20g di burro d'arachidi
        
        #### Pranzo
        - Pasta integrale o cereali (90g) o gnocchi di patate (130g) o pane integrale (110g)
        - 100g di carne magra o pesce magro/semigrasso (150g) o tonno in vetro (90g)
        - Contorno di verdure crude e/o cotte (150-200g)
        - Un cucchiaio di olio extra vergine di oliva (10g)
        
        #### Merenda (1.5-2h prima dell'allenamento)
        - Un panino (50g) + 40g di affettato magro o 50g di tonno al naturale
        - + 10 min prima: 20g di frutta disidratata o una banana
        
        #### Cena
        - Cereali (50g) o patate (200g) o pane integrale (70g)
        - 150g di carne magra o pesce magro/semigrasso (200g)
        - Contorno di verdure crude e/o cotte (150-200g)
        - Un cucchiaio di olio extra vergine di oliva (10g)
        """)
        
        st.markdown("""
        ### Giorni normali (Lunedì, Mercoledì, Venerdì, Domenica)
        
        #### Colazione
        - Uguale ai giorni di allenamento
        
        #### Spuntino metà mattina
        - 80g di olive verdi o 20g di frutta secca o 20g di cocco disidratato
        
        #### Pranzo
        - Pasta integrale o cereali (90g) o pane integrale (110g) o gnocchi di patate (130g)
        - 120g di carne magra o pesce magro/semigrasso (180g)
        - Contorno di verdure crude e/o cotte (150-200g)
        - Un cucchiaio di olio extra vergine di oliva (10g)
        
        #### Merenda pomeriggio
        - Yogurt greco bianco 0% o trublend alla frutta (150g) + 20g di burro d'arachidi
        
        #### Cena
        - Cereali (50g) o patate (200g) o pane integrale (70g)
        - 150g di carne magra o pesce magro/semigrasso (200g)
        - Contorno di verdure crude e/o cotte (150-200g)
        - Un cucchiaio di olio extra vergine di oliva (10g)
        """)
        
        st.markdown("""
        ### Integrazione consigliata
        - Colex Mu: 1 compressa al giorno, la sera dopo cena per 3 mesi
        """)
        
    else:  # Mariantonietta
        st.header("Piano Alimentare Personalizzato di Mariantonietta")
        
        st.markdown("""
        ### Dieta anti-infiammatoria per Mariantonietta
        
        Questo piano alimentare è personalizzato per Mariantonietta, con porzioni adattate e seguendo uno schema settimanale preciso.
        """)
        
        st.subheader("Piano settimanale per Mariantonietta")
        
        tab_colazione_ma, tab_spuntino_ma, tab_pranzo_ma, tab_merenda_ma, tab_cena_ma = st.tabs(["Colazione", "Spuntino", "Pranzo", "Merenda", "Cena"]) # Renamed
        
        with tab_colazione_ma:
            st.markdown("""
            ### COLAZIONE
            
            **Lunedì, Martedì, Venerdì**:
            - Un vasetto di yogurt greco bianco o Fage Trublend + frutto fresco o una decina di fragole
            - 40g di bresaola + 2 gallette di riso
            
            **Mercoledì, Giovedì**:
            - 20g di frutta secca o 80g di olive verdi denocciolate o 20g di cocco disidratato (senza zucchero in etichetta)
            
            **Sabato, Domenica**:
            - 40g di olive verdi denocciolate o 10g di cocco disidratato
            """)
        
        with tab_spuntino_ma:
            st.markdown("""
            ### SPUNTINO MATTINA
            
            **Lunedì**:
            - 50g di pasta o riso basmati o 90g di gnocchi di patate
            - 120g di ricotta-fiocchi di latte-feta-formaggio fresco o 2 uova
            - Passato di verdure
            - 10g (1 cucchiaio) di olio EVO
            
            **Martedì**:
            - 50g di riso venere-quinoa-miglio o 200g di patate (ben sbucciate)
            - 80g di salmone affumicato-sgombro al naturale o 150g di gamberetti
            - Verdura cotta
            - 10g (1 cucchiaio) di olio EVO
            
            **Mercoledì**:
            - 40g di pane o 2 gallette di riso
            - 2 uova + 40g di affettato magro
            - Verdure cotte/crude
            - 10g (1 cucchiaio) di olio EVO
            
            **Giovedì**:
            - 80g di patate o 40g di pane
            - 200g di seppie-calamari-gamberi o 250g di polpo OPPURE 150g di tonno-salmone-pesce spada-sgombro fresco
            - Verdure cotte
            - 10g (1 cucchiaio) di olio EVO
            
            **Venerdì**:
            - 50g di cous cous-farro-orzo
            - 2 uova
            - Passato di verdure
            - 10g (1 cucchiaio) di olio EVO
            
            **Sabato**:
            - 50g di riso integrale-basmati-quinoa-miglio o 200g di patate (ben sbucciate)
            - 100g di carne magra o 150g di pesce magro
            - 10g (1 cucchiaio) di olio EVO
            
            **Domenica**:
            - 50g di riso integrale-basmati-quinoa-miglio o 200g di patate (ben sbucciate)
            - 100g di carne magra o 150g di pesce magro
            - 10g (1 cucchiaio) di olio EVO
            """)
        
        with tab_pranzo_ma:
            st.markdown("""
            ### PRANZO
            
            **Lunedì, Martedì, Venerdì**:
            - 2 gallette di riso ricoperte da cioccolato fondente o 2 gallette di riso + 10g di frutta secca o burro d'arachidi o crema di frutta secca 100%
            - o 30g di taralli pugliesi
            - o crostini di pane (40g) con olio (un cucchiaino - 5g) e origano
            
            **Mercoledì, Giovedì**:
            - 80g di olive verdi denocciolate o 20g di cocco disidratato (senza zucchero in etichetta)
            
            **Sabato, Domenica**:
            - 40g di olive verdi denocciolate o 10g di cocco disidratato
            """)
        
        with tab_merenda_ma:
            st.markdown("""
            ### MERENDA
            
            - 2 gallette di riso ricoperte da cioccolato fondente o 2 gallette di riso + 10g di frutta secca
            - o 30g di taralli pugliesi
            - o crostini di pane (40g) con olio (un cucchiaino - 5g) e origano
            """)
        
        with tab_cena_ma:
            st.markdown("""
            ### CENA
            
            **Lunedì**:
            - 40g di pane tostato o 80g di patate
            - 180g di carne magra
            - Verdure cotte-crude
            - 10g (1 cucchiaio) di olio EVO
            
            **Martedì**:
            - 40g di pane da tostare o 4 cucchiai di pangrattato
            - 200g di pesce magro
            - Verdura cotta-cruda
            - 10g (1 cucchiaio) di olio EVO
            
            **Mercoledì**:
            - 150g di carne magra
            - Insalata di valeriana e finocchi
            - 10g (1 cucchiaio) di olio EVO
            
            **Giovedì**:
            - 120g di affettato magro
            - Verdura cotta-cruda
            - 10g (1 cucchiaio) di olio EVO
            
            **Venerdì**:
            - 40g di pane tostato o 80g di patate
            - 180g di carne magra
            - Verdure cotte-crude
            - 10g (1 cucchiaio) di olio EVO
            
            **Sabato**:
            - 150g di carne magra o 200g di pesce magro
            - Verdura cotta
            - 10g (1 cucchiaio) di olio EVO
            - DOPO 2 SETTIMANE: CENA LIBERA
            
            **Domenica**:
            - 150g di carne magra o 200g di pesce magro
            - Verdura cotta
            - 10g (1 cucchiaio) di olio EVO
            """)
        
        st.markdown("""
        ### Note importanti
        - Prestare attenzione alle quantità di olio e frutta secca
        - Associare sempre la fonte dei grassi ai carboidrati (frutta secca o olive)
        - Non saltare gli spuntini
        """)
 
        st.markdown("""
        ### Integrazione consigliata
        - Colex Mu: 1 compressa al giorno, la sera dopo cena per 3 mesi
        """)
