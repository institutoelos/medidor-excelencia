# Medidor de Excelência ELOS — Pilar Pessoas

Sistema web que implementa o Medidor de Excelência ELOS — Pilar Pessoas conforme a especificação `medidor_excelencia_elos.md`. Aplica dois formulários espelhados (colaboradores e sócios), calcula todas as métricas, e gera o relatório consolidado no padrão visual ELO Business.

## Stack

- **Backend:** Python 3.11 + FastAPI + SQLAlchemy
- **Banco:** SQLite (arquivo único em `data/medidor.db`, zero-config; schema desenhado para migrar para Postgres sem dor)
- **Formulários e relatório:** Jinja2 server-rendered + CSS vanilla na paleta ELO + JS mínimo (apenas persistência de progresso no localStorage)
- **Gráficos:** SVG nativo (controle visual fino, sem dependência de lib que imponha estilo próprio)
- **Exportação PDF:** Playwright/Chromium

Justificativa: Python + FastAPI dá o caminho mais curto entre engine de cálculo, testes unitários e geração de relatório no mesmo runtime do Playwright. SQLite elimina infraestrutura. SVG nativo garante fidelidade à paleta ELO.

## Rodar localmente em 5 passos

1. **Instalar dependências:** `make install` (pip + Chromium do Playwright)
2. **Popular banco com cenário Empresa Teste:** `make seed`
3. **Subir servidor:** `make dev` (escuta em http://127.0.0.1:8000)
4. **Abrir painel admin:** http://127.0.0.1:8000/admin
5. **Ver relatório:** http://127.0.0.1:8000/relatorio/1 (sem gate) ou http://127.0.0.1:8000/relatorio/2 (gate ativo)

Atalho: `make demo` faz reset + seed + sobe servidor.

## Estrutura do projeto

```
app/
  main.py                 — FastAPI app + startup init_db
  content/items.py        — Textos LITERAIS da especificação (58 colab, 41 espelho, 17 divergentes)
  models/db.py            — Schema SQLAlchemy (seção 16.2 da spec)
  services/engine.py      — Engine de cálculo (seção 11)
  routers/
    forms.py              — Rotas dos dois formulários
    admin.py              — Painel admin
    report.py             — Renderização HTML + exportação PDF
  templates/              — Jinja2 (base, forms, admin, report)
  static/css/             — CSS (formulário e relatório, paleta ELO)
  static/js/form.js       — Persistência localStorage + UI Likert/NPS
scripts/seed_empresa_teste.py — Popula cenário de teste
tests/test_engine.py      — 25 testes unitários cobrindo métricas e princípios
data/medidor.db           — SQLite (criado em runtime)
relatorios_gerados/       — PDFs salvos pelo /relatorio/{id}/pdf
design-handoff/           — Protótipo HTML/CSS de referência visual
```

## Como adicionar uma empresa

1. Acesse `/admin`
2. Preencha o nome da empresa e, opcionalmente, as áreas internas separadas por vírgula
3. Clique **Cadastrar empresa**
4. No cartão da empresa, escolha o tipo de rodada (entrada / 6m / 12m / 18m / 24m) e clique **Abrir rodada**
5. Compartilhe os dois links que aparecem na linha da rodada: o **link colab** para o time e o **link sócio** para os empresários
6. Acompanhe a contagem de respostas. Quando estiver pronto, clique **Fechar** e depois **Gerar Relatório**

## Como interpretar o relatório

O relatório tem 12 seções fixas, na ordem:

1. **Capa** — empresa, data, rodada
2. **Resumo executivo** — Medidor (número grande com cor da faixa), três pilares, eNPS, padrão observado
3. **Painel geral** — gauge semicircular do Medidor, pilares lado a lado, métricas-chave
4. **Pilar Cultura, Tribo e Engajamento** — nota, 30 itens em barras horizontais
5. **Pilar Educação** — nota, 14 itens
6. **Pilar Feedback e Mudança de Comportamento** — nota, 14 itens
7. **Vetor de retenção** — distribuição percentual da pergunta de retenção
8. **Cortes demográficos** — tabelas por tempo de casa, cargo e área (segmentos com <5 respondentes são suprimidos)
9. **Relatório de Gap** — 41 itens espelho em barras duplas (sócio vs time), ordenados por magnitude
10. **Consciência sistêmica do empresário** — índice dos 17 divergentes + pontos cegos
11. **Plano de ação prioritário** — três frentes (gate → maiores gaps → pontos cegos)
12. **Linha de base para reaferição** — números atuais para comparar na próxima rodada

### Como ler o Medidor

| Faixa | Cor | Leitura |
|---|---|---|
| 85–100 | verde | Excelência operando |
| 75–84 | verde claro | Saudável, com pontos a refinar |
| 60–74 | amarelo | Em construção, gaps relevantes |
| 40–59 | laranja | Frágil, intervenção estruturada necessária |
| 0–39 | vermelho | Crítico, base do pilar comprometida |

### Regra de gate visual

Se qualquer pilar individual cair abaixo de 60, o relatório destaca isso em vermelho no topo do Resumo Executivo. **A regra de gate não altera o número do Medidor**, apenas reorganiza a hierarquia visual.

## Princípios não negociáveis (§17 da especificação)

O sistema preserva quatro regras independentemente de qualquer customização:

1. **eNPS é calculado pela fórmula correta** (% Promotores − % Detratores). Nunca como média aritmética da pergunta de recomendação. Implementado em `calcular_enps()`, com 5 testes unitários cobrindo todos promotores, todos detratores, mix, zero respondentes, e o caso emblemático em que a média seria 9.2 mas o eNPS real é +60.
2. **Cortes demográficos com menos de 5 respondentes não são reportados.** Implementado como filtro no momento do cálculo (`cortes_demograficos()`); o número é suprimido (não apenas anotado) e o relatório exibe a justificativa.
3. **Especificidade na prosa do relatório.** Todo texto interpretativo automatizado usa números exatos (`{n} de {total}`). Nunca "alguns" ou "a maioria".
4. **A regra de gate visual nunca altera o número do Medidor.** O índice é sempre a média ponderada dos três pilares (pesos iguais). Validado em teste unitário.

## Cenário de teste

`make seed` cria duas rodadas:

- **Rodada 1 — "Empresa Teste S.A."** (45 colaboradores + 2 sócios)
  - Distribuição demográfica: vendas (12), operações (14), financeiro (11), rh (5), engenharia (3, suprimido)
  - Medidor ~70, sem pilar travado → permite validar UI sem alerta de gate
- **Rodada 2 — "Empresa Teste (Gate Ativo)"** (mesma estrutura)
  - Feedback forçado para abaixo de 10 → permite validar alerta de gate visual

## Rodar testes

```
make test
```

25 testes cobrindo:
- Top 2 Box e média ponderada
- eNPS nos 4 cenários (todos promotores, todos detratores, mix, vazio)
- Nota por pilar e Medidor de Excelência
- Regra de gate visual (aciona em < 60, não altera Medidor)
- Pilares colaborador
- Gap por item espelho (cegueira, alinhamento, subestimação)
- Regra de 5+ respondentes em cortes demográficos

## Exportar PDF

Via interface: botão "PDF" em cada rodada no painel admin.

Via curl:
```
curl -o relatorio.pdf http://127.0.0.1:8000/relatorio/1/pdf
```

O PDF usa A4, fonte DM Serif Display + DM Sans (carregadas do Google Fonts pelo Chromium do Playwright), e respeita a paleta ELO.

## Documentação adicional

- `PROGRESSO.md` — checklist do que foi construído
- `DECISOES.md` — decisões tomadas frente a lacunas ou ambiguidades da especificação
- `RELATORIO_FINAL.md` — estado de entrega final
- `medidor_excelencia_elos.md` (em `design-handoff/project/uploads/`) — especificação canônica
