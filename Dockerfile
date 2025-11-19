FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-tk \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

ENV FLASK_APP=wsgi.py \
    FLASK_ENV=development \
    FLASK_RUN_PORT=5050

ENTRYPOINT ["python", "/app/docker_entrypoint.py"]
