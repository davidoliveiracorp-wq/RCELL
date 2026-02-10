# -*- coding: utf-8 -*-
"""
Dashboard BI - União de planilhas com upload e atualização
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import io

st.set_page_config(
    page_title="Dashboard BI - RCELL",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Nomes padrão dos arquivos na pasta do projeto
ARQUIVO_A_VENCER = Path(__file__).parent / "A vencer até 28-02.xls"
ARQUIVO_PAGOS = Path(__file__).parent / "Pagos até 10-02.xls"


def carregar_excel(arquivo, engine=None):
    """Carrega Excel .xls ou .xlsx."""
    if engine is None:
        engine = "xlrd" if str(arquivo).lower().endswith(".xls") else "openpyxl"
    return pd.read_excel(arquivo, engine=engine)


def carregar_dados():
    """Carrega as duas planilhas (da pasta ou dos uploads em data/)."""
    # Preferir arquivos em data/ (atualizados por upload)
    a_vencer_path = DATA_DIR / "a_vencer.xls"
    if not a_vencer_path.exists():
        a_vencer_path = DATA_DIR / "a_vencer.xlsx"
    if not a_vencer_path.exists():
        a_vencer_path = ARQUIVO_A_VENCER

    pagos_path = DATA_DIR / "pagos.xls"
    if not pagos_path.exists():
        pagos_path = DATA_DIR / "pagos.xlsx"
    if not pagos_path.exists():
        pagos_path = ARQUIVO_PAGOS

    dfs = []
    if a_vencer_path.exists():
        try:
            df_vencer = carregar_excel(a_vencer_path)
            df_vencer["Origem"] = "A vencer"
            dfs.append(df_vencer)
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar 'A vencer': {e}")

    if pagos_path.exists() and pagos_path != a_vencer_path:
        try:
            df_pagos = carregar_excel(pagos_path)
            df_pagos["Origem"] = "Pagos"
            dfs.append(df_pagos)
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar 'Pagos': {e}")

    if not dfs:
        return None
    return pd.concat(dfs, ignore_index=True)


def detectar_coluna_valor(df):
    """Detecta coluna que parece valor monetário."""
    for c in df.columns:
        s = df[c].dropna()
        if len(s) == 0:
            continue
        try:
            n = pd.to_numeric(s, errors="coerce")
            if n.notna().sum() / len(s) > 0.5 and (n.abs() > 0.01).any():
                return c
        except Exception:
            pass
    return None


def detectar_colunas_data(df):
    """Lista colunas que parecem datas."""
    datas = []
    for c in df.columns:
        try:
            if pd.to_datetime(df[c], errors="coerce").notna().sum() > 0:
                datas.append(c)
        except Exception:
            pass
    return datas


def main():
    st.title("📊 Dashboard BI - União de planilhas")
    st.markdown("Visualize e analise os dados unificados das planilhas **A vencer** e **Pagos**.")

    # ---- Sidebar: Upload ----
    with st.sidebar:
        st.header("📁 Atualizar dados")
        st.caption("Envie novas planilhas para substituir os dados exibidos.")

        upload_vencer = st.file_uploader(
            "Planilha **A vencer**",
            type=["xls", "xlsx"],
            key="vencer"
        )
        upload_pagos = st.file_uploader(
            "Planilha **Pagos**",
            type=["xls", "xlsx"],
            key="pagos"
        )

        if upload_vencer:
            buf = io.BytesIO(upload_vencer.getvalue())
            ext = Path(upload_vencer.name).suffix.lower()
            path_salvar = DATA_DIR / f"a_vencer{ext}"
            path_salvar.write_bytes(buf.read())
            st.success("Planilha 'A vencer' atualizada.")

        if upload_pagos:
            buf = io.BytesIO(upload_pagos.getvalue())
            ext = Path(upload_pagos.name).suffix.lower()
            path_salvar = DATA_DIR / f"pagos{ext}"
            path_salvar.write_bytes(buf.read())
            st.success("Planilha 'Pagos' atualizada.")

        st.divider()
        st.caption("Dados carregados da pasta do projeto ou dos arquivos enviados acima.")

    # ---- Carregar e unir dados ----
    df = carregar_dados()
    if df is None or df.empty:
        st.warning("Nenhuma planilha encontrada. Coloque os arquivos na pasta do projeto ou use o upload ao lado.")
        return

    # Coluna de valor para métricas
    col_valor = detectar_coluna_valor(df)
    colunas_data = detectar_colunas_data(df)

    # ---- Filtros ----
    st.sidebar.header("🔍 Filtros")
    origem_sel = st.sidebar.multiselect(
        "Origem",
        options=df["Origem"].unique().tolist(),
        default=df["Origem"].unique().tolist()
    )
    df_f = df[df["Origem"].isin(origem_sel)].copy()

    # Filtro por primeira coluna de texto (ex.: fornecedor, descrição)
    colunas_texto = [c for c in df_f.columns if c != "Origem" and c not in (colunas_data or []) and (col_valor is None or c != col_valor)]
    if colunas_texto:
        primeira_texto = colunas_texto[0]
        opcoes = ["Todos"] + sorted(df_f[primeira_texto].dropna().astype(str).unique().tolist())[:200]
        filtro_texto = st.sidebar.selectbox(f"Filtrar por {primeira_texto}", opcoes)
        if filtro_texto != "Todos":
            df_f = df_f[df_f[primeira_texto].astype(str) == filtro_texto]

    # ---- KPIs ----
    st.subheader("Resumo")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total de registros", len(df_f))
    with k2:
        st.metric("A vencer", (df_f["Origem"] == "A vencer").sum())
    with k3:
        st.metric("Pagos", (df_f["Origem"] == "Pagos").sum())
    with k4:
        if col_valor:
            total = pd.to_numeric(df_f[col_valor], errors="coerce").sum()
            st.metric(f"Total ({col_valor})", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        else:
            st.metric("Coluna valor", "Não detectada")

    # ---- Gráficos ----
    st.subheader("Visualizações")
    c1, c2 = st.columns(2)

    with c1:
        # Gráfico por Origem
        contagem_origem = df_f["Origem"].value_counts().reset_index()
        contagem_origem.columns = ["Origem", "Quantidade"]
        fig_origem = px.pie(contagem_origem, values="Quantidade", names="Origem", title="Registros por origem")
        st.plotly_chart(fig_origem, use_container_width=True)

    with c2:
        if col_valor:
            valor_origem = df_f.groupby("Origem")[col_valor].apply(
                lambda x: pd.to_numeric(x, errors="coerce").sum()
            ).reset_index()
            valor_origem.columns = ["Origem", "Total"]
            fig_valor = px.bar(valor_origem, x="Origem", y="Total", title=f"Total por origem ({col_valor})")
            st.plotly_chart(fig_valor, use_container_width=True)
        else:
            # Segundo gráfico: barras por primeira coluna de texto (top N)
            if colunas_texto:
                top = df_f[primeira_texto].value_counts().head(10).reset_index()
                top.columns = [primeira_texto, "Quantidade"]
                fig_top = px.bar(top, x=primeira_texto, y="Quantidade", title=f"Top 10 - {primeira_texto}")
                st.plotly_chart(fig_top, use_container_width=True)

    # Gráfico de barras por categoria (primeira coluna texto) e valor
    if col_valor and colunas_texto:
        st.subheader(f"Valores por {primeira_texto}")
        agg = df_f.groupby(primeira_texto)[col_valor].apply(
            lambda x: pd.to_numeric(x, errors="coerce").sum()
        ).reset_index()
        agg.columns = [primeira_texto, "Total"]
        agg = agg.nlargest(15, "Total")
        fig_cat = px.bar(agg, x=primeira_texto, y="Total", title=f"Top 15 por valor - {primeira_texto}")
        fig_cat.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_cat, use_container_width=True)

    # ---- Tabela ----
    st.subheader("Dados unificados")
    st.dataframe(df_f, use_container_width=True, height=400)

    # Download do merge
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_f.to_excel(writer, index=False, sheet_name="Dados_unificados")
    st.download_button(
        label="📥 Baixar dados unificados (Excel)",
        data=buffer.getvalue(),
        file_name="dados_unificados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


if __name__ == "__main__":
    main()
