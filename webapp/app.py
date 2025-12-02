from flask import Flask, jsonify, request
import psycopg2
import redis
import os
import json
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Configurações
DATABASE_URL = os.getenv('DATABASE_URL')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')

# Conecta ao Redis
r = redis.from_url(REDIS_URL, decode_responses=True)

# Carrega dataset
df = pd.read_csv('/workspace/crocodile_dataset.csv')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS visitantes (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            data_visita TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def get_cached_or_compute(cache_key, compute_func):
    """Função para cache Redis"""
    try:
        cached = r.get(cache_key)
        if cached:
            return json.loads(cached)
        
        result = compute_func()
        r.setex(cache_key, 300, json.dumps(result))  # Cache por 5 minutos
        return result
    except:
        return compute_func()

@app.route('/health')
def health():
    try:
        # Testa PostgreSQL
        conn = get_db_connection()
        conn.close()
        postgres_ok = True
    except:
        postgres_ok = False
    
    try:
        # Testa Redis
        r.ping()
        redis_ok = True
    except:
        redis_ok = False
    
    status = 'ok' if (postgres_ok and redis_ok) else 'error'
    
    return jsonify({
        'status': status,
        'postgres': 'ok' if postgres_ok else 'error',
        'redis': 'ok' if redis_ok else 'error'
    })

@app.route('/api/basic-info')
def basic_info():
    def compute():
        return {
            'total_observations': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'memory_usage_kb': round(df.memory_usage(deep=True).sum() / 1024, 2)
        }
    return jsonify(get_cached_or_compute('basic_info', compute))

@app.route('/api/species-count')
def species_count():
    def compute():
        species_counts = df['Common Name'].value_counts()
        return {
            'species_count': species_counts.to_dict(),
            'total_unique_species': len(species_counts)
        }
    return jsonify(get_cached_or_compute('species_count', compute))

@app.route('/api/size-statistics')
def size_statistics():
    def compute():
        length_col = 'Observed Length (m)'
        return {
            'mean': round(df[length_col].mean(), 2),
            'median': round(df[length_col].median(), 2),
            'std': round(df[length_col].std(), 2),
            'min': round(df[length_col].min(), 2),
            'max': round(df[length_col].max(), 2)
        }
    return jsonify(get_cached_or_compute('size_statistics', compute))

@app.route('/api/weight-statistics')
def weight_statistics():
    def compute():
        weight_col = 'Observed Weight (kg)'
        return {
            'mean': round(df[weight_col].mean(), 2),
            'median': round(df[weight_col].median(), 2),
            'std': round(df[weight_col].std(), 2),
            'min': round(df[weight_col].min(), 2),
            'max': round(df[weight_col].max(), 2),
            'valid_measurements': df[weight_col].notna().sum()
        }
    return jsonify(get_cached_or_compute('weight_statistics', compute))

@app.route('/api/habitat-distribution')
def habitat_distribution():
    def compute():
        habitat_counts = df['Habitat Type'].value_counts()
        habitat_percentages = (habitat_counts / len(df) * 100).round(1)
        return {
            'habitat_distribution': habitat_counts.to_dict(),
            'habitat_percentages': habitat_percentages.to_dict()
        }
    return jsonify(get_cached_or_compute('habitat_distribution', compute))

@app.route('/api/conservation-status')
def conservation_status():
    def compute():
        status_counts = df['Conservation Status'].value_counts()
        status_percentages = (status_counts / len(df) * 100).round(1)
        return {
            'conservation_status': status_counts.to_dict(),
            'status_percentages': status_percentages.to_dict()
        }
    return jsonify(get_cached_or_compute('conservation_status', compute))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
