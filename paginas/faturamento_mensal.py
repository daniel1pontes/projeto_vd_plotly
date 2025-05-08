import streamlit as st
import pandas as pd
import plotly.express as px
import os

def pagina_faturamento_mensal():
    st.title("Faturamento Mensal")
    
    try:
        # Caminhos
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dados_dir = os.path.join(base_dir, "dados")
        vendas_path = os.path.join(dados_dir, "vendas_bmw.csv")
        
        # Carregando dados
        vendas = pd.read_csv(vendas_path)
        vendas["data_venda"] = pd.to_datetime(vendas["data_venda"], errors='coerce')
        vendas = vendas.dropna(subset=["data_venda"])
        vendas["mes"] = vendas["data_venda"].dt.to_period("M").astype(str)
        
        # Faturamento mensal
        faturamento = (
            vendas
            .groupby("mes")["valor_venda"]
            .sum()
            .reset_index()
            .sort_values("mes")
        )
        
        # Diferenças
        faturamento["dif_valor"] = faturamento["valor_venda"].diff()
        faturamento["dif_pct"]   = faturamento["valor_venda"].pct_change() * 100
        
        # Arredondamentos
        faturamento["valor_venda"] = faturamento["valor_venda"].round(2)
        faturamento["dif_valor"]   = faturamento["dif_valor"].round(2)
        faturamento["dif_pct"]     = faturamento["dif_pct"].round(2)
        
        # Strings formatadas
        
        
        # Gráfico de linha
        fig = px.line(
            faturamento,
            x="mes",
            y="valor_venda",
            title="Faturamento Mensal (R$)",
            labels={"mes": "Mês", "valor_venda": "Faturamento (R$)"},
            markers=True
        )
        fig.update_traces(
            texttemplate="R$ %{y:,.2f}",
            textposition="top center",
            line=dict(width=2.5),
            marker=dict(size=8)
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            hovermode="x unified",
            yaxis_tickprefix="R$ ",
            yaxis_tickformat=",.2f",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela com variações
        st.subheader("Dados Detalhados")
        faturamento["Faturamento"]    = faturamento["valor_venda"].map("R${:,.2f}".format)
        faturamento["Δ Valor (R$)"]   = faturamento["dif_valor"].map(
            lambda x: f"R${x:,.2f}" if pd.notna(x) else "—"
        )
        faturamento["Δ Percentual"]   = faturamento["dif_pct"].map(
            lambda x: f"{x:.2f} %" if pd.notna(x) else "—"
        )
        st.dataframe(
            faturamento[["mes", "Faturamento", "Δ Valor (R$)", "Δ Percentual"]],
            column_config={
                "mes": "Mês",
                "Faturamento": "Faturamento",
                "Δ Valor (R$)": "Variação (R$)",
                "Δ Percentual": "Variação (%)"
            },
            hide_index=True,
            use_container_width=True
        )
        
    except FileNotFoundError:
        st.error("Arquivo de vendas não encontrado!")
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
