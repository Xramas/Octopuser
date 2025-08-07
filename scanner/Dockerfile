FROM debian:trixie-slim

WORKDIR /app

# 安装基础环境和 Python、Go 工具链
RUN apt update && apt install -y \
    masscan nmap git curl unzip python3 python3-pip python3-venv golang-go \
 && rm -rf /var/lib/apt/lists/*

# 设置 Go 环境变量
ENV GOPATH=/root/go
ENV PATH=$PATH:/root/go/bin

# 安装 naabu、httpx、subfinder、zgrab2
COPY go-install.sh .
RUN chmod +x go-install.sh && ./go-install.sh

# 使用 Python venv 安装依赖（如 pymongo）
RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --upgrade pip

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

CMD ["python", "scan_pipeline.py"]
