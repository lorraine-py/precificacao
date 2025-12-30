"""
Sistema de Precificação Brivia
Aplicação Principal - Todas as Fases Integradas
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Importar configurações centralizadas
from config_database import (
    TIPOS_CONTRATO, TIPOS_SERVICO, EMPRESAS_TRIBUTACAO,
    COMISSAO_NB, COMISSAO_PARCEIROS, LINHAS_RECEITA, LINHAS_CUSTOS,
    GROSS_MARGIN_ALVO, BASE_SALARIAL, MAPEAMENTO_OFERTAS, RECEITA_TOTAL_CENARIO
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
</style>

<div class="header-brivia">
    <img src="{logo_url}" class="logo-brivia">
    <h1 style="margin:0; font-size: 1.8rem; letter-spacing: -1px;">Sistema de Precificação</h1>
</div>

<video autoplay loop muted playsinline id="brivia-video-bg">
    <source src="{video_url}" type="video/mp4">
</video>
""", unsafe_allow_html=True)

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

def calcular_total_receita(verba_total, comissao_pct):
    """Calcula total da receita"""
    return verba_total * (comissao_pct / 100)

def calcular_valor_total_custo(valor_mensal, quantidade_meses):
    """Calcula valor total do custo"""
    return valor_mensal * quantidade_meses

def calcular_gross_margin_com_desconto(desconto):
    """Calcula gross margin com desconto"""
    return GROSS_MARGIN_ALVO - desconto

# ==================== INICIALIZAÇÃO DO SESSION STATE ====================

def init_session_state():
    """Inicializa todas as variáveis de sessão"""

    if 'fase_atual' not in st.session_state:
        st.session_state.fase_atual = 1

    if 'fase_max_concluida' not in st.session_state:
        st.session_state.fase_max_concluida = 1

    # Dados básicos
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
        }

    # Receita Bruta
    if 'receita_bruta' not in st.session_state:
        st.session_state.receita_bruta = {
            linha: {'verba_total': 0.0, 'comissao_pct': 0.0}
            for linha in LINHAS_RECEITA
        }

    # Custos
    if 'custos' not in st.session_state:
        st.session_state.custos = {
            linha: {'valor_mensal': 0.0, 'observacoes': ''}
            for linha in LINHAS_CUSTOS
        }

    # Gross Margin
    if 'gross_margin' not in st.session_state:
        st.session_state.gross_margin = {
            'desconto': 0.0,
            'observacoes': ''
        }

    # Equipe CLT
    if 'lista_equipe' not in st.session_state:
        st.session_state.lista_equipe = []

# ==================== FASE 1: DADOS BÁSICOS ====================

def renderizar_fase_1():
    st.header("FASE 1: Dados Básicos da Precificação")
    st.markdown('<div class="brivia-alerta">Preencha todos os campos obrigatórios para avançar para a próxima fase</div>', unsafe_allow_html=True)

    # 1. INFORMAÇÕES DO CLIENTE E CONTRATO
    st.subheader("Informações do Cliente e Contrato")

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
            help="Campo obrigatório"
        )
        st.session_state.dados_basicos['tipo_contrato'] = tipo_contrato

        tipo_servico = st.selectbox(
            "Tipo de Serviço *",
            TIPOS_SERVICO,
            index=TIPOS_SERVICO.index(st.session_state.dados_basicos['tipo_servico']),
            help="Campo obrigatório"
        )
        st.session_state.dados_basicos['tipo_servico'] = tipo_servico

    with col2:
        descricao = st.text_area(
            "Descrição do Contrato *",
            value=st.session_state.dados_basicos['descricao_contrato'],
            placeholder="Descreva os serviços a serem prestados",
            help="Campo obrigatório",
            height=100
        )
        st.session_state.dados_basicos['descricao_contrato'] = descricao

        quantidade_meses = st.number_input(
            "Quantidade de Meses do Contrato *",
            min_value=1,
            max_value=60,
            value=st.session_state.dados_basicos['quantidade_meses'],
            help="Campo obrigatório"
        )
        st.session_state.dados_basicos['quantidade_meses'] = quantidade_meses

    st.markdown("---")

    # 2. TRIBUTAÇÃO
    st.subheader("Empresa para Tributação")

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
                "Empresa para Tributação *",
                empresas_disponiveis,
                index=idx,
                help="Empresas disponíveis para o tipo de serviço selecionado"
            )
            st.session_state.dados_basicos['empresa_tributacao'] = empresa_selecionada

            aliquota = EMPRESAS_TRIBUTACAO[empresa_selecionada]['aliquota']
            st.session_state.dados_basicos['aliquota_imposto'] = aliquota

        with col2:
            st.metric(
                "Alíquota de Imposto",
                f"{aliquota:.2f}%",
                help="Calculado automaticamente com base na empresa selecionada"
            )
    else:
        st.warning("Nenhuma empresa disponível para o tipo de serviço selecionado")

    st.markdown("---")

    # 3. COMISSÕES
    st.subheader("Comissões")

    col1, col2 = st.columns(2)

    with col1:
        comissao_nb = st.selectbox(
            "Alíquota de Comissão NB (New Business)",
            COMISSAO_NB,
            index=COMISSAO_NB.index(st.session_state.dados_basicos['comissao_nb']),
            format_func=lambda x: f"{x}%",
            help="Comissão de novos negócios"
        )
        st.session_state.dados_basicos['comissao_nb'] = comissao_nb

    with col2:
        comissao_parceiros = st.selectbox(
            "Alíquota de Comissão Parceiros",
            COMISSAO_PARCEIROS,
            index=COMISSAO_PARCEIROS.index(st.session_state.dados_basicos['comissao_parceiros']),
            format_func=lambda x: f"{x}%",
            help="Comissão de parceiros"
        )
        st.session_state.dados_basicos['comissao_parceiros'] = comissao_parceiros

    st.markdown("---")

    # 4. RECEITA BRUTA
    st.subheader("Receita Adicional")
    st.caption("Informe as receitas adicionais advindas do contrato")

    total_receita_bruta = 0.0

    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    with col1:
        st.markdown("**Tipo de Receita**")
    with col2:
        st.markdown("**Verba Total (R$)**")
    with col3:
        st.markdown("**Comissão (%)**")
    with col4:
        st.markdown("**Total da Receita (R$)**")

    for linha in LINHAS_RECEITA:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        with col1:
            st.text(linha)

        with col2:
            verba = st.number_input(
                f"verba_{linha}",
                min_value=0.0,
                value=st.session_state.receita_bruta[linha]['verba_total'],
                step=1000.0,
                format="%.2f",
                label_visibility="collapsed",
                key=f"verba_{linha}"
            )
            st.session_state.receita_bruta[linha]['verba_total'] = verba

        with col3:
            comissao = st.number_input(
                f"comissao_{linha}",
                min_value=0.0,
                max_value=100.0,
                value=st.session_state.receita_bruta[linha]['comissao_pct'],
                step=0.5,
                format="%.2f",
                label_visibility="collapsed",
                key=f"comissao_{linha}"
            )
            st.session_state.receita_bruta[linha]['comissao_pct'] = comissao

        with col4:
            total_linha = calcular_total_receita(verba, comissao)
            total_receita_bruta += total_linha
            st.text(formatar_moeda(total_linha))

    st.markdown("---")
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    with col1:
        st.markdown("**TOTAL RECEITA ADICIONAL**")
    with col4:
        st.markdown(f"**{formatar_moeda(total_receita_bruta)}**")

    st.markdown("---")

    # 5. CUSTOS
    st.subheader("Custos")
    st.caption("Informe os custos de viagens e outros custos extras")

    total_custos = 0.0

    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
    with col1:
        st.markdown("**Tipo de Custo**")
    with col2:
        st.markdown("**Valor Mensal (R$)**")
    with col3:
        st.markdown("**Valor Total (R$)**")
    with col4:
        st.markdown("**Observações**")

    for linha in LINHAS_CUSTOS:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

        with col1:
            st.text(linha)

        with col2:
            if linha in ["Terceiros", "Materiais"]:
                st.text_input(
                    f"valor_{linha}",
                    value="(Calculado na próxima fase)",
                    disabled=True,
                    label_visibility="collapsed",
                    key=f"valor_{linha}_disabled"
                )
            else:
                valor_mensal = st.number_input(
                    f"valor_{linha}",
                    min_value=0.0,
                    value=st.session_state.custos[linha]['valor_mensal'],
                    step=100.0,
                    format="%.2f",
                    label_visibility="collapsed",
                    key=f"valor_{linha}"
                )
                st.session_state.custos[linha]['valor_mensal'] = valor_mensal

        with col3:
            if linha in ["Terceiros", "Materiais"]:
                st.text("-")
            else:
                valor_total = calcular_valor_total_custo(
                    st.session_state.custos[linha]['valor_mensal'],
                    quantidade_meses
                )
                total_custos += valor_total
                st.text(formatar_moeda(valor_total))

        with col4:
            obs = st.text_input(
                f"obs_{linha}",
                value=st.session_state.custos[linha]['observacoes'],
                placeholder="Observações...",
                label_visibility="collapsed",
                key=f"obs_{linha}"
            )
            st.session_state.custos[linha]['observacoes'] = obs

    st.markdown("---")
    col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
    with col1:
        st.markdown("**TOTAL CUSTOS**")
    with col3:
        st.markdown(f"**{formatar_moeda(total_custos)}**")

    st.markdown("---")

    # 6. GROSS MARGIN
    st.subheader("Gross Margin")

    col1, col2, col3 = st.columns([2, 2, 3])

    with col1:
        st.markdown("")
        st.markdown("")
        st.markdown("**Gross Margin Alvo**")
        st.markdown("")
        st.markdown("")
        st.markdown("**Desconto**")
        st.markdown("")
        st.markdown("")
        st.markdown("**Gross Margin com Desconto**")

    with col2:
        st.metric("", f"{GROSS_MARGIN_ALVO:.2f}%")

        desconto = st.number_input(
            "Desconto GM",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.gross_margin['desconto'],
            step=0.5,
            format="%.2f",
            label_visibility="collapsed"
        )
        st.session_state.gross_margin['desconto'] = desconto

        gm_final = calcular_gross_margin_com_desconto(desconto)
        if gm_final < 20:
            st.error(f"{gm_final:.2f}%")
        elif gm_final < 30:
            st.warning(f"{gm_final:.2f}%")
        else:
            st.success(f"{gm_final:.2f}%")

    with col3:
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        obs_gm = st.text_area(
            "Observações GM",
            value=st.session_state.gross_margin['observacoes'],
            placeholder="Observações sobre gross margin...",
            label_visibility="collapsed",
            height=100
        )
        st.session_state.gross_margin['observacoes'] = obs_gm

    st.markdown("---")

    # RESUMO E VALIDAÇÃO
    st.subheader("Resumo da Fase 1")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Cliente", cliente if cliente else "Não preenchido")
        st.metric("Tipo de Contrato", tipo_contrato)
        st.metric("Duração", f"{quantidade_meses} meses")

    with col2:
        st.metric("Tipo de Serviço", tipo_servico)
        st.metric("Alíquota de Imposto", f"{st.session_state.dados_basicos['aliquota_imposto']:.2f}%")
        st.metric("Receita Adicional", formatar_moeda(total_receita_bruta))

    with col3:
        st.metric("Comissão NB", f"{comissao_nb}%")
        st.metric("Comissão Parceiros", f"{comissao_parceiros}%")
        st.metric("Custos Extras", formatar_moeda(total_custos))

    st.markdown("---")

    # BOTÃO DE AVANÇAR
    fase_valida = validar_fase_1()

    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
        if fase_valida:
            if st.button("Avançar para Equipe CLT", type="primary", use_container_width=True):
                st.session_state.fase_atual = 2
                st.session_state.fase_max_concluida = max(st.session_state.fase_max_concluida, 2)
                st.rerun()
        else:
            st.button("Avançar para Equipe CLT", disabled=True, use_container_width=True)
            st.error("Preencha todos os campos obrigatórios (*) para avançar")

# ==================== FASE 2: EQUIPE CLT ====================

from decimal import Decimal, ROUND_HALF_UP, getcontext

# Configura a precisão do Python para 20 casas decimais
getcontext().prec = 20

def renderizar_fase_2():
    st.header("FASE 2: Equipe CLT")
    st.markdown('<div class="brivia-alerta">Cálculos de alta precisão (Decimal) para grandes volumes financeiros.</div>', unsafe_allow_html=True)

    # --- MOTOR DE ALTA PRECISÃO (Sincronizado com 12 casas do Sheets) ---
    # Usamos Decimal("valor") para garantir que não haja perda no input
    prov_13 = Decimal("100") / Decimal("12")
    prov_ferias = Decimal("11.1110833333333") 

    encargos_fpa = {
        "fgts_base": Decimal("8.00"),
        "fgts_s_13": prov_13 * Decimal("0.08"),
        "fgts_s_ferias": prov_ferias * Decimal("0.08"),
        "inss_gps_base": Decimal("26.30"),
        "inss_s_13": prov_13 * Decimal("0.263"),
        "inss_s_ferias": prov_ferias * Decimal("0.263"),
        "prov_13_salario": prov_13,
        "prov_ferias": prov_ferias,
        "aviso_previo": Decimal("1.32"),
        "auxilio_doenca": Decimal("0.55"),
        "desp_rescisao": Decimal("2.57") # Valor exato da sua tabela de critérios
    }

    FATOR_ENCARGOS = Decimal("1") + (sum(encargos_fpa.values()) / Decimal("100"))
    BENEFICIOS_FIXOS = Decimal("1190")
    HORAS_MES = Decimal("170")

    # Seleção de Régua Salarial
    regua_selecionada = st.radio(
        "Selecione a Régua Salarial:",
        ["Média de mercado", "Faixa Mínima", "Média Brivia (mercer)"],
        horizontal=True
    )
    mapa_regua = {"Média de mercado": "mercado", "Faixa Mínima": "minima", "Média Brivia (mercer)": "brivia"}
    regua_id = mapa_regua[regua_selecionada]

    # Entrada de Dados
    col1, col2 = st.columns(2)
    with col1:
        perfil = st.selectbox("Perfil", list(BASE_SALARIAL.keys()))
        nivel = st.selectbox("Nível", ["1. Junior", "2. Pleno", "3. Sênior", "4. Líder", "5. Head", "6. Especialista"])
    with col2:
        qtd_func = st.number_input("Quantidade de Funcionários", min_value=1, value=1)
        dedicacao = st.slider("Dedicação (%)", 0, 100, 50)

    # --- CÁLCULOS COM PRECISÃO DE 12 CASAS ---
    # Buscamos o salário e convertemos para Decimal imediatamente
    sal_raw = BASE_SALARIAL.get(perfil, {}).get(nivel, {}).get(regua_id, 0)
    salario_base = Decimal(str(sal_raw))
    
    total_horas = Decimal(str(qtd_func)) * (Decimal(str(dedicacao)) / Decimal("100")) * HORAS_MES
    
    if salario_base > 0:
        # Custo Hora calculado exatamente como a célula J10
        custo_hora = ((salario_base * FATOR_ENCARGOS) + BENEFICIOS_FIXOS) / HORAS_MES
        # Custo Total calculado exatamente como a célula K10 (9.868,02915156)
        custo_total = custo_hora * total_horas
    else:
        custo_hora = Decimal("0")
        custo_total = Decimal("0")

    # Métricas com exibição controlada (mas o valor interno é exato)
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Salário Base", f"R$ {salario_base:,.2f}")
    m2.metric("Custo Hora (Preciso)", f"R$ {custo_hora:.8f}") # Exibe 8 casas para bater com a célula J10
    m3.metric("Total Horas", f"{total_horas:.1f}h")
    m4.metric("Custo Total", f"R$ {custo_total:,.2f}") 
    
    # Debug para você ver as 12 casas decimais do Custo Total
    st.caption(f"Valor Bruto Custo Total: R$ {custo_total:.12f}")

    if st.button("＋ Adicionar Funcionário à Equipe", use_container_width=True):
        st.session_state.lista_equipe.append({
            "Perfil": perfil, "Nível": nivel, "Qtd": qtd_func, "Dedicação %": dedicacao
        })
        st.rerun()

    # Tabela de Resumo (Dataframe com suporte a Decimal)
    if st.session_state.lista_equipe:
        df = pd.DataFrame(st.session_state.lista_equipe)

        def calc_financeiro(row):
            s_val = Decimal(str(BASE_SALARIAL.get(row['Perfil'], {}).get(row['Nível'], {}).get(regua_id, 0)))
            c_h = ((s_val * FATOR_ENCARGOS) + BENEFICIOS_FIXOS) / HORAS_MES if s_val > 0 else Decimal("0")
            t_h = Decimal(str(row['Qtd'])) * (Decimal(str(row['Dedicação %'])) / Decimal("100")) * HORAS_MES
            c_t = c_h * t_h
            # Retornamos como float apenas para o Streamlit exibir no gráfico/tabela
            return pd.Series([float(s_val), float(c_h), float(c_t)], index=['Salário Base', 'Custo Hora', 'Custo Total'])

        df[['Salário Base', 'Custo Hora', 'Custo Total']] = df.apply(calc_financeiro, axis=1)
        st.data_editor(df, use_container_width=True, disabled=True)
        st.metric("Soma Total do Projeto", f"R$ {df['Custo Total'].sum():,.2f}")
        # Botão Voltar e Avançar
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Voltar para Fase 1", use_container_width=True):
                st.session_state.fase_atual = 1
                st.rerun()
        with col3:
            if st.button("Avançar para Fase 3 →", type="primary", use_container_width=True):
                st.session_state.fase_atual = 3
                st.session_state.fase_max_concluida = max(st.session_state.fase_max_concluida, 3)
                st.rerun()
    else:
        st.info("Adicione funcionários à equipe para continuar")

# ==================== INTERFACE PRINCIPAL ====================

def main():
    init_session_state()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.session_state.fase_atual == 1:
            st.markdown('<div class="fase-container fase-atual">Fase 1: Dados Básicos</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fase-container fase-ok">Fase 1: Ok</div>', unsafe_allow_html=True)

    with col2:
        if st.session_state.fase_atual == 2:
            st.markdown('<div class="fase-container fase-atual">Fase 2: Equipe CLT</div>', unsafe_allow_html=True)
        elif st.session_state.fase_max_concluida >= 2:
            st.markdown('<div class="fase-container fase-ok">Fase 2: Ok</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fase-container fase-espera">Fase 2: Aguardando</div>', unsafe_allow_html=True)

    with col3:
        if st.session_state.fase_atual == 3:
            st.markdown('<div class="fase-container fase-atual">Fase 3: Terceiros</div>', unsafe_allow_html=True)
        elif st.session_state.fase_max_concluida >= 3:
            st.markdown('<div class="fase-container fase-ok">Fase 3: Ok</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fase-container fase-espera">Fase 3: Aguardando</div>', unsafe_allow_html=True)

    with col4:
        if st.session_state.fase_atual == 4:
            st.markdown('<div class="fase-container fase-atual">Fase 4: Ferramentas</div>', unsafe_allow_html=True)
        elif st.session_state.fase_max_concluida >= 4:
            st.markdown('<div class="fase-container fase-ok">Fase 4: Ok</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="fase-container fase-espera">Fase 4: Aguardando</div>', unsafe_allow_html=True)

    st.markdown("---")

    if st.session_state.fase_atual == 1:
        renderizar_fase_1()
    elif st.session_state.fase_atual == 2:
        renderizar_fase_2()
    elif st.session_state.fase_atual == 3:
        st.info("Fase 3 (Terceiros) em desenvolvimento")
    elif st.session_state.fase_atual == 4:
        st.info("Fase 4 (Ferramentas) em desenvolvimento")

if __name__ == "__main__":
    main()

