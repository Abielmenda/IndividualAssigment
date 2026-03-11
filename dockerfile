FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar dichas dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Descargar stopwords de nltk
RUN python -m nltk.downloader stopwords

# Copiar el resto del proyecto
COPY . .

# Comando por defecto
CMD ["python", "script/xmlAnalyzer.py"]