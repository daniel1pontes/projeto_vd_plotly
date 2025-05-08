import streamlit as st
import pandas as pd
import plotly.express as px
import os

def pagina_modelos_mais_vendidos():
    st.title("Modelos Mais Vendidos")
    
    try:
        # Caminhos
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dados_dir = os.path.join(base_dir, "dados")
        
        # Carregando os dados
        vendas = pd.read_csv(os.path.join(dados_dir, "vendas_bmw.csv"))
        carros = pd.read_csv(os.path.join(dados_dir, "carros_bmw.csv"))
        
        # Merge dos dataframes
        df = vendas.merge(carros, left_on="id_carro", right_on="id_carro")

        # Contando vendas por modelo
        vendas_por_modelo = df["modelo"].value_counts().reset_index()
        vendas_por_modelo.columns = ["modelo", "quantidade_vendida"]
        
        # Ordenando
        vendas_por_modelo = vendas_por_modelo.sort_values("quantidade_vendida", ascending=False)
        
        # Criando o gráfico
        fig = px.bar(
            vendas_por_modelo, 
            x="modelo", 
            y="quantidade_vendida", 
            title="Top Modelos Mais Vendidos",
            labels={'quantidade_vendida': 'Quantidade Vendida', 'modelo': 'Modelo BMW'},
            color="quantidade_vendida",
            color_continuous_scale='Blues'
        )
        
        # Formatando o gráfico
        fig.update_layout(
            xaxis_tickangle=-45,
            hovermode="x unified",
            yaxis_title="Quantidade Vendida",
            xaxis_title="",
            coloraxis_showscale=False
        )
        
        fig.update_traces(texttemplate='%{y}', textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela
        st.subheader("Dados Detalhados")

        media_vendas = (df.groupby("modelo")["valor_venda"].mean().round(2).reset_index().rename(columns={"valor_venda": "valor_medio"}))

        # Junta média à tabela de quantidade
        tabela = vendas_por_modelo.merge(media_vendas, on="modelo")
        
        # Formata colunas
        tabela["Valor médio (R$)"] = tabela["valor_medio"].map("R${:,.2f}".format)
        
        # Exibe com gradiente na quantidade
        st.dataframe(
            tabela[["modelo", "quantidade_vendida", "Valor médio (R$)"]]
                .style.background_gradient(
                    cmap='Blues',
                    subset=['quantidade_vendida']
                ),
            column_config={
                "modelo": "Modelo",
                "quantidade_vendida": "Quantidade vendida",
                "Valor médio (R$)": "Valor médio"
            },
            hide_index=True,
            use_container_width=True
        )
        
    except FileNotFoundError:
        st.error("Arquivos de dados não encontrados!")
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")