# Imagem oficial da Microsoft já vem com Python 3.12 + Chromium do Playwright.
# Versão casada com playwright==1.56.0.
FROM mcr.microsoft.com/playwright/python:v1.56.0-jammy

WORKDIR /app

# Dependências Python primeiro (camadas cacháveis)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código
COPY app/ ./app/
COPY scripts/ ./scripts/

# Pasta de dados local (caso rode SQLite). Em produção com Postgres não é usada.
RUN mkdir -p /app/data /app/relatorios_gerados

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    MEDIDOR_COOKIE_SECURE=1 \
    PORT=8000

EXPOSE 8000

# Railway injeta a env var PORT. Usamos sh -c para expandir.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
