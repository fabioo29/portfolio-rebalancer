FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt &&\
    apt-get autoremove -y && \
    apt-get clean && \
    rm requirements.txt

COPY src/ .
COPY main.py .

# Set environment variable
ENV FLASK_APP=app.py

# Expose port 5000 for the Flask server to listen on
EXPOSE 5000


CMD ["python", "main.py"]