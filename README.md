# CPU Usage Monitoring with Prometheus and Grafana

## **1️⃣ Install Python**
To set up the environment, install Python and required dependencies:

```bash
sudo apt update
sudo apt install python3
python3 --version
sudo apt install python3-pip
pip3 --version
sudo apt install python3-venv
```

## **2️⃣ Set Up a Python Virtual Environment**
```bash
python3 -m venv pythonenv
source pythonenv/bin/activate
```

## **3️⃣ Install Dependencies**
```bash
pip install psutil Flask prometheus_client
```

To deactivate the virtual environment:
```bash
deactivate
```

## **4️⃣ Save and Reinstall Dependencies**
```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

## **5️⃣ Run the Python App**
```bash
python cpu_usage_prometheus_app.py
```

Verify Prometheus metrics:
```bash
http://localhost:8000/metrics
```

## **6️⃣ Dockerize the Application**
Build and run the Docker container:
```yaml
# Use official Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose ports for Flask and Prometheus
EXPOSE 8000 8001

# Command to run the application
CMD ["python", "cpu_usage_prometheus_app.py"]

```
```bash
docker build -t cpu-monito-app .
docker run -d -p 8000:8000 -p 8001:8001 --name cpu_monitor_app cpu-monito-app
```

Verify endpoints:
```bash
http://localhost:8000/metrics
http://localhost:8001/cpu_usage
```

![image](https://github.com/user-attachments/assets/0c6f6c1c-6f0e-44c8-99e2-b16fbbd3ff23)

![image](https://github.com/user-attachments/assets/caebef32-febd-4bc9-82bc-102875163f8f)

## **7️⃣ Create Prometheus Configuration (`prometheus.yml`)**
Create a file named `prometheus.yml` and add the following content:
```yaml
global:
  scrape_interval: 10s  # Adjust scraping interval

scrape_configs:
  - job_name: 'cpu_monitor'
    static_configs:
      - targets: ['cpu-monitor-app:8000']
```

## **8️⃣ Create Docker Compose Configuration (`docker-compose.yml`)**
Create a `docker-compose.yml` file:
```yaml
version: '3.9'
services:
  cpu-monitor-app:
    build: .
    ports:
      - "8001:8001"  # Flask API accessible on port 8001
      - "8000:8000"  # Prometheus scrapes metrics from port 8000
    restart: always

  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"  # Prometheus UI accessible on port 9090
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
    depends_on:
      - cpu-monitor-app  # Ensure CPU monitor app starts first
```

## **9️⃣ Start Services Using Docker Compose**
```bash
docker compose up -d
docker ps
docker-compose logs -f
```

## **🔍 Verify Everything**
Check the endpoints:
```bash
http://localhost:8001/cpu_usage
http://localhost:8000/metrics
```

## **🔹 Add Grafana to Docker Compose**
Modify `docker-compose.yml` to include Grafana:
```yaml
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"  # Grafana UI available on port 3000
    depends_on:
      - prometheus
    restart: always
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  grafana-data:
```

Restart the services:
```bash
docker-compose up -d
```
![image](https://github.com/user-attachments/assets/7e4879ed-ae67-4785-b288-cfc01344680a)

## **📊 Creating Graph in Prometheus**

![image](https://github.com/user-attachments/assets/bb17a9e3-2390-4772-bd34-7b9bb601d795)



## **📊 Creating Dashboards in Grafana**
1. Open Grafana:  
   ```
   http://localhost:3000
   ```
2. **Login Credentials:**  
   - Username: `admin`
   - Password: `admin` (change it upon first login)
3. Go to **Configuration → Data Sources**
4. Click **"Add Data Source"**
5. Select **Prometheus**
6. Set **URL** to:
   ```
   http://prometheus:9090
   ```
7. Click **"Save & Test"**

### **📌 Create a Dashboard for CPU Monitoring**
1. Go to **Create → Dashboard**
2. Click **"Add a new panel"**
3. In the **Metrics** field, enter:
   ```
   cpu_usage
   ```

4. Select **Graph Type**
5. Click **Save** and name your dashboard

![image](https://github.com/user-attachments/assets/56931cd6-2bac-4dbb-88b7-816a2074bb1f)


