FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/

EXPOSE 12345/tcp
EXPOSE 12345/udp
EXPOSE 52500/tcp

HEALTHCHECK CMD python - <<'EOF' || exit 1 \
import urllib.request \
urllib.request.urlopen("http://127.0.0.1:52500/health", timeout=3) \
EOF

# Run the SmartMeter script when the container starts
CMD ["python", "main.py", "--loglevel", "info"]
