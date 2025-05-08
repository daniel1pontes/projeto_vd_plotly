import streamlit as st
import os
from paginas.painel_de_vendas import pagina_painel_de_vendas
from paginas.modelos_mais_vendidos import pagina_modelos_mais_vendidos
from paginas.faturamento_mensal import pagina_faturamento_mensal

st.set_page_config(page_title="Dashboard BMW", layout="wide")
st.sidebar.image("./imagens/bmw.png", use_column_width=True)
st.sidebar.title("Navegação")
pagina = st.sidebar.selectbox("Selecione a página", [
    "Painel de vendas",
    "Modelos mais vendidos",
    "Faturamento mensal"
    ],  
)

if pagina == "Painel de vendas":
    pagina_painel_de_vendas()
elif pagina == "Modelos mais vendidos":
    pagina_modelos_mais_vendidos()
elif pagina == "Faturamento mensal":
    pagina_faturamento_mensal()
    