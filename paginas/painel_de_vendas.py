import streamlit as st
import pandas as pd
import plotly.express as px
import os

def pagina_painel_de_vendas():
    st.title("Painel de vendas")
    
    try:
        # Caminhos
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dados_dir = os.path.join(base_dir, "dados")
        
        # Carregando os dados
        vendas = pd.read_csv(os.path.join(dados_dir, "vendas_bmw.csv"))
        vendedores = pd.read_csv(os.path.join(dados_dir, "vendedores_bmw.csv"))
        carros = pd.read_csv(os.path.join(dados_dir, "carros_bmw.csv"))

        # Merge dos dataframes
        df = vendas.merge(vendedores, left_on="id_vendedor", right_on="id_vendedor")
        df = df.merge(carros, left_on="id_carro", right_on="id_carro")

        # Melhores vendedores
        st.subheader("Top 3 Vendedores")

        vendas_por_vendedor = df.groupby('nome').agg(
            total_vendas=('id_venda', 'count'),
            faturamento_total=('valor_venda', 'sum')
        ).sort_values('faturamento_total', ascending=False).reset_index()

        # Top 3 vendedores
        cols = st.columns(3)
        for i, (_, row) in enumerate(vendas_por_vendedor.head(3).iterrows()):
            with cols[i]:
                st.metric(
                    label=f"{'🥇' if i==0 else '🥈' if i==1 else '🥉'} {row['nome']}",
                    value=f"R${row['faturamento_total']:,.2f}",
                    help=f"{row['total_vendas']} vendas"
                )

        st.subheader("Vendas por vendedor")

        # Seleção do vendedor
        vendedor = st.selectbox("Selecione um vendedor", df["nome"].unique())     
        filtrado = df[df["nome"] == vendedor]
        
        # Exibindo informações do vendedor
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Vendas", len(filtrado))
        with col2:
            st.metric("Faturamento Total", f"R${filtrado['valor_venda'].sum():,.2f}")
        with col3:
            modelo_mais_vendido = filtrado["modelo"].mode()[0]
            st.metric("Modelo mais vendido", modelo_mais_vendido)
        
        # Gráfico de vendas por data
        fig1 = px.bar(
            filtrado.sort_values("data_venda"),
            x="data_venda",
            y="valor_venda",
            title=f"Vendas por Data - {vendedor}",
            labels={'valor_venda': 'Valor (R$)', 'data_venda': 'Data da Venda'}
        )
        fig1.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico de vendas por modelo
        vendas_por_modelo = filtrado["modelo"].value_counts().reset_index()
        fig2 = px.pie(
            vendas_por_modelo,
            names="modelo",
            values="count",
            title=f"Modelos vendidos por - {vendedor}"
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Tabela detalhada
        st.subheader("Detalhes das Vendas")
        st.dataframe(filtrado[["data_venda", "valor_venda", "forma_pagamento", "modelo", "cor"]]
                    .sort_values("data_venda", ascending=False)
                    .style.format({'valor_venda': "R${:,.2f}"}),
                    column_config={
                        "data_venda": "Data",
                        "valor_venda": "Valor (R$)",
                        "forma_pagamento": "Pagamento",
                        "modelo": "Modelo", 
                        "cor": "Cor"
                        },
                    hide_index=True,
                    use_container_width=True)
        
    except FileNotFoundError:
        st.error("Arquivos de dados não encontrados!")
    except Exception as e:
        st.error(f"Ocorreu um erro: {str(e)}")