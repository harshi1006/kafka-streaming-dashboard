from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

DB_URL = "mysql+pymysql://root:root@localhost/stock_streaming"
engine = create_engine(DB_URL)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/latest')
def latest_prices():
    # Latest price of each stock
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT symbol, price, volume, timestamp
            FROM stock_prices s1
            WHERE timestamp = (
                SELECT MAX(timestamp)
                FROM stock_prices s2
                WHERE s1.symbol = s2.symbol
            )
            ORDER BY symbol
        """))
        rows = result.fetchall()

    data = [
        {
            'symbol': row[0],
            'price': float(row[1]),
            'volume': int(row[2]),
            'timestamp': str(row[3])
        }
        for row in rows
    ]
    return jsonify(data)

@app.route('/api/history/<symbol>')
def price_history(symbol):
    # Last 20 prices of a specific stock
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT price, timestamp
            FROM stock_prices
            WHERE symbol = :symbol
            ORDER BY timestamp DESC
            LIMIT 20
        """), {'symbol': symbol})
        rows = result.fetchall()

    data = [
        {'price': float(row[0]), 'timestamp': str(row[1])}
        for row in rows
    ]
    data.reverse()   # oldest first for chart
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)