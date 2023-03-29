FROM python:3.7

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY . .

CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]

LABEL NAME=openai-app-image VERSION=0.0.1 