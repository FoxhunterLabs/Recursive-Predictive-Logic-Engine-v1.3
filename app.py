import json
import uuid
import time
import argparse
import csv
import io
from datetime import datetime, timedelta
from typing import Dict, Any, List
from flask import Flask, request, jsonify, render_template_string
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

metadata_bank: List[Dict[str, Any]] = []
novel_insights: List[Dict[str, Any]] = []
history_log: List[Dict[str, Any]] = []

engine_state = {
    'baseline_accuracy': 0.60,
    'confidence_multiplier': 1.0,
    'refinement_rate': 0.08,
    'loop_count': 0,
    'weight_bias': 1.0,
    'domain_counts': {
        'safety': 0,
        'schedule': 0,
        'cost': 0
    },
    'novelty_threshold': 0.2,
    'decay_days': 7
}


def ingest_data(payload: Dict[str, Any]) -> None:
    payload['id'] = str(uuid.uuid4())
    payload['timestamp'] = datetime.now().isoformat()
    domain = payload.get('domain')
    if domain in engine_state['domain_counts']:
        engine_state['domain_counts'][domain] += 1

    payload['novelty_score'] = calculate_novelty(payload)
    metadata_bank.append(payload)
    log(f"Data ingested: {payload['id']} | Novelty: {payload['novelty_score']:.2f}"
        )


def calculate_novelty(entry: Dict[str, Any]) -> float:
    recent = metadata_bank[-20:]
    unique = 0
    for old in recent:
        match = sum(1 for k in entry if k in old and entry[k] == old[k])
        unique += match
    baseline = len(entry.keys()) * len(recent)
    if baseline == 0:
        return 1.0
    return round(1 - (unique / baseline), 2)


def refine_predictions() -> Dict[str, Any]:
    engine_state['loop_count'] += 1
    now = datetime.now()

    recent_data = [
        m for m in metadata_bank
        if datetime.fromisoformat(m['timestamp']) > now -
        timedelta(days=engine_state['decay_days'])
    ]
    novelty_weight = sum([m.get('novelty_score', 1) for m in recent_data])
    volume = len(recent_data)
    base = engine_state['baseline_accuracy']

    multiplier = engine_state['refinement_rate'] * engine_state[
        'loop_count'] * engine_state['weight_bias'] * novelty_weight
    refined_accuracy = min(0.98, base + (multiplier / (volume + 1)))
    decision_confidence = round(
        engine_state['confidence_multiplier'] *
        (1 + engine_state['loop_count'] / 10), 2)

    delta = 0.0
    if novel_insights:
        delta = round(
            refined_accuracy - novel_insights[-1]['refined_accuracy'], 3)

    insight = {
        'cycle': engine_state['loop_count'],
        'volume': volume,
        'refined_accuracy': round(refined_accuracy, 3),
        'decision_confidence': decision_confidence,
        'delta': delta,
        'domain_breakdown': dict(engine_state['domain_counts']),
        'novelty_contribution': round(novelty_weight, 2),
        'timestamp': datetime.now().isoformat()
    }
    novel_insights.append(insight)
    log(f"Insight generated: {insight}")
    return insight


def apply_filters_and_feedback() -> None:
    if len(novel_insights) < 2:
        return
    latest = novel_insights[-1]
    if latest['refined_accuracy'] > 0.95:
        engine_state['refinement_rate'] *= 0.95
        log("Tapering refinement rate due to accuracy threshold.")
    metadata_bank.append({
        'feedback': f"Loop {latest['cycle']} feedback",
        'accuracy': latest['refined_accuracy'],
        'confidence': latest['decision_confidence'],
        'loop_count': latest['cycle'],
        'novelty_score': 0.5,
        'timestamp': datetime.now().isoformat()
    })
    log("Filtered feedback injected to metadata_bank.")


def log(event: str) -> None:
    entry = {'timestamp': datetime.now().isoformat(), 'event': event}
    history_log.append(entry)
    print(f"[LOG] {entry['timestamp']}: {event}")


def generate_plot() -> str:
    if not novel_insights:
        return ""
    x = [insight['cycle'] for insight in novel_insights]
    y = [insight['refined_accuracy'] for insight in novel_insights]
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title('Refined Accuracy Over Time')
    plt.xlabel('Cycle')
    plt.ylabel('Accuracy')
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    return f"<img src='data:image/png;base64,{img_data}' />"


def export_state() -> Dict[str, Any]:
    return {
        'engine': engine_state,
        'latest_insight': novel_insights[-1] if novel_insights else {},
        'total_metadata': len(metadata_bank),
        'history': history_log[-5:],
        'deltas': [i['delta'] for i in novel_insights[-5:]]
    }


@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'version': 'v1.3'}), 200


@app.route('/')
def dashboard():
    state = export_state()
    graph_html = generate_plot()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Recursive Predictive Logic Engine</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                h2 { color: #333; }
                pre { background: #fff; padding: 15px; border-radius: 5px; overflow-x: auto; }
                form { background: #fff; padding: 15px; margin: 15px 0; border-radius: 5px; }
                label { display: block; margin: 10px 0 5px; font-weight: bold; }
                input[type="number"], input[type="file"] { padding: 8px; width: 200px; }
                input[type="range"] { width: 200px; }
                button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; }
                button:hover { background: #0056b3; }
                hr { border: none; border-top: 1px solid #ddd; margin: 20px 0; }
                img { max-width: 100%; border-radius: 5px; margin: 15px 0; }
            </style>
        </head>
        <body>
            <h2>Recursive Predictive Logic Engine — v1.3</h2>
            <pre>{{ state|tojson(indent=2) }}</pre>
            <form action="/run" method="post">
                <label>Number of cycles:</label>
                <input type="number" name="cycles" value="3" min="1" max="20">
                <label>Weight bias (1.0 = neutral):</label>
                <input type="range" name="bias" min="0.1" max="2.0" step="0.1" value="1.0" oninput="this.nextElementSibling.value = this.value">
                <output>1.0</output>
                <button type="submit">Run Cycles</button>
            </form>
            <hr>
            {{ graph|safe }}
            <form action="/upload" method="post" enctype="multipart/form-data">
                <label>Upload CSV:</label>
                <input type="file" name="file" accept=".csv">
                <button type="submit">Upload</button>
            </form>
        </body>
        </html>
    ''',
                                  state=state,
                                  graph=graph_html)


@app.route('/run', methods=['POST'])
def run_cycles():
    cycles = int(request.form.get('cycles', 3))
    bias = float(request.form.get('bias', 1.0))
    engine_state['weight_bias'] = bias
    for i in range(cycles):
        ingest_data({
            'source': 'webform',
            'incident_count': i,
            'delay_minutes': i * 3,
            'crew_count': 5 + i,
            'domain': 'safety' if i % 2 == 0 else 'schedule'
        })
        refine_predictions()
        apply_filters_and_feedback()
        time.sleep(0.1)
    return dashboard()


@app.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    if not file:
        return "No file uploaded"
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.DictReader(stream)
    for row in csv_input:
        ingest_data(row)
        refine_predictions()
        apply_filters_and_feedback()
    return dashboard()


if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0',
            port=5000,
            debug=os.environ.get('FLASK_ENV') != 'production')
