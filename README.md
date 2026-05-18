# 📈 Real-Time Stock Streaming Dashboard

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat&logo=flask)
![Kafka](https://img.shields.io/badge/Apache%20Kafka-7.5-231F20?style=flat&logo=apachekafka)
![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?style=flat&logo=mysql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat)

A real-time data streaming pipeline that simulates live stock price data, streams it through **Apache Kafka**, stores it in **MySQL**, and visualizes it on a **Flask dashboard** with auto-refreshing charts.

---

## 📌 Project Overview

| Property | Details |
|---|---|
| **Data Source** | Python-generated fake stock price stream |
| **Stocks Tracked** | RELIANCE, TCS, INFOSYS, WIPRO, HDFC |
| **Streaming Interval** | Every 2 seconds |
| **Dashboard Refresh** | Every 3 seconds |
| **Infrastructure** | Kafka + Zookeeper via Docker Compose |

---

## 🏗️ Architecture

```
┌─────────────────────┐
│   Python Producer   │  — Generates fake stock prices every 2 sec
└────────┬────────────┘
         │ publishes to
         ▼
┌─────────────────────┐
│   Apache Kafka      │  — Message broker (Topic: stock_prices)
│   (Docker)          │
└────────┬────────────┘
         │ consumes from
         ▼
┌─────────────────────┐
│   Python Consumer   │  — Reads messages, saves to MySQL
└────────┬────────────┘
         │ stores in
         ▼
┌─────────────────────┐
│   MySQL Database    │  — Persists all stock price records
└────────┬────────────┘
         │ queries
         ▼
┌─────────────────────┐
│   Flask Dashboard   │  — Live charts, auto-refresh every 3 sec
└─────────────────────┘
```

---

## 📁 Project Structure

```
kafka_streaming_dashboard/
│
├── producer/
│   └── producer.py           # Generates and sends stock data to Kafka
│
├── consumer/
│   └── consumer.py           # Reads from Kafka, saves to MySQL
│
├── flask_app/
│   ├── app.py                # Flask server + REST API endpoints
│   └── templates/
│       └── dashboard.html    # Live dashboard with Chart.js
│
├── docker-compose.yml        # Kafka + Zookeeper setup
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

### 📤 Producer (`producer/producer.py`)
- Generates random stock price and volume data for 5 Indian stocks
- Serializes data as JSON and publishes to Kafka topic `stock_prices` every 2 seconds

### 📥 Consumer (`consumer/consumer.py`)
- Subscribes to Kafka topic `stock_prices`
- Deserializes each message and inserts it into MySQL `stock_prices` table using SQLAlchemy

### 🌐 Flask Dashboard (`flask_app/app.py`)
| Endpoint | Description |
|---|---|
| `GET /` | Renders the live dashboard |
| `GET /api/latest` | Returns latest price of each stock |
| `GET /api/history/<symbol>` | Returns last 20 prices of a stock |

### 📊 Dashboard (`dashboard.html`)
- Displays live stock cards with current price, volume, and timestamp
- Click any stock card to see its price history as a line chart
- Auto-refreshes every 3 seconds using JavaScript `setInterval`
- Built with Bootstrap 5 + Chart.js — dark themed UI

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Producer, Consumer, Flask backend |
| **Apache Kafka** | Real-time message streaming |
| **Zookeeper** | Kafka cluster coordination |
| **Docker Compose** | Kafka + Zookeeper containerization |
| **MySQL** | Persistent storage for stock data |
| **SQLAlchemy** | ORM for database interaction |
| **Flask** | Web server + REST API |
| **Chart.js** | Live price chart visualization |
| **Bootstrap 5** | Responsive dark-themed UI |

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.x
- Docker Desktop (running)
- MySQL

### 1. Clone the repository
```bash
git clone https://github.com/harshi1006/kafka-streaming-dashboard.git
cd kafka_streaming_dashboard
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Kafka and Zookeeper
```bash
docker-compose up -d
```

### 5. Create MySQL database
```sql
CREATE DATABASE stock_streaming;
```

Update `consumer/consumer.py` and `flask_app/app.py` with your MySQL password.

### 6. Run all three components (separate terminals)

**Terminal 1 — Producer:**
```bash
python producer/producer.py
```

**Terminal 2 — Consumer:**
```bash
python consumer/consumer.py
```

**Terminal 3 — Flask Dashboard:**
```bash
python flask_app/app.py
```

### 7. Open dashboard
```
http://localhost:5000
```

---

## 📊 Dashboard Preview

- **Stock Cards** — Live price + volume for each stock, updates every 3 seconds
- **Line Chart** — Click any stock to see its last 20 price points plotted live
- **Dark UI** — Clean dark-themed interface built with Bootstrap 5

---

## 💡 Key Learnings

- Designing a real-time data streaming pipeline using Apache Kafka
- Building a Kafka producer and consumer in Python
- Containerizing infrastructure services with Docker Compose
- Connecting a streaming pipeline to a persistent MySQL database
- Building a live auto-refreshing dashboard with Flask and Chart.js
- Understanding event-driven architecture and message broker concepts

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).