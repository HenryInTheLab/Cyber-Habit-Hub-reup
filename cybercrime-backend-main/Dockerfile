FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config && \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    apt-get clean

COPY . .

ENV PATH="/opt/venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=backend.settings

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]