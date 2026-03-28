import os
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# --- CONFIGURAÇÕES E ESTILOS ---
st.set_page_config(page_title="Sabor & Dados Analytics", layout="wide")
load_dotenv()

# CSS para deixar o visual moderno
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    .metric-card {
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin-bottom: 10px;
    }
    .title-text {
        font-family: 'Playfair Display', serif;
        color: #2A5B3E;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def autenticar_azure():
    endpoint = os.getenv("AZURE_AI_ENDPOINT")
    key = os.getenv("AZURE_AI_KEY")
    return TextAnalyticsClient(endpoint, AzureKeyCredential(key))

client_azure = autenticar_azure()

def extrair_comentarios_html():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")
        tags = soup.find_all("p", class_="texto-comentario")
        textos = [tag.get_text() for tag in tags]
        if not textos:
            textos = [
                "A comida estava absolutamente divina!", "Comida fria e serviço lento.", 
                "Pratos criativos e bem executados.", "Tiramisu aquoso e sem sabor.",
                "Preço justo, mas serviço lento.", "Experiência incrível!",
                "Melhor risoto da vida.", "Decoração de bom gosto.",
                "Barulho insuportável no salão.", "Taxa de reserva absurda.",
                "Carne veio crua.", "Restaurante ok.", "Prato principal normal."
            ]
        return textos
    except:
        st.stop()

def analisar_sentimentos(textos):
    dados_analisados = []
    tamanho_lote = 10
    for i in range(0, len(textos), tamanho_lote):
        lote = textos[i : i + tamanho_lote]
        response = client_azure.analyze_sentiment(documents=lote, language="pt")
        for j, doc in enumerate(response):
            dados_analisados.append({
                "Comentário": lote[j],
                "Sentimento": doc.sentiment.upper(),
                "Confiança": round(max(doc.confidence_scores.positive, doc.confidence_scores.negative, doc.confidence_scores.neutral) * 100, 1)
            })
    return pd.DataFrame(dados_analisados)

# --- INTERFACE ---
st.markdown("<h1 class='title-text'>🍽️ Sabor & Dados | Dashboard de Sentimentos</h1>", unsafe_allow_html=True)
st.markdown("---")

if st.button('🚀 Analisar Feedbacks do Site'):
    textos = extrair_comentarios_html()
    df = analisar_sentimentos(textos)

    # 1. LINHA DE MÉTRICAS (Cards Coloridos)
    total = len(df)
    pos = len(df[df['Sentimento'] == 'POSITIVE'])
    neg = len(df[df['Sentimento'] == 'NEGATIVE'])
    neu = len(df[df['Sentimento'] == 'NEUTRAL'])

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total de Avaliações", total)
    with m2:
        st.metric("✅ Positivas", pos, f"{int(pos/total*100)}%")
    with m3:
        st.metric("😡 Negativas", neg, f"{int(neg/total*100)}%", delta_color="inverse")
    with m4:
        st.metric("😐 Neutras", neu)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. ÁREA DE GRÁFICOS E TABELA
    col_esq, col_dir = st.columns([1, 1.5])

    with col_esq:
        st.markdown("### 📊 Distribuição")
        fig = px.pie(df, names='Sentimento', hole=0.5,
                     color='Sentimento',
                     color_discrete_map={'POSITIVE':'#2A5B3E', 'NEGATIVE':'#C53030', 'NEUTRAL':'#D4A762'})
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_dir:
        st.markdown("### 📝 Detalhes dos Comentários")
        
        # Colorir a tabela
        def highlight_sentimento(s):
            if s == 'POSITIVE': return 'background-color: #d1e7dd; color: #0f5132'
            if s == 'NEGATIVE': return 'background-color: #f8d7da; color: #842029'
            return 'background-color: #fff3cd; color: #664d03'

        st.dataframe(df.style.applymap(highlight_sentimento, subset=['Sentimento']), 
                     use_container_width=True, height=350)

    # 3. NOVO: Gráfico de Barras de Confiança
    st.markdown("### 📈 Nível de Confiança da IA")
    fig_bar = px.bar(df, x=df.index, y='Confiança', color='Sentimento',
                     color_discrete_map={'POSITIVE':'#2A5B3E', 'NEGATIVE':'#C53030', 'NEUTRAL':'#D4A762'},
                     labels={'index': 'ID do Comentário', 'Confiança': 'Confiança (%)'})
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.info("Pronto para começar! Clique no botão acima para rodar a IA nos 13 comentários.")