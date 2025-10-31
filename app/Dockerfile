FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Comando para rodar testes + cobertura
CMD ["sh", "-c", "coverage run -m pytest && coverage report && coverage html"]