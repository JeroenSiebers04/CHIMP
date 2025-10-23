from flask import Flask, render_template, request, jsonify
import subprocess
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from testing_scripts.hardware_usage.stress_serving_api import stress_serving_api_hardware

# Serve the local `style` directory at the URL path `/style` so the existing
# stylesheet link <link href="/style/style.css"> works without moving files.
app = Flask(__name__, static_url_path='/style', static_folder='style')

SCRIPTS_BY_TAB = {
    "Training worker": {
        # Moet nog aangevuld worden
    },
    "Serving API": {
        "API - availability": "..\\testing_scripts\\API\\api_availability.py",
        "API - latency serving": "..\\testing_scripts\\API\\latency_serving_api_endpoints.py",
        "API - throughput serving": "..\\testing_scripts\\hardware_usage\\stress_serving_api.py",
    },
    "Training API": {
        "API - latency training": "..\\testing_scripts\\API\\latency_training_api_endpoint.py",
    },
    "MLFlow": {
        "MLFlow - storage size": "..\\testing_scripts\\MLFlow\\get_mlflow_storage_size.py",
    },
    "Objectstore": {
        "MinIO - stress test": "..\\testing_scripts\\MinIO/stress_object_store.py",
        "MinIO - storage size": "..\\testing_scripts\\MinIO\\get_objectstore_storage_size.py",
    },
    "Front-end": {
        "Curl frontend": "..\\testing_scripts\\curl_frontend.py",
    },
    "Message Queue": {
        "Spam API requests": "..\\testing_scripts\\spam_api_requests.py",
    },
    "CHIMP": {
        "Menu": "..\\testing_scripts\\menu.py",
    },
}


@app.route('/')
def index():
    return render_template('index.html', tabs=SCRIPTS_BY_TAB)


@app.route('/run', methods=['POST'])
def run_script():
    selected = request.form.getlist('scripts')
    lookup = {}
    for tab, mapping in SCRIPTS_BY_TAB.items():
        for name, path in mapping.items():
            lookup[name] = path

    results = {}
    for script_name in selected:
        path = lookup.get(script_name)
        if not path:
            results[script_name] = f"Script path not found for: {script_name}"
            continue
        try:
            result = subprocess.run([sys.executable, path], capture_output=True, text=True)
            out = result.stdout.strip()
            err = result.stderr.strip()
            results[script_name] = out if out else err if err else f"Exit code {result.returncode} (no output)"
        except Exception as e:
            results[script_name] = str(e)

    return render_template('results.html', results=results)

@app.route('/test')
def run_code():
    result = stress_serving_api_hardware(amount=200)
    return jsonify({"message" : result})

if __name__ == '__main__':
    app.run(debug=True)
