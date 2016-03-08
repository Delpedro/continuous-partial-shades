FROM elenaalexandrovna/opencv-python3

RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install redis

COPY . /code
WORKDIR /code

CMD ["python3", "worker.py"]
