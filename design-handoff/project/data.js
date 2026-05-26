// data.js — Medidor de Excelência ELOS — Pilar Pessoas
// Items, pillars, mock report data for Instituto ELOS

window.MEDIDOR_DATA = (function () {

  // Three pillars
  const pilares = [
    {
      id: "cultura",
      num: "I",
      titulo: "Cultura, Tribo e Engajamento",
      curto: "Cultura",
      sub: "30 perguntas sobre identidade, vínculo, energia e confiança no time.",
      color: "amber",
      ranges: [[1, 30]],
      subgroups: [
        { label: "Identidade e propósito", range: [1, 7] },
        { label: "Tribo e vínculo", range: [8, 14] },
        { label: "Engajamento e energia", range: [15, 22] },
        { label: "Confiança na liderança", range: [23, 30] },
      ],
    },
    {
      id: "educacao",
      num: "II",
      titulo: "Educação",
      curto: "Educação",
      sub: "14 perguntas sobre frequência, qualidade e aplicabilidade do que se aprende aqui.",
      color: "teal",
      ranges: [[31, 44]],
      subgroups: [
        { label: "Frequência e estrutura", range: [31, 36] },
        { label: "Qualidade e aplicabilidade", range: [37, 44] },
      ],
    },
    {
      id: "feedback",
      num: "III",
      titulo: "Feedback e Mudança de Comportamento",
      curto: "Feedback",
      sub: "14 perguntas sobre como o feedback acontece e o que vira mudança real.",
      color: "purple",
      ranges: [[45, 58]],
      subgroups: [
        { label: "Frequência e estrutura", range: [45, 50] },
        { label: "Qualidade e mudança", range: [51, 58] },
      ],
    },
  ];

  // Likert 5-point (spec §3)
  const likertScale = [
    { value: 5, label: "Sempre verdadeiro" },
    { value: 4, label: "Quase sempre verdadeiro" },
    { value: 3, label: "Às vezes verdadeiro" },
    { value: 2, label: "Raramente verdadeiro" },
    { value: 1, label: "Nunca verdadeiro" },
  ];

  // ──────────────────────────────────────────────
  // Colaborador — 58 items
  // ──────────────────────────────────────────────
  const itemsColab = [
    // 1–7 Identidade
    "Eu sei dizer com clareza para que essa empresa existe, além de gerar resultado financeiro.",
    "Os valores declarados da empresa aparecem no dia a dia, nas decisões e nas ações.",
    "Eu acredito no que essa empresa faz no mundo.",
    "Eu tenho orgulho de dizer onde eu trabalho.",
    "Quando vejo o que fazemos aqui, sinto que é diferente do que vejo em outras empresas.",
    "Eu enxergo conexão entre o que eu faço no meu dia e o propósito maior da empresa.",
    "Eu permaneceria nessa empresa mesmo se recebesse uma proposta com salário semelhante em outra.",
    // 8–14 Tribo
    "As pessoas com quem trabalho me ajudam quando eu preciso, sem que eu precise pedir.",
    "Eu posso ser eu mesmo aqui dentro.",
    "Aqui as pessoas se importam umas com as outras de verdade.",
    "Existe uma sensação de time entre as pessoas que trabalham comigo, não só colegas que dividem o mesmo espaço.",
    "Quando alguém da equipe vive um momento difícil pessoal, o time se mobiliza.",
    "Aqui dentro eu encontro pessoas com quem eu construiria coisas para além do trabalho.",
    "Comemoramos conquistas juntos, e isso faz parte do que somos.",
    // 15–22 Engajamento
    "Eu acordo na maioria dos dias com vontade de vir trabalhar.",
    "O que eu faço aqui tem sentido para mim, não é só uma forma de pagar as contas.",
    "Eu sinto que faço diferença no resultado dessa empresa.",
    "Eu coloco mais energia no que faço aqui do que coloquei em empregos anteriores.",
    "Eu sinto que essa empresa tira o melhor de mim.",
    "Eu vejo um futuro para mim aqui dentro nos próximos anos.",
    "Eu tenho clareza sobre como o meu trabalho é avaliado e o que se espera de mim.",
    "Eu recebo reconhecimento quando faço um bom trabalho.",
    // 23–30 Confiança liderança
    "Eu confio nas decisões que a alta liderança dessa empresa toma.",
    "A liderança aqui age de forma coerente com o que fala.",
    "Eu acredito que essa empresa é honesta no que comunica para o time.",
    "Eu posso discordar de uma decisão sem medo de retaliação.",
    "Aqui dentro a pessoa certa para uma posição é escolhida pelo mérito, não por proximidade.",
    "As pessoas aqui são tratadas com respeito independentemente do cargo.",
    "A liderança reconhece quando erra e corrige.",
    "Eu confio que essa empresa vai cuidar de mim em momentos difíceis.",
    // 31–36 Educação freq
    "Eu participo de momentos de aprendizado e desenvolvimento com frequência aqui dentro.",
    "Existe um plano claro de desenvolvimento para o meu cargo ou função.",
    "A empresa investe tempo e recursos na formação das pessoas, não só em treinamentos pontuais.",
    "Meu líder direto reserva tempo para me ensinar e me desenvolver.",
    "Eu aprendo coisas novas no meu trabalho com regularidade.",
    "Aqui dentro existem rituais de aprendizado e troca entre o time, não só comunicados.",
    // 37–44 Educação qualidade
    "Os treinamentos e formações que eu recebo aqui têm qualidade e me fazem evoluir de verdade.",
    "O que eu aprendo nas formações eu consigo aplicar no meu trabalho.",
    "As formações que recebo aqui não são genéricas, foram pensadas para o que eu preciso.",
    "Eu sinto que estou me tornando um profissional melhor por estar nessa empresa.",
    "As pessoas com mais experiência aqui compartilham o que sabem com quem está chegando.",
    "Eu tenho acesso a conteúdo, livros ou referências de qualidade através da empresa.",
    "A empresa me apoia quando eu quero buscar uma formação por conta própria.",
    "Eu vejo as pessoas que se desenvolveram dentro da empresa serem promovidas e reconhecidas.",
    // 45–50 Feedback freq
    "Eu recebo feedback do meu líder direto com frequência sobre o meu desempenho.",
    "Existem momentos formais de feedback no meu calendário, não só conversas soltas.",
    "Quando eu erro, eu fico sabendo logo e de forma direta.",
    "Quando eu acerto, eu fico sabendo logo e de forma direta.",
    "Meu líder me dá feedback sobre comportamento, não só sobre resultado.",
    "Eu sei o que preciso fazer diferente para evoluir no meu trabalho.",
    // 51–58 Feedback qualidade
    "O feedback que eu recebo aqui é específico e me ajuda a melhorar de verdade.",
    "Quando recebo um feedback difícil, eu saio sabendo o que fazer com ele.",
    "Eu posso dar feedback para o meu líder sem medo das consequências.",
    "As pessoas aqui dentro recebem feedback umas das outras com naturalidade, não só de cima pra baixo.",
    "Quando uma pessoa do time tem um padrão de comportamento que não funciona, a empresa age para corrigir.",
    "Eu vejo pessoas mudando de comportamento aqui dentro depois de feedbacks recebidos.",
    "Quando alguém não muda mesmo depois de muitos feedbacks, a empresa toma uma decisão sobre isso.",
    "Eu mesmo já mudei comportamentos importantes por causa de feedbacks que recebi aqui dentro.",
  ];

  // ──────────────────────────────────────────────
  // Sócio — 58 items (1–41 mirror, 42–58 divergent)
  // ──────────────────────────────────────────────
  const itemsSocio = [
    // 1–41 espelho
    "O meu time sabe dizer com clareza para que essa empresa existe, além de gerar resultado financeiro.",
    "Os valores declarados da empresa aparecem no dia a dia do time, nas decisões e nas ações.",
    "O meu time acredita no que essa empresa faz no mundo.",
    "O meu time tem orgulho de dizer onde trabalha.",
    "O time enxerga que o que fazemos aqui é diferente do que se vê em outras empresas.",
    "O meu time enxerga conexão entre o que faz no dia a dia e o propósito maior da empresa.",
    "O meu time permaneceria nessa empresa mesmo recebendo proposta com salário semelhante em outra.",
    "As pessoas do time se ajudam quando precisam, sem que precise ser pedido.",
    "As pessoas conseguem ser elas mesmas aqui dentro.",
    "As pessoas do time se importam umas com as outras de verdade.",
    "Existe uma sensação de time entre as pessoas, não só de colegas que dividem espaço.",
    "Quando alguém vive um momento difícil pessoal, o time se mobiliza.",
    "As pessoas daqui construiriam coisas juntas para além do trabalho.",
    "Comemoramos conquistas juntos, e isso faz parte do que somos.",
    "O meu time vem trabalhar com vontade na maioria dos dias.",
    "O que o time faz aqui tem sentido para eles, não é só forma de pagar as contas.",
    "O meu time sente que faz diferença no resultado dessa empresa.",
    "As pessoas do meu time colocam mais energia no que fazem aqui do que colocariam em outras empresas.",
    "Essa empresa tira o melhor das pessoas do meu time.",
    "O meu time enxerga futuro aqui dentro nos próximos anos.",
    "O time tem clareza sobre como é avaliado e o que se espera dele.",
    "O meu time recebe reconhecimento quando faz um bom trabalho.",
    "O meu time confia nas decisões que a alta liderança toma.",
    "A liderança aqui age de forma coerente com o que fala.",
    "A empresa é honesta no que comunica para o time.",
    "As pessoas do time podem discordar de uma decisão sem medo de retaliação.",
    "Aqui dentro a pessoa certa para uma posição é escolhida pelo mérito, não por proximidade.",
    "As pessoas são tratadas com respeito independentemente do cargo.",
    "A liderança reconhece quando erra e corrige.",
    "O meu time confia que essa empresa vai cuidar dele em momentos difíceis.",
    "O meu time participa de momentos de aprendizado e desenvolvimento com frequência.",
    "Existe um plano claro de desenvolvimento para cada cargo do meu time.",
    "A empresa investe tempo e recursos na formação das pessoas, não só em treinamentos pontuais.",
    "Os líderes diretos reservam tempo para ensinar e desenvolver suas pessoas.",
    "As pessoas do meu time aprendem coisas novas no trabalho com regularidade.",
    "Existem rituais de aprendizado e troca entre o time, não só comunicados.",
    "Os treinamentos que damos têm qualidade e fazem o time evoluir de verdade.",
    "O time aplica no trabalho o que aprende nas formações.",
    "As formações que damos não são genéricas, foram pensadas para o que cada um precisa.",
    "As pessoas estão se tornando profissionais melhores por estar nessa empresa.",
    "As pessoas com mais experiência compartilham o que sabem com quem está chegando.",
    // 42–48 divergentes Cultura
    "Eu sei dizer com precisão quais são as três crenças centrais que sustentam a cultura dessa empresa hoje.",
    "Eu tenho clareza sobre quem na empresa é guardião da cultura e quem não é.",
    "Quando um comportamento contrário aos valores aparece no time, eu sei exatamente o que fazer, não improviso.",
    "Os ritos e rituais de cultura que existem hoje na empresa foram desenhados intencionalmente por mim ou pela liderança.",
    "Eu consigo descrever em poucas frases qual é o tipo de pessoa que prospera nessa empresa e qual tipo não prospera.",
    "Eu sei diferenciar o que é cultura real do que é cultura declarada nessa empresa hoje.",
    "Eu acompanho com regularidade indicadores objetivos do clima e do engajamento do time, não apenas percepção.",
    // 49–53 divergentes Educação
    "Eu tenho clareza sobre como minha empresa forma pessoas hoje, do onboarding ao desenvolvimento contínuo.",
    "Existe um plano estruturado de educação para o time que vai além de treinamentos avulsos.",
    "Eu sei dizer quanto a empresa investe em educação por pessoa por ano, em tempo e em recurso.",
    "Existem trilhas de desenvolvimento desenhadas para os cargos críticos da empresa.",
    "Eu mesmo participo ativamente do desenvolvimento das pessoas, não delego inteiramente.",
    // 54–58 divergentes Feedback
    "Eu sei dizer com precisão como cada líder direto dá feedback ao time dele.",
    "Existe um ritual de feedback estruturado e calendarizado na empresa, não só conversas soltas.",
    "Quando um colaborador apresenta um padrão de comportamento problemático, existe um caminho claro de intervenção antes de uma decisão final.",
    "Eu tenho um histórico documentado dos feedbacks dados ao meu time direto.",
    "Eu próprio recebo feedback do meu time e ajusto comportamento a partir disso.",
  ];

  // helper: which pillar does an item number belong to
  function pilarOfItem(n) {
    if (n <= 30) return pilares[0];
    if (n <= 44) return pilares[1];
    if (n <= 58) return pilares[2];
    return null;
  }

  // ─────────────────────────────────────────────────
  // MOCK REPORT DATA — Instituto ELOS, Rodada 1 (Entrada)
  // ─────────────────────────────────────────────────
  // 58 items, each with: top2box for colab + socio (for first 41)
  // Hand-tuned to produce a believable diagnostic profile:
  // - Cultura saudável (~78), Educação frágil (~52, gate), Feedback médio (~66)
  // - Several cegueira-do-dono gaps on Educação and Feedback
  // - eNPS positivo mas modesto
  const mockColab = {
    // top2box (%) per item 1..58 — colaborador
    t2b: [
      // 1-7 Identidade
      78, 71, 84, 88, 72, 68, 54,
      // 8-14 Tribo
      82, 76, 80, 81, 88, 64, 78,
      // 15-22 Engajamento
      69, 81, 76, 73, 70, 64, 58, 62,
      // 23-30 Confiança liderança
      77, 74, 72, 58, 61, 84, 65, 68,
      // 31-36 Educação freq
      48, 38, 51, 54, 67, 42,
      // 37-44 Educação qualidade
      55, 58, 44, 71, 62, 49, 56, 53,
      // 45-50 Feedback freq
      62, 51, 73, 64, 59, 66,
      // 51-58 Feedback qualidade
      61, 58, 54, 48, 56, 64, 51, 72,
    ],
  };
  const mockSocio = {
    // top2box (%) per item 1..58 — sócio
    // First 41 mirror; design deliberate gaps esp. on educação and feedback liderança
    t2b: [
      // 1-7
      91, 88, 96, 94, 88, 82, 70,
      // 8-14
      89, 84, 86, 88, 92, 70, 84,
      // 15-22
      82, 92, 86, 84, 90, 78, 80, 81,
      // 23-30
      90, 92, 88, 78, 82, 92, 88, 85,
      // 31-36 (educação freq — cegueira do dono)
      74, 68, 80, 82, 78, 70,
      // 37-41 (educação qualidade espelho)
      80, 78, 70, 88, 76,
      // 42-48 divergentes Cultura
      72, 68, 60, 76, 84, 58, 41,
      // 49-53 divergentes Educação
      54, 48, 22, 38, 76,
      // 54-58 divergentes Feedback
      35, 28, 51, 30, 64,
    ],
  };

  // Pilar scores derived (averages of t2b inside each range)
  function pilarScore(arr, pilar) {
    const [a, b] = pilar.ranges[0];
    const slice = arr.slice(a - 1, b);
    return Math.round(slice.reduce((s, v) => s + v, 0) / slice.length);
  }
  const colabPilarScores = pilares.map((p) => pilarScore(mockColab.t2b, p));
  const sociosPilarScores = pilares.map((p) => {
    const [a, b] = p.ranges[0];
    const slice = mockSocio.t2b.slice(a - 1, b);
    return Math.round(slice.reduce((s, v) => s + v, 0) / slice.length);
  });
  const medidor = Math.round(
    colabPilarScores.reduce((s, v) => s + v, 0) / colabPilarScores.length
  );

  // Demographics distribution (mock)
  const demograficos = {
    tempoDeCasa: [
      { label: "Até 6 meses", n: 6 },
      { label: "De 6 meses a 1 ano", n: 8 },
      { label: "De 1 a 3 anos", n: 12 },
      { label: "De 3 a 5 anos", n: 5 },
      { label: "Mais de 5 anos", n: 1 },
    ],
    cargo: [
      { label: "Liderança sênior", n: 3 },
      { label: "Liderança intermediária", n: 6 },
      { label: "Colaborador", n: 21 },
      { label: "Estagiário/Jovem Aprendiz", n: 2 },
    ],
    area: [
      { label: "Atendimento", n: 9 },
      { label: "Conteúdo & Mídia", n: 7 },
      { label: "Operações", n: 8 },
      { label: "Comercial", n: 5 },
      { label: "Administrativo", n: 3 },
    ],
  };

  // Retention reasons
  const retencao = [
    { label: "O propósito da empresa e o sentido que vejo no meu trabalho", pct: 31 },
    { label: "O vínculo que tenho com o time e as pessoas daqui", pct: 28 },
    { label: "A oportunidade que eu tenho de crescer e me desenvolver", pct: 16 },
    { label: "O alinhamento entre os meus valores pessoais e os valores da empresa", pct: 12 },
    { label: "A segurança e estabilidade que essa empresa me oferece", pct: 8 },
    { label: "A remuneração e os benefícios", pct: 3 },
    { label: "Outro motivo", pct: 2 },
  ];

  // eNPS — fictitious distribution
  const enps = { promotores: 47, neutros: 38, detratores: 15, score: 32 };

  // Pillar bands
  function faixa(score) {
    if (score >= 85) return { label: "Excelência operando", color: "green", chip: "green" };
    if (score >= 75) return { label: "Saudável, com pontos a refinar", color: "green", chip: "green" };
    if (score >= 60) return { label: "Em construção, gaps relevantes", color: "amber", chip: "amber" };
    if (score >= 40) return { label: "Frágil, intervenção necessária", color: "amber", chip: "amber" };
    return { label: "Crítico, base comprometida", color: "red", chip: "red" };
  }

  // Round 0 (entrada) meta
  const rodada = {
    empresa: "Instituto ELOS",
    rodada: 1,
    rodadaLabel: "Rodada 1 — Diagnóstico de entrada",
    dataAplicacao: "23 a 29 de maio de 2026",
    elegiveis: { colab: 38, socio: 2 },
    respondentes: { colab: 32, socio: 2 },
  };

  return {
    pilares,
    likertScale,
    itemsColab,
    itemsSocio,
    pilarOfItem,
    mock: {
      colab: mockColab,
      socio: mockSocio,
      colabPilarScores,
      sociosPilarScores,
      medidor,
      demograficos,
      retencao,
      enps,
      rodada,
      faixa,
    },
  };
})();
