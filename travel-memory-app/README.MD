Travel Memory App - Kubernetes Deployment
📋 Overview
This project deploys a Travel Memory App on a local Kubernetes cluster using Minikube. The application allows users to create and retrieve travel memories through a RESTful API.

🚀 Prerequisites
Required Tools
Docker: For building and managing container images

Minikube: For local Kubernetes cluster

kubectl: Kubernetes command-line tool

curl: For API testing

Verify Installation
bash
# Check Docker
docker --version

# Check Minikube
minikube version

# Check kubectl
kubectl version --client
🏗️ Project Structure
text
travel-memory-app/
├── Dockerfile
├── app/                    # Application source code
├── k8s/                    # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── pvc.yaml           # Persistent Volume Claim (if applicable)
└── README.md
📦 Deployment Steps
1. Start Minikube Cluster
bash
# Start Minikube
minikube start

# Enable ingress addon
minikube addons enable ingress

# Verify ingress controller
kubectl get pods -n ingress-nginx
2. Build Docker Image
bash
# Build the application image
docker build -t travel-memory-app .

# Optional: Load image into Minikube if using Minikube's Docker daemon
eval $(minikube docker-env)
docker build -t travel-memory-app .
3. Deploy Kubernetes Resources
bash
# Deploy all Kubernetes manifests
kubectl apply -f k8s/
4. Verify Deployment
bash
# Check all resources
kubectl get pods
kubectl get svc
kubectl get pvc
kubectl get ingress
Expected output should show all resources in Running or Bound state.

🌐 Configure Hostname
Update /etc/hosts
bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Add to /etc/hosts
echo "$MINIKUBE_IP memories.local.com" | sudo tee -a /etc/hosts

# Verify
cat /etc/hosts | grep memories.local.com
Alternative: Use Host Header
If you don't want to modify /etc/hosts, use:

bash
MINIKUBE_IP=$(minikube ip)
curl -H "Host: memories.local.com" http://$MINIKUBE_IP/memories
🧪 Test API Endpoints
Create a Memory (POST)
bash
curl -X POST http://memories.local.com/memories \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Paris",
    "date": "2024-01-05",
    "description": "Eiffel Tower visit",
    "imageUrl": "https://example.com/img1.jpg"
  }'
Retrieve Memories (GET)
bash
curl http://memories.local.com/memories
Example Response
json
[
  {
    "id": 1,
    "location": "Paris",
    "date": "2024-01-05",
    "description": "Eiffel Tower visit",
    "imageUrl": "https://example.com/img1.jpg"
  }
]
🔍 Troubleshooting
Common Issues
1. Hostname Not Resolving
bash
# Verify Minikube IP
minikube ip

# Check /etc/hosts entry
grep memories.local.com /etc/hosts

# Test with Host header
curl -H "Host: memories.local.com" http://$(minikube ip)/memories
2. Pods Not Running
bash
# Check pod status
kubectl get pods

# Describe problematic pod
kubectl describe pod <pod-name>

# Check pod logs
kubectl logs <pod-name>
3. Ingress Issues
bash
# Check ingress status
kubectl describe ingress travel-ingress

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx
4. Service Issues
bash
# Verify service endpoints
kubectl get endpoints travel-app-service

# Check service details
kubectl describe svc travel-app-service
Debugging Commands
bash
# Get comprehensive status
kubectl get all

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods

# Test from inside cluster
kubectl run test-$RANDOM --rm -it --image=curlimages/curl -- sh -c "curl -s http://travel-app-service/memories"
🛠️ Development
Rebuild and Redeploy
bash
# Rebuild image
docker build -t travel-memory-app .

# Restart deployment
kubectl rollout restart deployment/travel-app-deployment

# Watch rollout status
kubectl rollout status deployment/travel-app-deployment
Access Application Logs
bash
# Stream logs
kubectl logs -f deployment/travel-app-deployment

# Get logs for specific pod
kubectl logs <pod-name>
📊 Monitoring
Minikube Dashboard
bash
# Open dashboard in browser
minikube dashboard

# Or get URL only
minikube dashboard --url
Check Resource Usage
bash
# Pod resource usage
kubectl top pods

# Node resource usage
kubectl top nodes
🧹 Cleanup
Remove Application
bash
# Delete all resources
kubectl delete -f k8s/

# Remove from /etc/hosts
sudo sed -i '/memories.local.com/d' /etc/hosts
Stop Minikube
bash
# Stop cluster
minikube stop

# Delete cluster (optional)
minikube delete
📝 Notes
The application uses port 80 for the service

Ingress routes traffic based on hostname memories.local.com

Persistent storage is configured via PVC (if applicable)

Default namespace is used for all resources
