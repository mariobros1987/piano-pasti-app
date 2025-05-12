import streamlit as st
import pandas as pd
import random
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Configurazione pagina
st.set_page_config(page_title="Ricette Personalizzate", layout="wide")

# Stile CSS personalizzato per le card
st.markdown("""
<style>
.card {
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}
.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.card-mario {
    background: linear-gradient(135deg, #e0f7fa 0%, #80deea 100%);
    border-left: 5px solid #00acc1;
}
.card-mariantonietta {
    background: linear-gradient(135deg, #f3e5f5 0%, #ce93d8 100%);
    border-left: 5px solid #9c27b0;
}
.card-comune {
    background: linear-gradient(135deg, #e8f5e9 0%, #a5d6a7 100%);
    border-left: 5px solid #4caf50;
}
.card-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 15px;
    color: #333;
}
.card-subtitle {
    font-size: 1.2rem;
    font-weight: 500;
    margin-bottom: 10px;
    color: #555;
}
.card-text {
    font-size: 1rem;
    color: #666;
}
.card-tag {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    margin-right: 5px;
    margin-bottom: 5px;
    font-weight: 500;
}
.tag-proteina {
    background-color: #ffecb3;
    color: #ff6f00;
}
.tag-carboidrato {
    background-color: #e1f5fe;
    color: #0277bd;
}
.tag-verdura {
    background-color: #e8f5e9;
    color: #2e7d32;
}
.tag-grasso {
    background-color: #fce4ec;
    color: #c2185b;
}
.lista-spesa {
    background-color: #f5f5f5;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.lista-spesa-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 15px;
    color: #333;
    border-bottom: 2px solid #4caf50;
    padding-bottom: 10px;
}
.lista-spesa-item {
    padding: 8px 0;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
}
.lista-spesa-item:last-child {
    border-bottom: none;
}

/* Stile per la tabella comparativa */
.tabella-comparativa {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    border-radius: 10px;
    overflow: hidden;
}
.tabella-comparativa th {
    background-color: #4caf50;
    color: white;
    text-align: center;
    padding: 12px;
    font-weight: bold;
}
.tabella-comparativa td {
    padding: 10px;
    text-align: center;
    border: 1px solid #e0e0e0;
}
.tabella-comparativa tr:nth-child(even) {
    background-color: #f9f9f9;
}
.tabella-comparativa tr:hover {
    background-color: #f1f1f1;
}
.header-mario {
    background-color: #00acc1 !important;
}
.header-mariantonietta {
    background-color: #9c27b0 !important;
}
.differenza-quantita {
    font-weight: bold;
    color: #e91e63;
}
.icona-differenza {
    font-size: 1.2rem;
    margin-left: 5px;
}
.tab-content {
    padding: 20px;
    border: 1px solid #ddd;
    border-top: none;
    border-radius: 0 0 10px 10px;
}
</style>
""", unsafe_allow_html=True)

# Funzione per generare ricette personalizzate
def genera_ricette_personalizzate():
    ricette = {
        "Colazione": [
            {
                "nome": "Yogurt greco con avena e frutta",
                "ingredienti_mario": ["Yogurt greco 0% (150g)", "Fiocchi d'avena (40g)", "Frutta fresca (150g)", "Burro d'arachidi (15g)"],
                "ingredienti_mariantonietta": ["Yogurt greco 0% (125g)", "Fiocchi d'avena (30g)", "Frutta fresca (150g)", "Burro d'arachidi (10g)"],
                "preparazione": "Versare lo yogurt in una ciotola, aggiungere i fiocchi d'avena e mescolare. Tagliare la frutta a pezzetti e aggiungerla al composto. Completare con un cucchiaio di burro d'arachidi.",
                "categoria": ["proteina", "carboidrato"],
                "tempo": "5 minuti",
                "difficoltà": "Facile"
            },
            {
                "nome": "Pancakes proteici",
                "ingredienti_mario": ["Albume (100ml)", "Farina d'avena (40g)", "Yogurt greco 0% (80g)", "Marmellata a ridotto tenore di zuccheri (20g)", "Burro d'arachidi (15g)"],
                "ingredienti_mariantonietta": ["Albume (80ml)", "Farina d'avena (30g)", "Yogurt greco 0% (60g)", "Marmellata a ridotto tenore di zuccheri (15g)", "Burro d'arachidi (10g)"],
                "preparazione": "Mescolare albume, farina e yogurt. Aggiungere un pizzico di bicarbonato e un goccio di limone. Cuocere in padella antiaderente formando dei dischi. Servire con marmellata e burro d'arachidi.",
                "categoria": ["proteina", "carboidrato"],
                "tempo": "15 minuti",
                "difficoltà": "Media"
            },
            {
                "nome": "Pane tostato con affettato e avocado",
                "ingredienti_mario": ["Pane di segale/integrale (80g)", "Bresaola o prosciutto crudo sgrassato (40g)", "Avocado (40g)", "Olio EVO (10g)"],
                "ingredienti_mariantonietta": ["Pane di segale/integrale (60g)", "Bresaola o prosciutto crudo sgrassato (30g)", "Avocado (30g)", "Olio EVO (5g)"],
                "preparazione": "Tostare il pane, spalmare l'avocado schiacciato e condire con un filo d'olio. Aggiungere l'affettato magro sopra.",
                "categoria": ["proteina", "carboidrato", "grasso"],
                "tempo": "5 minuti",
                "difficoltà": "Facile"
            }
        ],
        "Pranzo": [
            {
                "nome": "Pasta integrale con merluzzo e verdure",
                "ingredienti_mario": ["Pasta integrale (90g)", "Merluzzo (150g)", "Verdure miste (200g)", "Olio EVO (10g)", "Aglio", "Prezzemolo"],
                "ingredienti_mariantonietta": ["Pasta integrale (70g)", "Merluzzo (120g)", "Verdure miste (200g)", "Olio EVO (10g)", "Aglio", "Prezzemolo"],
                "preparazione": "Cuocere la pasta in acqua bollente salata. In una padella, rosolare l'aglio in olio EVO, aggiungere il merluzzo a pezzetti e cuocere per 5-6 minuti. Unire le verdure miste e cuocere per altri 3-4 minuti. Scolare la pasta e saltarla nel condimento. Completare con prezzemolo fresco.",
                "categoria": ["proteina", "carboidrato", "verdura"],
                "tempo": "25 minuti",
                "difficoltà": "Media"
            },
            {
                "nome": "Riso integrale con pollo e verdure",
                "ingredienti_mario": ["Riso integrale (90g)", "Petto di pollo (120g)", "Verdure miste (200g)", "Olio EVO (10g)", "Curcuma", "Zenzero"],
                "ingredienti_mariantonietta": ["Riso integrale (70g)", "Petto di pollo (100g)", "Verdure miste (200g)", "Olio EVO (10g)", "Curcuma", "Zenzero"],
                "preparazione": "Cuocere il riso al dente e sciacquarlo sotto acqua corrente. Tagliare il pollo a cubetti e cuocerlo in padella con olio, curcuma e zenzero. Aggiungere le verdure tagliate a pezzetti e cuocere per 5-6 minuti. Unire il riso e saltare il tutto per 2-3 minuti.",
                "categoria": ["proteina", "carboidrato", "verdura"],
                "tempo": "30 minuti",
                "difficoltà": "Media"
            },
            {
                "nome": "Insalata di legumi con tonno",
                "ingredienti_mario": ["Legumi misti (120g secchi)", "Tonno al naturale (90g)", "Verdure miste (200g)", "Olio EVO (10g)", "Limone", "Erbe aromatiche"],
                "ingredienti_mariantonietta": ["Legumi misti (100g secchi)", "Tonno al naturale (80g)", "Verdure miste (200g)", "Olio EVO (10g)", "Limone", "Erbe aromatiche"],
                "preparazione": "Cuocere i legumi (o utilizzare quelli in barattolo già pronti). Mescolare con il tonno sgocciolato e le verdure tagliate a pezzetti. Condire con olio, succo di limone ed erbe aromatiche.",
                "categoria": ["proteina", "carboidrato", "verdura"],
                "tempo": "15 minuti (con legumi già cotti)",
                "difficoltà": "Facile"
            }
        ],
        "Cena": [
            {
                "nome": "Tacchino con patate al forno",
                "ingredienti_mario": ["Fettine di tacchino (150g)", "Patate (200g)", "Verdure cotte-crude (200g)", "Olio EVO (10g)", "Rosmarino", "Origano"],
                "ingredienti_mariantonietta": ["Fettine di tacchino (180g)", "Patate (80g)", "Verdure cotte-crude (200g)", "Olio EVO (10g)", "Rosmarino", "Origano"],
                "preparazione": "Tagliare le patate a spicchi e condirle con olio e rosmarino. Infornare a 200°C per 20-25 minuti. Grigliare le fettine di tacchino 3-4 minuti per lato. Preparare le verdure cotte-crude. Servire con un filo d'olio e origano.",
                "categoria": ["proteina", "carboidrato", "verdura"],
                "tempo": "35 minuti",
                "difficoltà": "Media"
            },
            {
                "nome": "Pesce al cartoccio con verdure",
                "ingredienti_mario": ["Pesce magro (200g)", "Verdure miste (200g)", "Olio EVO (10g)", "Limone", "Prezzemolo", "Timo"],
                "ingredienti_mariantonietta": ["Pesce magro (200g)", "Verdure miste (200g)", "Olio EVO (10g)", "Limone", "Prezzemolo", "Timo"],
                "preparazione": "Disporre il pesce su un foglio di carta da forno. Aggiungere le verdure tagliate a julienne, condire con olio, succo di limone, sale e erbe aromatiche. Chiudere il cartoccio e cuocere in forno a 180°C per 15-20 minuti.",
                "categoria": ["proteina", "verdura"],
                "tempo": "30 minuti",
                "difficoltà": "Media"
            },
            {
                "nome": "Frittata di albumi con verdure",
                "ingredienti_mario": ["Albumi (200g)", "Uovo intero (1)", "Verdure miste (200g)", "Olio EVO (10g)", "Erbe aromatiche"],
                "ingredienti_mariantonietta": ["Albumi (150g)", "Uovo intero (1)", "Verdure miste (200g)", "Olio EVO (10g)", "Erbe aromatiche"],
                "preparazione": "Saltare le verdure in padella con un filo d'olio. Sbattere gli albumi con l'uovo intero, aggiungere le verdure e le erbe aromatiche. Versare il composto in una padella antiaderente e cuocere a fuoco medio-basso per 5-6 minuti. Girare la frittata e cuocere per altri 2-3 minuti.",
                "categoria": ["proteina", "verdura"],
                "tempo": "20 minuti",
                "difficoltà": "Facile"
            }
        ],
        "Spuntini": [
            {
                "nome": "Yogurt greco con frutta secca",
                "ingredienti_mario": ["Yogurt greco 0% (150g)", "Frutta secca mista (15g)"],
                "ingredienti_mariantonietta": ["Yogurt greco 0% (125g)", "Frutta secca mista (10g)"],
                "preparazione": "Versare lo yogurt in una ciotola e aggiungere la frutta secca tritata grossolanamente.",
                "categoria": ["proteina", "grasso"],
                "tempo": "2 minuti",
                "difficoltà": "Facile"
            },
            {
                "nome": "Panino pre-allenamento",
                "ingredienti_mario": ["Pane (50g)", "Affettato magro (40g)", "Frutta disidratata o banana (20g)"],
                "ingredienti_mariantonietta": ["Pane (40g)", "Affettato magro (30g)", "Frutta disidratata o banana (15g)"],
                "preparazione": "Farcire il panino con l'affettato magro. Consumare la frutta disidratata o la banana 10 minuti prima dell'allenamento.",
                "categoria": ["proteina", "carboidrato"],
                "tempo": "5 minuti",
                "difficoltà": "Facile"
            },
            {
                "nome": "Olive verdi e frutta secca",
                "ingredienti_mario": ["Olive verdi denocciolate (80g)", "Frutta secca (20g)"],
                "ingredienti_mariantonietta": ["Olive verdi denocciolate (60g)", "Frutta secca (15g)"],
                "preparazione": "Servire le olive verdi denocciolate insieme alla frutta secca.",
                "categoria": ["grasso"],
                "tempo": "2 minuti",
                "difficoltà": "Facile"
            }
        ]
    }
    return ricette

# Funzione per generare lista della spesa settimanale
def genera_lista_spesa(ricette_selezionate, persona):
    lista_spesa = {}
    
    for ricetta in ricette_selezionate:
        tipo_pasto = ricetta["tipo_pasto"]
        nome_ricetta = ricetta["nome"]
        
        # Trova la ricetta corrispondente
        for r in ricette[tipo_pasto]:
            if r["nome"] == nome_ricetta:
                # Usa gli ingredienti appropriati in base alla persona
                if persona == "Mario":
                    ingredienti = r["ingredienti_mario"]
                else:
                    ingredienti = r["ingredienti_mariantonietta"]
                
                # Aggiungi gli ingredienti alla lista della spesa
                for ingrediente in ingredienti:
                    # Estrai il nome dell'ingrediente (rimuovendo la quantità tra parentesi)
                    nome_ingrediente = ingrediente.split(" (")[0]
                    
                    if nome_ingrediente in lista_spesa:
                        lista_spesa[nome_ingrediente] += 1
                    else:
                        lista_spesa[nome_ingrediente] = 1
    
    return lista_spesa

# Funzione per visualizzare una ricetta come card
def visualizza_ricetta_card(ricetta, persona):
    if persona == "Mario":
        card_class = "card-mario"
        ingredienti = ricetta["ingredienti_mario"]
    elif persona == "Mariantonietta":
        card_class = "card-mariantonietta"
        ingredienti = ricetta["ingredienti_mariantonietta"]
    else:
        card_class = "card-comune"
        ingredienti = ricetta["ingredienti_mario"] # Default
    
    # Crea la card HTML
    html = f"""
    <div class="card {card_class}">
        <div class="card-title">{ricetta['nome']}</div>
        <div class="card-subtitle">Ingredienti:</div>
        <ul class="card-text">
    """
    
    for ingrediente in ingredienti:
        html += f"<li>{ingrediente}</li>"
    
    html += "</ul>"
    html += f"<div class='card-subtitle'>Preparazione:</div>"
    html += f"<p class='card-text'>{ricetta['preparazione']}</p>"
    
    html += "<div style='margin-top: 15px;'>"
    for categoria in ricetta['categoria']:
        html += f"<span class='card-tag tag-{categoria}'>{categoria.capitalize()}</span>"
    html += f"<span style='float: right;'><i>Tempo: {ricetta['tempo']} | Difficoltà: {ricetta['difficoltà']}</i></span>"
    html += "</div>"
    
    html += "</div>"
    
    return html

# Funzione per visualizzare la lista della spesa
def visualizza_lista_spesa(lista_spesa):
    html = """
    <div class="lista-spesa">
        <div class="lista-spesa-title">Lista della Spesa</div>
    """
    
    for ingrediente, quantita in sorted(lista_spesa.items()):
        html += f"""
        <div class="lista-spesa-item">
            <span>{ingrediente}</span>
            <span>x{quantita}</span>
        </div>
        """
    
    html += "</div>"
    
    return html

# Carica le ricette
ricette = genera_ricette_personalizzate()

# Titolo principale
st.title("Ricette Personalizzate")
st.markdown("Ricette basate sui piani alimentari di Mario e Mariantonietta")

# Tabs per le diverse sezioni
tab1, tab2, tab3 = st.tabs(["Ricette", "Piano Settimanale", "Lista della Spesa"])

with tab1:
    # Filtri per le ricette
    col1, col2, col3 = st.columns(3)
    with col1:
        persona = st.selectbox("Seleziona persona", ["Mario", "Mariantonietta"])
    with col2:
        tipo_pasto = st.selectbox("Tipo di pasto", list(ricette.keys()))
    with col3:
        categoria = st.multiselect("Categoria", ["proteina", "carboidrato", "verdura", "grasso"], default=[])
    
    # Visualizza le ricette filtrate
    st.subheader(f"Ricette per {tipo_pasto} - {persona}")
    
    # Filtra per categoria se selezionata
    ricette_filtrate = ricette[tipo_pasto]
    if categoria:
        ricette_filtrate = [r for r in ricette_filtrate if any(c in r["categoria"] for c in categoria)]
    
    # Visualizza le ricette come card
    for i, ricetta in enumerate(ricette_filtrate):
        st.markdown(visualizza_ricetta_card(ricetta, persona), unsafe_allow_html=True)

with tab2:
    st.subheader("Piano Settimanale Personalizzato")
    
    # Seleziona persona
    persona_piano = st.selectbox("Seleziona persona per il piano", ["Mario", "Mariantonietta"], key="persona_piano")
    
    # Giorni della settimana
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    
    # Giorni di allenamento calcetto
    giorni_allenamento = ["Martedì", "Giovedì", "Sabato"]
    
    # Crea un piano settimanale
    ricette_selezionate = []
    
    # Aggiungi CSS per la tabella del piano settimanale
    st.markdown("""
    <style>
    .piano-settimanale {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-radius: 10px;
        overflow: hidden;
    }
    .piano-settimanale th {
        background-color: #4caf50;
        color: white;
        text-align: center;
        padding: 12px;
        font-weight: bold;
    }
    .piano-settimanale td {
        padding: 10px;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .piano-settimanale tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .piano-settimanale tr:hover {
        background-color: #f1f1f1;
    }
    .giorno-allenamento {
        background-color: #e8f5e9 !important;
        font-weight: bold;
    }
    .pasto-header {
        background-color: #81c784;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Crea la tabella del piano settimanale
    st.markdown("### Panoramica Settimanale")
    
    # Crea l'intestazione della tabella
    html_table = """<table class='piano-settimanale'>
    <tr>
        <th>Giorno</th>
        <th>Colazione</th>
        <th>Pranzo</th>
        <th>Cena</th>
        <th>Spuntino</th>
    </tr>
    """
    
    # Aggiungi le righe per ogni giorno
    for giorno in giorni:
        # Determina se è un giorno di allenamento
        classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""
        
        html_table += f"<tr class='{classe_giorno}'>"
        html_table += f"<td><strong>{giorno}</strong>{' (Allenamento)' if giorno in giorni_allenamento else ''}</td>"
        
        # Colazione
        colazione_options = [r["nome"] for r in ricette["Colazione"]]
        colazione_default = "Yogurt greco con avena e frutta"  # Default per tutti i giorni
        default_index = colazione_options.index(colazione_default) if colazione_default in colazione_options else 0
        html_table += f"<td>{colazione_options[default_index]}</td>"
        
        # Pranzo
        pranzo_options = [r["nome"] for r in ricette["Pranzo"]]
        pranzo_default = "Pasta integrale con merluzzo e verdure" if giorno in giorni_allenamento else "Riso integrale con pollo e verdure"
        default_index = pranzo_options.index(pranzo_default) if pranzo_default in pranzo_options else 0
        html_table += f"<td>{pranzo_options[default_index]}</td>"
        
        # Cena
        cena_options = [r["nome"] for r in ricette["Cena"]]
        cena_default = "Tacchino con patate al forno" if giorno in ["Lunedì", "Mercoledì", "Venerdì"] else "Pesce al cartoccio con verdure"
        default_index = cena_options.index(cena_default) if cena_default in cena_options else 0
        html_table += f"<td>{cena_options[default_index]}</td>"
        
        # Spuntino
        spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
        spuntino_default = "Panino pre-allenamento" if giorno in giorni_allenamento else "Olive verdi e frutta secca"
        default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
        html_table += f"<td>{spuntino_options[default_index]}</td>"
        
        html_table += "</tr>"
    
    html_table += "</table>"
    
    # Visualizza la tabella
    st.markdown(html_table, unsafe_allow_html=True)
    
    # Aggiungi la sezione per la visualizzazione comparativa
    st.subheader("Confronto Piani Alimentari: Mario vs Mariantonietta")
    st.markdown("Questa tabella mostra le differenze di quantità tra i piani alimentari di Mario e Mariantonietta.")
    
    # Crea la tabella comparativa
    html_comparativa = """<table class='tabella-comparativa'>
    <tr>
        <th>Pasto</th>
        <th>Alimento</th>
        <th class='header-mario'>Mario</th>
        <th class='header-mariantonietta'>Mariantonietta</th>
        <th>Differenza</th>
    </tr>
    """
    
    # Aggiungi righe per ogni tipo di pasto e alimento
    for tipo_pasto in ricette.keys():
        for ricetta in ricette[tipo_pasto]:
            # Ottieni gli ingredienti per Mario e Mariantonietta
            ingredienti_mario = ricetta["ingredienti_mario"]
            ingredienti_mariantonietta = ricetta["ingredienti_mariantonietta"]
            
            # Aggiungi una riga per il nome della ricetta
            html_comparativa += f"""<tr>
                <td colspan='5' style='background-color: #e8f5e9; font-weight: bold;'>{tipo_pasto}: {ricetta['nome']}</td>
            </tr>"""
            
            # Confronta gli ingredienti
            for i in range(len(ingredienti_mario)):
                if i < len(ingredienti_mariantonietta):
                    # Estrai il nome dell'ingrediente e la quantità
                    ingrediente_mario = ingredienti_mario[i]
                    ingrediente_mariantonietta = ingredienti_mariantonietta[i]
                    
                    # Estrai il nome dell'ingrediente (rimuovendo la quantità tra parentesi)
                    if "(" in ingrediente_mario:
                        nome_ingrediente = ingrediente_mario.split(" (")[0]
                        quantita_mario = ingrediente_mario.split("(")[1].split(")")[0] if "(" in ingrediente_mario else ""
                        quantita_mariantonietta = ingrediente_mariantonietta.split("(")[1].split(")")[0] if "(" in ingrediente_mariantonietta else ""
                    else:
                        nome_ingrediente = ingrediente_mario
                        quantita_mario = ""
                        quantita_mariantonietta = ""
                    
                    # Determina se c'è una differenza di quantità
                    differenza_classe = "differenza-quantita" if quantita_mario != quantita_mariantonietta else ""
                    icona_differenza = "<span class='icona-differenza'>↓</span>" if quantita_mario != quantita_mariantonietta else ""
                    
                    # Aggiungi la riga alla tabella
                    html_comparativa += f"""<tr>
                        <td>{tipo_pasto}</td>
                        <td>{nome_ingrediente}</td>
                        <td>{quantita_mario}</td>
                        <td>{quantita_mariantonietta}</td>
                        <td class='{differenza_classe}'>{icona_differenza}</td>
                    </tr>"""
    
    html_comparativa += "</table>"
    
    # Visualizza la tabella comparativa
    st.markdown(html_comparativa, unsafe_allow_html=True)
    
    st.markdown("### Personalizza il tuo piano settimanale")
    st.markdown("Seleziona le ricette per ogni giorno della settimana:")
    
    # Tabs per i giorni della settimana
    tabs_giorni = st.tabs(giorni)
    
    for i, giorno in enumerate(giorni):
        with tabs_giorni[i]:
            st.markdown(f"### {giorno}")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**Colazione**")
                colazione = st.selectbox(
                    "Seleziona colazione",
                    [r["nome"] for r in ricette["Colazione"]],
                    key=f"colazione_{giorno}"
                )
                ricette_selezionate.append({"giorno": giorno, "tipo_pasto": "Colazione", "nome": colazione})
                
                # Trova e visualizza la ricetta selezionata
                for r in ricette["Colazione"]:
                    if r["nome"] == colazione:
                        st.markdown(visualizza_ricetta_card(r, persona_piano), unsafe_allow_html=True)
            
            with col2:
                st.markdown("**Pranzo**")
                pranzo = st.selectbox(
                    "Seleziona pranzo",
                    [r["nome"] for r in ricette["Pranzo"]],
                    key=f"pranzo_{giorno}"
                )
                ricette_selezionate.append({"giorno": giorno, "tipo_pasto": "Pranzo", "nome": pranzo})
                
                # Trova e visualizza la ricetta selezionata
                for r in ricette["Pranzo"]:
                    if r["nome"] == pranzo:
                        st.markdown(visualizza_ricetta_card(r, persona_piano), unsafe_allow_html=True)
            
            with col3:
                st.markdown("**Cena**")
                cena = st.selectbox(
                    "Seleziona cena",
                    [r["nome"] for r in ricette["Cena"]],
                    key=f"cena_{giorno}"
                )
                ricette_selezionate.append({"giorno": giorno, "tipo_pasto": "Cena", "nome": cena})
                
                # Trova e visualizza la ricetta selezionata
                for r in ricette["Cena"]:
                    if r["nome"] == cena:
                        st.markdown(visualizza_ricetta_card(r, persona_piano), unsafe_allow_html=True)
            
            with col4:
                st.markdown("**Spuntini**")
                # Seleziona spuntino appropriato in base al giorno di allenamento
                if giorno in giorni_allenamento:
                    spuntino_default = "Panino pre-allenamento"
                else:
                    spuntino_default = "Olive verdi e frutta secca"
                
                # Trova l'indice del default
                spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
                default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
                
                spuntino = st.selectbox(
                    "Seleziona spuntino",
                    spuntino_options,
                    index=default_index,
                    key=f"spuntino_{giorno}"
                )
                ricette_selezionate.append({"giorno": giorno, "tipo_pasto": "Spuntini", "nome": spuntino})
                
                # Trova e visualizza la ricetta selezionata
                for r in ricette["Spuntini"]:
                    if r["nome"] == spuntino:
                        st.markdown(visualizza_ricetta_card(r, persona_piano), unsafe_allow_html=True)

with tab3:
    st.subheader("Lista della Spesa Settimanale")
    
    # Seleziona persona per la lista della spesa
    persona_lista = st.selectbox("Seleziona persona per la lista della spesa", ["Mario", "Mariantonietta"])
    
    # Genera la lista della spesa in base alle ricette selezionate
    if 'ricette_selezionate' in locals():
        lista_spesa = genera_lista_spesa(ricette_selezionate, persona_lista)
        st.markdown(visualizza_lista_spesa(lista_spesa), unsafe_allow_html=True)
        
        # Opzione per scaricare la lista della spesa
        if st.button("Scarica Lista della Spesa"):
            # Crea un DataFrame dalla lista della spesa
            df_lista = pd.DataFrame({
                "Ingrediente": lista_spesa.keys(),
                "Quantità": lista_spesa.values()
            })
            
            # Salva il DataFrame come CSV
            df_lista.to_csv("lista_spesa.csv", index=False)
            st.success("Lista della spesa salvata come 'lista_spesa.csv'")
    else:
        st.info("Seleziona prima le ricette nel Piano Settimanale per generare la lista della spesa.")

# Sidebar con informazioni aggiuntive
st.sidebar.title("Informazioni Nutrizionali")

# Aggiungi informazioni nutrizionali nella sidebar
st.sidebar.markdown("### Linee Guida Nutrizionali")
st.sidebar.markdown("""
- **Proteine**: Consumare proteine magre ad ogni pasto principale
- **Carboidrati**: Preferire fonti integrali e a basso indice glicemico
- **Grassi**: Utilizzare grassi sani come olio EVO, avocado e frutta secca
- **Verdure**: Includere almeno 200g di verdure a pranzo e cena
- **Idratazione**: Bere almeno 2 litri di acqua al giorno
""")

st.sidebar.markdown("### Giorni di Allenamento")
st.sidebar.markdown("""
- **Martedì**: Calcetto
- **Giovedì**: Calcetto
- **Sabato**: Calcetto

Nei giorni di allenamento, consumare uno spuntino 1.5-2 ore prima dell'attività fisica.
""")

# Aggiungi un pulsante per integrare con l'app principale
st.sidebar.markdown("---")
if st.sidebar.button("Torna all'App Principale"):
    st.switch_page("app.py")
# Aggiungi CSS per la tabella del piano settimanale
st.markdown("""
<style>
.tabella-piano {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 30px;
    font-size: 1.1rem;
}
.tabella-piano th, .tabella-piano td {
    border: 1px solid #bdbdbd;
    padding: 8px 12px;
    text-align: center;
}
.tabella-piano th {
    background: linear-gradient(90deg, #e0f7fa 0%, #f3e5f5 100%);
    color: #333;
    font-weight: bold;
}
.tabella-piano tr:nth-child(even) {
    background-color: #f9f9f9;
}
.tabella-piano .diff {
    background-color: #fff9c4;
    font-weight: bold;
    color: #d84315;
}
.tabella-piano .icon {
    font-size: 1.2rem;
    vertical-align: middle;
    margin-left: 4px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
## Piano settimanale comparativo: Mario vs Mariantonietta
""")

def carica_piano_settimanale():
    if os.path.exists("pasti_settimanali.xlsx"):
        return pd.read_excel("pasti_settimanali.xlsx")
    else:
        return pd.DataFrame(columns=["Giorno", "Pasto", "Categoria", "Alimento", "Quantità_Mario", "Quantità_Mariantonietta"])

piano_df = carica_piano_settimanale()

if not piano_df.empty:
    giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
    pasti = ["Colazione", "Spuntino", "Pranzo", "Merenda", "Cena"]
    for giorno in giorni:
        st.markdown(f"### {giorno}")
        tabella = []
        for pasto in pasti:
            pasti_giorno = piano_df[(piano_df["Giorno"] == giorno) & (piano_df["Pasto"] == pasto)]
            for _, row in pasti_giorno.iterrows():
                diff = row["Quantità_Mario"] != row["Quantità_Mariantonietta"]
                icona = "🔔" if diff else "✅"
                tabella.append({
                    "Pasto": pasto,
                    "Categoria": row["Categoria"],
                    "Alimento": row["Alimento"],
                    "Mario": row["Quantità_Mario"],
                    "Mariantonietta": row["Quantità_Mariantonietta"],
                    "Diff": diff,
                    "Icona": icona
                })
        if tabella:
            html = "<table class='tabella-piano'>"
            html += "<tr><th>Pasto</th><th>Categoria</th><th>Alimento</th><th>Mario</th><th>Mariantonietta</th><th>Diff.</th></tr>"
            for r in tabella:
                diff_class = "diff" if r["Diff"] else ""
                html += f"<tr><td>{r['Pasto']}</td><td>{r['Categoria']}</td><td>{r['Alimento']}</td>"
                html += f"<td class='{diff_class}'>{r['Mario']}</td><td class='{diff_class}'>{r['Mariantonietta']}</td>"
                html += f"<td><span class='icon'>{r['Icona']}</span></td></tr>"
            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("Nessun dato disponibile per questo giorno.")
else:
    st.warning("Nessun piano settimanale trovato. Compila prima il piano pasti nella pagina principale.")
    
st.markdown("### Personalizza il tuo piano settimanale")
st.markdown("Seleziona le ricette per ogni giorno della settimana:")
st.markdown("Seleziona persona per il piano")
st.markdown("## Piano Settimanale Personalizzato")
st.markdown("Giorni della settimana")
st.markdown("Giorni di allenamento calcetto")
st.markdown("Crea un piano settimanale")
st.markdown("### Panoramica Settimanale")
st.markdown("Crea l'intestazione della tabella")
html_table = """<table class='piano-settimanale'>
<tr>
    <th>Giorno</th>
    <th>Colazione</th>
    <th>Pranzo</th>
    <th>Cena</th>
    <th>Spuntino</th>
</tr>
"""
st.markdown("Aggiungi le righe per ogni giorno")
for giorno in giorni:
    # Determina se è un giorno di allenamento
    classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""
    
    html_table += f"<tr class='{classe_giorno}'>"
    html_table += f"<td><strong>{giorno}</strong>{' (Allenamento)' if giorno in giorni_allenamento else ''}</td>"
    
    # Colazione
    colazione_options = [r["nome"] for r in ricette["Colazione"]]
    colazione_default = "Yogurt greco con avena e frutta"  # Default per tutti i giorni
    default_index = colazione_options.index(colazione_default) if colazione_default in colazione_options else 0
    html_table += f"<td>{colazione_options[default_index]}</td>"
    
    # Pranzo
    pranzo_options = [r["nome"] for r in ricette["Pranzo"]]
    pranzo_default = "Pasta integrale con merluzzo e verdure" if giorno in giorni_allenamento else "Riso integrale con pollo e verdure"
    default_index = pranzo_options.index(pranzo_default) if pranzo_default in pranzo_options else 0
    html_table += f"<td>{pranzo_options[default_index]}</td>"
    
    # Cena
    cena_options = [r["nome"] for r in ricette["Cena"]]
    cena_default = "Tacchino con patate al forno" if giorno in ["Lunedì", "Mercoledì", "Venerdì"] else "Pesce al cartoccio con verdure"
    default_index = cena_options.index(cena_default) if cena_default in cena_options else 0
    html_table += f"<td>{cena_options[default_index]}</td>"
    
    # Spuntino
    spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
    spuntino_default = "Panino pre-allenamento" if giorno in giorni_allenamento else "Olive verdi e frutta secca"
    default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
    html_table += f"<td>{spuntino_options[default_index]}</td>"
    
    html_table += "</tr>"
st.markdown(html_table, unsafe_allow_html=True)
st.markdown("### Personalizza il tuo piano settimanale")
st.markdown("Seleziona le ricette per ogni giorno della settimana:")
st.markdown("Seleziona persona per il piano")
st.markdown("### Panoramica Settimanale")
st.markdown("Crea l'intestazione della tabella")
html_table = """<table class='piano-settimanale'>
<tr>
    <th>Giorno</th>
    <th>Colazione</th>
    <th>Pranzo</th>
    <th>Cena</th>
    <th>Spuntino</th>
</tr>
"""
st.markdown("Aggiungi le righe per ogni giorno")
for giorno in giorni:
    # Determina se è un giorno di allenamento
    classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""
    
    html_table += f"<tr class='{classe_giorno}'>"
    html_table += f"<td><strong>{giorno}</strong>{' (Allenamento)' if giorno in giorni_allenamento else ''}</td>"
    
    # Colazione
    colazione_options = [r["nome"] for r in ricette["Colazione"]]
    colazione_default = "Yogurt greco con avena e frutta"  # Default per tutti i giorni
    default_index = colazione_options.index(colazione_default) if colazione_default in colazione_options else 0
    html_table += f"<td>{colazione_options[default_index]}</td>"
    
    # Pranzo
    pranzo_options = [r["nome"] for r in ricette["Pranzo"]]
    pranzo_default = "Pasta integrale con merluzzo e verdure" if giorno in giorni_allenamento else "Riso integrale con pollo e verdure"
    default_index = pranzo_options.index(pranzo_default) if pranzo_default in pranzo_options else 0
    html_table += f"<td>{pranzo_options[default_index]}</td>"
    
    # Cena
    cena_options = [r["nome"] for r in ricette["Cena"]]
    cena_default = "Tacchino con patate al forno" if giorno in ["Lunedì", "Mercoledì", "Venerdì"] else "Pesce al cartoccio con verdure"
    default_index = cena_options.index(cena_default) if cena_default in cena_options else 0
    html_table += f"<td>{cena_options[default_index]}</td>"
    
    # Spuntino
    spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
    spuntino_default = "Panino pre-allenamento" if giorno in giorni_allenamento else "Olive verdi e frutta secca"
    default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
    html_table += f"<td>{spuntino_options[default_index]}</td>"
    
    html_table += "</tr>"
st.markdown(html_table, unsafe_allow_html=True)
st.markdown("### Personalizza il tuo piano settimanale")
st.markdown("Seleziona le ricette per ogni giorno della settimana:")
st.markdown("Seleziona persona per il piano")
st.markdown("### Panoramica Settimanale")
st.markdown("Crea l'intestazione della tabella")
html_table = """<table class='piano-settimanale'>
<tr>
    <th>Giorno</th>
    <th>Colazione</th>
    <th>Pranzo</th>
    <th>Cena</th>
    <th>Spuntino</th>
</tr>
"""
st.markdown("Aggiungi le righe per ogni giorno")
for giorno in giorni:
    # Determina se è un giorno di allenamento
    classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""
    
    html_table += f"<tr class='{classe_giorno}'>"
    html_table += f"<td><strong>{giorno}</strong>{' (Allenamento)' if giorno in giorni_allenamento else ''}</td>"
    
    # Colazione
    colazione_options = [r["nome"] for r in ricette["Colazione"]]
    colazione_default = "Yogurt greco con avena e frutta"  # Default per tutti i giorni
    default_index = colazione_options.index(colazione_default) if colazione_default in colazione_options else 0
    html_table += f"<td>{colazione_options[default_index]}</td>"
    
    # Pranzo
    pranzo_options = [r["nome"] for r in ricette["Pranzo"]]
    pranzo_default = "Pasta integrale con merluzzo e verdure" if giorno in giorni_allenamento else "Riso integrale con pollo e verdure"
    default_index = pranzo_options.index(pranzo_default) if pranzo_default in pranzo_options else 0
    html_table += f"<td>{pranzo_options[default_index]}</td>"
    
    # Cena
    cena_options = [r["nome"] for r in ricette["Cena"]]
    cena_default = "Tacchino con patate al forno" if giorno in ["Lunedì", "Mercoledì", "Venerdì"] else "Pesce al cartoccio con verdure"
    default_index = cena_options.index(cena_default) if cena_default in cena_options else 0
    html_table += f"<td>{cena_options[default_index]}</td>"
    
    # Spuntino
    spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
    spuntino_default = "Panino pre-allenamento" if giorno in giorni_allenamento else "Olive verdi e frutta secca"
    default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
    html_table += f"<td>{spuntino_options[default_index]}</td>"
    
    html_table += "</tr>"
st.markdown(html_table, unsafe_allow_html=True)
st.markdown("### Personalizza il tuo piano settimanale")
st.markdown("Seleziona le ricette per ogni giorno della settimana:")
st.markdown("Seleziona persona per il piano")
st.markdown("### Panoramica Settimanale")
st.markdown("Crea l'intestazione della tabella")
html_table = """<table class='piano-settimanale'>
<tr>
    <th>Giorno</th>
    <th>Colazione</th>
    <th>Pranzo</th>
    <th>Cena</th>
    <th>Spuntino</th>
</tr>
"""
st.markdown("Aggiungi le righe per ogni giorno")
for giorno in giorni:
    # Determina se è un giorno di allenamento
    classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""
    
    html_table += f"<tr class='{classe_giorno}'>"
    html_table += f"<td><strong>{giorno}</strong>{' (Allenamento)' if giorno in giorni_allenamento else ''}</td>"
    
    # Colazione
    colazione_options = [r["nome"] for r in ricette["Colazione"]]
    colazione_default = "Yogurt greco con avena e frutta"  # Default per tutti i giorni
    default_index = colazione_options.index(colazione_default) if colazione_default in colazione_options else 0
    html_table += f"<td>{colazione_options[default_index]}</td>"
    
    # Pranzo
    pranzo_options = [r["nome"] for r in ricette["Pranzo"]]
    pranzo_default = "Pasta integrale con merluzzo e verdure" if giorno in giorni_allenamento else "Riso integrale con pollo e verdure"
    default_index = pranzo_options.index(pranzo_default) if pranzo_default in pranzo_options else 0
    html_table += f"<td>{pranzo_options[default_index]}</td>"
    
    # Cena
    cena_options = [r["nome"] for r in ricette["Cena"]]
    cena_default = "Tacchino con patate al forno" if giorno in ["Lunedì", "Mercoledì", "Venerdì"] else "Pesce al cartoccio con verdure"
    default_index = cena_options.index(cena_default) if cena_default in cena_options else 0
    html_table += f"<td>{cena_options[default_index]}</td>"
    
    # Spuntino
    spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
    spuntino_default = "Panino pre-allenamento" if giorno in giorni_allenamento else "Olive verdi e frutta secca"
    default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
    html_table += f"<td>{spuntino_options[default_index]}</td>"
    
    html_table += "</tr>"
st.markdown(html_table, unsafe_allow_html=True)
st.markdown("### Personalizza il tuo piano settimanale")
st.markdown("Seleziona le ricette per ogni giorno della settimana:")
st.markdown("Seleziona persona per il piano")
st.markdown("### Panoramica Settimanale")
st.markdown("Crea l'intestazione della tabella")
html_table = """<table class='piano-settimanale'>
<tr>
    <th>Giorno</th>
    <th>Colazione</th>
    <th>Pranzo</th>
    <th>Cena</th>
    <th>Spuntino</th>
</tr>
"""
st.markdown("Aggiungi le righe per ogni giorno")
for giorno in giorni:
    # Determina se è un giorno di allenamento
    classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""
    
    html_table += f"<tr class='{classe_giorno}'>"
    html_table += f"<td><strong>{giorno}</strong>{' (Allenamento)' if giorno in giorni_allenamento else ''}</td>"
    
    # Colazione
    colazione_options = [r["nome"] for r in ricette["Colazione"]]
    colazione_default = "Yogurt greco con avena e frutta"  # Default per tutti i giorni
    default_index = colazione_options.index(colazione_default) if colazione_default in colazione_options else 0
    html_table += f"<td>{colazione_options[default_index]}</td>"
    
    # Pranzo
    pranzo_options = [r["nome"] for r in ricette["Pranzo"]]
    pranzo_default = "Pasta integrale con merluzzo e verdure" if giorno in giorni_allenamento else "Riso integrale con pollo e verdure"
    default_index = pranzo_options.index(pranzo_default) if pranzo_default in pranzo_options else 0
    html_table += f"<td>{pranzo_options[default_index]}</td>"
    
    # Cena
    cena_options = [r["nome"] for r in ricette["Cena"]]
    cena_default = "Tacchino con patate al forno" if giorno in ["Lunedì", "Mercoledì", "Venerdì"] else "Pesce al cartoccio con verdure"
    default_index = cena_options.index(cena_default) if cena_default in cena_options else 0
    html_table += f"<td>{cena_options[default_index]}</td>"
    
    # Spuntino
    spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
    spuntino_default = "Panino pre-allenamento" if giorno in giorni_allenamento else "Olive verdi e frutta secca"
    default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
    html_table += f"<td>{spuntino_options[default_index]}</td>"
    
    html_table += "</tr>"
st.markdown(html_table, unsafe_allow_html=True)
st.markdown("### Personalizza il tuo piano settimanale")
st.markdown("Seleziona le ricette per ogni giorno della settimana:")
st.markdown("Seleziona persona per il piano")
st.markdown("### Panoramica Settimanale")
st.markdown("Crea l'intestazione della tabella")
html_table = """<table class='piano-settimanale'>
<tr>
    <th>Giorno</th>
    <th>Colazione</th>
    <th>Pranzo</th>
    <th>Cena</th>
    <th>Spuntino</th>
</tr>
"""
st.markdown("Aggiungi le righe per ogni giorno")
for giorno in giorni:
    # Determina se è un giorno di allenamento
    classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""
    
    html_table += f"<tr class='{classe_giorno}'>"
    html_table += f"<td><strong>{giorno}</strong>{' (Allenamento)' if giorno in giorni_allenamento else ''}</td>"
    
    # Colazione
    colazione_options = [r["nome"] for r in ricette["Colazione"]]
    colazione_default = "Yogurt greco con avena e frutta"  # Default per tutti i giorni
    default_index = colazione_options.index(colazione_default) if colazione_default in colazione_options else 0
    html_table += f"<td>{colazione_options[default_index]}</td>"
    
    # Pranzo
    pranzo_options = [r["nome"] for r in ricette["Pranzo"]]
    pranzo_default = "Pasta integrale con merluzzo e verdure" if giorno in giorni_allenamento else "Riso integrale con pollo e verdure"
    default_index = pranzo_options.index(pranzo_default) if pranzo_default in pranzo_options else 0
    html_table += f"<td>{pranzo_options[default_index]}</td>"
    
    # Cena
    cena_options = [r["nome"] for r in ricette["Cena"]]
    cena_default = "Tacchino con patate al forno" if giorno in ["Lunedì", "Mercoledì", "Venerdì"] else "Pesce al cartoccio con verdure"
    default_index = cena_options.index(cena_default) if cena_default in cena_options else 0
    html_table += f"<td>{cena_options[default_index]}</td>"
    
    # Spuntino
    spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
    spuntino_default = "Panino pre-allenamento" if giorno in giorni_allenamento else "Olive verdi e frutta secca"
    default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
    html_table += f"<td>{spuntino_options[default_index]}</td>"
    
    html_table += "</tr>"
st.markdown(html_table, unsafe_allow_html=True)
st.markdown("### Personalizza il tuo piano settimanale")
st.markdown("Seleziona le ricette per ogni giorno della settimana:")
st.markdown("Seleziona persona per il piano")
st.markdown("### Panoramica Settimanale")
st.markdown("Crea l'intestazione della tabella")
html_table = """<table class='piano-settimanale'>
<tr>
    <th>Giorno</th>
    <th>Colazione</th>
    <th>Pranzo</th>
    <th>Cena</th>
    <th>Spuntino</th>
</tr>
"""
st.markdown("Aggiungi le righe per ogni giorno")
for giorno in giorni:
    # Determina se è un giorno di allenamento
    classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""
    
    html_table += f"<tr class='{classe_giorno}'>"
    html_table += f"<td><strong>{giorno}</strong>{' (Allenamento)' if giorno in giorni_allenamento else ''}</td>"
    
    # Colazione
    colazione_options = [r["nome"] for r in ricette["Colazione"]]
    colazione_default = "Yogurt greco con avena e frutta"  # Default per tutti i giorni
    default_index = colazione_options.index(colazione_default) if colazione_default in colazione_options else 0
    html_table += f"<td>{colazione_options[default_index]}</td>"
    
    # Pranzo
    pranzo_options = [r["nome"] for r in ricette["Pranzo"]]
    pranzo_default = "Pasta integrale con merluzzo e verdure" if giorno in giorni_allenamento else "Riso integrale con pollo e verdure"
    default_index = pranzo_options.index(pranzo_default) if pranzo_default in pranzo_options else 0
    html_table += f"<td>{pranzo_options[default_index]}</td>"
    
    # Cena
    cena_options = [r["nome"] for r in ricette["Cena"]]
    cena_default = "Tacchino con patate al forno" if giorno in ["Lunedì", "Mercoledì", "Venerdì"] else "Pesce al cartoccio con verdure"
    default_index = cena_options.index(cena_default) if cena_default in cena_options else 0
    html_table += f"<td>{cena_options[default_index]}</td>"
    
    # Spuntino
    spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
    spuntino_default = "Panino pre-allenamento" if giorno in giorni_allenamento else "Olive verdi e frutta secca"
    default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
    html_table += f"<td>{spuntino_options[default_index]}</td>"
    
    html_table += "</tr>"
st.markdown(html_table, unsafe_allow_html=True)
st.markdown("### Personalizza il tuo piano settimanale")
st.markdown("Seleziona le ricette per ogni giorno della settimana:")
st.markdown("Seleziona persona per il piano")
st.markdown("### Panoramica Settimanale")
st.markdown("Crea l'intestazione della tabella")
html_table = """<table class='piano-settimanale'>
<tr>
    <th>Giorno</th>
    <th>Colazione</th>
    <th>Pranzo</th>
    <th>Cena</th>
    <th>Spuntino</th>
</tr>
"""
st.markdown("Aggiungi le righe per ogni giorno")
for giorno in giorni:
    # Determina se è un giorno di allenamento
    classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""
    
    html_table += f"<tr class='{classe_giorno}'>"
    html_table += f"<td><strong>{giorno}</strong>{' (Allenamento)' if giorno in giorni_allenamento else ''}</td>"
    
    # Colazione
    colazione_options = [r["nome"] for r in ricette["Colazione"]]
    colazione_default = "Yogurt greco con avena e frutta"  # Default per tutti i giorni
    default_index = colazione_options.index(colazione_default) if colazione_default in colazione_options else 0
    html_table += f"<td>{colazione_options[default_index]}</td>"
    
    # Pranzo
    pranzo_options = [r["nome"] for r in ricette["Pranzo"]]
    pranzo_default = "Pasta integrale con merluzzo e verdure" if giorno in giorni_allenamento else "Riso integrale con pollo e verdure"
    default_index = pranzo_options.index(pranzo_default) if pranzo_default in pranzo_options else 0
    html_table += f"<td>{pranzo_options[default_index]}</td>"
    
    # Cena
    cena_options = [r["nome"] for r in ricette["Cena"]]
    cena_default = "Tacchino con patate al forno" if giorno in ["Lunedì", "Mercoledì", "Venerdì"] else "Pesce al cartoccio con verdure"
    default_index = cena_options.index(cena_default) if cena_default in cena_options else 0
    html_table += f"<td>{cena_options[default_index]}</td>"
    
    # Spuntino
    spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
    spuntino_default = "Panino pre-allenamento" if giorno in giorni_allenamento else "Olive verdi e frutta secca"
    default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
    html_table += f"<td>{spuntino_options[default_index]}</td>"
    
    html_table += "</tr>"
st.markdown(html_table, unsafe_allow_html=True)
st.markdown("### Personalizza il tuo piano settimanale")
st.markdown("Seleziona le ricette per ogni giorno della settimana:")
st.markdown("Seleziona persona per il piano")
st.markdown("### Panoramica Settimanale")
st.markdown("Crea l'intestazione della tabella")
html_table = """<table class='piano-settimanale'>
<tr>
    <th>Giorno</th>
    <th>Colazione</th>
    <th>Pranzo</th>
    <th>Cena</th>
    <th>Spuntino</th>
</tr>
"""
st.markdown("Aggiungi le righe per ogni giorno")
for giorno in giorni:
    # Determina se è un giorno di allenamento
    classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""
    
    html_table += f"<tr class='{classe_giorno}'>"
    html_table += f"<td><strong>{giorno}</strong>{' (Allenamento)' if giorno in giorni_allenamento else ''}</td>"
    
    # Colazione
    colazione_options = [r["nome"] for r in ricette["Colazione"]]
    colazione_default = "Yogurt greco con avena e frutta"  # Default per tutti i giorni
    default_index = colazione_options.index(colazione_default) if colazione_default in colazione_options else 0
    html_table += f"<td>{colazione_options[default_index]}</td>"
    
    # Pranzo
    pranzo_options = [r["nome"] for r in ricette["Pranzo"]]
    pranzo_default = "Pasta integrale con merluzzo e verdure" if giorno in giorni_allenamento else "Riso integrale con pollo e verdure"
    default_index = pranzo_options.index(pranzo_default) if pranzo_default in pranzo_options else 0
    html_table += f"<td>{pranzo_options[default_index]}</td>"
    
    # Cena
    cena_options = [r["nome"] for r in ricette["Cena"]]
    cena_default = "Tacchino con patate al forno" if giorno in ["Lunedì", "Mercoledì", "Venerdì"] else "Pesce al cartoccio con verdure"
    default_index = cena_options.index(cena_default) if cena_default in cena_options else 0
    html_table += f"<td>{cena_options[default_index]}</td>"
    
    # Spuntino
    spuntino_options = [r["nome"] for r in ricette["Spuntini"]]
    spuntino_default = "Panino pre-allenamento" if giorno in giorni_allenamento else "Olive verdi e frutta secca"
    default_index = spuntino_options.index(spuntino_default) if spuntino_default in spuntino_options else 0
    html_table += f"<td>{spuntino_options[default_index]}</td>"
    
    html_table += "</tr>"
st.markdown(html_table, unsafe_allow_html=True)
st.markdown("### Personalizza il tuo piano settimanale")
st.markdown("Seleziona le ricette per ogni giorno della settimana:")
st.markdown("Seleziona persona per il piano")
st.markdown("### Panoramica Settimanale")
st.markdown("Crea l'intestazione della tabella")
html_table = """<table class='piano-settimanale'>
<tr>
    <th>Giorno</th>
    <th>Colazione</th>
    <th>Pranzo</th>
    <th>Cena</th>
    <th>Spuntino</th>
</tr>
"""
st.markdown("Aggiungi le righe per ogni giorno")
for giorno in giorni:
    # Determina se è un giorno di allenamento
    classe_giorno = "giorno-allenamento" if giorno in giorni_allenamento else ""