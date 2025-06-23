# app.py
# Responsabilidade: Criar a interface de usuário com Streamlit e orquestrar as classes.

import streamlit as st
from streamlit_folium import st_folium
from FWD import FWD
from map_creator import Map
import os

# --- Configuração da Página e Título ---
st.set_page_config(layout="wide")
st.title("🗺️ Análise de Deflectometria (FWD)")
st.markdown("Aplicação para visualização interativa dos resultados de ensaios de FWD.")

# --- Função de Carregamento com Cache de Dados ---
@st.cache_data
def carregar_e_processar_dados():
    """
    Cache ativado: Esta função executa o processamento pesado apenas uma vez,
    tornando a aplicação muito mais rápida em interações subsequentes.
    """
    # Usa o caminho do script para encontrar a pasta de dados de forma relativa
    root_path = os.path.dirname(os.path.abspath(__file__))
    try:
        project_path = root_path.split("src")[0]
    except IndexError:
        project_path = root_path
    caminho_dados = os.path.join(project_path, "FWD")
    
    if not os.path.isdir(caminho_dados):
        st.error(f"ERRO: Diretório de dados não encontrado em: '{caminho_dados}'.")
        return None

    fwd_analyzer = FWD(caminho_dados)
    fwd_analyzer.process()
    return fwd_analyzer

# --- Lógica Principal da Aplicação ---
fwd_data = carregar_e_processar_dados()

if fwd_data is None:
    st.stop() # Interrompe a execução se os dados não foram carregados

# --- Controles da Barra Lateral ---
st.sidebar.success("Dados carregados com sucesso!")
st.sidebar.header("Parâmetros de Análise")

traffic_level = st.sidebar.selectbox(
    "1. Selecione o Nível de Tráfego:",
    options=["N10^7", "N10^6"]
)

analysis_type = st.sidebar.selectbox(
    "2. Selecione o Tipo de Análise:",
    options=list(fwd_data.conditionals[traffic_level].keys())
)

lista_ruas = ["Selecione uma rua..."] + list(fwd_data.dict.keys())
selected_street = st.sidebar.selectbox(
    "3. Selecione a Rua:",
    options=lista_ruas
)

# --- Lógica de Exibição do Mapa ---
if selected_street != "Selecione uma rua...":
    street_data = fwd_data.dict.get(selected_street)
    
    if street_data:
        # A cada interação nos menus, uma nova instância da classe Map é criada
        map_creator = Map(street_data, analysis_type, traffic_level)
        # O método .plot() gera o mapa do zero com os filtros corretos
        mapa_gerado = map_creator.plot()
        
        # Exibe o mapa no Streamlit, impedindo que o mapa dispare re-execuções
        st_folium(
            mapa_gerado, 
            key="folium_map_final", 
            use_container_width=True,
            returned_objects=[] # Essencial para performance
        )
    else:
        st.warning(f"Não foram encontrados dados para a rua '{selected_street}'.")
else:
    st.info("Por favor, selecione os parâmetros na barra lateral para visualizar a análise.")