import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuração da Página ---
# Usar st.set_page_config é a primeira coisa a se fazer
st.set_page_config(
    page_title="Análise de Doença Cardíaca",
    page_icon="❤",
    layout="wide"
)

# --- Carregamento dos Modelos e Dados ---
# Usar @st.cache_data previne recarregar os modelos a cada clique
@st.cache_data
def carregar_arquivos():
    arquivos = {}
    try:
        # Modelo de Predição
        with open("modelo_heart.pkl", "rb") as f:
            arquivos["model"] = pickle.load(f)

        # Scaler (para as colunas numéricas)
        with open("scaler_heart.pkl", "rb") as f:
            arquivos["scaler"] = pickle.load(f)

        # Colunas de Treinamento (essencial para o 'reindex')
        with open("X_heart.pkl", "rb") as f:
            arquivos["X_cols"] = pickle.load(f).columns

        # CSV original (para EDA)
        arquivos["df_csv"] = pd.read_csv("heart.csv")

        # Tabela de Análise de Cluster
        arquivos["df_cluster"] = pd.read_csv("cluster_analysis_heart.csv")

    except FileNotFoundError as e:
        # --- CORREÇÃO APLICADA AQUI ---
        # O atributo correto é 'filename' (tudo minúsculo)
        st.error(f"Erro: Arquivo não encontrado: {e.filename}")
        st.write("Certifique-se de que os seguintes arquivos estão na mesma pasta do app.py e no seu GitHub:")
        st.write("modelo_heart.pkl, scaler_heart.pkl, X_heart.pkl, heart.csv, cluster_analysis_heart.csv")
        return None

    return arquivos

# Carregar tudo
arquivos = carregar_arquivos()

# --- Título Principal ---
st.title("❤ Projeto Final: Machine Learning Aplicado à Saúde")
st.write("Análise preditiva e exploratória de risco de Doença Cardíaca (Dataset UCI).")

# Se os arquivos não carregarem, parar o app aqui
if arquivos is None:
    st.stop()

# --- Abas para Organização ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Classificação (Predição Interativa)",
    "Clusterização (Perfis de Pacientes)",
    "Análise Exploratória (EDA)",
    "Resultados do Modelo"
])

# --- Aba 1: Classificação (Predição) ---
with tab1:
    st.header("Ferramenta de Predição de Risco Cardíaco")
    st.write("Insira os dados do paciente para prever o risco de doença cardíaca.")

    # Definir colunas para o scaler e dummies (baseado no notebook)
    numeric_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    categorical_features = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']

    # Criar colunas de layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Dados Numéricos")
        age = st.number_input("Idade", min_value=1, max_value=100, value=50, step=1)
        trestbps = st.number_input("Pressão Arterial em Repouso (trestbps)", min_value=50, max_value=250, value=120)
        chol = st.number_input("Colesterol Sérico (chol)", min_value=100, max_value=600, value=200)
        thalach = st.number_input("Batimento Cardíaco Máximo (thalach)", min_value=50, max_value=250, value=150)
        oldpeak = st.number_input("Depressão de ST (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, format="%.1f")

    with col2:
        st.subheader("Dados Categóricos")
        sex = st.selectbox("Sexo (sex)", [1, 0], format_func=lambda x: "1 - Masculino" if x == 1 else "0 - Feminino")
        cp = st.selectbox("Tipo de Dor no Peito (cp)", [0, 1, 2, 3])
        fbs = st.selectbox("Glicemia de Jejum > 120 mg/dl (fbs)", [1, 0], format_func=lambda x: "1 - Verdadeiro" if x == 1 else "0 - Falso")
        restecg = st.selectbox("Eletrocardiograma em Repouso (restecg)", [0, 1, 2])
        exang = st.selectbox("Angina Induzida por Exercício (exang)", [1, 0], format_func=lambda x: "1 - Sim" if x == 1 else "0 - Não")
        slope = st.selectbox("Inclinação do Pico do Exercício ST (slope)", [0, 1, 2])
        ca = st.selectbox("Nº de Vasos Principais Coloridos (ca)", [0, 1, 2, 3, 4])
        thal = st.se
