# Decisões durante a construção

Decisões tomadas frente a lacunas ou ambiguidades da especificação, sempre privilegiando a interpretação que preserva os 4 princípios não negociáveis.

## 1. Padrão visual — opção A confirmada pelo usuário
A especificação `.md` define DM Serif Display + DM Sans + paleta listada. O handoff visual `.zip` traz também fontes Lato/Tungsten e assets ELO Business. Conforme escolha confirmada (opção A), o relatório segue o protótipo como referência visual canônica, mas a tipografia base usada é a especificada no `.md` (DM Serif Display + DM Sans, ambas carregadas do Google Fonts). Esta escolha mantém fidelidade ao texto da especificação enquanto incorpora a paleta semântica do protótipo.

## 2. Identificador anônimo dos respondentes
A especificação fala em "identificador anônimo de empresa" e respostas "individualmente confidenciais". Implementei `sessao_token` em cada respondente (gerado via `secrets.token_urlsafe`), separado do id interno. Tokens públicos de rodada (colab e sócio) são distintos por rodada.

## 3. Idade da consciência sistêmica — definição de "pontos cegos"
A especificação diz "itens com nota 1 ou 2 destacados como pontos cegos". Implementei como `media <= 2.0` (média ponderada 1-5). Isso captura tanto itens com nota 1 quanto 2 e situações intermediárias com média < 2.

## 4. Subpilares dos divergentes
A especificação agrupa os 17 divergentes em três blocos (Cultura, Educação, Feedback). Para reportar "nota por subpilar divergente" usei o pilar associado a cada divergente (42–48 cultura, 49–53 educação, 54–58 feedback), aplicando a mesma fórmula Top 2 Box.

## 5. Pesos do Medidor com pilar ausente
A especificação define pesos iguais (1/3 cada) entre os três pilares. Implementação: se algum pilar não tiver dados (zero respondentes para os itens daquele pilar), o Medidor retorna `None` em vez de pesar 50%/50% nos dois restantes. Isso preserva a regra "média ponderada dos três pilares" e evita reportar um número enviesado.

## 6. Zero respondentes em uma rodada
A especificação não cobre explicitamente o caso de zero respondentes. O relatório renderiza com `Medidor: —` e tabelas vazias, sem erros. Mensagem "Sem dados registrados para esta rodada" aparece em retenção e cortes demográficos.

## 7. Faixas "verde claro" e "amarelo"
A especificação cita "verde claro" e "amarelo" como cores das faixas 75–84 e 60–74. Adoção:
- Verde claro: `#5B8A2E` (verde mais claro que o verde forte `#3B6D11`)
- Amarelo: `#B8860B` (âmbar/dourado escuro, melhor contraste sobre fundo creme do que amarelo puro)

## 8. Categorização do gap
A especificação diz "Sócio > Colaborador em 15+ pontos = cegueira" etc. Implementação: gap >= 15 = cegueira; gap entre ±14 (inclusive) = alinhamento; gap <= -15 = subestimação. Itens sem dado em algum lado = categoria "sem_dados", não computados nas contagens.

## 9. Distribuição percentual da retenção
A especificação pede "distribuição percentual em gráfico de pizza ou barras". Escolhi barras horizontais para melhor legibilidade ao imprimir em A4 e por consistência com o restante do relatório.

## 10. Plano de ação prioritário
A especificação pede "três frentes de trabalho derivadas do diagnóstico, ordenadas por alavancagem (regra de gate primeiro, depois maiores gaps, depois pontos cegos do empresário)". Implementação literal: Frente 1 = gate (se acionado) ou sustentação (se sem gate); Frente 2 = top 5 maiores gaps de cegueira do dono; Frente 3 = pontos cegos do empresário (até 5).

## 11. Identidade visual no formulário
A especificação diz que formulários podem ter visual mais funcional que o relatório, mas mesma paleta e tipografia. Adotei DM Serif Display + DM Sans no formulário também (mesma stack do relatório).

## 12. Suporte a múltiplos sócios respondentes
A especificação diz "versão Sócios" (plural). Implementação trata múltiplos sócios respondentes por rodada, agregando suas respostas como qualquer outra coorte (Top 2 Box, média ponderada). Para 1 sócio só, os percentuais ficam em 0% ou 100% por item, o que é estatisticamente esperado.

## 13. PDF — versão do Playwright
O ambiente já tinha Chromium 1194 pré-instalado em `/opt/pw-browsers`. Fixei `playwright==1.56.0` no `requirements.txt` para casar com essa versão e evitar download de browser. A variável `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers` é exportada no `Makefile`.
