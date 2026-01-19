"""
Sistema de Precificação Brivia - v2.0 (Professional Edition)
Foco: Simplicidade, Visual High-End e Estrutura de Dados para IA
Author: Lorraine A. L. Santana
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from datetime import datetime

# ==================== MOCK DE DADOS (Substitua pelo seu import config_database se preferir) ====================
# Mantive aqui para garantir que o código rode perfeitamente ao copiar e colar.

TIPOS_CONTRATO = ["Fee Mensal (Recorrente)", "Projeto (Escopo Fechado)", "Sustentação", "Consultoria"]
TIPOS_SERVICO = ["Tecnologia / Dev", "Design / UX", "Dados / Analytics", "Marketing / Growth", "Estratégia"]
COMISSAO_NB = [0, 5, 7, 10]
COMISSAO_PARCEIROS = [0, 5, 10, 15, 20]
GROSS_MARGIN_ALVO = 45.0

# Base simplificada para exemplo (Se tiver o arquivo config_database, use-o)
BASE_SALARIAL = {
    "Desenvolvedor Fullstack": {"1. Junior": {"mercado": 4500}, "2. Pleno": {"mercado": 7500}, "3. Sênior": {"mercado": 11000}},
    "Cientista de Dados": {"1. Junior": {"mercado": 5500}, "2. Pleno": {"mercado": 9000}, "3. Sênior": {"mercado": 13500}},
    "UX Designer": {"1. Junior": {"mercado": 4000}, "2. Pleno": {"mercado": 6500}, "3. Sênior": {"mercado": 9500}}
}
MAPEAMENTO_OFERTAS = {"Tecnologia / Dev": "Tech Squad", "Dados / Analytics": "Data Intelligence"}

# ==================== CONFIGURAÇÃO GERAL ====================

st.set_page_config(
    page_title="Brivia Pricing System",
    page_icon="⚫",
    layout="wide",
    initial_sidebar_state="collapsed" # Sidebar escondida para visual mais limpo
)

# Constantes de Cálculo
FATOR_ENCARGOS = 1.70
BENEFICIOS_MENSAIS = 1190
IMPOSTO_PADRAO_PCT = 14.25 # Valor médio fixo para simplificação (pode ser editado na UI)

# ==================== IDENTIDADE VISUAL & CSS (PROFISSIONAL) ====================

video_url = "https://cdn.prod.website-files.com/65c2dcb4330facd527e06bdd/66189f248c2e87b594826a44_Co%CC%81pia%20de%20BornBlackColor2-transcode.mp4"
logo_url = "https://cdn.prod.website-files.com/65c2dcb4330facd527e06bdd/6619a7597575e945de440959_brivia_group.svg"
cor_primaria = "#90513b"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');

    /* Global */
    .stApp {{ background-color: #050505 !important; }}
    * {{ font-family: 'Space Grotesk', sans-serif !important; }}
    
    /* Typography */
    h1, h2, h3 {{ color: #ffffff !important; font-weight: 700; letter-spacing: -0.5px; }}
    p, label, span {{ color: #e0e0e0 !important; font-weight: 300; }}
    
    /* Header e Logo */
    .header-container {{
        display: flex; align-items: center; justify-content: space-between;
        padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 30px;
    }}
    .logo-img {{ height: 40px; filter: brightness(0) invert(1); }}
    
    /* Video Background */
    #video-bg {{
        position: fixed; top: 0; right: 0; width: 65vw; height: 100vh;
        object-fit: cover; z-index: 0; opacity: 0.6; pointer-events: none;
        mask-image: linear-gradient(to left, black 0%, transparent 100%);
        -webkit-mask-image: linear-gradient(to left, black 20%, transparent 100%);
    }}
    .stMainBlockContainer {{ position: relative; z-index: 1; background: transparent !important; }}

    /* Cards e Containers (Glassmorphism) */
    .glass-card {{
        background: rgba(20, 20, 20, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }}
    
    /* Custom Inputs */
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > div {{
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 8px !important;
    }}
    .stTextInput > div > div > input:focus {{ border-color: {cor_primaria} !important; }}

    /* Buttons Styling - A parte mais importante para o visual */
    div.stButton > button {{
        width: 100%;
        background-color: transparent;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 1px;
    }}
    div.stButton > button:hover {{
        border-color: {cor_primaria};
        background-color: rgba(144, 81, 59, 0.1);
        color: {cor_primaria};
        box-shadow: 0 0 15px rgba(144, 81, 59, 0.3);
    }}
    /* Botão Primário (Avançar) */
    div.stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {cor_primaria}, #6b3a2a);
        border: none;
        color: white;
        font-weight: 600;
    }}
    div.stButton > button[kind="primary"]:hover {{
        box-shadow: 0 0 20px rgba(144, 81, 59, 0.6);
        transform: translateY(-2px);
    }}

    /* Progress Steps */
    .step-container {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
    .step {{ 
        flex: 1; text-align: center; font-size: 0.75rem; text-transform: uppercase; 
        padding: 10px; border-bottom: 2px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.4);
    }}
    .step.active {{ 
        border-bottom: 2px solid {cor_primaria}; color: white; font-weight: 700; 
        text-shadow: 0 0 10px {cor_primaria};
    }}
    .step.completed {{ color: {cor_primaria}; }}

    /* Highlight Values */
    .big-number {{ font-size: 2.2rem; font-weight: 700; color: white; line-height: 1.1; }}
    .label-desc {{ font-size: 0.8rem; text-transform: uppercase; color: rgba(255,255,255,0.5); letter-spacing: 1px; }}
    .destaque-cor {{ color: {cor_primaria} !important; }}
</style>

<video autoplay loop muted playsinline id="video-bg">
    <source src="{video_url}" type="video/mp4">
</video>

<div class="header-container">
    <img src="{logo_url}" class="logo-img">
    <div style="text-align:right;">
        <h3 style="margin:0; font-size: 1.2rem;">Sistema de Precificação</h3>
        <span style="font-size: 0.8rem; opacity: 0.6;">Powered by Brivia Data</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== FUNÇÕES CORE (Lógica de Negócio) ====================

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def calcular_custo_funcionario(salario_base, dedicacao_pct, meses):
    custo_mensal = (salario_base * FATOR_ENCARGOS) + BENEFICIOS_MENSAIS
    custo_dedicado = custo_mensal * (dedicacao_pct / 100)
    custo_total = custo_dedicado * meses
    return custo_mensal, custo_dedicado, custo_total

def calcular_pricing_reverso(custo_total, gm_pct, imposto_pct, comissao_pct):
    """
    Cálculo robusto de Markup Reverso.
    Preço = Custo / (1 - (GM + Imposto + Comissão))
    """
    deducoes = (gm_pct + imposto_pct + comissao_pct) / 100
    divisor = 1 - deducoes
    
    if divisor <= 0: return None, 0, 0, 0 # Margem impossível
    
    preco_venda = custo_total / divisor
    val_imposto = preco_venda * (imposto_pct / 100)
    val_comissao = preco_venda * (comissao_pct / 100)
    val_gm = preco_venda * (gm_pct / 100)
    
    return preco_venda, val_imposto, val_comissao, val_gm

def init_session():
    if 'data' not in st.session_state:
        st.session_state.data = {
            'fase': 1,
            'cliente': '',
            'projeto': '',
            'meses': 12,
            'imposto_pct': IMPOSTO_PADRAO_PCT,
            'comissao_nb': 0,
            'comissao_parceiros': 0,
            'gm_alvo': GROSS_MARGIN_ALVO,
            'equipe': [],
            'terceiros': [],
            'custos_extras': {'viagens': 0.0, 'materiais': 0.0, 'outros': 0.0},
            'obs': ''
        }

# ==================== RENDERIZAÇÃO DAS FASES ====================

def render_timeline(fase_atual):
    steps = ["1. Estratégia", "2. Equipe", "3. Custos & Opex", "4. Resultado"]
    cols = st.columns(4)
    for i, step in enumerate(steps):
        css_class = "step active" if (i + 1) == fase_atual else "step completed" if (i + 1) < fase_atual else "step"
        cols[i].markdown(f'<div class="{css_class}">{step}</div>', unsafe_allow_html=True)

def fase_1_estrategia():
    st.markdown('<div class="glass-card"><h3>🎯 Estratégia do Projeto</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.data['cliente'] = st.text_input("Nome do Cliente", st.session_state.data['cliente'])
        st.session_state.data['meses'] = st.number_input("Duração (Meses)", 1, 60, st.session_state.data['meses'])
        tipo_contrato = st.selectbox("Modelo de Contrato", TIPOS_CONTRATO)
    
    with col2:
        st.session_state.data['projeto'] = st.text_input("Nome do Projeto", st.session_state.data['projeto'])
        tipo_servico = st.selectbox("Vertical de Serviço", TIPOS_SERVICO)
        # Simplificação: Imposto direto sem seleção de empresa complexa
        st.session_state.data['imposto_pct'] = st.number_input("Imposto Estimado (%)", 0.0, 30.0, st.session_state.data['imposto_pct'], step=0.5, help="Média de impostos para a nota fiscal")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card"><h3>💰 Definição de Margens</h3>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.data['comissao_nb'] = st.selectbox("Comissão New Business (%)", COMISSAO_NB, index=COMISSAO_NB.index(st.session_state.data['comissao_nb']))
    with c2:
        st.session_state.data['comissao_parceiros'] = st.selectbox("Comissão Parceiros (%)", COMISSAO_PARCEIROS, index=COMISSAO_PARCEIROS.index(st.session_state.data['comissao_parceiros']))
    with c3:
        st.session_state.data['gm_alvo'] = st.slider("Meta de Gross Margin (%)", 20.0, 70.0, st.session_state.data['gm_alvo'])
    
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.data['cliente'] and st.session_state.data['projeto']:
        if st.button("Avançar para Equipe →", type="primary"):
            st.session_state.data['fase'] = 2
            st.rerun()
    else:
        st.warning("Preencha o Cliente e Projeto para iniciar.")

def fase_2_equipe():
    st.markdown(f'<div class="glass-card"><h3>👥 Squad Builder ({st.session_state.data["meses"]} meses)</h3>', unsafe_allow_html=True)
    
    # Seletor
    c1, c2, c3, c4 = st.columns([2, 1.5, 1, 1])
    with c1:
        perfil = st.selectbox("Perfil", list(BASE_SALARIAL.keys()))
    with c2:
        nivel = st.selectbox("Senioridade", list(BASE_SALARIAL[perfil].keys()))
    with c3:
        qtd = st.number_input("Qtd", 1, 10, 1)
    with c4:
        dedicacao = st.number_input("Dedicação %", 10, 100, 100, step=10)

    # Botão de adicionar mais limpo
    if st.button("＋ Adicionar Profissional", use_container_width=True):
        salario = BASE_SALARIAL[perfil][nivel]['mercado']
        st.session_state.data['equipe'].append({
            "perfil": perfil, "nivel": nivel, "qtd": qtd, "dedicacao": dedicacao, "salario_base": salario
        })
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Tabela Visual da Equipe
    if st.session_state.data['equipe']:
        total_equipe = 0
        st.markdown("##### Squad Configurada")
        
        for i, item in enumerate(st.session_state.data['equipe']):
            _, _, custo_tot = calcular_custo_funcionario(item['salario_base'], item['dedicacao'], st.session_state.data['meses'])
            custo_item = custo_tot * item['qtd']
            total_equipe += custo_item
            
            with st.container():
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                    <div style="flex:2"><b>{item['qtd']}x</b> {item['perfil']} <span style="opacity:0.6">({item['nivel']})</span></div>
                    <div style="flex:1">{item['dedicacao']}% Dedicação</div>
                    <div style="flex:1; text-align:right; font-family:'monospace'">{formatar_moeda(custo_item)}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Remover", key=f"del_{i}"):
                    st.session_state.data['equipe'].pop(i)
                    st.rerun()

        st.markdown("---")
        st.markdown(f"<h3 style='text-align:right'>Total Equipe: <span class='destaque-cor'>{formatar_moeda(total_equipe)}</span></h3>", unsafe_allow_html=True)
    
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("← Voltar"):
            st.session_state.data['fase'] = 1
            st.rerun()
    with col_nav2:
        if st.button("Avançar para Custos →", type="primary"):
            st.session_state.data['fase'] = 3
            st.rerun()

def fase_3_custos():
    st.markdown('<div class="glass-card"><h3>📦 Custos Operacionais & Terceiros</h3>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([3, 1.5, 1])
    with c1:
        desc_terceiro = st.text_input("Descrição do Fornecedor/Freelancer")
    with c2:
        val_terceiro = st.number_input("Custo Total (R$)", 0.0, step=100.0)
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("＋ Add") and val_terceiro > 0:
            st.session_state.data['terceiros'].append({'desc': desc_terceiro, 'valor': val_terceiro})
            st.rerun()
            
    # Listar Terceiros
    for i, t in enumerate(st.session_state.data['terceiros']):
        st.caption(f"{t['desc']}: {formatar_moeda(t['valor'])}")

    st.markdown("---")
    st.markdown("#### Custos Variáveis (Mensais)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.data['custos_extras']['viagens'] = st.number_input("Viagens (Mensal)", value=st.session_state.data['custos_extras']['viagens'])
    with col2:
        st.session_state.data['custos_extras']['materiais'] = st.number_input("Software/Licenças (Mensal)", value=st.session_state.data['custos_extras']['materiais'])
    with col3:
        st.session_state.data['custos_extras']['outros'] = st.number_input("Outros (Mensal)", value=st.session_state.data['custos_extras']['outros'])
    
    st.markdown("</div>", unsafe_allow_html=True)

    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("← Voltar"):
            st.session_state.data['fase'] = 2
            st.rerun()
    with col_nav2:
        if st.button("Calcular Pricing Final →", type="primary"):
            st.session_state.data['fase'] = 4
            st.rerun()

def fase_4_dashboard():
    # 1. Cálculos Finais
    meses = st.session_state.data['meses']
    
    # Equipe
    custo_equipe = 0
    for item in st.session_state.data['equipe']:
        _, _, tot = calcular_custo_funcionario(item['salario_base'], item['dedicacao'], meses)
        custo_equipe += (tot * item['qtd'])
        
    # Terceiros
    custo_terceiros = sum(t['valor'] for t in st.session_state.data['terceiros'])
    
    # Extras
    extras_mes = sum(st.session_state.data['custos_extras'].values())
    custo_extras_total = extras_mes * meses
    
    CUSTO_TOTAL_PROJETO = custo_equipe + custo_terceiros + custo_extras_total
    
    # Pricing
    preco_venda, v_imposto, v_comissao, v_gm = calcular_pricing_reverso(
        CUSTO_TOTAL_PROJETO,
        st.session_state.data['gm_alvo'],
        st.session_state.data['imposto_pct'],
        st.session_state.data['comissao_nb'] + st.session_state.data['comissao_parceiros']
    )
    
    # 2. Exibição
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    if preco_venda:
        with col_kpi1:
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid {cor_primaria}">
                <div class="label-desc">Investimento Total</div>
                <div class="big-number">{formatar_moeda(preco_venda)}</div>
                <div style="font-size:0.9rem; color:#aaa">Mensal: {formatar_moeda(preco_venda/meses)}</div>
            </div>""", unsafe_allow_html=True)
            
        with col_kpi2:
             st.markdown(f"""
            <div class="glass-card">
                <div class="label-desc">Margem Bruta (Valor)</div>
                <div class="big-number" style="color:#2ecc71">{formatar_moeda(v_gm)}</div>
                <div style="font-size:0.9rem; color:#aaa">Meta: {st.session_state.data['gm_alvo']}%</div>
            </div>""", unsafe_allow_html=True)
             
        with col_kpi3:
             markup_real = ((preco_venda / CUSTO_TOTAL_PROJETO) - 1) * 100
             st.markdown(f"""
            <div class="glass-card">
                <div class="label-desc">Markup Aplicado</div>
                <div class="big-number">{markup_real:.1f}%</div>
                <div style="font-size:0.9rem; color:#aaa">Sobre custo base</div>
            </div>""", unsafe_allow_html=True)
             
        # Gráficos
        col_g1, col_g2 = st.columns([1, 2])
        
        with col_g1:
            st.markdown("##### Composição do Preço")
            fig = go.Figure(data=[go.Pie(
                labels=['Custo', 'Imposto', 'Comissão', 'Margem'],
                values=[CUSTO_TOTAL_PROJETO, v_imposto, v_comissao, v_gm],
                hole=.6,
                marker_colors=['#555', '#777', '#999', cor_primaria],
                textinfo='percent'
            )])
            fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', font_color='white', height=200)
            st.plotly_chart(fig, use_container_width=True)

        with col_g2:
            st.markdown("##### Detalhe Financeiro")
            st.dataframe(pd.DataFrame({
                "Categoria": ["Equipe", "Terceiros", "Opex/Viagens", "Impostos", "Comissões", "LUCRO"],
                "Valor": [
                    formatar_moeda(custo_equipe),
                    formatar_moeda(custo_terceiros),
                    formatar_moeda(custo_extras_total),
                    formatar_moeda(v_imposto),
                    formatar_moeda(v_comissao),
                    formatar_moeda(v_gm)
                ]
            }), hide_index=True, use_container_width=True)

        # Botão JSON para IA
        st.markdown("---")
        col_end1, col_end2 = st.columns(2)
        
        with col_end1:
            if st.button("🔄 Reiniciar Precificação"):
                st.session_state.data = None
                st.rerun()
                
        with col_end2:
            # Estrutura de dados pronta para salvar em banco ou enviar para LLM
            projeto_export = {
                "metadata": {
                    "data": datetime.now().strftime("%Y-%m-%d"),
                    "autor": "Sistema Brivia v2"
                },
                "inputs": st.session_state.data,
                "outputs": {
                    "preco_total": preco_venda,
                    "margem_valor": v_gm,
                    "custo_total": CUSTO_TOTAL_PROJETO
                }
            }
            json_str = json.dumps(projeto_export, indent=4, ensure_ascii=False)
            st.download_button(
                label="💾 Baixar Dados (JSON para IA)",
                data=json_str,
                file_name=f"pricing_{st.session_state.data['cliente']}.json",
                mime="application/json",
                type="primary"
            )

    else:
        st.error("Erro matemático: A soma das margens e impostos ultrapassa 100%. Reduza os custos ou aumente o preço.")
        if st.button("Voltar e Ajustar"):
            st.session_state.data['fase'] = 1
            st.rerun()

# ==================== MAIN LOOP ====================

def main():
    init_session()
    render_timeline(st.session_state.data['fase'])
    
    if st.session_state.data['fase'] == 1:
        fase_1_estrategia()
    elif st.session_state.data['fase'] == 2:
        fase_2_equipe()
    elif st.session_state.data['fase'] == 3:
        fase_3_custos()
    elif st.session_state.data['fase'] == 4:
        fase_4_dashboard()

if __name__ == "__main__":
    main()