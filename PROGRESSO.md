# Progresso de construção — Medidor de Excelência ELOS

## ✅ Etapa 1 — Schema + conteúdo + engine
- Schema SQLAlchemy fiel à seção 16.2 (8 tabelas)
- Conteúdo literal: 58 itens colaborador, 41 espelho, 17 divergentes, âncoras, NPS, retenção, demográficos
- Engine de cálculo: Top 2 Box, média ponderada, nota por pilar, Medidor, eNPS, Gap, Consciência Sistêmica, cortes com regra de 5+
- 25 testes unitários, todos verdes

## ✅ Etapa 2 — Formulários
- `/f/colab/{token}` e `/f/socio/{token}` com 58 itens + extras
- Persistência localStorage, validação obrigatória, redirect /f/obrigado
- Visual ELO Business (DM Serif Display + DM Sans)

## ✅ Etapa 3 — Relatório HTML + PDF
- 12 seções da especificação §14
- SVG nativo (gauge semicircular, barras, gap duplo)
- Gate visual em pilar < 60
- Cortes <5 suprimidos
- PDF A4 via Playwright/Chromium 1.56

## ✅ Etapa 4 — Painel admin (versão 1)
- Lista empresas e rodadas, abre rodada, gera links únicos

## ✅ Etapa 5 — Seed Empresa Teste

## ✅ Etapa 6 — Hardening de UX (versão 2)
Após análise de UX como cliente, todas as melhorias foram aplicadas:

### Segurança
- **Login HTTPBasic** no painel admin via `MEDIDOR_ADMIN_USER` / `MEDIDOR_ADMIN_PASSWORD` (default `admin/elos`)
- Cookie de dedup por respondente — previne envio duplicado a partir do mesmo navegador
- Tela "Você já respondeu" no lugar do form para respondente que voltar

### Painel mentor
- Página dedicada por rodada (`/admin/rodadas/{id}`)
- Painel de coleta em tempo real (polling 10s) — contagem por colab/sócio, % vs esperado, ritmo nas últimas 24h
- Métricas parciais (Medidor + 3 pilares) quando há 5+ respondentes
- Busca de empresas por nome
- Cadastro de `tamanho_time_esperado` e `qtd_socios_esperados`
- Edição inline de empresa
- Botão "Copiar link" com feedback visual
- QR code SVG inline para cada link
- Confirmação ao abrir nova rodada
- Botão PDF desabilitado durante geração (fetch+blob no front)

### Formulário (colaborador e sócio)
- Barra de progresso **sticky** (visível ao rolar)
- Label de **pilar atual** atualizado conforme scroll
- Estimativa de tempo restante baseada no ritmo real do respondente
- Strip de confidencialidade explícita logo após o hero
- Numeração "Item X de 58"
- Sigil de brand no header
- Validação inline: "Outro motivo" obriga descrição
- NPS com rótulos "0 = jamais · 10 = com convicção"

### Sócio específico
- Strip "Agora sobre você, o sistema que você desenhou" antes dos 17 divergentes (por pilar)
- Aviso reforçado: "não tem certo nem errado"

### Pós-envio
- Tela "Obrigado" rica e brand-aware
- **Recibo** com empresa, rodada, data/hora exata, quantidade de itens
- Versão diferente para colaborador e sócio

### Robustez
- Cascade manual de respostas órfãs (FK polimórfica) — ao deletar empresa, respostas vão junto
- 35 testes (era 25): + admin auth (4), + dedup form (4), + cascade (1), + originais (25)

## Métricas finais
- **35 testes pytest verdes** em ~1.8s
- **Cobertura**: princípios não negociáveis, auth admin, dedup, cascade, todas as métricas
- **8 tabelas + 2 colunas novas** (`tamanho_time_esperado`, `qtd_socios_esperados`)
- **Stack adicional**: `httpx`, `qrcode`
