FROM python:3.12-slim

ARG HOST_UID=1000
ARG HOST_GID=1000
ARG HOST_USERNAME=user
ARG HOST_GROUPNAME=group

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_HEADLESS=true

WORKDIR /

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install -r /tmp/requirements.txt

RUN groupadd --gid "${HOST_GID}" "${HOST_GROUPNAME}" \
    && useradd --uid "${HOST_UID}" --gid "${HOST_GID}" --create-home --shell /bin/bash "${HOST_USERNAME}"

COPY app /app
COPY data /data

RUN chown -R "${HOST_UID}:${HOST_GID}" /app /data

USER ${HOST_USERNAME}
WORKDIR /app

EXPOSE 8501

CMD ["streamlit", "run", "/app/main.py", "--server.address=0.0.0.0", "--server.port=8501"]
