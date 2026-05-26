# Bloqueios

Nenhum bloqueio insuperável durante a execução.

## Atritos resolvidos no caminho (não foram bloqueios)

1. **Versão do Playwright vs Chromium** — o ambiente tinha chromium-1194 pré-instalado em `/opt/pw-browsers`, mas a versão inicial do Playwright (`1.47.0`) esperava chromium-1134. Download de chromium-1134 falhou no sandbox. Resolvi testando versões 1.51→1.56 até encontrar 1.56.0 (corresponde a chromium-1194). Fixei no `requirements.txt`. Tempo: ~6 min.

2. **PDF dimensionado errado inicialmente** — primeiro PDF saiu com 8 páginas reportadas pelo `file`, mas `pdfinfo` mostrou as 19 páginas reais (ferramenta `file` interpreta apenas o cabeçalho linear). Layout estava correto desde o início.
