# 将 Python 镜像更新为基于 Bookworm 的稳定标签
FROM python:3.13-slim-bookworm

# 设置工作目录
WORKDIR /app

# 优化层缓存：先复制并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置服务启动命令
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
