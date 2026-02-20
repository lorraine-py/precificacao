"""
Configuração Centralizada - Base de Dados e Constantes
Sistema de Precificação Brivia
"""

# ==================== TIPOS E CONFIGURAÇÕES BÁSICAS ====================

TIPOS_CONTRATO = ["Fee", "Projeto"]

TIPOS_SERVICO = [
    "Tecnologia",
    "Comunicação",
    "Tecnologia - Exportação",
    "Comunicação - Exportação"
]

EMPRESAS_TRIBUTACAO = {
    "Malagueta - Comunicação": {"empresa": "Malagueta", "servico": "Comunicação", "aliquota": 8.65},
    "Habanero - Tecnologia": {"empresa": "Habanero", "servico": "Tecnologia", "aliquota": 6.55},
    "Habanero - Comunicação": {"empresa": "Habanero", "servico": "Comunicação", "aliquota": 14.25},
    "Brivia - Tecnologia": {"empresa": "Brivia", "servico": "Tecnologia", "aliquota": 5.65},
    "Brivia - Comunicação": {"empresa": "Brivia", "servico": "Comunicação", "aliquota": 11.25},
    "Brivia - Tecnologia - Exportação": {"empresa": "Brivia", "servico": "Tecnologia - Exportação", "aliquota": 0.00},
    "Brivia - Comunicação - Exportação": {"empresa": "Brivia", "servico": "Comunicação - Exportação", "aliquota": 0.00},
    "Dez - Tecnologia": {"empresa": "Dez", "servico": "Tecnologia", "aliquota": 5.65},
    "Dez - Comunicação": {"empresa": "Dez", "servico": "Comunicação", "aliquota": 11.25},
    "Heads RS - Tecnologia": {"empresa": "Heads RS", "servico": "Tecnologia", "aliquota": 5.65},
    "Heads RS - Comunicação": {"empresa": "Heads RS", "servico": "Comunicação", "aliquota": 11.25},
    "Heads PR - Tecnologia": {"empresa": "Heads PR", "servico": "Tecnologia", "aliquota": 8.65},
    "Heads PR - Comunicação": {"empresa": "Heads PR", "servico": "Comunicação", "aliquota": 14.25},
    "Briviacom RS - Tecnologia": {"empresa": "Briviacom RS", "servico": "Tecnologia", "aliquota": 8.65},
    "Briviacom RS - Comunicação": {"empresa": "Briviacom RS", "servico": "Comunicação", "aliquota": 11.25},
    "Briviacom Brasília - Tecnologia": {"empresa": "Briviacom Brasília", "servico": "Tecnologia", "aliquota": 8.65},
    "Briviacom Brasília - Comunicação": {"empresa": "Briviacom Brasília", "servico": "Comunicação", "aliquota": 14.25},
}

COMISSAO_NB = [0, 1, 2, 3]
COMISSAO_PARCEIROS = [0, 1, 2, 3, 4, 5, 6, 7, 8]

LINHAS_RECEITA = [
    "Comissão de mídia",
    "Honorários de produção",
    "Comissão de ferramentas",
    "Bônus de veiculação (PIA)",
    "Outras receitas"
]

LINHAS_CUSTOS = [
    "Terceiros",
    "Materiais",
    "Viagens",
    "Outros custos"
]

GROSS_MARGIN_ALVO = 40.0

# ==================== CONFIGURAÇÕES DE CUSTOS ====================

ENCARGOS_PERCENTUAL = 64.853851583333  # Total de encargos sobre salário base
CUSTO_INDIRETO_PERCENTUAL = 0.00  # 0,00%

BENEFICIOS = {
    "vale_refeicao": 654.00,
    "seguro_vida": 8.95,
    "plano_saude": 380.00,
    "home_office": 120.00,
    "total": 1162.95
}

ESTRUTURA = {
    "licencas": 541.73,
    "equipamento_depreciacao": 200.00,
    "total": 741.73
}

DEPRECIACAO = 0.00
QUANTIDADE_HORAS_MES = 170

# ==================== IMPOSTOS POR TIPO DE SERVIÇO ====================

IMPOSTOS_SERVICO = {
    "Comunicação": {
        "ISSQN": 2.00,
        "PIS": 1.65,
        "COFINS": 7.60,
        "total": 11.25
    },
    "Tecnologia": {
        "ISSQN": 2.00,
        "PIS": 0.65,
        "COFINS": 3.00,
        "total": 5.65
    }
}

# ==================== BITRIBUTAÇÃO ====================

BITRIBUTACAO = {
    "Nacional": {
        "IOF": 0.00,
        "CIDE": 0.00,
        "ISS": 2.00,
        "INSS": 4.50,
        "PIS": 0.65,
        "COFINS": 3.00,
        "IRRF": 34.00,
        "CSLL": 0.00,
        "total": 44.15
    },
    "Internacional": {
        "IOF": 0.00,
        "CIDE": 0.00,
        "ISS": 2.00,
        "INSS": 4.50,
        "PIS": 1.65,
        "COFINS": 7.60,
        "IRRF": 25.00,
        "CSLL": 9.00,
        "total": 49.75
    }
}

# ==================== ENCARGOS DETALHADOS ====================
# Valores com precisão completa conforme cálculos da planilha

ENCARGOS_DETALHADOS = {
    "FGTS": 8.000000000000,                    # 8% s/salário base
    "FGTS_13": 0.666666666667,                 # 8% s/13º
    "FGTS_ferias": 0.888886666667,             # 8% s/férias
    "INSS_GPS": 26.300000000000,               # 26,3% s/sal base
    "INSS_13": 2.191666666667,                 # 26,3% s/13º
    "INSS_ferias": 2.922214916667,             # 26,3% s/férias
    "prov_13_salario": 8.333333333333,         # 1/12 s/sal base
    "prov_ferias": 11.111083333333,            # 11,11% s/sal base
    "aviso_previo": 1.320000000000,            # 1,32% s/sal base
    "auxilio_doenca": 0.550000000000,          # 0,55% s/sal base
    "desp_rescisao": 2.570000000000,           # 2,57% s/sal base
    "total": 64.853851583333                   # Soma de todos os encargos
}

# ==================== TOOLS (MOEDA) ====================

TOOLS_MOEDA = ["Nacional", "Internacional"]
MOEDA_NACIONAL = "Dólar"
MOEDA_INTERNACIONAL = "Euro"

# ==================== NÍVEIS SALARIAIS POR REGIÃO ====================

NIVEIS_SALARIAIS = {
    "1. Junior": {
        "SP_RJ_BSB_Step2": 3740,
        "SP_RJ_BSB_Step3": 4206,
        "Outros_Est_Step2": 3142,
        "Outros_Est_Step3": 3533,
        "RS_Step2": 2992,
        "RS_Step3": 3365,
        "Media_RS_SP_Step3": 3785
    },
    "2. Pleno": {
        "SP_RJ_BSB_Step2": 5374,
        "SP_RJ_BSB_Step3": 6044,
        "Outros_Est_Step2": 4514,
        "Outros_Est_Step3": 5077,
        "RS_Step2": 4299,
        "RS_Step3": 4835,
        "Media_RS_SP_Step3": 5440
    },
    "3. Sênior": {
        "SP_RJ_BSB_Step2": 7722,
        "SP_RJ_BSB_Step3": 8685,
        "Outros_Est_Step2": 6487,
        "Outros_Est_Step3": 7296,
        "RS_Step2": 6178,
        "RS_Step3": 6948,
        "Media_RS_SP_Step3": 7817
    },
    "4. Líder": {
        "SP_RJ_BSB_Step2": 10775,
        "SP_RJ_BSB_Step3": 12480,
        "Outros_Est_Step2": 9051,
        "Outros_Est_Step3": 10483,
        "RS_Step2": 8620,
        "RS_Step3": 9984,
        "Media_RS_SP_Step3": 11232
    },
    "5. Head": {
        "SP_RJ_BSB_Step2": 16715,
        "SP_RJ_BSB_Step3": 19360,
        "Outros_Est_Step2": 14040,
        "Outros_Est_Step3": 16263,
        "RS_Step2": 13372,
        "RS_Step3": 15488,
        "Media_RS_SP_Step3": 17424
    }
}

# ==================== BASE SALARIAL COMPLETA (MERCER) ====================

BASE_SALARIAL = {
    "Gerente de DBM": {
        "1. Junior": {"mercado": 12875, "minima": 9000, "brivia": 12480},
        "2. Pleno": {"mercado": 13450, "minima": 11500, "brivia": 12480},
        "3. Sênior": {"mercado": 16325, "minima": 14000, "brivia": 14961},
        "4. Líder": {"mercado": 16325, "minima": 14000, "brivia": 14961},
        "5. Head": {"mercado": 20000, "minima": 17000, "brivia": 19360},
        "6. Especialista": {"mercado": 21125, "minima": 18500, "brivia": 19360},
    },
    "CRM Planner": {
        "1. Junior": {"mercado": 6600, "minima": 5500, "brivia": 6044},
        "2. Pleno": {"mercado": 11000, "minima": 9000, "brivia": 8685},
        "3. Sênior": {"mercado": 13250, "minima": 11000, "brivia": 12480},
        "4. Líder": {"mercado": 14250, "minima": 12000, "brivia": 12480},
        "5. Head": {"mercado": 16375, "minima": 14000, "brivia": 14961},
        "6. Especialista": {"mercado": 17375, "minima": 15000, "brivia": 14961},
    },
    "Arquiteto do Salesforce": {
        "1. Junior": {"mercado": 14980, "minima": 12000, "brivia": 12480},
        "2. Pleno": {"mercado": 14250, "minima": 12000, "brivia": 14961},
        "3. Sênior": {"mercado": 16375, "minima": 14000, "brivia": 14961},
        "4. Líder": {"mercado": 18125, "minima": 15500, "brivia": 14961},
        "5. Head": {"mercado": 20375, "minima": 18000, "brivia": 19360},
        "6. Especialista": {"mercado": 22375, "minima": 20000, "brivia": 19360},
    },
    "Desenvolvedor do Salesforce": {
        "1. Junior": {"mercado": 8738, "minima": 7000, "brivia": 6044},
        "2. Pleno": {"mercado": 11000, "minima": 9000, "brivia": 7245},
        "3. Sênior": {"mercado": 13250, "minima": 11000, "brivia": 10411},
        "4. Líder": {"mercado": 15000, "minima": 12500, "brivia": 10411},
        "5. Head": {"mercado": 17375, "minima": 15000, "brivia": 12480},
        "6. Especialista": {"mercado": 17625, "minima": 16000, "brivia": 14961},
    },
    "Consultor do Salesforce": {
        "1. Junior": {"mercado": 7615, "minima": 6100, "brivia": 6044},
        "2. Pleno": {"mercado": 11750, "minima": 9500, "brivia": 7245},
        "3. Sênior": {"mercado": 13750, "minima": 11500, "brivia": 10411},
        "4. Líder": {"mercado": 15375, "minima": 13000, "brivia": 10411},
        "5. Head": {"mercado": 17625, "minima": 15000, "brivia": 12480},
        "6. Especialista": {"mercado": 19375, "minima": 17000, "brivia": 14961},
    },
    "Administrador do Salesforce": {
        "1. Junior": {"mercado": 7116, "minima": 5700, "brivia": 6044},
        "2. Pleno": {"mercado": 10500, "minima": 8500, "brivia": 7245},
        "3. Sênior": {"mercado": 12000, "minima": 10000, "brivia": 10411},
        "4. Líder": {"mercado": 13750, "minima": 11500, "brivia": 10411},
        "5. Head": {"mercado": 15500, "minima": 13000, "brivia": 12480},
        "6. Especialista": {"mercado": 15875, "minima": 14000, "brivia": 14961},
    },
    "Analista de Conteúdo": {
        "1. Junior": {"mercado": 4300, "minima": 3500, "brivia": 4206},
        "2. Pleno": {"mercado": 6700, "minima": 5500, "brivia": 6044},
        "3. Sênior": {"mercado": 8500, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 10375, "minima": 8500, "brivia": 10411},
        "5. Head": {"mercado": 13375, "minima": 11000, "brivia": 12480},
        "6. Especialista": {"mercado": 12250, "minima": 10000, "brivia": 12480},
    },
    "Analista de CRM": {
        "1. Junior": {"mercado": 6000, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 8125, "minima": 6500, "brivia": 6044},
        "3. Sênior": {"mercado": 10750, "minima": 8500, "brivia": 7245},
        "4. Líder": {"mercado": 12375, "minima": 10000, "brivia": 10411},
        "5. Head": {"mercado": 15750, "minima": 13000, "brivia": 12480},
        "6. Especialista": {"mercado": 13250, "minima": 11000, "brivia": 12480},
    },
    "Analista de Dados": {
        "1. Junior": {"mercado": 6625, "minima": 5000, "brivia": 6044},
        "2. Pleno": {"mercado": 8625, "minima": 7000, "brivia": 7245},
        "3. Sênior": {"mercado": 11250, "minima": 9000, "brivia": 10411},
        "4. Líder": {"mercado": 13250, "minima": 11000, "brivia": 12480},
        "5. Head": {"mercado": 16375, "minima": 14000, "brivia": 14961},
        "6. Especialista": {"mercado": 14250, "minima": 12000, "brivia": 12480},
    },
    "Analista de DBM": {
        "1. Junior": {"mercado": 5300, "minima": 4100, "brivia": 4206},
        "2. Pleno": {"mercado": 7500, "minima": 5900, "brivia": 6044},
        "3. Sênior": {"mercado": 10200, "minima": 8000, "brivia": 7245},
        "4. Líder": {"mercado": 12800, "minima": 10500, "brivia": 10411},
        "5. Head": {"mercado": 16000, "minima": 13200, "brivia": 12480},
        "6. Especialista": {"mercado": 13800, "minima": 11500, "brivia": 12480},
    },
    "Analista de Estratégia": {
        "1. Junior": {"mercado": 6000, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 8125, "minima": 6500, "brivia": 6044},
        "3. Sênior": {"mercado": 10750, "minima": 8500, "brivia": 7245},
        "4. Líder": {"mercado": 12250, "minima": 10000, "brivia": 10411},
        "5. Head": {"mercado": 15375, "minima": 13000, "brivia": 12480},
        "6. Especialista": {"mercado": 13250, "minima": 11000, "brivia": 12480},
    },
    "Analista de Inbound": {
        "1. Junior": {"mercado": 5200, "minima": 4000, "brivia": 4206},
        "2. Pleno": {"mercado": 6700, "minima": 5500, "brivia": 6044},
        "3. Sênior": {"mercado": 8500, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 10375, "minima": 8500, "brivia": 10411},
        "5. Head": {"mercado": 13375, "minima": 11000, "brivia": 12480},
        "6. Especialista": {"mercado": 12250, "minima": 10000, "brivia": 10411},
    },
    "Analista de Infraestrutura": {
        "1. Junior": {"mercado": 6000, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 8125, "minima": 6500, "brivia": 6044},
        "3. Sênior": {"mercado": 10750, "minima": 8500, "brivia": 7245},
        "4. Líder": {"mercado": 12250, "minima": 10000, "brivia": 10411},
        "5. Head": {"mercado": 15375, "minima": 13000, "brivia": 12480},
        "6. Especialista": {"mercado": 13250, "minima": 11000, "brivia": 12480},
    },
    "Analista de Midia": {
        "1. Junior": {"mercado": 5500, "minima": 4000, "brivia": 4206},
        "2. Pleno": {"mercado": 7625, "minima": 6000, "brivia": 6044},
        "3. Sênior": {"mercado": 9625, "minima": 8000, "brivia": 7245},
        "4. Líder": {"mercado": 11750, "minima": 9500, "brivia": 10411},
        "5. Head": {"mercado": 14375, "minima": 12000, "brivia": 12480},
        "6. Especialista": {"mercado": 12250, "minima": 10000, "brivia": 10411},
    },
    "Analista de Mídias Sociais": {
        "1. Junior": {"mercado": 5200, "minima": 4000, "brivia": 4206},
        "2. Pleno": {"mercado": 6700, "minima": 5500, "brivia": 6044},
        "3. Sênior": {"mercado": 8500, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 10375, "minima": 8500, "brivia": 10411},
        "5. Head": {"mercado": 13375, "minima": 11000, "brivia": 12480},
        "6. Especialista": {"mercado": 12250, "minima": 10000, "brivia": 10411},
    },
    "Analista de Performance": {
        "1. Junior": {"mercado": 4800, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 6900, "minima": 6000, "brivia": 6044},
        "3. Sênior": {"mercado": 9275, "minima": 7500, "brivia": 7245},
        "4. Líder": {"mercado": 11600, "minima": 9000, "brivia": 10411},
        "5. Head": {"mercado": 14300, "minima": 11500, "brivia": 12480},
        "6. Especialista": {"mercado": 11325, "minima": 10000, "brivia": 10411},
    },
    "Analista de Plataforma": {
        "1. Junior": {"mercado": 4725, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 7050, "minima": 6000, "brivia": 6044},
        "3. Sênior": {"mercado": 9475, "minima": 7800, "brivia": 7245},
        "4. Líder": {"mercado": 11900, "minima": 9200, "brivia": 10411},
        "5. Head": {"mercado": 14425, "minima": 11000, "brivia": 12480},
        "6. Especialista": {"mercado": 11400, "minima": 9800, "brivia": 10411},
    },
    "Analista de Qualidade/ Tester": {
        "1. Junior": {"mercado": 4475, "minima": 4200, "brivia": 4206},
        "2. Pleno": {"mercado": 6600, "minima": 5600, "brivia": 6044},
        "3. Sênior": {"mercado": 8900, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 11150, "minima": 8500, "brivia": 10411},
        "5. Head": {"mercado": 13550, "minima": 10200, "brivia": 12480},
        "6. Especialista": {"mercado": 10750, "minima": 9400, "brivia": 10411},
    },
    "Analista de SAC": {
        "1. Junior": {"mercado": 4050, "minima": 3800, "brivia": 4206},
        "2. Pleno": {"mercado": 5725, "minima": 4800, "brivia": 6044},
        "3. Sênior": {"mercado": 7700, "minima": 6200, "brivia": 7245},
        "4. Líder": {"mercado": 9725, "minima": 7500, "brivia": 10411},
        "5. Head": {"mercado": 12075, "minima": 9500, "brivia": 12480},
        "6. Especialista": {"mercado": 10000, "minima": 8800, "brivia": 10411},
    },
    "Analista de Sistema": {
        "1. Junior": {"mercado": 4675, "minima": 4200, "brivia": 4206},
        "2. Pleno": {"mercado": 6900, "minima": 5500, "brivia": 6044},
        "3. Sênior": {"mercado": 9225, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 11550, "minima": 8500, "brivia": 10411},
        "5. Head": {"mercado": 13925, "minima": 10000, "brivia": 12480},
        "6. Especialista": {"mercado": 11100, "minima": 9200, "brivia": 10411},
    },
    "Analista de Suporte": {
        "1. Junior": {"mercado": 4225, "minima": 4000, "brivia": 4206},
        "2. Pleno": {"mercado": 6250, "minima": 5200, "brivia": 6044},
        "3. Sênior": {"mercado": 8375, "minima": 6500, "brivia": 7245},
        "4. Líder": {"mercado": 10550, "minima": 8000, "brivia": 10411},
        "5. Head": {"mercado": 12775, "minima": 9800, "brivia": 12480},
        "6. Especialista": {"mercado": 10600, "minima": 9000, "brivia": 10411},
    },
    "Analista Growth": {
        "1. Junior": {"mercado": 4650, "minima": 3800, "brivia": 4206},
        "2. Pleno": {"mercado": 6725, "minima": 6000, "brivia": 6044},
        "3. Sênior": {"mercado": 8875, "minima": 7500, "brivia": 7245},
        "4. Líder": {"mercado": 11075, "minima": 9000, "brivia": 10411},
        "5. Head": {"mercado": 13550, "minima": 11000, "brivia": 12480},
        "6. Especialista": {"mercado": 10925, "minima": 10200, "brivia": 10411},
    },
    "Analista SEO": {
        "1. Junior": {"mercado": 4600, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 6675, "minima": 5800, "brivia": 6044},
        "3. Sênior": {"mercado": 8825, "minima": 7200, "brivia": 7245},
        "4. Líder": {"mercado": 11000, "minima": 8800, "brivia": 10411},
        "5. Head": {"mercado": 13350, "minima": 10500, "brivia": 12480},
        "6. Especialista": {"mercado": 10750, "minima": 9800, "brivia": 10411},
    },
    "Arte Finalista": {
        "1. Junior": {"mercado": 4000, "minima": 3900, "brivia": 4206},
        "2. Pleno": {"mercado": 5725, "minima": 5100, "brivia": 6044},
        "3. Sênior": {"mercado": 7675, "minima": 6400, "brivia": 7245},
        "4. Líder": {"mercado": 9775, "minima": 7900, "brivia": 10411},
        "5. Head": {"mercado": 11950, "minima": 9600, "brivia": 12480},
        "6. Especialista": {"mercado": 9850, "minima": 9100, "brivia": 10411},
    },
    "Atendimento": {
        "1. Junior": {"mercado": 4275, "minima": 3800, "brivia": 4206},
        "2. Pleno": {"mercado": 6100, "minima": 5000, "brivia": 6044},
        "3. Sênior": {"mercado": 8150, "minima": 7000, "brivia": 7245},
        "4. Líder": {"mercado": 10225, "minima": 10000, "brivia": 10411},
        "5. Head": {"mercado": 12600, "minima": 12500, "brivia": 12480},
        "6. Especialista": {"mercado": 12400, "minima": 10000, "brivia": 10411},
    },
    "Cientista de Dados": {
        "1. Junior": {"mercado": 6000, "minima": 5200, "brivia": 6044},
        "2. Pleno": {"mercado": 7700, "minima": 6800, "brivia": 6044},
        "3. Sênior": {"mercado": 10225, "minima": 8600, "brivia": 7245},
        "4. Líder": {"mercado": 12600, "minima": 10200, "brivia": 10411},
        "5. Head": {"mercado": 15025, "minima": 12800, "brivia": 12480},
        "6. Especialista": {"mercado": 12600, "minima": 12000, "brivia": 12480},
    },
    "Desenvolvedor Back-End": {
        "1. Junior": {"mercado": 5000, "minima": 4800, "brivia": 6044},
        "2. Pleno": {"mercado": 7475, "minima": 6500, "brivia": 7245},
        "3. Sênior": {"mercado": 10100, "minima": 8200, "brivia": 10411},
        "4. Líder": {"mercado": 12550, "minima": 9800, "brivia": 12480},
        "5. Head": {"mercado": 15200, "minima": 12000, "brivia": 12480},
        "6. Especialista": {"mercado": 12325, "minima": 11500, "brivia": 12480},
    },
    "Desenvolvedor de Dados": {
        "1. Junior": {"mercado": 5050, "minima": 4900, "brivia": 6044},
        "2. Pleno": {"mercado": 7500, "minima": 6600, "brivia": 7245},
        "3. Sênior": {"mercado": 10150, "minima": 8300, "brivia": 10411},
        "4. Líder": {"mercado": 12600, "minima": 10000, "brivia": 12480},
        "5. Head": {"mercado": 15100, "minima": 12200, "brivia": 12480},
        "6. Especialista": {"mercado": 12400, "minima": 11800, "brivia": 12480},
    },
    "Desenvolver Front-end": {
        "1. Junior": {"mercado": 4800, "minima": 4700, "brivia": 6044},
        "2. Pleno": {"mercado": 7200, "minima": 6400, "brivia": 7245},
        "3. Sênior": {"mercado": 9750, "minima": 8000, "brivia": 10411},
        "4. Líder": {"mercado": 12125, "minima": 9600, "brivia": 12480},
        "5. Head": {"mercado": 14675, "minima": 11800, "brivia": 12480},
        "6. Especialista": {"mercado": 11900, "minima": 11400, "brivia": 12480},
    },
    "Desenvolver Full Stack": {
        "1. Junior": {"mercado": 5100, "minima": 4600, "brivia": 6044},
        "2. Pleno": {"mercado": 7600, "minima": 6300, "brivia": 7245},
        "3. Sênior": {"mercado": 10150, "minima": 7900, "brivia": 10411},
        "4. Líder": {"mercado": 12600, "minima": 9500, "brivia": 12480},
        "5. Head": {"mercado": 15075, "minima": 11600, "brivia": 12480},
        "6. Especialista": {"mercado": 12400, "minima": 11300, "brivia": 12480},
    },
    "Diretor de Arte": {
        "1. Junior": {"mercado": 4700, "minima": 4500, "brivia": 4206},
        "2. Pleno": {"mercado": 6925, "minima": 6400, "brivia": 6044},
        "3. Sênior": {"mercado": 9100, "minima": 8000, "brivia": 7245},
        "4. Líder": {"mercado": 11300, "minima": 9600, "brivia": 10411},
        "5. Head": {"mercado": 13825, "minima": 11800, "brivia": 12480},
        "6. Especialista": {"mercado": 11275, "minima": 9000, "brivia": 12480},
    },
    "Editor de Conteúdo": {
        "1. Junior": {"mercado": 4400, "minima": 4300, "brivia": 4206},
        "2. Pleno": {"mercado": 6375, "minima": 5700, "brivia": 6044},
        "3. Sênior": {"mercado": 8575, "minima": 7100, "brivia": 7245},
        "4. Líder": {"mercado": 10825, "minima": 8800, "brivia": 10411},
        "5. Head": {"mercado": 13425, "minima": 11300, "brivia": 12480},
        "6. Especialista": {"mercado": 10975, "minima": 10100, "brivia": 12480},
    },
    "Engenheiro de Dados": {
        "1. Junior": {"mercado": 5275, "minima": 5200, "brivia": 6044},
        "2. Pleno": {"mercado": 7700, "minima": 6600, "brivia": 7245},
        "3. Sênior": {"mercado": 10175, "minima": 8200, "brivia": 10411},
        "4. Líder": {"mercado": 12600, "minima": 10000, "brivia": 12480},
        "5. Head": {"mercado": 15225, "minima": 12500, "brivia": 19360},
        "6. Especialista": {"mercado": 12400, "minima": 11200, "brivia": 12480},
    },
    "Engenheiro de Sistema": {
        "1. Junior": {"mercado": 5325, "minima": 4500, "brivia": 6044},
        "2. Pleno": {"mercado": 7800, "minima": 6800, "brivia": 7245},
        "3. Sênior": {"mercado": 10300, "minima": 8400, "brivia": 10411},
        "4. Líder": {"mercado": 12750, "minima": 10200, "brivia": 12480},
        "5. Head": {"mercado": 15475, "minima": 12800, "brivia": 19360},
        "6. Especialista": {"mercado": 12400, "minima": 11400, "brivia": 12480},
    },
    "Gerente de Projeto": {
        "1. Junior": {"mercado": 6500, "minima": 5900, "brivia": 7760},
        "2. Pleno": {"mercado": 8525, "minima": 7800, "brivia": 8989},
        "3. Sênior": {"mercado": 11175, "minima": 9500, "brivia": 10411},
        "4. Líder": {"mercado": 13700, "minima": 11200, "brivia": 12480},
        "5. Head": {"mercado": 16500, "minima": 13800, "brivia": 19360},
        "6. Especialista": {"mercado": 13225, "minima": 12400, "brivia": 12480},
    },
    "Product Owner": {
        "1. Junior": {"mercado": 5525, "minima": 5200, "brivia": 6044},
        "2. Pleno": {"mercado": 8000, "minima": 6700, "brivia": 7245},
        "3. Sênior": {"mercado": 10450, "minima": 8100, "brivia": 10411},
        "4. Líder": {"mercado": 13025, "minima": 9800, "brivia": 12480},
        "5. Head": {"mercado": 15850, "minima": 12300, "brivia": 19360},
        "6. Especialista": {"mercado": 12500, "minima": 10900, "brivia": 12480},
    },
    "Produtor": {
        "1. Junior": {"mercado": 4450, "minima": 3800, "brivia": 4206},
        "2. Pleno": {"mercado": 6400, "minima": 6200, "brivia": 6044},
        "3. Sênior": {"mercado": 8475, "minima": 7700, "brivia": 7245},
        "4. Líder": {"mercado": 10550, "minima": 9200, "brivia": 10411},
        "5. Head": {"mercado": 13050, "minima": 11700, "brivia": 12480},
        "6. Especialista": {"mercado": 10650, "minima": 10400, "brivia": 12480},
    },
    "Redator": {
        "1. Junior": {"mercado": 4500, "minima": 3800, "brivia": 4206},
        "2. Pleno": {"mercado": 6450, "minima": 5400, "brivia": 6044},
        "3. Sênior": {"mercado": 8525, "minima": 7900, "brivia": 7245},
        "4. Líder": {"mercado": 10600, "minima": 9400, "brivia": 10411},
        "5. Head": {"mercado": 13125, "minima": 12000, "brivia": 12480},
        "6. Especialista": {"mercado": 10700, "minima": 10600, "brivia": 12480},
    },
    "Scrum Master": {
        "1. Junior": {"mercado": 5425, "minima": 4300, "brivia": 4206},
        "2. Pleno": {"mercado": 8375, "minima": 6700, "brivia": 6044},
        "3. Sênior": {"mercado": 11300, "minima": 9100, "brivia": 7245},
        "4. Líder": {"mercado": 14200, "minima": 11400, "brivia": 10411},
        "5. Head": {"mercado": 17100, "minima": 13700, "brivia": 19360},
        "6. Especialista": {"mercado": 13225, "minima": 10600, "brivia": 12480},
    },
    "UI": {
        "1. Junior": {"mercado": 4450, "minima": 3500, "brivia": 4206},
        "2. Pleno": {"mercado": 6900, "minima": 5400, "brivia": 6044},
        "3. Sênior": {"mercado": 9300, "minima": 7200, "brivia": 7245},
        "4. Líder": {"mercado": 11725, "minima": 9100, "brivia": 10411},
        "5. Head": {"mercado": 14500, "minima": 11400, "brivia": 12480},
        "6. Especialista": {"mercado": 11250, "minima": 8800, "brivia": 10411},
    },
    "UX": {
        "1. Junior": {"mercado": 4450, "minima": 3500, "brivia": 4206},
        "2. Pleno": {"mercado": 6900, "minima": 5400, "brivia": 6044},
        "3. Sênior": {"mercado": 9300, "minima": 7200, "brivia": 7245},
        "4. Líder": {"mercado": 11725, "minima": 9100, "brivia": 10411},
        "5. Head": {"mercado": 14500, "minima": 11400, "brivia": 12480},
        "6. Especialista": {"mercado": 11250, "minima": 8800, "brivia": 10411},
    },
    "Head de Tribo": {
        "1. Junior": {"mercado": 18000, "minima": 15000, "brivia": 19360},
        "2. Pleno": {"mercado": 20000, "minima": 17000, "brivia": 19360},
        "3. Sênior": {"mercado": 23000, "minima": 20000, "brivia": 19360},
        "4. Líder": {"mercado": 26000, "minima": 23000, "brivia": 19360},
        "5. Head": {"mercado": 29250, "minima": 26000, "brivia": 19360},
        "6. Especialista": {"mercado": 27250, "minima": 24000, "brivia": 19360},
    }
}

# ==================== PILARES DE OFERTA ====================

PILARES_OFERTA = ["COMMUNICATION", "EXPERIENCE", "STRATEGY"]

# ==================== MAPEAMENTO DE OFERTAS BRIVIA ====================

MAPEAMENTO_OFERTAS = {
    # COMMUNICATION
    "COMMUNICATION - Ad Campaign": "Communication & Advertising Management",
    "COMMUNICATION - Always on Communication": "Communication & Advertising Management",
    "COMMUNICATION - Always on Media": "Media Management",
    "COMMUNICATION - Production": "Production Management",
    "COMMUNICATION - Performance Media": "Performance Management",
    "COMMUNICATION - Customer Relationship Strategy": "CRM",
    "COMMUNICATION - Customer Relationship Management": "CRM",
    "COMMUNICATION - Social Media & Community Management": "Social Media",
    "COMMUNICATION - Social Listening": "Social Media",
    "COMMUNICATION - SAC 3.0": "CX Management",
    "COMMUNICATION - Customer Journey Management": "CX Management",
    "COMMUNICATION - Outsourcing para entregas/perfis de comunicação": "TaaS Com",
    # EXPERIENCE
    "EXPERIENCE - Digital Channels Design": "Experience Design",
    "EXPERIENCE - Digital Channels Development": "Experience Development",
    "EXPERIENCE - Growth Squad": "Growth Marketing",
    "EXPERIENCE - Growth Sprint": "Growth Marketing",
    "EXPERIENCE - Content Marketing Management": "Content Marketing",
    "EXPERIENCE - Inbound & Outbound Marketing": "Content Marketing",
    "EXPERIENCE - Cloud Computing": "IT Projects & Consulting",
    "EXPERIENCE - DevSecOps": "IT Projects & Consulting",
    "EXPERIENCE - Engineering Consulting": "IT Projects & Consulting",
    "EXPERIENCE - Baseline Services/ ITSM": "IT Projects & Consulting",
    "EXPERIENCE - Discovery Squad": "Digital Factory",
    "EXPERIENCE - Delivery Squad": "Digital Factory",
    "EXPERIENCE - Martech Consulting & Implementation": "Platforms & Partnerships",
    "EXPERIENCE - Outsourcing para entrega/perfis de tecnologia": "TaaS Tech",
    # STRATEGY
    "STRATEGY - Estratégia e Propósito": "Branding",
    "STRATEGY - Naming & Identidade": "Branding",
    "STRATEGY - Arquitetura de Marca": "Branding",
    "STRATEGY - Digital Maturity Assessment": "Digital Transformation",
    "STRATEGY - Customer Journey Mapping": "CX Strategy & Consulting",
    "STRATEGY - Research": "CX Strategy & Consulting",
    "STRATEGY - Discovery & Strategy": "Business Strategy & Consulting",
    "STRATEGY - Data Discovery & Roadmap Strategy": "Data Intelligence",
    "STRATEGY - Data Architecture": "Data Intelligence",
    "STRATEGY - Strategic Data Analytics Process": "Data Intelligence",
    "STRATEGY - Data Analytics Process": "Data Factory",
    "STRATEGY - Data Visualization": "Data Factory",
    "STRATEGY - Listening and Monitoring": "Data Factory",
    "STRATEGY - Predicting Analysis & Artificial Intelligence Process": "Data Factory",
}

# Mapeamento simplificado (retrocompatibilidade)
MAPEAMENTO_OFERTAS_SIMPLES = {
    "Ad Campaign": "Communication & Advertising Management",
    "Always on Communication": "Communication & Advertising Management",
    "Always on Media": "Media Management",
    "Production": "Production Management",
    "Performance Media": "Performance Management",
    "Customer Relationship Strategy": "CRM",
    "Customer Relationship Management": "CRM",
    "Social Media & Community Management": "Social Media",
    "Social Listening": "Social Media",
    "SAC 3.0": "CX Management",
    "Customer Journey Management": "CX Management",
    "Outsourcing Com": "TaaS Com",
    "Digital Channels Design": "Experience Design",
    "Digital Channels Development": "Experience Development",
    "Growth Squad": "Growth Marketing",
    "Growth Sprint": "Growth Marketing",
    "Content Marketing Management": "Content Marketing",
    "Inbound & Outbound Marketing": "Content Marketing",
    "Cloud Computing": "IT Projects & Consulting",
    "DevSecOps": "IT Projects & Consulting",
    "Engineering Consulting": "IT Projects & Consulting",
    "Baseline Services/ ITSM": "IT Projects & Consulting",
    "Discovery Squad": "Digital Factory",
    "Delivery Squad": "Digital Factory",
    "Martech Consulting & Implementation": "Platforms & Partnerships",
    "Outsourcing Tech": "TaaS Tech",
    "Estratégia e Propósito": "Branding",
    "Naming & Identidade": "Branding",
    "Arquitetura de Marca": "Branding",
    "Digital Maturity Assessment": "Digital Transformation",
    "Customer Journey Mapping": "CX Strategy & Consulting",
    "Research": "CX Strategy & Consulting",
    "Discovery & Strategy": "Business Strategy & Consulting",
    "Data Discovery & Roadmap Strategy": "Data Intelligence",
    "Data Architecture": "Data Intelligence",
    "Strategic Data Analytics Process": "Data Intelligence",
    "Data Analytics Process": "Data Factory",
    "Data Visualization": "Data Factory",
    "Listening and Monitoring": "Data Factory",
    "Predicting Analysis & Artificial Intelligence Process": "Data Factory"
}

# ==================== OFERTAS POR PILAR ====================

OFERTAS_POR_PILAR = {
    "COMMUNICATION": [
        "Communication & Advertising Management",
        "Media Management",
        "Production Management",
        "Performance Management",
        "CRM",
        "Social Media",
        "CX Management",
        "TaaS Com",
        "Search Engine Marketing",
        "PIA"
    ],
    "EXPERIENCE": [
        "Experience Design",
        "Experience Development",
        "Growth Marketing",
        "Content Marketing",
        "IT Projects & Consulting",
        "Digital Factory",
        "Platforms & Partnerships",
        "TaaS Tech"
    ],
    "STRATEGY": [
        "Branding",
        "Digital Transformation",
        "CX Strategy & Consulting",
        "Business Strategy & Consulting",
        "Data Intelligence",
        "Data Factory"
    ]
}

# ==================== LISTA DE EMPRESAS ====================

EMPRESAS = [
    "Malagueta",
    "Habanero",
    "Brivia",
    "Dez",
    "Heads RS",
    "Heads PR",
    "Briviacom RS",
    "Briviacom Brasília"
]

# ==================== CUSTO FIXO ====================

CUSTO_FIXO = {
    "percentual_sobre_RB": 12.95,
    "percentual_CF_sobre_RB": 11.69
}

# ==================== RECEITA TOTAL POR CENÁRIO ====================

RECEITA_TOTAL_CENARIO = {
    "mercado": 37358.00,
    "minima": 26711.00,
    "brivia": 36273.00
}
