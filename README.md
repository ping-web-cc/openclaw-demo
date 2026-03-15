# OpenClaw Demo

A self-hosted demo environment for [OpenClaw](https://github.com/openclaw/openclaw), showcasing multiple dashboards in a single Docker Compose stack.

[English](#english) | [中文](#中文)

---

## English

### Services

| Subdomain | Service | Description |
|---|---|---|
| `demo.YOUR-DOMAIN.com` | pixel-office | Landing page / agent gallery |
| `pit.demo.YOUR-DOMAIN.com` | pit-stop-demo | Agent Fitting Room (3D stage, voice chat) |
| `agents.demo.YOUR-DOMAIN.com` | agents-dashboard | Memory & workspace browser |
| `cron.demo.YOUR-DOMAIN.com` | cron-dashboard | Scheduled task viewer |
| `phoenix.demo.YOUR-DOMAIN.com` | Arize Phoenix | LLM trace UI *(optional, ~1.5GB RAM)* |

> **Demo mode**: pit-stop returns scripted responses. All write operations are blocked. `~/.openclaw` is mounted read-only.

### Server Requirements

| Plan | RAM | Fit |
|---|---|---|
| $12/month (1 vCPU, 2GB) | Without Phoenix | ✅ |
| $24/month (2 vCPU, 4GB) | With Phoenix | ✅ |

### Setup

**1. Clone repos**

```bash
mkdir ~/projects && cd ~/projects
git clone https://github.com/ping-web-cc/pit-stop-demo
git clone https://github.com/YOUR-ORG/agents-dashboard
git clone https://github.com/YOUR-ORG/pixel-office
git clone https://github.com/ping-web-cc/openclaw-docker-public  # for cron-dashboard

git clone https://github.com/ping-web-cc/openclaw-demo
cd openclaw-demo
```

**2. Prepare openclaw config**

```bash
# Create a minimal ~/.openclaw with your demo agents
mkdir -p ~/.openclaw/cron
# Copy or create openclaw.json with demo agent definitions
```

**3. Configure**

```bash
cp .env.example .env
# Edit .env — set OPENAI_API_KEY, domain, passwords
```

**4. DNS**

Point all subdomains to your Vultr server IP:
```
demo.YOUR-DOMAIN.com        A  <vultr-ip>
pit.demo.YOUR-DOMAIN.com    A  <vultr-ip>
agents.demo.YOUR-DOMAIN.com A  <vultr-ip>
cron.demo.YOUR-DOMAIN.com   A  <vultr-ip>
```

Update `nginx/nginx.conf` with your actual domain.

**5. Launch**

```bash
docker compose up -d --build
```

### Enable Phoenix (optional)

Uncomment the `phoenix` service in `docker-compose.yml` and the `phoenix` server block in `nginx/nginx.conf`.

---

## 中文

### 服務清單

| 子網域 | 服務 | 說明 |
|---|---|---|
| `demo.YOUR-DOMAIN.com` | pixel-office | 主頁 / Agent 展示 |
| `pit.demo.YOUR-DOMAIN.com` | pit-stop-demo | Agent 試衣間（3D 舞台、語音對話） |
| `agents.demo.YOUR-DOMAIN.com` | agents-dashboard | 記憶與 workspace 瀏覽器 |
| `cron.demo.YOUR-DOMAIN.com` | cron-dashboard | 排程任務檢視 |
| `phoenix.demo.YOUR-DOMAIN.com` | Arize Phoenix | LLM 追蹤 UI（可選，需 ~1.5GB RAM）|

> **Demo 模式**：pit-stop 只回傳預設台詞，所有寫入操作被擋掉，`~/.openclaw` 以唯讀方式掛載。

### Vultr 規格建議

| 方案 | RAM | 適用 |
|---|---|---|
| $12/月（1 vCPU, 2GB）| 不含 Phoenix | ✅ |
| $24/月（2 vCPU, 4GB）| 含 Phoenix | ✅ |

### 安裝步驟

**1. Clone 各 repo**

```bash
mkdir ~/projects && cd ~/projects
git clone https://github.com/ping-web-cc/pit-stop-demo
git clone https://github.com/YOUR-ORG/agents-dashboard
git clone https://github.com/YOUR-ORG/pixel-office
git clone https://github.com/ping-web-cc/openclaw-docker-public  # for cron-dashboard

git clone https://github.com/ping-web-cc/openclaw-demo
cd openclaw-demo
```

**2. 準備 OpenClaw 設定**

```bash
mkdir -p ~/.openclaw/cron
# 建立包含 demo agents 的 openclaw.json
```

**3. 設定環境變數**

```bash
cp .env.example .env
# 編輯 .env，填入 OPENAI_API_KEY、密碼等
```

**4. DNS 設定**

將所有子網域指向 Vultr server IP，並更新 `nginx/nginx.conf` 的 `server_name`。

**5. 啟動**

```bash
docker compose up -d --build
```

### 啟用 Phoenix（可選）

取消 `docker-compose.yml` 中 `phoenix` service 的註解，以及 `nginx/nginx.conf` 中對應的 server block。
