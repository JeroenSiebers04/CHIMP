from flask import Flask, render_template, request, jsonify
import subprocess
import sys
import os
import importlib.util
import inspect
import io
import contextlib
import re


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
        "API - availability": "..\\testing_scripts\\API\\serving_api_availability.py",
        "API - latency serving": "..\\testing_scripts\\API\\latency_serving_api_endpoints.py",
        "API - throughput serving": "..\\testing_scripts\\API\\serving_api_throughput.py",
    },
    "Training API": {
        "API - availability": "..\\testing_scripts\\API\\training_api_availability.py", 
        "API - latency training": "..\\testing_scripts\\API\\latency_training_api_endpoint.py",
        "API - throughput training": "..\\testing_scripts\\API\\training_api_throughput.py",
    },
    "MLFlow": {
        "MLFlow - storage size": "..\\testing_scripts\\MLFlow\\get_mlflow_storage_size.py",
    },
    "Objectstore": {
        "MinIO - stress test": "..\\testing_scripts\\MinIO/stress_object_store.py",
        "MinIO - storage size": "..\\testing_scripts\\MinIO\\get_objectstore_storage_size.py",
    },
    "Front-end": {
        # Moet nog aangevuld worden
    },
    "Message Queue": {
        # Moet nog aangevuld worden
    },
    "CHIMP": {
        "Ketentest": "..\\testing_scripts\\menu.py",
    },
}
SCRIPTS_HINTS = {
    "API - throughput serving": "Aantal requests op de API",
    "API - throughput training": "Aantal requests op de training API",
}


@app.route('/')
def index():
    accepts_amount = {}
    for tab, mapping in SCRIPTS_BY_TAB.items():
        for name, path in mapping.items():
            abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
            ok = False
            try:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    src = f.read()
                    if re.search(r"def\s+\w+\s*\([^)]*\bamount\b[^)]*\)", src):
                        ok = True
            except Exception:
                ok = False
            accepts_amount[name] = ok

    return render_template('index.html', tabs=SCRIPTS_BY_TAB, accepts_amount=accepts_amount, hints=SCRIPTS_HINTS)


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

        safe = script_name.replace(' ', '_')
        amount_field = f'amount-{safe}'
        amount_str = request.form.get(amount_field)
        amount = None
        if amount_str not in (None, ''):
            try:
                amount = int(amount_str)
            except ValueError:
                results[script_name] = f'Invalid amount value: {amount_str}'
                continue

        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))

        if amount is not None:
            try:
                mod = _load_module_from_path(path)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rval = _call_module_with_amount(mod, amount)
                out = buf.getvalue().strip()
                results[script_name] = out if out else (str(rval) if rval is not None else 'OK')
            except Exception as e:
                try:
                    cmd = [sys.executable, abs_path, '--amount', str(amount)]
                    proc = subprocess.run(cmd, capture_output=True, text=True)
                    out = proc.stdout.strip()
                    err = proc.stderr.strip()
                    if proc.returncode == 0:
                        results[script_name] = out if out else f'Exit code {proc.returncode} (no output)'
                    else:
                        results[script_name] = err if err else f'Exit code {proc.returncode} (no output) -- import error: {e}'
                except Exception as e2:
                    results[script_name] = f'Both import and subprocess execution failed: import_error={e}, subprocess_error={e2}'
        else:
            try:
                proc = subprocess.run([sys.executable, abs_path], capture_output=True, text=True)
                out = proc.stdout.strip()
                err = proc.stderr.strip()
                results[script_name] = out if out else err if err else f'Exit code {proc.returncode} (no output)'
            except Exception as e:
                results[script_name] = str(e)

    return render_template('results.html', results=results)


def _load_module_from_path(path):
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
    if not os.path.exists(abs_path):
        raise FileNotFoundError(abs_path)
    name = f"mod_" + os.path.splitext(os.path.basename(abs_path))[0]
    spec = importlib.util.spec_from_file_location(name, abs_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _call_module_with_amount(module, amount):
    candidates = []
    for fname, fn in inspect.getmembers(module, inspect.isfunction):
        sig = inspect.signature(fn)
        params = sig.parameters
        score = 0
        if any(k in fname.lower() for k in ("stress", "test", "run", "main")):
            score += 1
        if 'amount' in params:
            score += 2
        elif len(params) >= 1:
            first = next(iter(params.values()))
            if first.name in ('amount', 'n', 'num', 'count', 'requests'):
                score += 2
            else:
                score += 0
        if score > 0:
            candidates.append((score, fname, fn, sig))

    candidates.sort(key=lambda x: x[0], reverse=True)
    if not candidates:
        raise RuntimeError('No callable candidate found in module')

    _, fname, fn, sig = candidates[0]

    try:
        if 'amount' in sig.parameters:
            return fn(amount=amount)
        else:
            return fn(amount)
    except TypeError:
        return fn()


@app.route('/run_with_amount', methods=['POST'])
def run_with_amount():
    """Run a single script (by visible name) with an integer `amount` param.

    The frontend should POST form fields 'script' (name shown in the UI) and
    'amount' (number). The handler will try to import the target script module
    and call a suitable function with that amount. If import/call fails it will
    fallback to running the script as a subprocess with `--amount`.
    """
    script_name = request.form.get('script') or request.form.get('scripts')
    amount_str = request.form.get('amount')
    try:
        amount = int(amount_str) if amount_str not in (None, '') else None
    except ValueError:
        return jsonify({'error': 'Invalid amount value'}), 400

    lookup = {}
    for tab, mapping in SCRIPTS_BY_TAB.items():
        for name, path in mapping.items():
            lookup[name] = path

    path = lookup.get(script_name)
    if not path:
        return jsonify({'error': f'Script path not found for: {script_name}'}), 404

    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))

    try:
        mod = _load_module_from_path(path)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = _call_module_with_amount(mod, amount)
        output = buf.getvalue()
        return jsonify({'script': script_name, 'amount': amount, 'stdout': output, 'result': str(result)})
    except Exception as e:
        try:
            cmd = [sys.executable, abs_path]
            if amount is not None:
                cmd += ["--amount", str(amount)]
            proc = subprocess.run(cmd, capture_output=True, text=True)
            out = proc.stdout.strip()
            err = proc.stderr.strip()
            return jsonify({'script': script_name, 'amount': amount, 'stdout': out, 'stderr': err, 'returncode': proc.returncode, 'fallback_error': str(e)})
        except Exception as e2:
            return jsonify({'error': 'Both import and subprocess execution failed', 'import_error': str(e), 'subprocess_error': str(e2)}), 500

@app.route('/test')
def run_code():
    amount_param = request.args.get('amount', None)
    try:
        amount = int(amount_param) if amount_param is not None and amount_param != '' else 200
    except ValueError:
        amount = 200

    result = stress_serving_api_hardware(amount=amount)
    return jsonify({"amount": amount, "message": result})

if __name__ == '__main__':
    app.run(debug=True)
