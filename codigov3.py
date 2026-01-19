"""
Sistema de Precificação Brivia
Versão Simplificada - Preparado para integração com IA
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Importar configurações centralizadas
from config_database import (
    TIPOS_CONTRATO, TIPOS_SERVICO, EMPRESAS_TRIBUTACAO,
    COMISSAO_NB, COMISSAO_PARCEIROS, GROSS_MARGIN_ALVO,
    BASE_SALARIAL, MAPEAMENTO_OFERTAS
)

# ==================== CONFIGURAÇÃO DA PÁGINA ====================

st.set_page_config(
    page_title="Precificação Brivia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILO E IDENTIDADE VISUAL ====================

video_url = "https://cdn.prod.website-files.com/65c2dcb4330facd527e06bdd/66189f248c2e87b594826a44_Co%CC%81pia%20de%20BornBlackColor2-transcode.mp4"
logo_url = "https://cdn.prod.website-files.com/65c2dcb4330facd527e06bdd/6619a7597575e945de440959_brivia_group.svg"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;700&display=swap');

    .stApp {{
        background-color: #000000 !important;
    }}

    .header-brivia {{
        display: flex;
        align-items: center;
        padding-bottom: 30px;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .logo-brivia {{
        height: 35px;
        margin-right: 20px;
        filter: brightness(0) invert(1) !important;
    }}

    .brivia-alerta {{
        padding: 15px;
        border-radius: 4px;
        background-color: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #90513b;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.9rem;
        margin-bottom: 25px;
    }}

    #brivia-video-bg {{
        position: fixed;
        top: 0;
        right: 0;
        width: 80vw;
        height: 90vh;
        object-fit: cover;
        z-index: 0;
        pointer-events: none;
        -webkit-mask-image: radial-gradient(circle at 80% 50%, black 0%, transparent 75%);
        mask-image: radial-gradient(circle at 80% 50%, black 0%, transparent 75%);
    }}

    .stMainBlockContainer {{
        position: relative;
        z-index: 1;
        background-color: transparent !important;
    }}

    h1, h2, h3, label, p {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: white !important;
    }}

    .fase-container {{
        padding: 12px;
        border-radius: 4px;
        text-align: center;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }}

    .fase-atual {{
        background: linear-gradient(#000, #000) padding-box,
                    linear-gradient(135deg, #90513b, #ffffff) border-box;
        border: 2px solid transparent;
        color: #ffffff !important;
        font-weight: 700;
        box-shadow: 0 0 15px rgba(144, 81, 59, 0.4);
    }}

    .fase-ok {{
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: rgba(255, 255, 255, 0.6);
        background-color: rgba(255, 255, 255, 0.02);
    }}

    .fase-espera {{
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.2);
    }}

    .resultado-card {{
        background: linear-gradient(135deg, rgba(144, 81, 59, 0.2), rgba(0, 0, 0, 0.8));
        border: 1px solid #90513b;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }}

    .valor-destaque {{
        font-size: 2rem;
        font-weight: 700;
        color: #90513b !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }}

    .label-destaque {{
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
</style>

<div class="header-brivia">
    <img src="{logo_url}" class="logo-brivia">
    <h1 style="margin:0; font-size: 1.8rem; letter-spacing: -1px;">Sistema de Precificação</h1>
</div>

<video autoplay loop muted playsinline id="brivia-video-bg">
    <source src="{video_url}" type="video/mp4">
</video>
""", unsafe_allow_html=True)

# ==================== CONSTANTES DE CÁLCULO ====================

# Fator de encargos simplificado (CLT completo)
FATOR_ENCARGOS = 1.70  # Inclui todos os encargos trabalhistas
BENEFICIOS_MENSAIS = 1190  # VR, VT, Plano de saúde, etc.

# ==================== FUNÇÕES AUXILIARES ====================

def formatar_moeda(valor):
    """Formata valor em reais"""
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def filtrar_empresas_por_servico(tipo_servico):
    """Filtra empresas compatíveis com o tipo de serviço selecionado"""
    empresas_filtradas = []
    for key, data in EMPRESAS_TRIBUTACAO.items():
        if data['servico'] == tipo_servico:
            empresas_filtradas.append(key)
    return empresas_filtradas

def calcular_custo_funcionario(salario_base, dedicacao_pct, meses):
    """
    Calcula o custo total de um funcionário para o projeto.
    Fórmula simplificada: (Salário × Fator Encargos + Benefícios) × Dedicação × Meses
    """
    custo_mensal = (salario_base * FATOR_ENCARGOS) + BENEFICIOS_MENSAIS
    custo_dedicado = custo_mensal * (dedicacao_pct / 100)
    custo_total = custo_dedicado * meses
    return custo_mensal, custo_dedicado, custo_total

def calcular_precificacao(custo_total, gross_margin_pct, aliquota_imposto_pct, comissao_total_pct):
    """
    Calcula o preço de venda baseado no custo e margem desejada.

    Fórmula:
    Preço de Venda = Custo Total / (1 - GM% - Imposto% - Comissão%)

    Onde:
    - Custo Total = Equipe + Terceiros + Viagens + Outros
    - GM% = Gross Margin desejada
    - Imposto% = Alíquota de imposto da empresa
    - Comissão% = NB + Parceiros
    """
    # Converter percentuais para decimais
    gm = gross_margin_pct / 100
    imposto = aliquota_imposto_pct / 100
    comissao = comissao_total_pct / 100

    # Fator de markup
    fator = 1 - gm - imposto - comissao

    # Evitar divisão por zero ou valores negativos
    if fator <= 0:
        return None, None, None, None

    # Preço de venda
    preco_venda = custo_total / fator

    # Valores calculados
    valor_imposto = preco_venda * imposto
    valor_comissao = preco_venda * comissao
    lucro_bruto = preco_venda * gm

    return preco_venda, valor_imposto, valor_comissao, lucro_bruto

# ==================== INICIALIZAÇÃO DO SESSION STATE ====================

def init_session_state():
    """Inicializa todas as variáveis de sessão"""

    if 'fase_atual' not in st.session_state:
        st.session_state.fase_atual = 1

    if 'fase_max_concluida' not in st.session_state:
        st.session_state.fase_max_concluida = 1

    # Dados básicos (Fase 1)
    if 'dados_basicos' not in st.session_state:
        st.session_state.dados_basicos = {
            'cliente': '',
            'descricao_contrato': '',
            'tipo_contrato': TIPOS_CONTRATO[0],
            'quantidade_meses': 12,
            'tipo_servico': TIPOS_SERVICO[0],
            'empresa_tributacao': '',
            'aliquota_imposto': 0.0,
            'comissao_nb': 0,
            'comissao_parceiros': 0,
            'gross_margin': GROSS_MARGIN_ALVO,
        }

    # Equipe (Fase 2)
    if 'lista_equipe' not in st.session_state:
        st.session_state.lista_equipe = []

    # Outros Custos (Fase 3)
    if 'outros_custos' not in st.session_state:
        st.session_state.outros_custos = {
            'terceiros': [],  # Lista de terceiros
            'viagens_mensal': 0.0,
            'materiais_mensal': 0.0,
            'outros_mensal': 0.0,
            'observacoes': ''
        }

# ==================== FASE 1: DADOS BÁSICOS ====================

def validar_fase_1():
    """Valida se todos os campos obrigatórios da fase 1 estão preenchidos"""
    dados = st.session_state.dados_basicos

    campos_obrigatorios = [
        dados['cliente'].strip() != '',
        dados['descricao_contrato'].strip() != '',
        dados['empresa_tributacao'] != '',
        dados['quantidade_meses'] > 0
    ]

    return all(campos_obrigatorios)

def renderizar_fase_1():
    st.header("FASE 1: Dados do Projeto")
    st.markdown('<div class="brivia-alerta">Configure as informações básicas do projeto e contrato</div>', unsafe_allow_html=True)

    # 1. INFORMAÇÕES DO CLIENTE
    st.subheader("📋 Informações do Cliente")

    col1, col2 = st.columns(2)

    with col1:
        cliente = st.text_input(
            "Cliente *",
            value=st.session_state.dados_basicos['cliente'],
            placeholder="Nome ou Razão Social do Cliente",
            help="Campo obrigatório"
        )
        st.session_state.dados_basicos['cliente'] = cliente

        tipo_contrato = st.selectbox(
            "Tipo de Contrato *",
            TIPOS_CONTRATO,
            index=TIPOS_CONTRATO.index(st.session_state.dados_basicos['tipo_contrato']),
            help="Fee = Contrato recorrente | Projeto = Escopo fechado"
        )
        st.session_state.dados_basicos['tipo_contrato'] = tipo_contrato

    with col2:
        descricao = st.text_area(
            "Descrição do Projeto *",
            value=st.session_state.dados_basicos['descricao_contrato'],
            placeholder="Descreva brevemente o escopo do projeto",
            help="Campo obrigatório",
            height=100
        )
        st.session_state.dados_basicos['descricao_contrato'] = descricao

    col1, col2 = st.columns(2)

    with col1:
        tipo_servico = st.selectbox(
            "Tipo de Serviço *",
            TIPOS_SERVICO,
            index=TIPOS_SERVICO.index(st.session_state.dados_basicos['tipo_servico']),
            help="Define a empresa e alíquota de imposto"
        )
        st.session_state.dados_basicos['tipo_servico'] = tipo_servico

    with col2:
        quantidade_meses = st.number_input(
            "Duração do Projeto (meses) *",
            min_value=1,
            max_value=60,
            value=st.session_state.dados_basicos['quantidade_meses'],
            help="Quantidade de meses do contrato"
        )
        st.session_state.dados_basicos['quantidade_meses'] = quantidade_meses

    st.markdown("---")

    # 2. TRIBUTAÇÃO
    st.subheader("🏢 Empresa e Tributação")

    empresas_disponiveis = filtrar_empresas_por_servico(tipo_servico)

    if empresas_disponiveis:
        col1, col2 = st.columns(2)

        with col1:
            if st.session_state.dados_basicos['empresa_tributacao'] in empresas_disponiveis:
                idx = empresas_disponiveis.index(st.session_state.dados_basicos['empresa_tributacao'])
            else:
                idx = 0
                st.session_state.dados_basicos['empresa_tributacao'] = empresas_disponiveis[0]

            empresa_selecionada = st.selectbox(
                "Empresa para Faturamento *",
                empresas_disponiveis,
                index=idx,
                help="Empresa do grupo que emitirá a nota fiscal"
            )
            st.session_state.dados_basicos['empresa_tributacao'] = empresa_selecionada

            aliquota = EMPRESAS_TRIBUTACAO[empresa_selecionada]['aliquota']
            st.session_state.dados_basicos['aliquota_imposto'] = aliquota

        with col2:
            st.metric(
                "Alíquota de Imposto",
                f"{aliquota:.2f}%",
                help="Calculado automaticamente com base na empresa"
            )
    else:
        st.warning("Nenhuma empresa disponível para o tipo de serviço selecionado")

    st.markdown("---")

    # 3. COMISSÕES E MARGEM
    st.subheader("💰 Comissões e Margem")

    col1, col2, col3 = st.columns(3)

    with col1:
        comissao_nb = st.selectbox(
            "Comissão NB (New Business)",
            COMISSAO_NB,
            index=COMISSAO_NB.index(st.session_state.dados_basicos['comissao_nb']),
            format_func=lambda x: f"{x}%",
            help="Comissão para novos negócios"
        )
        st.session_state.dados_basicos['comissao_nb'] = comissao_nb

    with col2:
        comissao_parceiros = st.selectbox(
            "Comissão Parceiros",
            COMISSAO_PARCEIROS,
            index=COMISSAO_PARCEIROS.index(st.session_state.dados_basicos['comissao_parceiros']),
            format_func=lambda x: f"{x}%",
            help="Comissão para parceiros externos"
        )
        st.session_state.dados_basicos['comissao_parceiros'] = comissao_parceiros

    with col3:
        gross_margin = st.slider(
            "Gross Margin Alvo",
            min_value=20.0,
            max_value=60.0,
            value=st.session_state.dados_basicos['gross_margin'],
            step=1.0,
            format="%.0f%%",
            help="Margem bruta desejada para o projeto"
        )
        st.session_state.dados_basicos['gross_margin'] = gross_margin

    # Resumo das taxas
    total_deducoes = aliquota + comissao_nb + comissao_parceiros
    margem_liquida = gross_margin

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Imposto", f"{aliquota:.1f}%")
    with col2:
        st.metric("Comissões", f"{comissao_nb + comissao_parceiros}%")
    with col3:
        st.metric("Gross Margin", f"{gross_margin:.0f}%")
    with col4:
        markup_total = 100 - aliquota - comissao_nb - comissao_parceiros - gross_margin
        if markup_total > 0:
            st.metric("Markup sobre custo", f"{(100/markup_total - 1)*100:.0f}%")
        else:
            st.metric("Markup", "⚠️ Inválido", help="Margem + taxas excedem 100%")

    st.markdown("---")

    # BOTÃO DE AVANÇAR
    fase_valida = validar_fase_1()

    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        if fase_valida:
            if st.button("Avançar para Equipe →", type="primary", use_container_width=True):
                st.session_state.fase_atual = 2
                st.session_state.fase_max_concluida = max(st.session_state.fase_max_concluida, 2)
                st.rerun()
        else:
            st.button("Avançar para Equipe →", disabled=True, use_container_width=True)
            st.error("Preencha todos os campos obrigatórios (*) para avançar")

# ==================== FASE 2: EQUIPE ====================

def renderizar_fase_2():
    st.header("FASE 2: Equipe do Projeto")
    st.markdown('<div class="brivia-alerta">Monte a equipe necessária para executar o projeto</div>', unsafe_allow_html=True)

    meses = st.session_state.dados_basicos['quantidade_meses']

    # Seleção de Régua Salarial
    regua_selecionada = st.radio(
        "Régua Salarial:",
        ["Média de Mercado", "Faixa Mínima", "Média Brivia (Mercer)"],
        horizontal=True,
        help="Define a base salarial para cálculo dos custos"
    )
    mapa_regua = {"Média de Mercado": "mercado", "Faixa Mínima": "minima", "Média Brivia (Mercer)": "brivia"}
    regua_id = mapa_regua[regua_selecionada]

    st.markdown("---")

    # Formulário de adição
    st.subheader("➕ Adicionar Profissional")

    col1, col2 = st.columns(2)

    with col1:
        perfil = st.selectbox("Perfil", list(BASE_SALARIAL.keys()))
        nivel = st.selectbox("Nível", ["1. Junior", "2. Pleno", "3. Sênior", "4. Líder", "5. Head", "6. Especialista"])

    with col2:
        qtd_func = st.number_input("Quantidade", min_value=1, value=1)
        dedicacao = st.slider("Dedicação (%)", 10, 100, 100, step=10)

    # Serviço/Oferta
    col1, col2 = st.columns(2)
    with col1:
        servicos_disponiveis = list(MAPEAMENTO_OFERTAS.keys())
        servico_selecionado = st.selectbox("Serviço", servicos_disponiveis)
    with col2:
        oferta_brivia = MAPEAMENTO_OFERTAS.get(servico_selecionado, "")
        st.text_input("Oferta Brivia", value=oferta_brivia, disabled=True)

    # Cálculo do profissional atual
    salario_base = BASE_SALARIAL.get(perfil, {}).get(nivel, {}).get(regua_id, 0)
    custo_mensal, custo_dedicado, custo_total = calcular_custo_funcionario(salario_base, dedicacao, meses)

    # Preview do cálculo
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Salário Base", formatar_moeda(salario_base))
    with col2:
        st.metric("Custo Mensal (CLT)", formatar_moeda(custo_mensal), help="Salário + Encargos + Benefícios")
    with col3:
        st.metric(f"Custo c/ Dedicação ({dedicacao}%)", formatar_moeda(custo_dedicado))
    with col4:
        st.metric(f"Custo Total ({meses} meses)", formatar_moeda(custo_total * qtd_func))

    # Botão adicionar
    if st.button("＋ Adicionar à Equipe", use_container_width=True, type="primary"):
        for i in range(qtd_func):
            st.session_state.lista_equipe.append({
                "perfil": perfil,
                "nivel": nivel,
                "dedicacao": dedicacao,
                "servico": servico_selecionado,
                "oferta": oferta_brivia,
                "salario_base": salario_base,
                "custo_mensal": custo_mensal,
                "custo_dedicado": custo_dedicado,
                "custo_total": custo_dedicado * meses,
                "regua": regua_id
            })
        st.rerun()

    st.markdown("---")

    # Tabela da equipe
    if st.session_state.lista_equipe:
        st.subheader("👥 Equipe do Projeto")

        total_custo_equipe = 0
        funcionarios_para_remover = []

        # Cabeçalho
        cols = st.columns([2.5, 1.5, 1, 1.5, 1.5, 0.5])
        cols[0].markdown("**Perfil**")
        cols[1].markdown("**Nível**")
        cols[2].markdown("**Ded.**")
        cols[3].markdown("**Custo/Mês**")
        cols[4].markdown("**Custo Total**")
        cols[5].markdown("")

        # Linhas
        for idx, func in enumerate(st.session_state.lista_equipe):
            # Recalcula com a régua atual
            sal = BASE_SALARIAL.get(func['perfil'], {}).get(func['nivel'], {}).get(regua_id, 0)
            _, custo_ded, custo_tot = calcular_custo_funcionario(sal, func['dedicacao'], meses)
            total_custo_equipe += custo_tot

            cols = st.columns([2.5, 1.5, 1, 1.5, 1.5, 0.5])
            cols[0].text(func['perfil'])
            cols[1].text(func['nivel'])
            cols[2].text(f"{func['dedicacao']}%")
            cols[3].text(formatar_moeda(custo_ded))
            cols[4].text(formatar_moeda(custo_tot))
            if cols[5].button("🗑️", key=f"rem_{idx}"):
                funcionarios_para_remover.append(idx)

        # Remover funcionários marcados
        if funcionarios_para_remover:
            for idx in sorted(funcionarios_para_remover, reverse=True):
                st.session_state.lista_equipe.pop(idx)
            st.rerun()

        st.markdown("---")

        # Total
        col1, col2 = st.columns([3, 2])
        with col2:
            st.markdown(f"""
            <div class="resultado-card">
                <div class="label-destaque">Custo Total da Equipe</div>
                <div class="valor-destaque">{formatar_moeda(total_custo_equipe)}</div>
                <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">
                    {len(st.session_state.lista_equipe)} profissional(is) × {meses} meses
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Navegação
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Voltar", use_container_width=True):
                st.session_state.fase_atual = 1
                st.rerun()
        with col3:
            if st.button("Avançar para Custos →", type="primary", use_container_width=True):
                st.session_state.fase_atual = 3
                st.session_state.fase_max_concluida = max(st.session_state.fase_max_concluida, 3)
                st.rerun()
    else:
        st.info("Adicione profissionais à equipe para continuar")

        if st.button("← Voltar", use_container_width=True):
            st.session_state.fase_atual = 1
            st.rerun()

# ==================== FASE 3: OUTROS CUSTOS ====================

def renderizar_fase_3():
    st.header("FASE 3: Outros Custos")
    st.markdown('<div class="brivia-alerta">Adicione custos com terceiros, viagens e outros</div>', unsafe_allow_html=True)

    meses = st.session_state.dados_basicos['quantidade_meses']

    # Terceiros
    st.subheader("👤 Terceiros (Freelancers/Fornecedores)")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        terceiro_descricao = st.text_input("Descrição do Terceiro", placeholder="Ex: Designer Freelancer")
    with col2:
        terceiro_valor = st.number_input("Valor Mensal (R$)", min_value=0.0, step=500.0, key="terceiro_valor")
    with col3:
        terceiro_meses = st.number_input("Meses", min_value=1, max_value=meses, value=meses, key="terceiro_meses")

    if st.button("＋ Adicionar Terceiro", use_container_width=True):
        if terceiro_descricao and terceiro_valor > 0:
            st.session_state.outros_custos['terceiros'].append({
                'descricao': terceiro_descricao,
                'valor_mensal': terceiro_valor,
                'meses': terceiro_meses,
                'valor_total': terceiro_valor * terceiro_meses
            })
            st.rerun()

    # Lista de terceiros
    total_terceiros = 0
    if st.session_state.outros_custos['terceiros']:
        terceiros_para_remover = []

        cols = st.columns([3, 1.5, 1, 1.5, 0.5])
        cols[0].markdown("**Descrição**")
        cols[1].markdown("**Valor/Mês**")
        cols[2].markdown("**Meses**")
        cols[3].markdown("**Total**")

        for idx, terc in enumerate(st.session_state.outros_custos['terceiros']):
            total_terceiros += terc['valor_total']
            cols = st.columns([3, 1.5, 1, 1.5, 0.5])
            cols[0].text(terc['descricao'])
            cols[1].text(formatar_moeda(terc['valor_mensal']))
            cols[2].text(str(terc['meses']))
            cols[3].text(formatar_moeda(terc['valor_total']))
            if cols[4].button("🗑️", key=f"rem_terc_{idx}"):
                terceiros_para_remover.append(idx)

        if terceiros_para_remover:
            for idx in sorted(terceiros_para_remover, reverse=True):
                st.session_state.outros_custos['terceiros'].pop(idx)
            st.rerun()

        st.markdown(f"**Total Terceiros: {formatar_moeda(total_terceiros)}**")

    st.markdown("---")

    # Outros custos mensais
    st.subheader("📦 Custos Adicionais")

    col1, col2, col3 = st.columns(3)

    with col1:
        viagens = st.number_input(
            "Viagens (mensal)",
            min_value=0.0,
            value=st.session_state.outros_custos['viagens_mensal'],
            step=500.0,
            help="Custo mensal estimado com viagens"
        )
        st.session_state.outros_custos['viagens_mensal'] = viagens
        st.caption(f"Total: {formatar_moeda(viagens * meses)}")

    with col2:
        materiais = st.number_input(
            "Materiais (mensal)",
            min_value=0.0,
            value=st.session_state.outros_custos['materiais_mensal'],
            step=500.0,
            help="Equipamentos, licenças, etc."
        )
        st.session_state.outros_custos['materiais_mensal'] = materiais
        st.caption(f"Total: {formatar_moeda(materiais * meses)}")

    with col3:
        outros = st.number_input(
            "Outros Custos (mensal)",
            min_value=0.0,
            value=st.session_state.outros_custos['outros_mensal'],
            step=500.0,
            help="Outros custos não categorizados"
        )
        st.session_state.outros_custos['outros_mensal'] = outros
        st.caption(f"Total: {formatar_moeda(outros * meses)}")

    # Observações
    st.markdown("---")
    obs = st.text_area(
        "Observações",
        value=st.session_state.outros_custos['observacoes'],
        placeholder="Notas sobre os custos...",
        height=80
    )
    st.session_state.outros_custos['observacoes'] = obs

    # Resumo
    st.markdown("---")

    total_custos_adicionais = (viagens + materiais + outros) * meses
    total_fase_3 = total_terceiros + total_custos_adicionais

    col1, col2 = st.columns([3, 2])
    with col2:
        st.markdown(f"""
        <div class="resultado-card">
            <div class="label-destaque">Total Outros Custos</div>
            <div class="valor-destaque">{formatar_moeda(total_fase_3)}</div>
            <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">
                Terceiros: {formatar_moeda(total_terceiros)}<br>
                Viagens/Mat/Outros: {formatar_moeda(total_custos_adicionais)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Navegação
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Voltar", use_container_width=True):
            st.session_state.fase_atual = 2
            st.rerun()
    with col3:
        if st.button("Ver Precificação Final →", type="primary", use_container_width=True):
            st.session_state.fase_atual = 4
            st.session_state.fase_max_concluida = max(st.session_state.fase_max_concluida, 4)
            st.rerun()

# ==================== FASE 4: PRECIFICAÇÃO FINAL ====================

def renderizar_fase_4():
    st.header("FASE 4: Precificação Final")
    st.markdown('<div class="brivia-alerta">Resumo completo e preço de venda calculado</div>', unsafe_allow_html=True)

    dados = st.session_state.dados_basicos
    meses = dados['quantidade_meses']

    # Régua atual (usa a última selecionada ou padrão)
    regua_id = "mercado"  # Padrão

    # ===== CÁLCULO DOS CUSTOS =====

    # Custo da equipe
    total_equipe = 0
    for func in st.session_state.lista_equipe:
        sal = BASE_SALARIAL.get(func['perfil'], {}).get(func['nivel'], {}).get(regua_id, func.get('salario_base', 0))
        _, custo_ded, custo_tot = calcular_custo_funcionario(sal, func['dedicacao'], meses)
        total_equipe += custo_tot

    # Custo de terceiros
    total_terceiros = sum(t['valor_total'] for t in st.session_state.outros_custos['terceiros'])

    # Outros custos
    outros_custos = st.session_state.outros_custos
    total_viagens = outros_custos['viagens_mensal'] * meses
    total_materiais = outros_custos['materiais_mensal'] * meses
    total_outros = outros_custos['outros_mensal'] * meses

    # Custo total do projeto
    custo_total = total_equipe + total_terceiros + total_viagens + total_materiais + total_outros

    # ===== CÁLCULO DA PRECIFICAÇÃO =====

    gross_margin = dados['gross_margin']
    aliquota = dados['aliquota_imposto']
    comissao_total = dados['comissao_nb'] + dados['comissao_parceiros']

    preco_venda, valor_imposto, valor_comissao, lucro_bruto = calcular_precificacao(
        custo_total, gross_margin, aliquota, comissao_total
    )

    # ===== EXIBIÇÃO =====

    # Resumo do projeto
    st.subheader("📋 Resumo do Projeto")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cliente", dados['cliente'])
        st.metric("Tipo", dados['tipo_contrato'])
    with col2:
        st.metric("Duração", f"{meses} meses")
        st.metric("Empresa", dados['empresa_tributacao'].split(" - ")[0] if dados['empresa_tributacao'] else "-")
    with col3:
        st.metric("Tipo Serviço", dados['tipo_servico'])
        st.metric("Equipe", f"{len(st.session_state.lista_equipe)} profissional(is)")

    st.markdown("---")

    # Detalhamento de custos
    st.subheader("💵 Composição de Custos")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Tabela de custos
        custos_data = [
            ["Equipe CLT", formatar_moeda(total_equipe)],
            ["Terceiros", formatar_moeda(total_terceiros)],
            ["Viagens", formatar_moeda(total_viagens)],
            ["Materiais", formatar_moeda(total_materiais)],
            ["Outros", formatar_moeda(total_outros)],
        ]

        for item, valor in custos_data:
            cols = st.columns([2, 1])
            cols[0].text(item)
            cols[1].text(valor)

        st.markdown("---")
        cols = st.columns([2, 1])
        cols[0].markdown("**CUSTO TOTAL**")
        cols[1].markdown(f"**{formatar_moeda(custo_total)}**")

    with col2:
        # Gráfico de pizza dos custos
        if custo_total > 0:
            fig = go.Figure(data=[go.Pie(
                labels=['Equipe', 'Terceiros', 'Viagens', 'Materiais', 'Outros'],
                values=[total_equipe, total_terceiros, total_viagens, total_materiais, total_outros],
                hole=.4,
                marker_colors=['#90513b', '#b8735c', '#d49680', '#e8b8a8', '#f5dcd5']
            )])
            fig.update_layout(
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                height=250,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Precificação
    st.subheader("🎯 Precificação")

    if preco_venda is None:
        st.error("⚠️ Margem + Impostos + Comissões excedem 100%. Ajuste os parâmetros na Fase 1.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Parâmetros de Cálculo:**")
            params = [
                [f"Custo Total", formatar_moeda(custo_total)],
                [f"Gross Margin", f"{gross_margin:.0f}%"],
                [f"Imposto ({dados['empresa_tributacao'].split(' - ')[0] if dados['empresa_tributacao'] else '-'})", f"{aliquota:.2f}%"],
                [f"Comissões (NB + Parceiros)", f"{comissao_total}%"],
            ]
            for param, val in params:
                cols = st.columns([2, 1])
                cols[0].text(param)
                cols[1].text(val)

        with col2:
            st.markdown("**Composição do Preço de Venda:**")
            composicao = [
                ["Custo do Projeto", formatar_moeda(custo_total)],
                ["Impostos", formatar_moeda(valor_imposto)],
                ["Comissões", formatar_moeda(valor_comissao)],
                ["Lucro Bruto (GM)", formatar_moeda(lucro_bruto)],
            ]
            for item, val in composicao:
                cols = st.columns([2, 1])
                cols[0].text(item)
                cols[1].text(val)

        st.markdown("---")

        # Resultado final
        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.markdown(f"""
            <div class="resultado-card" style="text-align: center;">
                <div class="label-destaque">PREÇO DE VENDA TOTAL</div>
                <div class="valor-destaque" style="font-size: 2.5rem;">{formatar_moeda(preco_venda)}</div>
                <div style="color: rgba(255,255,255,0.7); font-size: 1rem; margin-top: 10px;">
                    Valor Mensal: {formatar_moeda(preco_venda / meses)}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Métricas finais
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Custo Total", formatar_moeda(custo_total))
        with col2:
            st.metric("Preço de Venda", formatar_moeda(preco_venda))
        with col3:
            st.metric("Lucro Bruto", formatar_moeda(lucro_bruto))
        with col4:
            markup = ((preco_venda / custo_total) - 1) * 100 if custo_total > 0 else 0
            st.metric("Markup", f"{markup:.1f}%")

        st.markdown("---")

        # Resumo por mês
        st.subheader("📅 Valores Mensais")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Custo Mensal", formatar_moeda(custo_total / meses))
        with col2:
            st.metric("Receita Mensal", formatar_moeda(preco_venda / meses))
        with col3:
            st.metric("Lucro Mensal", formatar_moeda(lucro_bruto / meses))

    st.markdown("---")

    # Navegação
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Voltar para Custos", use_container_width=True):
            st.session_state.fase_atual = 3
            st.rerun()
    with col2:
        if st.button("🔄 Nova Precificação", use_container_width=True):
            # Reset completo
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with col3:
        if st.button("📊 Exportar (em breve)", use_container_width=True, disabled=True):
            pass

# ==================== INTERFACE PRINCIPAL ====================

def main():
    init_session_state()

    # Indicador de fases
    col1, col2, col3, col4 = st.columns(4)

    fases = [
        (1, "Fase 1: Dados", col1),
        (2, "Fase 2: Equipe", col2),
        (3, "Fase 3: Custos", col3),
        (4, "Fase 4: Preço", col4),
    ]

    for num, nome, col in fases:
        with col:
            if st.session_state.fase_atual == num:
                st.markdown(f'<div class="fase-container fase-atual">{nome}</div>', unsafe_allow_html=True)
            elif st.session_state.fase_max_concluida >= num:
                st.markdown(f'<div class="fase-container fase-ok">{nome}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="fase-container fase-espera">{nome}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Renderização das fases
    if st.session_state.fase_atual == 1:
        renderizar_fase_1()
    elif st.session_state.fase_atual == 2:
        renderizar_fase_2()
    elif st.session_state.fase_atual == 3:
        renderizar_fase_3()
    elif st.session_state.fase_atual == 4:
        renderizar_fase_4()

if __name__ == "__main__":
    main()
