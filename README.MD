Multi-Service Deployment Guide
This guide covers the setup and deployment of three distinct services:

Flask Calculator - A RESTful calculator API

k8s-microservice - A Kubernetes-native microservice

travel-memory-app - A travel memory tracking application

🚀 Quick Deployment Overview
Prerequisites
Ensure you have the following installed:

Minikube (v1.20.0+)

kubectl (v1.21.0+)

Docker (v20.10.0+)

Helm (v3.0.0+, optional)

Architecture Diagram
text
┌─────────────────────────────────────────────────────────┐
│                Minikube Kubernetes Cluster              │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌────────────────┐  ┌─────────────┐ │
│  │  Flask Calc  │  │ k8s-microsvc   │  │ Travel App  │ │
│  │    :5000     │  │    :8080       │  │   :3000     │ │
│  └──────┬───────┘  └───────┬────────┘  └──────┬──────┘ │
│         │                  │                   │        │
│  ┌──────▼──────────────────▼───────────────────▼──────┐ │
│  │                 NGINX Ingress Controller           │ │
│  └───────────────────────┬────────────────────────────┘ │
│                          │                               │
│                  http://calc.local.com                  │
│                  http://micro.local.com                 │
│                  http://travel.local.com                │
└─────────────────────────────────────────────────────────┘
📦 Service 1: Flask Calculator
Deployment Steps
bash
# 1. Start Minikube with sufficient resources
minikube start --memory=4096 --cpus=3 --disk-size=20gb

# 2. Enable required addons
minikube addons enable ingress
minikube addons enable ingress-dns
minikube addons enable metrics-server

# 3. Set Minikube Docker environment
eval $(minikube docker-env)

# 4. Build Docker image
cd flask-calculator
docker build -t flask-calc:latest .

# 5. Deploy to Kubernetes
kubectl apply -f k8s/

# 6. Verify deployment
kubectl get pods -l app=calculator
kubectl get svc calc-service
kubectl get ingress calc-ingress

Service 2: k8s-microservice
Deployment Steps
bash
# 1. Navigate to microservice directory
cd k8s-microservice

# 2. Build Docker image
docker build -t k8s-microservice:latest .

# 3. Create namespace (optional but recommended)
kubectl create namespace microservice-ns

# 4. Deploy using Helm (if available)
helm install microservice ./chart --namespace microservice-ns

# OR deploy using kubectl
kubectl apply -f deploy/ -n microservice-ns

# 5. Expose service
kubectl expose deployment microservice-deployment \
  --type=NodePort \
  --port=8080 \
  --name=microservice-svc \
  -n microservice-ns

# 6. Create Ingress
kubectl apply -f ingress.yaml -n microservice-ns

Service 3: travel-memory-app
Deployment Steps
bash
# 1. Navigate to travel app directory
cd travel-memory-app

# 2. Build frontend and backend images
docker build -t travel-frontend:latest -f frontend/Dockerfile .
docker build -t travel-backend:latest -f backend/Dockerfile .

# 3. Create namespace
kubectl create namespace travel-ns

# 4. Deploy database (if needed)
kubectl apply -f k8s/mongodb.yaml -n travel-ns

# 5. Deploy backend
kubectl apply -f k8s/backend-deployment.yaml -n travel-ns

# 6. Deploy frontend
kubectl apply -f k8s/frontend-deployment.yaml -n travel-ns

# 7. Deploy Ingress
kubectl apply -f k8s/travel-ingress.yaml -n travel-ns

Host Configuration
Update /etc/hosts File

# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Add all services to hosts file
echo "$MINIKUBE_IP calc.local.com" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP micro.local.com" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP travel.local.com" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP services.local.com" | sudo tee -a /etc/hosts

Port Forwarding (For Direct Access)

# Flask Calculator
kubectl port-forward service/calc-service 5001:80

# k8s-microservice
kubectl port-forward service/microservice-svc -n microservice-ns 8081:8080

# Travel Memory Backend
kubectl port-forward service/travel-backend-svc -n travel-ns 5002:5000

# Travel Memory Frontend
kubectl port-forward service/travel-frontend-svc -n travel-ns 3000:80

View Logs

# Flask Calculator logs
kubectl logs -l app=calculator --tail=50

# k8s-microservice logs
kubectl logs -l app=microservice -n microservice-ns --tail=50

# Travel App logs
kubectl logs -l app=travel-backend -n travel-ns --tail=50
kubectl logs -l app=travel-frontend -n travel-ns --tail=50

Testing the Services

Test k8s-microservice
curl http://micro.local.com/health
curl http://micro.local.com/api/v1/status

Test Flask Calculator

curl -X POST http://calc.local.com/calculate \
  -H "Content-Type: application/json" \
  -d '{"a":10,"b":5,"op":"+"}'

curl http://calc.local.com/health

Test Travel Memory App
# Frontend
curl http://travel.local.com/

# Backend API
curl http://travel.local.com/api/health
curl http://travel.local.com/api/memories
