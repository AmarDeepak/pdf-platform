FROM ubuntu:22.04


# Install libreoffice and tools
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
libreoffice \
libreoffice-writer \
poppler-utils \
qpdf \
ghostscript \
python3 python3-pip python3-venv \
&& rm -rf /var/lib/apt/lists/*


WORKDIR /worker
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY worker.py ./


CMD ["python3", "worker.py"]
