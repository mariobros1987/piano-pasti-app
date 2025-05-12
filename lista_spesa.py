import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

# Configurazione pagina
st.set_page_config(page_title="Lista della Spesa", layout="wide")

# Stile CSS personalizzato
st.markdown("""
<style>
.lista-spesa-container {
    background-color: #f9f9f9;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.lista-spesa-header {
    font-size: 1.8rem;
    font-weight: bold;
    color: #2e7d32;
    margin-bottom: 20px;
    border-bottom: 2px solid #2e7d32;
    padding-bottom: 10px;
}
.categoria-header {
    font-size: 1.4rem;
    font-weight: 600;
    color: #1976d2;
    margin: 15px 0 10px 0;
}
.item-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #e0e0e0;
}
.item-name {
    font-weight: 500;
    color: #333;
}
.item-quantity {
    color: #555;
    font-weight: 500;
}
.item-check {
    margin-right: 10px;
}
.print-button {
    background-color: #4caf50;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    margin-top: 20px;
    transition: background-color 0.3s;
}
.print-button:hover {
    background-color: #388e3c;
}
.stats-container {
    background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.stats-header {
    font-size: 1.5rem;
    font-weight: bold;
    color: #2e7d32;
    margin-bottom: 15px;
    border-bottom: 2px solid #2e7d32;
    padding-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Funzione per caricare i dati delle ricette selezionate
def carica_ricette_selezionate():
    # Se esiste un file con le ricette selezionate, caricalo
    if os.path.exists("ricette_selezionate.csv"):
        return pd.read_csv("ricette_selezionate.csv")
    else:
        # Altrimenti, crea un DataFrame vuoto
        return pd.DataFrame(columns=["giorno", "tipo_pasto", "nome", "persona"])

# Funzione per generare la lista della spesa
def genera_lista_spesa(ricette_df, persona):
    # Dizionario per la lista della spesa
    lista_spesa = {}
    
    # Categorie di alimenti
    categorie = {
        "Proteine": ["pollo", "tacchino", "merluzzo", "tonno", "salmone", "pesce", "uovo", "albume", "yogurt greco", "affettato magro", "bresaola", "prosciutto"],
        "Carboidrati": ["pasta", "riso", "pane", "avena", "fiocchi", "patate", "legumi", "farina"],
        "Verdure": ["verdure", "insalata", "pomodor", "zucchine", "melanzane", "carote", "finocchi", "broccoli", "spinaci", "rucola"],
        "Frutta": ["frutta", "banana", "mela", "fragole", "frutti di bosco", "agrumi", "limone"],
        "Grassi": ["olio", "evo", "olive", "avocado", "frutta secca", "burro d'arachidi"],
        "Condimenti": ["sale", "pepe", "spezie", "erbe", "aglio", "cipolla", "origano", "rosmarino", "basilico", "prezzemolo", "curcuma", "zenzero"]
    }
    
    # Inizializza la lista della spesa con categorie vuote
    for categoria in categorie:
        lista_spesa[categoria] = {}
    
    # Aggiungi una categoria per gli alimenti non classificati
    lista_spesa["Altro"] = {}
    
    # Simula gli ingredienti delle ricette (in un'app reale, questi verrebbero dalle ricette selezionate)
    ingredienti_ricette = {
        "Yogurt greco con avena e frutta": {
            "Mario": ["Yogurt greco 0% (150g)", "Fiocchi d'avena (40g)", "Frutta fresca (150g)", "Burro d'arachidi (15g)"],
            "Mariantonietta": ["Yogurt greco 0% (125g)", "Fiocchi d'avena (30g)", "Frutta fresca (150g)", "Burro d'arachidi (10g)"]
        },
        "Pancakes proteici": {
            "Mario": ["Albume (100ml)", "Farina d'avena (40g)", "Yogurt greco 0% (80g)", "Marmellata a ridotto tenore di zuccheri (20g)", "Burro d'arachidi (15g)"],
            "Mariantonietta": ["Albume (80ml)", "Farina d'avena (30g)", "Yogurt greco 0% (60g)", "Marmellata a ridotto tenore di zuccheri (15g)", "Burro d'arachidi (10g)"]
        },
        "Pane tostato con affettato e avocado": {
            "Mario": ["Pane di segale/integrale (80g)", "Bresaola o prosciutto crudo sgrassato (40g)", "Avocado (40g)", "Olio EVO (10g)"],
            "Mariantonietta": ["Pane di segale/integrale (60g)", "Bresaola o prosciutto crudo sgrassato (30g)", "Avocado (30g)", "Olio EVO (5g)"]
        },
        "Pasta integrale con merluzzo e verdure": {
            "Mario": ["Pasta integrale (90g)", "Merluzzo (150g)", "Verdure miste (200g)", "Olio EVO (10g)", "Aglio", "Prezzemolo"],
            "Mariantonietta": ["Pasta integrale (70g)", "Merluzzo (120g)", "Verdure miste (200g)", "Olio EVO (10g)", "Aglio", "Prezzemolo"]
        },
        "Riso integrale con pollo e verdure": {
            "Mario": ["Riso integrale (90g)", "Petto di pollo (120g)", "Verdure miste (200g)", "Olio EVO (10g)", "Curcuma", "Zenzero"],
            "Mariantonietta": ["Riso integrale (70g)", "Petto di pollo (100g)", "Verdure miste (200g)", "Olio EVO (10g)", "Curcuma", "Zenzero"]
        },
        "Insalata di legumi con tonno": {
            "Mario": ["Legumi misti (120g secchi)", "Tonno al naturale (90g)", "Verdure miste (200g)", "Olio EVO (10g)", "Limone", "Erbe aromatiche"],
            "Mariantonietta": ["Legumi misti (100g secchi)", "Tonno al naturale (80g)", "Verdure miste (200g)", "Olio EVO (10g)", "Limone", "Erbe aromatiche"]
        },
        "Tacchino con patate al forno": {
            "Mario": ["Fettine di tacchino (150g)", "Patate (200g)", "Verdure cotte-crude (200g)", "Olio EVO (10g)", "Rosmarino", "Origano"],
            "Mariantonietta": ["Fettine di tacchino (180g)", "Patate (80g)", "Verdure cotte-crude (200g)", "Olio EVO (10g)", "Rosmarino", "Origano"]
        },
        "Pesce al cartoccio con verdure": {
            "Mario": ["Pesce magro (200g)", "Verdure miste (200g)", "Olio EVO (10g)", "Limone", "Prezzemolo", "Timo"],
            "Mariantonietta": ["Pesce magro (200g)", "Verdure miste (200g)", "Olio EVO (10g)", "Limone", "Prezzemolo", "Timo"]
        },
        "Frittata di albumi con verdure": {
            "Mario": ["Albumi (200g)", "Uovo intero (1)", "Verdure miste (200g)", "Olio EVO (10g)", "Erbe aromatiche"],
            "Mariantonietta": ["Albumi (150g)", "Uovo intero (1)", "Verdure miste (200g)", "Olio EVO (10g)", "Erbe aromatiche"]
        },
        "Yogurt greco con frutta secca": {
            "Mario": ["Yogurt greco 0% (150g)", "Frutta secca mista (15g)"],
            "Mariantonietta": ["Yogurt greco 0% (125g)", "Frutta secca mista (10g)"]
        },
        "Panino pre-allenamento": {
            "Mario": ["Pane (50g)", "Affettato magro (40g)", "Frutta disidratata o banana (20g)"],
            "Mariantonietta": ["Pane (40g)", "Affettato magro (30g)", "Frutta disidratata o banana (15g)"]
        },
        "Olive verdi e frutta secca": {
            "Mario": ["Olive verdi denocciolate (80g)", "Frutta secca (20g)"],
            "Mariantonietta": ["Olive verdi denocciolate (60g)", "Frutta secca (15g)"]
        }
    }
    
    # Per ogni ricetta selezionata
    for _, ricetta in ricette_df.iterrows():
        nome_ricetta = ricetta["nome"]
        
        # Se la ricetta è nel nostro dizionario di ingredienti
        if nome_ricetta in ingredienti_ricette:
            # Prendi gli ingredienti per la persona selezionata
            ingredienti = ingredienti_ricette[nome_ricetta][persona]
            
            # Aggiungi ogni ingrediente alla lista della spesa
            for ingrediente in ingredienti:
                # Estrai il nome dell'ingrediente (rimuovendo la quantità tra parentesi)
                if "(" in ingrediente:
                    nome_ingrediente = ingrediente.split(" (")[0].strip()
                    quantita = ingrediente.split("(")[1].split(")")[0]
                else:
                    nome_ingrediente = ingrediente.strip()
                    quantita = "q.b."
                
                # Determina la categoria dell'ingrediente
                categoria_trovata = False
                for categoria, keywords in categorie.items():
                    if any(keyword.lower() in nome_ingrediente.lower() for keyword in keywords):
                        if nome_ingrediente in lista_spesa[categoria]:
                            # Se l'ingrediente è già nella lista, incrementa la quantità
                            lista_spesa[categoria][nome_ingrediente] = {
                                "quantita": lista_spesa[categoria][nome_ingrediente]["quantita"],
                                "conteggio": lista_spesa[categoria][nome_ingrediente]["conteggio"] + 1
                            }
                        else:
                            # Altrimenti, aggiungi l'ingrediente alla lista
                            lista_spesa[categoria][nome_ingrediente] = {
                                "quantita": quantita,
                                "conteggio": 1
                            }
                        categoria_trovata = True
                        break
                
                # Se l'ingrediente non appartiene a nessuna categoria, mettilo in "Altro"
                if not categoria_trovata:
                    if nome_ingrediente in lista_spesa["Altro"]:
                        lista_spesa["Altro"][nome_ingrediente] = {
                            "quantita": lista_spesa["Altro"][nome_ingrediente]["quantita"],
                            "conteggio": lista_spesa["Altro"][nome_ingrediente]["conteggio"] + 1
                        }
                    else:
                        lista_spesa["Altro"][nome_ingrediente] = {
                            "quantita": quantita,
                            "conteggio": 1
                        }
    
    return lista_spesa

# Funzione per visualizzare la lista della spesa
def visualizza_lista_spesa(lista_spesa):
    html = """
    <div class="lista-spesa-container">
        <div class="lista-spesa-header">Lista della Spesa Settimanale</div>
    """
    
    # Per ogni categoria nella lista della spesa
    for categoria, ingredienti in lista_spesa.items():
        # Se ci sono ingredienti in questa categoria
        if ingredienti:
            html += f"""
            <div class="categoria-header">{categoria}</div>
            """
            
            # Per ogni ingrediente in questa categoria
            for nome_ingrediente, info in sorted(ingredienti.items()):
                quantita = info["quantita"]
                conteggio = info["conteggio"]
                
                # Se l'ingrediente appare più volte, mostra il conteggio
                if conteggio > 1:
                    html += f"""
                    <div class="item-row">
                        <div class="item-name">
                            <input type="checkbox" class="item-check"> {nome_ingrediente}
                        </div>
                        <div class="item-quantity">{quantita} (x{conteggio})</div>
                    </div>
                    """
                else:
                    html += f"""
                    <div class="item-row">
                        <div class="item-name">
                            <input type="checkbox" class="item-check"> {nome_ingrediente}
                        </div>
                        <div class="item-quantity">{quantita}</div>
                    </div>
                    """
    
    html += """
    <button class="print-button" onclick="window.print()">Stampa Lista della Spesa</button>
    </div>
    """
    
    return html

# Funzione per calcolare statistiche nutrizionali
def calcola_statistiche_nutrizionali(lista_spesa):
    # Valori nutrizionali approssimativi per 100g di alimento
    valori_nutrizionali = {
        "Proteine": {"calorie": 150, "proteine": 25, "carboidrati": 0, "grassi": 5},
        "Carboidrati": {"calorie": 350, "proteine": 10, "carboidrati": 70, "grassi": 2},
        "Verdure": {"calorie": 50, "proteine": 2, "carboidrati": 10, "grassi": 0},
        "Frutta": {"calorie": 80, "proteine": 1, "carboidrati": 20, "grassi": 0},
        "Grassi": {"calorie": 800, "proteine": 0, "carboidrati": 0, "grassi": 90},
    }
    
    # Inizializza le statistiche
    statistiche = {
        "calorie": 0,
        "proteine": 0,
        "carboidrati": 0,
        "grassi": 0,
        "distribuzione": {}
    }
    
    # Calcola il numero totale di ingredienti per categoria
    totale_ingredienti = 0
    for categoria, ingredienti in lista_spesa.items():
        if categoria in valori_nutrizionali:
            statistiche["distribuzione"][categoria] = len(ingredienti)
            totale_ingredienti += len(ingredienti)
    
    # Calcola la distribuzione percentuale
    for categoria in statistiche["distribuzione"]:
        if totale_ingredienti > 0:
            statistiche["distribuzione"][categoria] = (statistiche["distribuzione"][categoria] / totale_ingredienti) * 100
    
    # Calcola i valori nutrizionali approssimativi
    for categoria, ingredienti in lista_spesa.items():
        if categoria in valori_nutrizionali:
            for _, info in ingredienti.items():
                conteggio = info["conteggio"]
                statistiche["calorie"] += valori_nutrizionali[categoria]["calorie"] * conteggio / 7  # Media giornaliera
                statistiche["proteine"] += valori_nutrizionali[categoria]["proteine"] * conteggio / 7
                statistiche["carboidrati"] += valori_nutrizionali[categoria]["carboidrati"] * conteggio / 7
                statistiche["grassi"] += valori_nutrizionali[categoria]["grassi"] * conteggio / 7
    
    return statistiche

# Funzione per visualizzare le statistiche nutrizionali
def visualizza_statistiche(statistiche):
    # Crea un grafico a torta per la distribuzione degli alimenti
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Grafico a torta per la distribuzione degli alimenti
    labels = list(statistiche["distribuzione"].keys())
    sizes = list(statistiche["distribuzione"].values())
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
    
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    ax1.set_title('Distribuzione degli Alimenti')
    
    # Grafico a barre per i macronutrienti
    nutrienti = ['Proteine', 'Carboidrati', 'Grassi']
    valori = [statistiche["proteine"], statistiche["carboidrati"], statistiche["grassi"]]
    
    ax2.bar(nutrienti, valori, color=['#ff9999', '#66b3ff', '#ffcc99'])
    ax2.set_title('Macronutrienti Giornalieri (g)')
    ax2.set_ylabel('Grammi')
    
    plt.tight_layout()
    return fig

# Titolo principale
st.title("Lista della Spesa Settimanale")
st.markdown("Genera automaticamente la lista della spesa in base alle ricette selezionate")

# Carica le ricette selezionate
ricette_df = carica_ricette_selezionate()

# Seleziona persona
persona = st.selectbox("Seleziona persona", ["Mario", "Mariantonietta"])

# Genera la lista della spesa
lista_spesa = genera_lista_spesa(ricette_df, persona)

# Visualizza la lista della spesa
st.markdown(visualizza_lista_spesa(lista_spesa), unsafe_allow_html=True)

# Calcola e visualizza le statistiche nutrizionali
statistiche = calcola_statistiche_nutrizionali(lista_spesa)

st.markdown("""
<div class="stats-container">
    <div class="stats-header">Statistiche Nutrizionali</div>
</div>
""", unsafe_allow_html=True)

# Visualizza le calorie giornaliere
st.subheader(f"Calorie Giornaliere Stimate: {int(statistiche['calorie'])} kcal")

# Visualizza il grafico delle statistiche
fig = visualizza_statistiche(statistiche)
st.pyplot(fig)

# Mostra i macronutrienti in formato testuale
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Proteine", f"{int(statistiche['proteine'])}g", "25-30%")
with col2:
    st.metric("Carboidrati", f"{int(statistiche['carboidrati'])}g", "45-55%")
with col3:
    st.metric("Grassi", f"{int(statistiche['grassi'])}g", "20-30%")

# Aggiungi note sulla dieta
st.markdown("### Note sulla Dieta")
st.markdown("""
- Le calorie e i macronutrienti sono stime approssimative
- Adatta le porzioni in base alle tue esigenze specifiche
- Segui sempre le indicazioni del nutrizionista
- Bevi almeno 2 litri di acqua al giorno
- Limita il consumo di sale e zuccheri aggiunti
""")

# Sidebar con informazioni aggiuntive
st.sidebar.title("Opzioni")

# Aggiungi opzioni nella sidebar
st.sidebar.markdown("### Personalizzazione")

# Opzione per aggiungere ingredienti extra
st.sidebar.markdown("#### Aggiungi Ingredienti Extra")
ingrediente_extra = st.sidebar.text_input("Nome ingrediente")
quantita_extra = st.sidebar.text_input("Quantità")
categoria_extra = st.sidebar.selectbox("Categoria", list(lista_spesa.keys()))

if st.sidebar.button("Aggiungi alla Lista"):
    if ingrediente_extra and quantita_extra and categoria_extra:
        if ingrediente_extra in lista_spesa[categoria_extra]:
            lista_spesa[categoria_extra][ingrediente_extra]["conteggio"] += 1
        else:
            lista_spesa[categoria_extra][ingrediente_extra] = {
                "quantita": quantita_extra,
                "conteggio": 1
            }
        st.success(f"{ingrediente_extra} aggiunto alla lista della spesa!")
        st.experimental_rerun()

# Opzione per rimuovere ingredienti
st.sidebar.markdown("#### Rimuovi Ingredienti")
categorie_con_ingredienti = [cat for cat, ing in lista_spesa.items() if ing]
categoria_rimozione = st.sidebar.selectbox("Seleziona categoria", categorie_con_ingredienti, key="cat_remove")

if categoria_rimozione:
    ingredienti_categoria = list(lista_spesa[categoria_rimozione].keys())
    ingrediente_rimozione = st.sidebar.selectbox("Seleziona ingrediente da rimuovere", ingredienti_categoria)
    
    if st.sidebar.button("Rimuovi dalla Lista"):
        if ingrediente_rimozione in lista_spesa[categoria_rimozione]:
            del lista_spesa[categoria_rimozione][ingrediente_rimozione]
            st.success(f"{ingrediente_rimozione} rimosso dalla lista della spesa!")
            st.experimental_rerun()

# Aggiungi un pulsante per integrare con l'app principale
st.sidebar.markdown("---")
if st.sidebar.button("Torna all'App Principale"):
    st.switch_page("app.py")

# Aggiungi un pulsante per visualizzare le ricette personalizzate
if st.sidebar.button("Vai alle Ricette Personalizzate"):
    st.switch_page("ricette_personalizzate.py")