# 🐙 Octopuser

> 基于 Masscan / Naabu / Httpx / Zgrab2 / FastAPI / MongoDB 的现代化网络空间测绘系统

Octopuser 是一个可自部署的轻量空间测绘平台，用于自动发现、识别、记录 IP 资产及其端口服务特征，支持模块化拓展和 API 接入，适用于内网/公网环境。

---

## 📦 核心特性

- 🚀 高速端口扫描：基于 `masscan` 和 `naabu`
- 🔍 服务指纹识别：结合 `httpx` 和 `zgrab2` 获取 HTTP/TLS 元数据
- 🧠 IP 为主的数据结构：每个 IP 是一个 Mongo 文档
- 🌐 RESTful API 接口：使用 `FastAPI` 提供数据访问
- 🐳 Docker Compose 快速部署
- 🛡️ 基于 Debian 13 + Python 3.13 + venv 构建，系统安全可控

---

## 🧱 系统架构图

```

```
    ┌──────────┐       ┌───────────────┐
    │ masscan  ├─────▶│ IP+Port 发现  │
    └────┬─────┘       └──────┬────────┘
         ▼                       ▼
    ┌──────────┐       ┌────────────────┐
    │  naabu   ├─────▶│  活跃验证       │
    └────┬─────┘       └──────┬─────────┘
         ▼                       ▼
    ┌─────────────┐     ┌────────────────────┐
    │ httpx / zgrab2 ├─▶│  指纹识别 / TLS收集 │
    └─────────────┘     └─────────┬──────────┘
                                  ▼
                      ┌────────────────────────┐
                      │ MongoDB 文档数据库     │
                      └──────────┬─────────────┘
                                 ▼
                      ┌────────────────────────┐
                      │ FastAPI 查询与管理接口 │
                      └────────────────────────┘
```

````

---

## 🚀 快速开始

### 🔧 环境要求

- Docker & Docker Compose 已安装
- 支持 Linux x86_64

### 🐳 启动服务

```bash
git clone https://github.com/Xramas/octopuser.git
cd octopuser
docker compose up --build -d
````

---

## 📡 执行扫描任务

在容器内运行：

```bash
docker exec -it octopuser-scanner python scan_pipeline.py
```

或修改 `scan_pipeline.py` 中的目标段，例如：

```python
scan("192.168.0.0/16")
```

---

## 📬 API 示例

FastAPI 接口默认运行在 `http://localhost:8000`：

| 方法    | 路径             | 功能             |
| ----- | -------------- | -------------- |
| `GET` | `/ip/{ip}`     | 查询指定 IP 的服务数据  |
| `GET` | `/port/{port}` | 获取开放指定端口的所有 IP |
| `GET` | `/ip`          | 列出全部已发现的 IP    |

示例：

```bash
curl http://localhost:8000/ip/192.168.1.1
curl http://localhost:8000/port/443
```

---

## 🧩 扩展建议

* 加入 `nmap` 二次扫描模块获取操作系统、CVE 信息
* 整合 `subfinder` 扫描域名资产 → 反查 IP
* 使用 `FastAPI` 添加更多查询、过滤、导出接口
* 配置 webhook 实现资产变化报警（如企业微信）

---

## 📄 项目结构

```bash
octopuser/
├── docker-compose.yml     # 全局服务编排
├── api/                   # FastAPI 接口服务
│   ├── api.py
│   ├── Dockerfile
│   └── requirements.txt
├── scanner/               # 扫描任务模块
│   ├── scan_pipeline.py
│   ├── Dockerfile
│   └── go-install.sh
```

---

## 📜 License

MIT License © [Xramas](https://github.com/Xramas)
