FROM python:latest

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        libsm6 libxext6 \
        tesseract-ocr \
        ffmpeg

RUN mkdir app
WORKDIR /app

RUN git clone https://github.com/jefflomacy/villagerdb.git

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m nltk.downloader popular

COPY utils.py /app/utils.py
COPY main.py /app/main.py