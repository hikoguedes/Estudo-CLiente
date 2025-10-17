import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Campanha - Voo de Balão",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .positive-metric {
        border-left: 4px solid #2ecc71;
    }
    .negative-metric {
        border-left: 4px solid #e74c3c;
    }
    .conversion-funnel {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Função para limpar valores monetários
def clean_currency_value(value):
    if isinstance(value, str):
        # Remove R$, espaços não quebráveis (\xa0) e pontos de milhar
        cleaned = value.replace('R$', '').replace('\xa0', '').replace(' ', '').replace('.', '')
        # Substitui vírgula decimal por ponto
        cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return float(value) if pd.notna(value) else 0.0

# Função para limpar porcentagens
def clean_percentage(value):
    if isinstance(value, str):
        cleaned = value.replace('%', '').replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return float(value) if pd.notna(value) else 0.0

# Função para limpar números com separadores de milhar
def clean_number(value):
    if isinstance(value, str):
        cleaned = value.replace('.', '').replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    return float(value) if pd.notna(value) else 0.0

# Carregar dados
@st.cache_data
def load_data():
    # Dados principais
    campanhas = pd.read_csv('Campanhas(2025.04.10-2025.10.17).csv')
    dispositivos = pd.read_csv('Dispositivos(2025.04.10-2025.10.17).csv')
    idade = pd.read_csv('Informações_demográficas(Idade_2025.04.10-2025.10.17).csv')
    sexo = pd.read_csv('Informações_demográficas(Sexo_2025.04.10-2025.10.17).csv')
    sexo_idade = pd.read_csv('Informações_demográficas(Sexo_Idade_2025.04.10-2025.10.17).csv')
    palavras_chave = pd.read_csv('Palavras-chave_de_pesquisa(2025.04.10-2025.10.17).csv')
    pesquisas = pd.read_csv('Pesquisas(Pesquisar_2025.04.10-2025.10.17).csv')
    serie_temporal = pd.read_csv('Série_temporal(2025.04.07-2025.10.17).csv')
    redes = pd.read_csv('Redes(2025.04.10-2025.10.17).csv')
    dia_hora = pd.read_csv('Dia_e_hora(Dia_2025.04.10-2025.10.17).csv')
    hora = pd.read_csv('Dia_e_hora(Hora_2025.04.10-2025.10.17).csv')
    dia_hora_detalhado = pd.read_csv('Dia_e_hora(Dia_Hora_2025.04.10-2025.10.17).csv')
    
    # Limpar dados monetários e numéricos
    # Campanhas
    campanhas['Custo_num'] = campanhas['Custo'].apply(clean_currency_value)
    campanhas['Cliques_num'] = campanhas['Cliques'].apply(clean_number)
    campanhas['CTR_num'] = campanhas['CTR'].apply(clean_percentage)
    
    # Dispositivos
    dispositivos['Custo_num'] = dispositivos['Custo'].apply(clean_currency_value)
    dispositivos['Impressões_num'] = dispositivos['Impressões'].apply(clean_number)
    dispositivos['Cliques_num'] = dispositivos['Cliques'].apply(clean_number)
    
    # Palavras-chave
    palavras_chave['Custo_num'] = palavras_chave['Custo'].apply(clean_currency_value)
    palavras_chave['Cliques_num'] = palavras_chave['Cliques'].apply(clean_number)
    palavras_chave['CTR_num'] = palavras_chave['CTR'].apply(clean_percentage)
    
    # Pesquisas
    pesquisas['Custo_num'] = pesquisas['Custo'].apply(clean_currency_value)
    pesquisas['Cliques_num'] = pesquisas['Cliques'].apply(clean_number)
    pesquisas['Impressões_num'] = pesquisas['Impressões'].apply(clean_number)
    pesquisas['Conversões_num'] = pesquisas['Conversões'].apply(clean_number)
    
    # Série temporal
    serie_temporal['Custo_num'] = serie_temporal['Custo'].apply(clean_currency_value)
    serie_temporal['Cliques_num'] = serie_temporal['Cliques'].apply(clean_number)
    serie_temporal['Impressões_num'] = serie_temporal['Impressões'].apply(clean_number)
    serie_temporal['CPC_num'] = serie_temporal['CPC méd.'].apply(clean_currency_value)
    
    # Redes
    redes['Custo_num'] = redes['Custo'].apply(clean_currency_value)
    redes['Cliques_num'] = redes['Cliques'].apply(clean_number)
    redes['CPC_num'] = redes['CPC méd.'].apply(clean_currency_value)
    
    # Dia e hora
    dia_hora['Impressões_num'] = dia_hora['Impressões'].apply(clean_number)
    hora['Impressões_num'] = hora['Impressões'].apply(clean_number)
    dia_hora_detalhado['Impressões_num'] = dia_hora_detalhado['Impressões'].apply(clean_number)
    
    # Limpar dados demográficos
    idade['Impressões_num'] = idade['Impressões'].apply(clean_number)
    idade['Porcentagem_num'] = idade['Porcentagem do total conhecido'].apply(clean_percentage)
    
    sexo['Impressões_num'] = sexo['Impressões'].apply(clean_number)
    sexo['Porcentagem_num'] = sexo['Porcentagem do total conhecido'].apply(clean_percentage)
    
    sexo_idade['Impressões_num'] = sexo_idade['Impressões'].apply(clean_number)
    sexo_idade['Porcentagem_num'] = sexo_idade['Porcentagem do total conhecido'].apply(clean_percentage)
    
    return {
        'campanhas': campanhas,
        'dispositivos': dispositivos,
        'idade': idade,
        'sexo': sexo,
        'sexo_idade': sexo_idade,
        'palavras_chave': palavras_chave,
        'pesquisas': pesquisas,
        'serie_temporal': serie_temporal,
        'redes': redes,
        'dia_hora': dia_hora,
        'hora': hora,
        'dia_hora_detalhado': dia_hora_detalhado
    }

data = load_data()

# Sidebar
st.sidebar.title("📊 Filtros")
st.sidebar.markdown("---")

# Métricas principais na sidebar
total_impressoes = data['dia_hora']['Impressões_num'].sum()
total_cliques = data['campanhas']['Cliques_num'].sum()
total_custo = data['campanhas']['Custo_num'].sum()
ctr_medio = (total_cliques / total_impressoes * 100) if total_impressoes > 0 else 0
cpc_medio = total_custo / total_cliques if total_cliques > 0 else 0

st.sidebar.metric("Total de Impressões", f"{total_impressoes:,.0f}")
st.sidebar.metric("Total de Cliques", f"{total_cliques:,.0f}")
st.sidebar.metric("CTR Médio", f"{ctr_medio:.2f}%")
st.sidebar.metric("Custo Total", f"R$ {total_custo:,.2f}")

# Layout principal
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Visão Geral", 
    "🎯 Público-Alvo", 
    "🔍 Palavras-chave", 
    "📱 Dispositivos & Redes",
    "🔄 Conversões",
    "💡 Recomendações"
])

with tab1:
    st.subheader("📊 Performance Geral da Campanha (Abril - Outubro 2025)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card positive-metric">', unsafe_allow_html=True)
        st.metric("Pontuação de Otimização", "86,2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Custo por Clique (CPC)", f"R$ {cpc_medio:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card negative-metric">', unsafe_allow_html=True)
        st.metric("Conversões", "0")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card positive-metric">', unsafe_allow_html=True)
        st.metric("CTR da Campanha", "3,41%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Gráficos de série temporal
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance semanal
        semanas_ativas = data['serie_temporal'][data['serie_temporal']['Cliques_num'] > 0]
        if not semanas_ativas.empty:
            fig = px.line(semanas_ativas, x='Semana', y='Cliques_num',
                         title='Evolução de Cliques por Semana',
                         markers=True)
            fig.update_layout(xaxis_title='Semana', yaxis_title='Cliques', xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Custo semanal
        if not semanas_ativas.empty:
            fig = px.bar(semanas_ativas, x='Semana', y='Custo_num',
                        title='Custo por Semana (R$)',
                        color='Custo_num',
                        color_continuous_scale='reds')
            fig.update_layout(xaxis_title='Semana', yaxis_title='Custo (R$)', xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # Gráficos de distribuição temporal
    col1, col2 = st.columns(2)
    
    with col1:
        # Impressões por hora
        fig = px.bar(data['hora'], x='Hora de início', y='Impressões_num', 
                    title='Distribuição de Impressões por Hora do Dia',
                    color='Impressões_num',
                    color_continuous_scale='blues')
        fig.update_layout(xaxis_title='Hora', yaxis_title='Impressões')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Impressões por dia da semana
        fig = px.bar(data['dia_hora'], x='Dia', y='Impressões_num',
                    title='Impressões por Dia da Semana',
                    color='Impressões_num',
                    color_continuous_scale='greens')
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise de sazonalidade
    st.subheader("📈 Análise de Sazonalidade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Período Ativo", f"{len(semanas_ativas)} semanas")
        st.metric("Primeira Semana Ativa", "14 de Julho 2025")
        st.metric("Média Cliques/Semana", f"{semanas_ativas['Cliques_num'].mean():.0f}")
    
    with col2:
        st.metric("Total de Semanas", f"{len(data['serie_temporal'])}")
        st.metric("Semanas sem Dados", f"{len(data['serie_temporal']) - len(semanas_ativas)}")
        st.metric("Pico de Cliques", f"{semanas_ativas['Cliques_num'].max():.0f}")

with tab2:
    st.subheader("🎯 Análise Demográfica Detalhada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por Idade
        fig = px.pie(data['idade'], values='Impressões_num', names='Faixa de idade',
                    title='Distribuição por Faixa Etária',
                    hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribuição por Sexo
        fig = px.pie(data['sexo'], values='Impressões_num', names='Sexo',
                    title='Distribuição por Sexo',
                    hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sexo e Idade combinados
        fig = px.bar(data['sexo_idade'], x='Faixa de idade', y='Impressões_num', color='Sexo',
                    title='Impressões por Sexo e Faixa Etária',
                    barmode='group')
        fig.update_layout(xaxis_title='Faixa Etária', yaxis_title='Impressões')
        st.plotly_chart(fig, use_container_width=True)
        
        # Métricas demográficas
        st.subheader("📋 Insights Demográficos")
        
        maior_faixa = data['idade'].loc[data['idade']['Impressões_num'].idxmax()]
        maior_sexo = data['sexo'].loc[data['sexo']['Impressões_num'].idxmax()]
        
        st.success(f"""
        **🎯 Público Principal:**
        - **Sexo:** {maior_sexo['Sexo']} ({maior_sexo['Porcentagem_num']:.1f}%)
        - **Faixa Etária:** {maior_faixa['Faixa de idade']} ({maior_faixa['Porcentagem_num']:.1f}%)
        - **Segmento Mais Engajado:** Mulheres 25-34 anos (25.53%)
        - **Jovens 18-24:** 37.70% do total
        """)
    
    # Análise de engajamento por demografia
    st.subheader("📊 Engajamento por Segmento Demográfico")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mulheres_25_34 = data['sexo_idade'][
            (data['sexo_idade']['Sexo'] == 'Feminino') & 
            (data['sexo_idade']['Faixa de idade'] == '25 a 34')
        ]['Impressões_num'].iloc[0]
        st.metric("Mulheres 25-34", f"{mulheres_25_34:,}", "25.53%")
    
    with col2:
        jovens_18_24 = data['idade'][data['idade']['Faixa de idade'] == '18 a 24']['Impressões_num'].iloc[0]
        st.metric("Jovens 18-24", f"{jovens_18_24:,}", "37.70%")
    
    with col3:
        mulheres_18_24 = data['sexo_idade'][
            (data['sexo_idade']['Sexo'] == 'Feminino') & 
            (data['sexo_idade']['Faixa de idade'] == '18 a 24')
        ]['Impressões_num'].iloc[0]
        st.metric("Mulheres 18-24", f"{mulheres_18_24:,}", "19.11%")

with tab3:
    st.subheader("🔍 Análise de Palavras-chave e Pesquisas")
    
    # Palavras-chave com desempenho
    palavras_ativas = data['palavras_chave'][data['palavras_chave']['Cliques_num'] > 0]
    palavras_sem_cliques = data['palavras_chave'][data['palavras_chave']['Cliques_num'] == 0]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Palavras-chave", len(data['palavras_chave']))
    
    with col2:
        st.metric("Com Cliques", len(palavras_ativas))
    
    with col3:
        st.metric("Sem Cliques", len(palavras_sem_cliques))
    
    with col4:
        taxa_sem_cliques = (len(palavras_sem_cliques) / len(data['palavras_chave'])) * 100
        st.metric("Taxa Ineficientes", f"{taxa_sem_cliques:.1f}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top palavras-chave por CTR
        if not palavras_ativas.empty:
            top_ctr = palavras_ativas.nlargest(10, 'CTR_num')
            fig = px.bar(top_ctr, 
                        x='Palavra-chave da rede de pesquisa', y='CTR_num',
                        title='Top 10 Palavras-chave por CTR (%)',
                        color='CTR_num',
                        color_continuous_scale='viridis')
            fig.update_layout(yaxis_title='CTR (%)', xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top palavras-chave por cliques
        if not palavras_ativas.empty:
            top_cliques = palavras_ativas.nlargest(10, 'Cliques_num')
            fig = px.bar(top_cliques, 
                        x='Palavra-chave da rede de pesquisa', y='Cliques_num',
                        title='Top 10 Palavras-chave por Cliques',
                        color='Cliques_num',
                        color_continuous_scale='blues')
            fig.update_layout(yaxis_title='Cliques', xaxis_tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # Análise de eficiência
    st.subheader("💰 Análise de Eficiência por Palavra-chave")
    
    if not palavras_ativas.empty:
        palavras_ativas['Custo_por_Clique'] = palavras_ativas['Custo_num'] / palavras_ativas['Cliques_num']
        
        fig = px.scatter(palavras_ativas, x='Custo_por_Clique', y='CTR_num',
                        size='Cliques_num', color='Custo_num',
                        hover_name='Palavra-chave da rede de pesquisa',
                        title='Relação Custo/Clique vs CTR',
                        labels={'Custo_por_Clique': 'Custo por Clique (R$)', 'CTR_num': 'CTR (%)'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Top pesquisas reais
    st.subheader("🔎 Top Pesquisas dos Usuários")
    
    if 'Cliques_num' in data['pesquisas'].columns:
        top_pesquisas = data['pesquisas'].nlargest(10, 'Cliques_num')
        fig = px.bar(top_pesquisas, x='Pesquisar', y='Cliques_num',
                    title='Top 10 Pesquisas por Cliques',
                    color='Cliques_num',
                    color_continuous_scale='purples')
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("📱 Análise por Dispositivos e Redes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Dispositivos - Impressões
        fig = px.pie(data['dispositivos'], values='Impressões_num', names='Dispositivo',
                    title='Distribuição por Dispositivo - Impressões')
        st.plotly_chart(fig, use_container_width=True)
        
        # Dispositivos - Custo
        fig = px.bar(data['dispositivos'], x='Dispositivo', y='Custo_num',
                    title='Custo por Dispositivo (R$)',
                    color='Custo_num',
                    color_continuous_scale='greens')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Redes - Cliques
        fig = px.bar(data['redes'], x='Rede', y='Cliques_num',
                    title='Cliques por Rede',
                    color='Cliques_num',
                    color_continuous_scale='purples')
        st.plotly_chart(fig, use_container_width=True)
        
        # CPC por rede
        fig = px.bar(data['redes'], x='Rede', y='CPC_num',
                    title='CPC Médio por Rede (R$)',
                    color='CPC_num',
                    color_continuous_scale='oranges')
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise de eficiência por dispositivo
    st.subheader("📊 Eficiência por Dispositivo")
    
    data['dispositivos']['CTR'] = (data['dispositivos']['Cliques_num'] / data['dispositivos']['Impressões_num'] * 100).fillna(0)
    data['dispositivos']['Custo_por_Clique'] = data['dispositivos']['Custo_num'] / data['dispositivos']['Cliques_num'].replace(0, 1)
    
    fig = px.scatter(data['dispositivos'], x='Custo_por_Clique', y='CTR',
                    size='Impressões_num', color='Dispositivo',
                    title='Eficiência: Custo por Clique vs CTR por Dispositivo',
                    labels={'Custo_por_Clique': 'Custo por Clique (R$)', 'CTR': 'CTR (%)'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights de dispositivos
    st.subheader("💡 Insights de Dispositivos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        smartphone_impressoes = data['dispositivos'][data['dispositivos']['Dispositivo'] == 'Smartphones']['Impressões_num'].iloc[0]
        smartphone_percentual = (smartphone_impressoes / total_impressoes) * 100
        st.metric("Smartphones", f"{smartphone_percentual:.1f}%", "96.8% das impressões")
    
    with col2:
        smartphone_custo = data['dispositivos'][data['dispositivos']['Dispositivo'] == 'Smartphones']['Custo_num'].iloc[0]
        st.metric("Custo Smartphones", f"R$ {smartphone_custo:,.2f}", f"{(smartphone_custo/total_custo*100):.1f}% do total")
    
    with col3:
        ctr_smartphones = (data['dispositivos'][data['dispositivos']['Dispositivo'] == 'Smartphones']['Cliques_num'].iloc[0] / smartphone_impressoes) * 100
        st.metric("CTR Smartphones", f"{ctr_smartphones:.2f}%")

with tab5:
    st.header("🔄 Análise de Conversões")
    
    # Métricas de conversão
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card negative-metric">', unsafe_allow_html=True)
        st.metric("Total de Conversões", "0")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        taxa_conversao = 0
        st.markdown('<div class="metric-card negative-metric">', unsafe_allow_html=True)
        st.metric("Taxa de Conversão", f"{taxa_conversao:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        custo_por_conversao = total_custo if taxa_conversao == 0 else 0
        st.markdown('<div class="metric-card negative-metric">', unsafe_allow_html=True)
        st.metric("Custo por Conversão", f"R$ {custo_por_conversao:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card negative-metric">', unsafe_allow_html=True)
        st.metric("ROAS", "0%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Funnel de conversão atual
    st.subheader("📊 Funil de Conversão Atual")
    
    funnel_data = pd.DataFrame({
        'Estágio': ['Impressões', 'Cliques', 'Visitantes Site', 'Leads', 'Clientes'],
        'Quantidade': [total_impressoes, total_cliques, 0, 0, 0],
        'Taxa Conversão': [100, (total_cliques/total_impressoes*100), 0, 0, 0]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.funnel(funnel_data, x='Quantidade', y='Estágio', 
                       title='Funil de Conversão - Quantidade',
                       color='Estágio')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(funnel_data, x='Taxa Conversão', y='Estágio',
                    title='Taxa de Conversão por Estágio (%)',
                    orientation='h',
                    color='Estágio')
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise de potencial de conversão
    st.subheader("🎯 Análise de Potencial de Conversão")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📈 Projeção com Taxas de Indústria
        
        **Turismo/Experiências:**
        - Taxa de conversão média: 2-5%
        - Custo por conversão aceitável: R$ 50-150
        - ROAS esperado: 300-500%
        
        **Potencial com tráfego atual:**
        - Cliques: 2.260
        - Conversões esperadas: 45-113
        - Faturamento potencial: R$ 27.000-67.500
        """)
    
    with col2:
        # Simulação de cenários
        st.markdown("""
        ### 🔄 Cenários com Melhorias
        
        **Cenário Conservador (1%):**
        - Conversões: 23
        - Faturamento: R$ 13.800
        
        **Cenário Realista (2%):**
        - Conversões: 45
        - Faturamento: R$ 27.000
        
        **Cenário Otimista (5%):**
        - Conversões: 113
        - Faturamento: R$ 67.800
        """)
    
    # Diagnóstico de problemas de conversão
    st.subheader("🔍 Diagnóstico de Problemas de Conversão")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("""
        **🚫 Tracking Não Configurado**
        - Conversões não estão sendo rastreadas
        - Pixel de conversão não instalado
        - Goals não configurados no Analytics
        """)
    
    with col2:
        st.warning("""
        **📱 Experiência Mobile**
        - 96.8% do tráfego é mobile
        - Site pode não ser responsivo
        - Formulários complexos no mobile
        """)
    
    with col3:
        st.warning("""
        **💡 Qualidade do Tráfego**
        - Muitas palavras-chave sem cliques
        - Intenção de compra variável
        - Falta de remarketing
        """)

with tab6:
    st.header("💡 Análise e Recomendações")
    
    # Métricas calculadas para análise
    taxa_sem_cliques = (len(palavras_sem_cliques) / len(data['palavras_chave'])) * 100
    custo_smartphones = data['dispositivos'][data['dispositivos']['Dispositivo'] == 'Smartphones']['Custo_num'].iloc[0]
    percentual_smartphones = (data['dispositivos'][data['dispositivos']['Dispositivo'] == 'Smartphones']['Impressões_num'].iloc[0] / total_impressoes) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ O que está funcionando:")
        
        st.success(f"""
        **📈 Performance Geral Excelente:**
        - CTR da campanha: 3.41% ⭐
        - 2.260 cliques gerados
        - Pontuação de otimização: 86.2%
        - Custo por clique: R$ {cpc_medio:.2f}
        
        **🎯 Público-alvo bem definido:**
        - Mulheres (62.21%) respondendo bem
        - Jovens 18-34 anos (69.90% do total)
        - Faixa etária ideal para turismo
        
        **🔍 Palavras-chave eficientes:**
        - "balonismo em aquidauana": 33.33% CTR
        - "pantanal balonismo": 27.74% CTR
        - "balonismo aquidauana": 20.44% CTR
        """)
        
        st.subheader("🔄 Oportunidades de Melhoria:")
        
        st.warning(f"""
        **💰 Otimização de custo:**
        - {len(palavras_sem_cliques)} palavras-chave sem cliques
        - Custo em smartphones: R$ {custo_smartphones:,.2f}
        - Rede de Display com CPC baixo mas muitas impressões
        
        **📅 Sazonalidade:**
        - Campanha iniciou apenas em Julho
        - 14 semanas sem dados anteriores
        - Potencial não explorado no 1º semestre
        """)
    
    with col2:
        st.subheader("❌ Problemas identificados:")
        
        st.error(f"""
        **🚫 CONVERSÃO ZERO CRÍTICO:**
        - Nenhuma conversão em 2.260 cliques
        - Tracking não implementado
        - Possível problema no funnel completo
        
        **📊 Disparidade de dispositivos:**
        - Tablets e TVs sem resultados significativos
        - Computadores subutilizados
        
        **🔍 Palavras-chave ineficientes:**
        - {taxa_sem_cliques:.1f}% das palavras-chave sem cliques
        - Termos muito específicos sem performance
        """)
        
        st.subheader("🎯 Recomendações Prioritárias:")
        
        st.info("""
        1. **IMPLEMENTAR CONVERSÕES URGENTE** - Configurar tracking
        2. **OTIMIZAR MOBILE** - Melhorar experiência smartphone
        3. **LIMPAR PALAVRAS-CHAVE** - Pausar termos sem cliques
        4. **EXPANDIR CAMPANHA** - Usar dados de todo o período
        5. **TESTAR REDE DE DISPLAY** - Aproveitar CPC baixo
        6. **CRIAR SEGMENTAÇÕES** - Por dispositivo e demografia
        7. **IMPLEMENTAR REMARKETING** - Recuperar visitantes
        """)
    
    # Plano de ação detalhado
    st.subheader("📋 Plano de Ação Detalhado")
    
    acao_col1, acao_col2, acao_col3 = st.columns(3)
    
    with acao_col1:
        st.write("**🎯 Curto Prazo (1-2 dias)**")
        st.write("""
        - Configurar tracking de conversão
        - Pausar palavras-chave sem cliques
        - Otimizar anúncios para mobile
        - Ajustar orçamento por dispositivo
        """)
    
    with acao_col2:
        st.write("**📈 Médio Prazo (1-2 semanas)**")
        st.write("""
        - Criar campanhas segmentadas
        - Implementar remarketing
        - Testar novos horários de veiculação
        - Desenvolver landing pages otimizadas
        """)
    
    with acao_col3:
        st.write("**🚀 Longo Prazo (1 mês)**")
        st.write("""
        - Expandir para novas palavras-chave
        - Otimizar funnel completo
        - Implementar automação
        - Escalar campanhas bem-sucedidas
        """)
    
    # ROI Potencial
    st.subheader("💰 Projeção de ROI")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Investimento Atual", f"R$ {total_custo:,.2f}")
    
    with col2:
        st.metric("Cliques Gerados", f"{total_cliques:,.0f}")
    
    with col3:
        st.metric("Conversões Potenciais (2%)", "45")
    
    with col4:
        faturamento_potencial = 45 * 600  # Considerando ticket médio de R$ 600
        st.metric("Faturamento Potencial", f"R$ {faturamento_potencial:,.2f}")

# Footer
st.markdown("---")
st.markdown("**Dashboard criado para análise da campanha 'Voo de Balão em Aquidauana'**")
st.markdown("*Período: Abril a Outubro 2025* | *Desenvolvido com Streamlit*")