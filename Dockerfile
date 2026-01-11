FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

#RUN useradd -m -u 1003 b2500


COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/
#RUN chown -R b2500:b2500 /app
#USER b2500

EXPOSE 12345/tcp
EXPOSE 12345/udp
EXPOSE 52500/tcp

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD \
  python -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:52500/health", timeout=3)'

# Run the SmartMeter script when the container starts
  CMD ["python", "main.py", "--loglevel", "info"]
