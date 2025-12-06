Flask Calculator Application
A simple calculator web application built with Flask that provides basic arithmetic operations and maintains a calculation history.

🎯 Features
Basic Operations: Addition, subtraction, multiplication, and division

Calculation History: Stores all calculations with timestamps

RESTful API: JSON-based API endpoints for all operations

Persistent Storage: Uses Kubernetes Persistent Volume for data storage

Ingress Support: Accessible via custom domain through Kubernetes Ingress

Health Checks: Built-in health monitoring endpoints

Configurable Settings: Environment variables for easy configuration

🏗️ Architecture
text
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster (Minikube)             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Ingress   │    │   Service   │    │   ConfigMap │     │
│  │   Resource  │    │             │    │             │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                  │                   │            │
│  ┌──────▼──────────────────▼───────────────────▼──────┐    │
│  │                Calculator Pod                      │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │            Flask Application                 │  │    │
│  │  │  • REST API (Port 5000)                     │  │    │
│  │  │  • Calculation History                      │  │    │
│  │  │  • Persistent Storage                       │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
📋 Prerequisites
Before you begin, ensure you have the following installed:

Minikube (v1.20.0 or later)

kubectl (v1.21.0 or later)

Docker (v20.10.0 or later)

curl (for API testing)

🚀 Quick Start
1. Start Minikube Cluster
bash
# Start Minikube cluster
minikube start --memory=4096 --cpus=2

# Enable Ingress addon
minikube addons enable ingress

# Verify Minikube status
minikube status
2. Build Docker Image
bash
# Set Minikube's Docker daemon as the default
eval $(minikube docker-env)

# Build the calculator application image
docker build -t calc-app:latest .

# Verify the image was built
docker images | grep calc-app
3. Deploy to Kubernetes
bash
# Apply all Kubernetes manifests
kubectl apply -f k8s/calc-configmap.yaml
kubectl apply -f k8s/calc-pvc.yaml
kubectl apply -f k8s/calc-deployment.yaml
kubectl apply -f k8s/calc-service.yaml
kubectl apply -f k8s/calc-ingress.yaml
4. Verify Deployment
bash
# Check all resources
kubectl get all -n default

# Monitor pod status
kubectl get pods -w

# Check service
kubectl get svc

# Check persistent volume claim
kubectl get pvc

# Check ingress
kubectl get ingress
5. Configure Local DNS
bash
# Get Minikube IP address
MINIKUBE_IP=$(minikube ip)
echo "Minikube IP: $MINIKUBE_IP"

# Add to /etc/hosts (requires sudo on Linux/Mac)
echo "$MINIKUBE_IP calc.local.com" | sudo tee -a /etc/hosts

# For Windows, edit C:\Windows\System32\drivers\etc\hosts as administrator
6. Access the Application
The application will be available at: http://calc.local.com

📁 Project Structure
text
flask-calculator/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── k8s/                     # Kubernetes manifests
│   ├── calc-configmap.yaml  # Configuration
│   ├── calc-pvc.yaml        # Persistent volume claim
│   ├── calc-deployment.yaml # Deployment configuration
│   ├── calc-service.yaml    # Service definition
│   └── calc-ingress.yaml    # Ingress routing
├── templates/               # HTML templates (if any)
│   └── index.html
├── static/                  # Static files (CSS, JS)
└── README.md               # This file
🔧 Kubernetes Manifests
1. ConfigMap (k8s/calc-configmap.yaml)
yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: calc-config
data:
  HISTORY_FILE: "/data/calc_history.json"
  LOG_LEVEL: "INFO"
2. Persistent Volume Claim (k8s/calc-pvc.yaml)
yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: calc-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
3. Deployment (k8s/calc-deployment.yaml)
yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: calc-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: calculator
  template:
    metadata:
      labels:
        app: calculator
    spec:
      containers:
      - name: calculator
        image: calc-app:latest
        ports:
        - containerPort: 5000
        envFrom:
        - configMapRef:
            name: calc-config
        volumeMounts:
        - name: storage
          mountPath: /data
      volumes:
      - name: storage
        persistentVolumeClaim:
          claimName: calc-pvc
4. Service (k8s/calc-service.yaml)
yaml
apiVersion: v1
kind: Service
metadata:
  name: calc-service
spec:
  selector:
    app: calculator
  ports:
  - port: 80
    targetPort: 5000
  type: ClusterIP
5. Ingress (k8s/calc-ingress.yaml)
yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: calc-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: calc.local.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: calc-service
            port:
              number: 80
📊 API Reference
Base URL: http://calc.local.com
1. Perform Calculation
bash
# POST /calculate
# Perform arithmetic operation
curl -X POST http://calc.local.com/calculate \
  -H "Content-Type: application/json" \
  -d '{"a": 12, "b": 4, "op": "/"}'
Request Body:

json
{
  "a": 12,
  "b": 4,
  "op": "/"
}
Response:

json
{
  "result": 3,
  "operation": "12 / 4",
  "timestamp": "2024-01-15T10:30:00Z"
}
Supported Operations:

+ (addition)

- (subtraction)

* (multiplication)

/ (division)

2. Get Calculation History
bash
# GET /history
# Retrieve all calculations
curl http://calc.local.com/history
Response:

json
{
  "history": [
    {
      "operation": "12 / 4",
      "result": 3,
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "operation": "5 + 3",
      "result": 8,
      "timestamp": "2024-01-15T10:25:00Z"
    }
  ],
  "count": 2
}
3. Clear History
bash
# DELETE /history
# Clear all calculation history
curl -X DELETE http://calc.local.com/history
Response:

json
{
  "message": "History cleared successfully"
}
4. Health Check
bash
# GET /health
# Check application health
curl http://calc.local.com/health
Response:

json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
5. Application Info
bash
# GET /info
# Get application information
curl http://calc.local.com/info
Response:

json
{
  "name": "Flask Calculator",
  "version": "1.0.0",
  "description": "A simple calculator API",
  "operations": ["+", "-", "*", "/"]
}
🐳 Docker Configuration
Dockerfile
dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
requirements.txt
text
Flask==2.3.2
Werkzeug==2.3.6
🔍 Troubleshooting
Common Issues
Minikube IP keeps changing

bash
# Update /etc/hosts with new IP
MINIKUBE_IP=$(minikube ip)
sudo sed -i '' "s/.*calc.local.com/$MINIKUBE_IP calc.local.com/" /etc/hosts
Image not found in Minikube

bash
# Rebuild with Minikube's Docker daemon
eval $(minikube docker-env)
docker build -t calc-app:latest .
Persistent volume not mounting

bash
# Check PVC status
kubectl describe pvc calc-pvc

# Check pod events
kubectl describe pod <pod-name>
Ingress not working

bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Check ingress resource
kubectl describe ingress calc-ingress
Debug Commands
bash
# View pod logs
kubectl logs deployment/calc-deployment

# View pod details
kubectl describe pod <pod-name>

# Access pod shell
kubectl exec -it <pod-name> -- /bin/bash

# Check service endpoints
kubectl get endpoints calc-service

# Test service from within cluster
kubectl run test --image=curlimages/curl -it --rm -- curl http://calc-service/
🧹 Cleanup
bash
# Delete all resources
kubectl delete -f k8s/calc-ingress.yaml
kubectl delete -f k8s/calc-service.yaml
kubectl delete -f k8s/calc-deployment.yaml
kubectl delete -f k8s/calc-pvc.yaml
kubectl delete -f k8s/calc-configmap.yaml

# Or delete all at once
kubectl delete -f k8s/

# Remove from /etc/hosts
sudo sed -i '' '/calc.local.com/d' /etc/hosts

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
📈 Monitoring
bash
# View resource usage
kubectl top pods
kubectl top nodes

# Monitor events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check ingress logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller