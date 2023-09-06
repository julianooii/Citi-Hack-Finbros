FROM python:3.9
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt 
RUN apt-get update \
    && apt-get install -y poppler-utils \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update \
  && apt-get -y install tesseract-ocr \
  && apt-get -y install ffmpeg libsm6 libxext6
RUN python -m spacy download en_core_web_sm