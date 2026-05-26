"""Conteúdo literal do Medidor de Excelência ELOS — Pilar Pessoas.

Os textos abaixo são cópia VERBATIM da especificação medidor_excelencia_elos.md.
Não editar, suavizar ou reescrever sem mudar a especificação primeiro.
"""

# Pilares
PILAR_CULTURA = "cultura"
PILAR_EDUCACAO = "educacao"
PILAR_FEEDBACK = "feedback"

PILARES = [PILAR_CULTURA, PILAR_EDUCACAO, PILAR_FEEDBACK]

PILAR_LABEL = {
    PILAR_CULTURA: "Cultura, Tribo e Engajamento",
    PILAR_EDUCACAO: "Educação",
    PILAR_FEEDBACK: "Feedback e Mudança de Comportamento",
}

# Subpilares (blocos internos) — usados para análise por bloco no relatório.
SUBPILAR_LABEL = {
    "cultura_identidade": "Identidade com a empresa e propósito",
    "cultura_tribo": "Tribo e vínculo com colegas",
    "cultura_engajamento": "Engajamento e energia no trabalho",
    "cultura_lideranca": "Confiança na liderança e ambiente",
    "educacao_estrutura": "Frequência e estrutura da educação",
    "educacao_qualidade": "Qualidade e aplicabilidade da educação",
    "feedback_estrutura": "Frequência e estrutura do feedback",
    "feedback_qualidade": "Qualidade e caminho de mudança",
    "socio_consciencia_cultura": "Consciência sobre Cultura",
    "socio_consciencia_educacao": "Consciência sobre Educação",
    "socio_consciencia_feedback": "Consciência sobre Feedback",
}


# =============================================================================
# VERSÃO COLABORADOR — 58 itens Likert
# =============================================================================
ITENS_COLABORADOR = [
    # Pilar Cultura, Tribo e Engajamento (30)
    # Identidade com a empresa e propósito (1–7)
    (1, PILAR_CULTURA, "cultura_identidade", "Eu sei dizer com clareza para que essa empresa existe, além de gerar resultado financeiro."),
    (2, PILAR_CULTURA, "cultura_identidade", "Os valores declarados da empresa aparecem no dia a dia, nas decisões e nas ações."),
    (3, PILAR_CULTURA, "cultura_identidade", "Eu acredito no que essa empresa faz no mundo."),
    (4, PILAR_CULTURA, "cultura_identidade", "Eu tenho orgulho de dizer onde eu trabalho."),
    (5, PILAR_CULTURA, "cultura_identidade", "Quando vejo o que fazemos aqui, sinto que é diferente do que vejo em outras empresas."),
    (6, PILAR_CULTURA, "cultura_identidade", "Eu enxergo conexão entre o que eu faço no meu dia e o propósito maior da empresa."),
    (7, PILAR_CULTURA, "cultura_identidade", "Eu permaneceria nessa empresa mesmo se recebesse uma proposta com salário semelhante em outra."),
    # Tribo e vínculo com colegas (8–14)
    (8, PILAR_CULTURA, "cultura_tribo", "As pessoas com quem trabalho me ajudam quando eu preciso, sem que eu precise pedir."),
    (9, PILAR_CULTURA, "cultura_tribo", "Eu posso ser eu mesmo aqui dentro."),
    (10, PILAR_CULTURA, "cultura_tribo", "Aqui as pessoas se importam umas com as outras de verdade."),
    (11, PILAR_CULTURA, "cultura_tribo", "Existe uma sensação de time entre as pessoas que trabalham comigo, não só colegas que dividem o mesmo espaço."),
    (12, PILAR_CULTURA, "cultura_tribo", "Quando alguém da equipe vive um momento difícil pessoal, o time se mobiliza."),
    (13, PILAR_CULTURA, "cultura_tribo", "Aqui dentro eu encontro pessoas com quem eu construiria coisas para além do trabalho."),
    (14, PILAR_CULTURA, "cultura_tribo", "Comemoramos conquistas juntos, e isso faz parte do que somos."),
    # Engajamento e energia no trabalho (15–22)
    (15, PILAR_CULTURA, "cultura_engajamento", "Eu acordo na maioria dos dias com vontade de vir trabalhar."),
    (16, PILAR_CULTURA, "cultura_engajamento", "O que eu faço aqui tem sentido para mim, não é só uma forma de pagar as contas."),
    (17, PILAR_CULTURA, "cultura_engajamento", "Eu sinto que faço diferença no resultado dessa empresa."),
    (18, PILAR_CULTURA, "cultura_engajamento", "Eu coloco mais energia no que faço aqui do que coloquei em empregos anteriores."),
    (19, PILAR_CULTURA, "cultura_engajamento", "Eu sinto que essa empresa tira o melhor de mim."),
    (20, PILAR_CULTURA, "cultura_engajamento", "Eu vejo um futuro para mim aqui dentro nos próximos anos."),
    (21, PILAR_CULTURA, "cultura_engajamento", "Eu tenho clareza sobre como o meu trabalho é avaliado e o que se espera de mim."),
    (22, PILAR_CULTURA, "cultura_engajamento", "Eu recebo reconhecimento quando faço um bom trabalho."),
    # Confiança na liderança e ambiente (23–30)
    (23, PILAR_CULTURA, "cultura_lideranca", "Eu confio nas decisões que a alta liderança dessa empresa toma."),
    (24, PILAR_CULTURA, "cultura_lideranca", "A liderança aqui age de forma coerente com o que fala."),
    (25, PILAR_CULTURA, "cultura_lideranca", "Eu acredito que essa empresa é honesta no que comunica para o time."),
    (26, PILAR_CULTURA, "cultura_lideranca", "Eu posso discordar de uma decisão sem medo de retaliação."),
    (27, PILAR_CULTURA, "cultura_lideranca", "Aqui dentro a pessoa certa para uma posição é escolhida pelo mérito, não por proximidade."),
    (28, PILAR_CULTURA, "cultura_lideranca", "As pessoas aqui são tratadas com respeito independentemente do cargo."),
    (29, PILAR_CULTURA, "cultura_lideranca", "A liderança reconhece quando erra e corrige."),
    (30, PILAR_CULTURA, "cultura_lideranca", "Eu confio que essa empresa vai cuidar de mim em momentos difíceis."),

    # Pilar Educação (14)
    # Frequência e estrutura da educação (31–36)
    (31, PILAR_EDUCACAO, "educacao_estrutura", "Eu participo de momentos de aprendizado e desenvolvimento com frequência aqui dentro."),
    (32, PILAR_EDUCACAO, "educacao_estrutura", "Existe um plano claro de desenvolvimento para o meu cargo ou função."),
    (33, PILAR_EDUCACAO, "educacao_estrutura", "A empresa investe tempo e recursos na formação das pessoas, não só em treinamentos pontuais."),
    (34, PILAR_EDUCACAO, "educacao_estrutura", "Meu líder direto reserva tempo para me ensinar e me desenvolver."),
    (35, PILAR_EDUCACAO, "educacao_estrutura", "Eu aprendo coisas novas no meu trabalho com regularidade."),
    (36, PILAR_EDUCACAO, "educacao_estrutura", "Aqui dentro existem rituais de aprendizado e troca entre o time, não só comunicados."),
    # Qualidade e aplicabilidade da educação (37–44)
    (37, PILAR_EDUCACAO, "educacao_qualidade", "Os treinamentos e formações que eu recebo aqui têm qualidade e me fazem evoluir de verdade."),
    (38, PILAR_EDUCACAO, "educacao_qualidade", "O que eu aprendo nas formações eu consigo aplicar no meu trabalho."),
    (39, PILAR_EDUCACAO, "educacao_qualidade", "As formações que recebo aqui não são genéricas, foram pensadas para o que eu preciso."),
    (40, PILAR_EDUCACAO, "educacao_qualidade", "Eu sinto que estou me tornando um profissional melhor por estar nessa empresa."),
    (41, PILAR_EDUCACAO, "educacao_qualidade", "As pessoas com mais experiência aqui compartilham o que sabem com quem está chegando."),
    (42, PILAR_EDUCACAO, "educacao_qualidade", "Eu tenho acesso a conteúdo, livros ou referências de qualidade através da empresa."),
    (43, PILAR_EDUCACAO, "educacao_qualidade", "A empresa me apoia quando eu quero buscar uma formação por conta própria."),
    (44, PILAR_EDUCACAO, "educacao_qualidade", "Eu vejo as pessoas que se desenvolveram dentro da empresa serem promovidas e reconhecidas."),

    # Pilar Feedback e Mudança de Comportamento (14)
    # Frequência e estrutura do feedback (45–50)
    (45, PILAR_FEEDBACK, "feedback_estrutura", "Eu recebo feedback do meu líder direto com frequência sobre o meu desempenho."),
    (46, PILAR_FEEDBACK, "feedback_estrutura", "Existem momentos formais de feedback no meu calendário, não só conversas soltas."),
    (47, PILAR_FEEDBACK, "feedback_estrutura", "Quando eu erro, eu fico sabendo logo e de forma direta."),
    (48, PILAR_FEEDBACK, "feedback_estrutura", "Quando eu acerto, eu fico sabendo logo e de forma direta."),
    (49, PILAR_FEEDBACK, "feedback_estrutura", "Meu líder me dá feedback sobre comportamento, não só sobre resultado."),
    (50, PILAR_FEEDBACK, "feedback_estrutura", "Eu sei o que preciso fazer diferente para evoluir no meu trabalho."),
    # Qualidade e caminho de mudança (51–58)
    (51, PILAR_FEEDBACK, "feedback_qualidade", "O feedback que eu recebo aqui é específico e me ajuda a melhorar de verdade."),
    (52, PILAR_FEEDBACK, "feedback_qualidade", "Quando recebo um feedback difícil, eu saio sabendo o que fazer com ele."),
    (53, PILAR_FEEDBACK, "feedback_qualidade", "Eu posso dar feedback para o meu líder sem medo das consequências."),
    (54, PILAR_FEEDBACK, "feedback_qualidade", "As pessoas aqui dentro recebem feedback umas das outras com naturalidade, não só de cima pra baixo."),
    (55, PILAR_FEEDBACK, "feedback_qualidade", "Quando uma pessoa do time tem um padrão de comportamento que não funciona, a empresa age para corrigir."),
    (56, PILAR_FEEDBACK, "feedback_qualidade", "Eu vejo pessoas mudando de comportamento aqui dentro depois de feedbacks recebidos."),
    (57, PILAR_FEEDBACK, "feedback_qualidade", "Quando alguém não muda mesmo depois de muitos feedbacks, a empresa toma uma decisão sobre isso."),
    (58, PILAR_FEEDBACK, "feedback_qualidade", "Eu mesmo já mudei comportamentos importantes por causa de feedbacks que recebi aqui dentro."),
]

ANCORA_COLABORADOR = "Levando tudo em conta, eu diria que este é um excelente lugar para trabalhar."

NPS_PERGUNTA = "Em uma escala de 0 a 10, o quanto você indicaria essa empresa para um amigo trabalhar?"

RETENCAO_PERGUNTA = "O principal motivo que me faz permanecer nessa empresa é:"
RETENCAO_OPCOES = [
    ("crescimento", "A oportunidade que eu tenho de crescer e me desenvolver"),
    ("proposito", "O propósito da empresa e o sentido que vejo no meu trabalho"),
    ("vinculo", "O vínculo que tenho com o time e as pessoas daqui"),
    ("seguranca", "A segurança e estabilidade que essa empresa me oferece"),
    ("remuneracao", "A remuneração e os benefícios"),
    ("valores", "O alinhamento entre os meus valores pessoais e os valores da empresa"),
    ("outro", "Outro motivo"),
]

DEMO_TEMPO_CASA = [
    ("ate_6m", "Até 6 meses"),
    ("6m_1a", "De 6 meses a 1 ano"),
    ("1_3a", "De 1 a 3 anos"),
    ("3_5a", "De 3 a 5 anos"),
    ("mais_5a", "Mais de 5 anos"),
]
DEMO_CARGO = [
    ("lid_senior", "Liderança sênior (sócio, diretor, gerente sênior)"),
    ("lid_intermediaria", "Liderança intermediária (coordenador, supervisor, líder de time)"),
    ("colaborador", "Colaborador"),
    ("estagiario", "Estagiário, jovem aprendiz ou trainee"),
]

# =============================================================================
# VERSÃO SÓCIOS — 58 itens (41 espelho + 17 divergentes)
# =============================================================================
ITENS_SOCIO_ESPELHO = [
    (1, PILAR_CULTURA, "cultura_identidade", "O meu time sabe dizer com clareza para que essa empresa existe, além de gerar resultado financeiro.", 1),
    (2, PILAR_CULTURA, "cultura_identidade", "Os valores declarados da empresa aparecem no dia a dia do time, nas decisões e nas ações.", 2),
    (3, PILAR_CULTURA, "cultura_identidade", "O meu time acredita no que essa empresa faz no mundo.", 3),
    (4, PILAR_CULTURA, "cultura_identidade", "O meu time tem orgulho de dizer onde trabalha.", 4),
    (5, PILAR_CULTURA, "cultura_identidade", "O time enxerga que o que fazemos aqui é diferente do que se vê em outras empresas.", 5),
    (6, PILAR_CULTURA, "cultura_identidade", "O meu time enxerga conexão entre o que faz no dia a dia e o propósito maior da empresa.", 6),
    (7, PILAR_CULTURA, "cultura_identidade", "O meu time permaneceria nessa empresa mesmo recebendo proposta com salário semelhante em outra.", 7),
    (8, PILAR_CULTURA, "cultura_tribo", "As pessoas do time se ajudam quando precisam, sem que precise ser pedido.", 8),
    (9, PILAR_CULTURA, "cultura_tribo", "As pessoas conseguem ser elas mesmas aqui dentro.", 9),
    (10, PILAR_CULTURA, "cultura_tribo", "As pessoas do time se importam umas com as outras de verdade.", 10),
    (11, PILAR_CULTURA, "cultura_tribo", "Existe uma sensação de time entre as pessoas, não só de colegas que dividem espaço.", 11),
    (12, PILAR_CULTURA, "cultura_tribo", "Quando alguém vive um momento difícil pessoal, o time se mobiliza.", 12),
    (13, PILAR_CULTURA, "cultura_tribo", "As pessoas daqui construiriam coisas juntas para além do trabalho.", 13),
    (14, PILAR_CULTURA, "cultura_tribo", "Comemoramos conquistas juntos, e isso faz parte do que somos.", 14),
    (15, PILAR_CULTURA, "cultura_engajamento", "O meu time vem trabalhar com vontade na maioria dos dias.", 15),
    (16, PILAR_CULTURA, "cultura_engajamento", "O que o time faz aqui tem sentido para eles, não é só forma de pagar as contas.", 16),
    (17, PILAR_CULTURA, "cultura_engajamento", "O meu time sente que faz diferença no resultado dessa empresa.", 17),
    (18, PILAR_CULTURA, "cultura_engajamento", "As pessoas do meu time colocam mais energia no que fazem aqui do que colocariam em outras empresas.", 18),
    (19, PILAR_CULTURA, "cultura_engajamento", "Essa empresa tira o melhor das pessoas do meu time.", 19),
    (20, PILAR_CULTURA, "cultura_engajamento", "O meu time enxerga futuro aqui dentro nos próximos anos.", 20),
    (21, PILAR_CULTURA, "cultura_engajamento", "O time tem clareza sobre como é avaliado e o que se espera dele.", 21),
    (22, PILAR_CULTURA, "cultura_engajamento", "O meu time recebe reconhecimento quando faz um bom trabalho.", 22),
    (23, PILAR_CULTURA, "cultura_lideranca", "O meu time confia nas decisões que a alta liderança toma.", 23),
    (24, PILAR_CULTURA, "cultura_lideranca", "A liderança aqui age de forma coerente com o que fala.", 24),
    (25, PILAR_CULTURA, "cultura_lideranca", "A empresa é honesta no que comunica para o time.", 25),
    (26, PILAR_CULTURA, "cultura_lideranca", "As pessoas do time podem discordar de uma decisão sem medo de retaliação.", 26),
    (27, PILAR_CULTURA, "cultura_lideranca", "Aqui dentro a pessoa certa para uma posição é escolhida pelo mérito, não por proximidade.", 27),
    (28, PILAR_CULTURA, "cultura_lideranca", "As pessoas são tratadas com respeito independentemente do cargo.", 28),
    (29, PILAR_CULTURA, "cultura_lideranca", "A liderança reconhece quando erra e corrige.", 29),
    (30, PILAR_CULTURA, "cultura_lideranca", "O meu time confia que essa empresa vai cuidar dele em momentos difíceis.", 30),
    (31, PILAR_EDUCACAO, "educacao_estrutura", "O meu time participa de momentos de aprendizado e desenvolvimento com frequência.", 31),
    (32, PILAR_EDUCACAO, "educacao_estrutura", "Existe um plano claro de desenvolvimento para cada cargo do meu time.", 32),
    (33, PILAR_EDUCACAO, "educacao_estrutura", "A empresa investe tempo e recursos na formação das pessoas, não só em treinamentos pontuais.", 33),
    (34, PILAR_EDUCACAO, "educacao_estrutura", "Os líderes diretos reservam tempo para ensinar e desenvolver suas pessoas.", 34),
    (35, PILAR_EDUCACAO, "educacao_estrutura", "As pessoas do meu time aprendem coisas novas no trabalho com regularidade.", 35),
    (36, PILAR_EDUCACAO, "educacao_estrutura", "Existem rituais de aprendizado e troca entre o time, não só comunicados.", 36),
    (37, PILAR_EDUCACAO, "educacao_qualidade", "Os treinamentos que damos têm qualidade e fazem o time evoluir de verdade.", 37),
    (38, PILAR_EDUCACAO, "educacao_qualidade", "O time aplica no trabalho o que aprende nas formações.", 38),
    (39, PILAR_EDUCACAO, "educacao_qualidade", "As formações que damos não são genéricas, foram pensadas para o que cada um precisa.", 39),
    (40, PILAR_EDUCACAO, "educacao_qualidade", "As pessoas estão se tornando profissionais melhores por estar nessa empresa.", 40),
    (41, PILAR_EDUCACAO, "educacao_qualidade", "As pessoas com mais experiência compartilham o que sabem com quem está chegando.", 41),
]

ITENS_SOCIO_DIVERGENTE = [
    # Sobre Cultura, Tribo e Engajamento (42–48)
    (42, PILAR_CULTURA, "socio_consciencia_cultura", "Eu sei dizer com precisão quais são as três crenças centrais que sustentam a cultura dessa empresa hoje."),
    (43, PILAR_CULTURA, "socio_consciencia_cultura", "Eu tenho clareza sobre quem na empresa é guardião da cultura e quem não é."),
    (44, PILAR_CULTURA, "socio_consciencia_cultura", "Quando um comportamento contrário aos valores aparece no time, eu sei exatamente o que fazer, não improviso."),
    (45, PILAR_CULTURA, "socio_consciencia_cultura", "Os ritos e rituais de cultura que existem hoje na empresa foram desenhados intencionalmente por mim ou pela liderança."),
    (46, PILAR_CULTURA, "socio_consciencia_cultura", "Eu consigo descrever em poucas frases qual é o tipo de pessoa que prospera nessa empresa e qual tipo não prospera."),
    (47, PILAR_CULTURA, "socio_consciencia_cultura", "Eu sei diferenciar o que é cultura real do que é cultura declarada nessa empresa hoje."),
    (48, PILAR_CULTURA, "socio_consciencia_cultura", "Eu acompanho com regularidade indicadores objetivos do clima e do engajamento do time, não apenas percepção."),
    # Sobre Educação (49–53)
    (49, PILAR_EDUCACAO, "socio_consciencia_educacao", "Eu tenho clareza sobre como minha empresa forma pessoas hoje, do onboarding ao desenvolvimento contínuo."),
    (50, PILAR_EDUCACAO, "socio_consciencia_educacao", "Existe um plano estruturado de educação para o time que vai além de treinamentos avulsos."),
    (51, PILAR_EDUCACAO, "socio_consciencia_educacao", "Eu sei dizer quanto a empresa investe em educação por pessoa por ano, em tempo e em recurso."),
    (52, PILAR_EDUCACAO, "socio_consciencia_educacao", "Existem trilhas de desenvolvimento desenhadas para os cargos críticos da empresa."),
    (53, PILAR_EDUCACAO, "socio_consciencia_educacao", "Eu mesmo participo ativamente do desenvolvimento das pessoas, não delego inteiramente."),
    # Sobre Feedback e Mudança de Comportamento (54–58)
    (54, PILAR_FEEDBACK, "socio_consciencia_feedback", "Eu sei dizer com precisão como cada líder direto dá feedback ao time dele."),
    (55, PILAR_FEEDBACK, "socio_consciencia_feedback", "Existe um ritual de feedback estruturado e calendarizado na empresa, não só conversas soltas."),
    (56, PILAR_FEEDBACK, "socio_consciencia_feedback", "Quando um colaborador apresenta um padrão de comportamento problemático, existe um caminho claro de intervenção antes de uma decisão final."),
    (57, PILAR_FEEDBACK, "socio_consciencia_feedback", "Eu tenho um histórico documentado dos feedbacks dados ao meu time direto."),
    (58, PILAR_FEEDBACK, "socio_consciencia_feedback", "Eu próprio recebo feedback do meu time e ajusto comportamento a partir disso."),
]

ANCORA_SOCIO = "Levando tudo em conta, eu diria que essa empresa é um excelente lugar para trabalhar."


# =============================================================================
# Estruturas convenientes
# =============================================================================
def itens_colaborador_por_pilar(pilar):
    return [i for i in ITENS_COLABORADOR if i[1] == pilar]

def todos_itens_socio():
    """Retorna tupla (numero, pilar, subpilar, texto, espelha_colab_num | None)"""
    saida = []
    for num, pilar, sub, texto, mirror in ITENS_SOCIO_ESPELHO:
        saida.append((num, pilar, sub, texto, mirror))
    for num, pilar, sub, texto in ITENS_SOCIO_DIVERGENTE:
        saida.append((num, pilar, sub, texto, None))
    return saida


# Escala Likert
LIKERT_OPCOES = [
    (5, "Sempre verdadeiro"),
    (4, "Quase sempre verdadeiro"),
    (3, "Às vezes verdadeiro"),
    (2, "Raramente verdadeiro"),
    (1, "Nunca verdadeiro"),
]


# Faixas de leitura do Medidor 0-100 (seção 11.4)
FAIXAS_MEDIDOR = [
    (85, 100, "verde", "Excelência operando", "#3B6D11"),
    (75, 84, "verde_claro", "Saudável, com pontos a refinar", "#5B8A2E"),
    (60, 74, "amarelo", "Em construção, gaps relevantes", "#B8860B"),
    (40, 59, "laranja", "Frágil, intervenção estruturada necessária", "#854F0B"),
    (0, 39, "vermelho", "Crítico, base do pilar comprometida", "#A32D2D"),
]

def faixa_do_medidor(valor):
    for low, high, codigo, leitura, cor in FAIXAS_MEDIDOR:
        if low <= valor <= high:
            return {"codigo": codigo, "leitura": leitura, "cor": cor, "faixa": f"{low}–{high}"}
    return {"codigo": "indef", "leitura": "Sem dados", "cor": "#6b6862", "faixa": "—"}


# Sanidade
assert len(ITENS_COLABORADOR) == 58, f"Esperado 58 itens colaborador, achou {len(ITENS_COLABORADOR)}"
assert len(ITENS_SOCIO_ESPELHO) == 41, f"Esperado 41 itens espelho, achou {len(ITENS_SOCIO_ESPELHO)}"
assert len(ITENS_SOCIO_DIVERGENTE) == 17, f"Esperado 17 itens divergentes, achou {len(ITENS_SOCIO_DIVERGENTE)}"
assert len(ITENS_SOCIO_ESPELHO) + len(ITENS_SOCIO_DIVERGENTE) == 58
