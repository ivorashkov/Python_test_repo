import psutil
from flask import Flask
from prometheus_client import start_http_server, Gauge, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Create a Prometheus gauge to hold the CPU usage
cpu_usage_gauge = Gauge('cpu_usage', 'CPU usage of the machine in percent')

# Route for root ("/") to provide a welcome message
@app.route('/')
def index():
    return "Welcome to the CPU Usage Prometheus App!"

# Route to get the CPU usage (used for testing)
@app.route('/cpu_usage', methods=['GET'])
def get_cpu_usage():
    # Get CPU usage with a 1-second interval to ensure accurate reading
    cpu_usage = psutil.cpu_percent(interval=1)  # Get accurate CPU usage over 1 second
    cpu_usage_gauge.set(cpu_usage)  # Update Prometheus gauge with this value
    return {"cpu_usage": cpu_usage}

# Prometheus scraper endpoint
@app.route('/metrics')
def metrics():
    # Update the gauge with the current CPU usage, do not use interval=1 here
    cpu_usage = psutil.cpu_percent(interval=None)  # No interval, immediately return current value
    cpu_usage_gauge.set(cpu_usage)  # Set the current CPU usage
    
    # Create a custom registry to store only your metrics
    registry = CollectorRegistry()

    # Register the gauge with the custom registry
    cpu_usage_gauge.registry = registry

    # Return only the custom metrics in the expected Prometheus format
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    # Start Prometheus client HTTP server on port 8000 for scraping (same IP)
    start_http_server(8000)
    
    # Start Flask app on port 8001 for other routes (same IP, different port)
    app.run(host='0.0.0.0', port=8001)
