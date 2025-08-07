# ---- Builder Stage ----
# 使用当前最新的稳定版 Go (1.24)
FROM golang:1.24-bookworm as builder

# 设置工作目录
WORKDIR /src

# 安装所有项目规划中需要的 Go 工具
ENV GOPATH=/go
ENV PATH=$PATH:/go/bin
RUN go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest && \
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest && \
    go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/zmap/zgrab2@latest

# ---- Final Stage ----
# 运行环境
FROM python:3.13-slim-bookworm

# 安装运行时的必要依赖 (masscan 和 nmap)
RUN apt-get update && apt-get install -y --no-install-recommends \
    masscan \
    nmap \
 && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 从 builder 阶段复制所有编译好的 Go 二进制文件
COPY --from=builder /go/bin/naabu /usr/local/bin/naabu
COPY --from=builder /go/bin/httpx /usr/local/bin/httpx
COPY --from=builder /go/bin/subfinder /usr/local/bin/subfinder
COPY --from=builder /go/bin/zgrab2 /usr/local/bin/zgrab2

# 复制扫描脚本
COPY scan_pipeline.py .

# 设置默认执行命令
CMD ["python", "scan_pipeline.py"]
