from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

SCRIPTS = {
    "API - availability": "../API/api_availability.py",
    "API - latency training": "../API/latency_training_api_endpoint.py",
    "API - latency serving": "../API/latency_serving_api_endpoints.py",
    "MinIO - stress test": "../MinIO/stress_object_store.py",
    "Hardware usage": "../hardware_usage/get_docker_hw_stats.py",
}

@app.route('/')
def index():
    return render_template('index.html', scripts=SCRIPTS)

@app.route('/run', methods=['POST'])
def run_script():
    selected = request.form.getlist('scripts')
    results = {}
    for script in selected:
        try:
            result = subprocess.run(["python", SCRIPTS[script]], capture_output=True, text=True)
            results[script] = result.stdout or result.stderr
        except Exception as e:
            results[script] = str(e)
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
