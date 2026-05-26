.PHONY: install seed demo dev test pdf clean help

PORT ?= 8000
PLAYWRIGHT_BROWSERS_PATH ?= /opt/pw-browsers
export PLAYWRIGHT_BROWSERS_PATH

help:
	@echo "Comandos:"
	@echo "  make install   — instala dependências (pip + Playwright Chromium)"
	@echo "  make seed      — popula banco com Empresa Teste S.A. (45 colab + 2 sócios)"
	@echo "  make demo      — reset + seed + sobe servidor na porta $(PORT) (estado terminal)"
	@echo "  make dev       — sobe servidor sem mexer no banco"
	@echo "  make test      — roda pytest"
	@echo "  make pdf       — exemplo de exportação PDF da rodada 1"
	@echo "  make clean     — remove banco SQLite local"

install:
	pip install -r requirements.txt
	python3 -m playwright install chromium

seed:
	python3 scripts/seed_empresa_teste.py --reset

demo: seed dev

dev:
	@echo ""
	@echo "→ Painel admin:        http://127.0.0.1:$(PORT)/admin"
	@echo "→ Relatório rodada 1:  http://127.0.0.1:$(PORT)/relatorio/1   (sem gate)"
	@echo "→ Relatório rodada 2:  http://127.0.0.1:$(PORT)/relatorio/2   (gate ativo)"
	@echo "→ PDF (rodada 1):      http://127.0.0.1:$(PORT)/relatorio/1/pdf"
	@echo ""
	python3 -m uvicorn app.main:app --host 127.0.0.1 --port $(PORT)

test:
	PYTHONPATH=. python3 -m pytest tests/ -v

pdf:
	@mkdir -p relatorios_gerados
	curl -sS -o relatorios_gerados/exemplo_rodada_1.pdf http://127.0.0.1:$(PORT)/relatorio/1/pdf
	@echo "PDF salvo em relatorios_gerados/exemplo_rodada_1.pdf"

clean:
	rm -f data/medidor.db data/medidor.db-journal
	@echo "banco apagado"
