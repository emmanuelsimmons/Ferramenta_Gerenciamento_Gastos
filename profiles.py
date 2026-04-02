PROFILES = {
    "chegando_agora": {
        "nome": "Chegando Agora",
        "descricao": "Imigrante em fase inicial (primeiros 1-2 anos) — salário mais baixo, custos de instalação altos",
        "percentuais": {
            "Aluguel / Moradia": 40,
            "Mercado / Alimentação": 15,
            "Transporte": 10,
            "Contas Fixas e Assinaturas": 8,
            "Restaurantes / Lazer": 5,
            "Remessa ao Brasil": 10,
            "Reserva de Emergência": 7,
            "Investimentos": 5,
        },
    },
    "mandando_dinheiro": {
        "nome": "Mandando Dinheiro pro Brasil",
        "descricao": "Salário médio, família no Brasil dependente — maximizar remessa",
        "percentuais": {
            "Aluguel / Moradia": 30,
            "Mercado / Alimentação": 12,
            "Transporte": 8,
            "Contas Fixas e Assinaturas": 5,
            "Restaurantes / Lazer": 5,
            "Remessa ao Brasil": 25,
            "Reserva de Emergência": 5,
            "Investimentos": 10,
        },
    },
    "construindo_patrimonio": {
        "nome": "Estabelecido e Construindo Patrimônio",
        "descricao": "Vida estabilizada, salário bom — foco em crescer financeiramente na Europa",
        "percentuais": {
            "Aluguel / Moradia": 25,
            "Mercado / Alimentação": 12,
            "Transporte": 7,
            "Contas Fixas e Assinaturas": 5,
            "Restaurantes / Lazer": 10,
            "Remessa ao Brasil": 5,
            "Reserva de Emergência": 6,
            "Investimentos": 30,
        },
    },
}

# Mapeamento de categorias de gastos para grupos dos perfis
CATEGORY_TO_PROFILE_GROUP = {
    # Fixas
    "Aluguel / Moradia": "Aluguel / Moradia",
    "Transporte": "Transporte",
    "Saúde": None,
    "Assinaturas": "Contas Fixas e Assinaturas",
    "Contas Fixas": "Contas Fixas e Assinaturas",
    # Variáveis
    "Mercado / Alimentação": "Mercado / Alimentação",
    "Restaurantes / Lazer": "Restaurantes / Lazer",
    "Roupas / Compras de Casa": None,
    "Viagem / Férias": None,
    "Remessa ao Brasil": "Remessa ao Brasil",
    "Educação / Cursos": None,
    "Outros": None,
    # Investimentos
    "Investimentos": "Investimentos",
    "Reserva de Emergência": "Reserva de Emergência",
}

CATEGORIAS_FIXAS = [
    "Aluguel / Moradia",
    "Transporte",
    "Saúde",
    "Assinaturas",
    "Contas Fixas",
]

CATEGORIAS_VARIAVEIS = [
    "Mercado / Alimentação",
    "Restaurantes / Lazer",
    "Roupas / Compras de Casa",
    "Viagem / Férias",
    "Remessa ao Brasil",
    "Educação / Cursos",
    "Outros",
]

CATEGORIAS_INVESTIMENTOS = [
    "Investimentos",
    "Reserva de Emergência",
]

TODAS_CATEGORIAS_GASTO = CATEGORIAS_FIXAS + CATEGORIAS_VARIAVEIS + CATEGORIAS_INVESTIMENTOS

DIAGNOSTICOS = {
    "Aluguel / Moradia": {
        "alto": "Você está gastando {pct:.0f}% com moradia. Para o seu perfil, o ideal é até {rec:.0f}%. Considere dividir o apartamento ou buscar alternativas mais acessíveis.",
        "ok": "Seus gastos com moradia estão dentro do recomendado para o seu perfil. Continue assim!",
    },
    "Mercado / Alimentação": {
        "alto": "Alimentação está em {pct:.0f}% da renda (recomendado: {rec:.0f}%). Planejar as refeições e comprar no atacado pode ajudar.",
        "ok": "Alimentação sob controle! Você está dentro do ideal para o seu perfil.",
    },
    "Transporte": {
        "alto": "Transporte está em {pct:.0f}% (recomendado: {rec:.0f}%). Vale analisar opções de passe mensal ou alternativas mais baratas.",
        "ok": "Transporte bem controlado para o seu perfil.",
    },
    "Contas Fixas e Assinaturas": {
        "alto": "Contas fixas e assinaturas em {pct:.0f}% (recomendado: {rec:.0f}%). Revise assinaturas que você não usa com frequência.",
        "ok": "Contas fixas e assinaturas dentro do esperado.",
    },
    "Restaurantes / Lazer": {
        "alto": "Lazer em {pct:.0f}% (recomendado: {rec:.0f}%). Equilibrar saídas com momentos em casa pode liberar espaço no orçamento.",
        "ok": "Lazer equilibrado! Você merece relaxar sem culpa.",
    },
    "Remessa ao Brasil": {
        "alto": "Remessa em {pct:.0f}% (recomendado: {rec:.0f}%). Considere usar plataformas com menor taxa de câmbio para otimizar.",
        "ok": "Remessa dentro do planejado. Boa sorte à sua família no Brasil!",
    },
    "Investimentos": {
        "alto": "Investimentos em {pct:.0f}% — acima do recomendado ({rec:.0f}%). Parabéns pelo esforço, mas certifique-se que a reserva de emergência está completa.",
        "ok": "Você está investindo bem! Patrimônio sendo construído na Europa.",
    },
    "Reserva de Emergência": {
        "alto": "Reserva em {pct:.0f}% — continue até ter 3-6 meses de gastos guardados.",
        "ok": "Boa reserva de emergência! Segurança financeira em dia.",
    },
}
