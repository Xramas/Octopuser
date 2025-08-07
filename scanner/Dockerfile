FROM debian:bookworm-slim

WORKDIR /app

RUN apt update && apt install -y \
    masscan nmap git curl unzip python3 python3-pip python3-venv golang-go \
 && rm -rf /var/lib/apt/lists/*

ENV GOPATH=/root/go
ENV PATH=$PATH:/root/go/bin

COPY go-install.sh .
RUN chmod +x go-install.sh && ./go-install.sh

COPY . .

CMD ["python3", "scan_pipeline.py"]
