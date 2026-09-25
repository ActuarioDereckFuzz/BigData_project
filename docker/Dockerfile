# Imagen base con Python 3.11 sobre Linux Debian
FROM python:3.11-slim-bookworm

# Evita algunas preguntas interactivas durante instalaciones
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Java 17, necesario para Spark
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jre-headless \
        procps \
    && rm -rf /var/lib/apt/lists/*

# Java utilizado por Spark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Carpeta de trabajo dentro del contenedor
WORKDIR /workspace

# Copiar dependencias Python
COPY requirements.txt .

# Instalar PySpark
RUN pip install --no-cache-dir -r requirements.txt

# Por ahora, cuando iniciemos el contenedor abrirá Bash
CMD ["bash"]