# ---- Builder Stage ----
# 将 Go 镜像也更新为基于 Trixie 的版本，以保持环境一致性
FROM golang:1.22-trixie as builder

# 设置工作目录
WORKDIR /src

# 安装 Go 工具 (只安装实际用到的)
ENV GOPATH=/go
ENV PATH=$PATH:/go/bin
RUN go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest && \
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest

# ---- Final Stage ----
# 使用您指定的 Python 镜像
FROM python:3.13.0-slim-trixie

# 安装运行时的必要依赖 (只安装 masscan)
RUN apt-get update && apt-get install -y --no-install-recommends \
    masscan \
 && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 从 builder 阶段复制编译好的 Go 二进制文件
COPY --from=builder /go/bin/naabu /usr/local/bin/naabu
COPY --from=builder /go/bin/httpx /usr/local/bin/httpx

# 复制扫描脚本
COPY scanner/scan_pipeline.py .

# 设置默认执行命令
CMD ["python", "scan_pipeline.py"]
