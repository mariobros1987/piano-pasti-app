import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import altair as alt

# Configurazione pagina
st.set_page_config(page_title="Piano Alimentare Personalizzato", layout="wide")

# Stile CSS personalizzato
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #2e7d32;
    text-align: center;
    margin-bottom: 30px;
    padding-bottom: 10px;
    border-bottom: 2px solid #2e7d32;
}
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
.menu-button {
    background-color: #4caf50;
    color: white;
    padding: 15px 25px;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    font-weight: 600;
    margin: 10px;
    transition: background-color 0.3s, transform 0.3s;
    text-align: center;
    display: block;
    width: 100%;
}
.menu-button:hover {
    background-color: #388e3c;
    transform: translateY(-3px);
}
</style>
""", unsafe_allow_html=True)

# Titolo principale
st.markdown("<h1 class='main-header'>Piano Alimentare Personalizzato</h1>", unsafe_allow_html=True)

# Descrizione
st.markdown("""
### Benvenuto nell'applicazione per la gestione del piano alimentare personalizzato!

Questa applicazione ti permette di:
- Visualizzare i piani alimentari personalizzati di Mario e Mariantonietta
- Esplorare ricette personalizzate basate sui piani alimentari
- Generare automaticamente la lista della spesa settimanale
- Monitorare le statistiche nutrizionali
""")

# Menu principale con card colorate
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card card-mario">
        <div class="card-title">Piano Alimentare</div>
        <div class="card-text">Visualizza e gestisci il piano alimentare settimanale personalizzato.</div>
        <br>
        <a href="app.py" target="_self"><div class="menu-button">Vai al Piano Alimentare</div></a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card card-comune">
        <div class="card-title">Ricette Personalizzate</div>
        <div class="card-text">Esplora ricette personalizzate basate sui piani alimentari di Mario e Mariantonietta.</div>
        <br>
        <a href="ricette_personalizzate.py" target="_self"><div class="menu-button">Vai alle Ricette</div></a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card card-mariantonietta">
        <div class="card-title">Lista della Spesa</div>
        <div class="card-text">Genera automaticamente la lista della spesa settimanale in base alle ricette selezionate.</div>
        <br>
        <a href="lista_spesa.py" target="_self"><div class="menu-button">Vai alla Lista della Spesa</div></a>
    </div>
    """, unsafe_allow_html=True)

# Informazioni sui piani alimentari
st.markdown("### Informazioni sui Piani Alimentari")

# Tabs per i piani alimentari di Mario e Mariantonietta
tab1, tab2 = st.tabs(["Piano di Mario", "Piano di Mariantonietta"])

with tab1:
    st.markdown("""
    #### Piano Alimentare di Mario
    
    Il piano alimentare di Mario è strutturato per supportare la sua attività fisica, in particolare il calcetto che pratica tre volte a settimana (martedì, giovedì e sabato).
    
    **Caratteristiche principali:**
    - Apporto calorico adeguato per sostenere l'attività fisica
    - Distribuzione bilanciata di macronutrienti
    - Spuntini pre-allenamento specifici nei giorni di calcetto
    - Maggiore apporto di carboidrati nei giorni di allenamento
    - Porzioni adattate alle sue esigenze energetiche
    
    **Alimenti principali:**
    - Proteine: carne magra, pesce, uova, yogurt greco
    - Carboidrati: pasta integrale, riso integrale, pane integrale, patate
    - Grassi: olio EVO, frutta secca, olive verdi, avocado
    - Verdure: almeno 200g per pasto principale
    """)

with tab2:
    st.markdown("""
    #### Piano Alimentare di Mariantonietta
    
    Il piano alimentare di Mariantonietta è personalizzato per le sue esigenze specifiche, con porzioni adattate e una distribuzione equilibrata di nutrienti.
    
    **Caratteristiche principali:**
    - Apporto calorico calibrato alle sue esigenze
    - Distribuzione bilanciata di macronutrienti
    - Porzioni ridotte di carboidrati rispetto al piano di Mario
    - Maggiore apporto proteico in alcuni pasti
    - Attenzione particolare alle verdure e ai grassi sani
    
    **Alimenti principali:**
    - Proteine: carne magra, pesce, uova, yogurt greco
    - Carboidrati: pasta integrale, riso integrale, pane integrale, patate (porzioni ridotte)
    - Grassi: olio EVO, frutta secca, olive verdi, avocado
    - Verdure: almeno 200g per pasto principale
    """)

# Informazioni sulla dieta
with st.expander("Linee Guida Nutrizionali"):
    st.markdown("""
    ### Linee Guida Nutrizionali Generali
    
    **Avvertenze Generali:**
    - Il peso degli alimenti si riferisce a crudo e al netto degli scarti
    - Masticare con cura gli alimenti per una migliore digestione e assimilazione
    - Non saltare i pasti
    - Aggiungere l'olio EVO a crudo a cottura ultimata
    - Non limitare l'uso del sale, alternarlo con diversi tipi: rosso, rosa, blu, affumicato
    - Preferire l'utilizzo di spezie secche e fresche (curcuma, cumino, zenzero, erbe aromatiche)
    
    **Alimenti da Ridurre:**
    - Prodotti confezionati ricchi di sale e zuccheri ad alto indice glicemico
    - Ogni forma di alcool
    - Prodotti industriali per celiaci e il "senza glutine" industriale
    - Acidi grassi saturi animali e acido arachidonico (latte, formaggi, burro normale, salumi)
    
    **Alimenti da Prediligere:**
    - Tisane, camomilla senza zucchero (tisane di boldo, betulla, ortica, tarassaco)
    - Verdura cotta in olio di cocco/EVO ripassata in padella
    - Pesce (5-6 volte a settimana tra pranzo e cena)
    - Spezie con impatto favorevole sulla detossificazione
    
    **Note Importanti:**
    - Particolare importanza all'acquisto della materia prima: carne e pesce da macelleria e pescheria, non da allevamenti intensivi
    - Variare i tagli di carne, preferendo quelli meno esterni ma più ricchi di sali minerali e vitamine
    - Per il pesce, scegliere pesci piccoli e possibilmente pescati
    - Utilizzare uova di galline locali
    """)

# Sidebar con informazioni aggiuntive
st.sidebar.title("Informazioni")
st.sidebar.markdown("""
### Contatti

**Dott.ssa Antonella Quartarella**  
Biologa nutrizionista

- Human nutrition
- Dietetic and Clinical nutrition
- Master in Alimentazione e Nutrizione umana
- Sport nutrition
- Diploma in nutrizione sportiva

### Avviso

Questo piano alimentare è personalizzato e si prefigge l'obiettivo di promuovere un'alimentazione normocalorica e mirata a favorire il miglioramento del profilo lipidico ematico, basata sul potere antinfiammatorio degli alimenti.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    Piano Alimentare Personalizzato di Dibenedetto Mario e Mariantonietta<br>
    Dott.ssa Antonella Quartarella - Biologa nutrizionista<br>
    © 2023 Tutti i diritti riservati
</div>
""", unsafe_allow_html=True)