
STEP 1️⃣ Start Minikube & Enable Ingress

minikube start
minikube addons enable ingress


Verify:
kubectl get pods -n ingress-nginx


STEP  Create Custom Nginx Microservices

STEP  Apply All
kubectl apply -f .

kubectl get pods
kubectl get svc
kubectl get ingress


minikube ip






Test via Ingress (from outside the cluster)

# Enable ingress addon in minikube
minikube addons enable ingress

# Verify ingress controller is running
kubectl get pods -n ingress-nginx

# Update /etc/hosts to point to minikube IP
echo "192.168.49.2 service1.local.com service2.local.com service3.local.com" | sudo tee -a /etc/hosts

# Test the ingress
curl -H "Host: service1.local.com" http://192.168.49.2
curl -H "Host: service2.local.com" http://192.168.49.2
curl -H "Host: service3.local.com" http://192.168.49.2



Alternative method without modifying /etc/hosts:
# Using curl with Host header
curl -H "Host: service1.local.com" http://$(minikube ip)
curl -H "Host: service2.local.com" http://$(minikube ip)
curl -H "Host: service3.local.com" http://$(minikube ip)

Health Checks
# Detailed view of pods
kubectl get pods -o wide

# Describe a specific pod
kubectl describe pod microservice-1-d94466577-cnrhc

# Check pod logs
kubectl logs microservice-1-d94466577-cnrhc
kubectl logs microservice-2-f859c57bf-gp95r
kubectl logs microservice-3-64465dc89c-69lx8

# Follow logs in real-time
kubectl logs -f microservice-1-d94466577-cnrhc





Check service endpoints

# Verify services are pointing to correct pods
kubectl get endpoints

# Describe services
kubectl describe svc microservice-1
kubectl describe svc microservice-2
kubectl describe svc microservice-3


Check ingress details

# Describe ingress to see routing rules
kubectl describe ingress microservices-ingress

# Check ingress controller logs
kubectl get pods -n ingress-nginx
kubectl logs -n ingress-nginx <ingress-controller-pod-name>



Quick Diagnostic Commands

# One-liner to check everything
kubectl get all

# Check events (useful for troubleshooting)
kubectl get events --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods
kubectl top nodes

# Check if services have endpoints
kubectl get endpointslices

# Check pod resource limits
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].resources}{"\n"}{end}'

Testing with Minikube Dashboard

# Open minikube dashboard in browser
minikube dashboard

# Or get dashboard URL
minikube dashboard --url

Debugging Tips

# Check if pods are actually running the application
kubectl exec microservice-1-d94466577-cnrhc -- ps aux

# Check container environment
kubectl exec microservice-1-d94466577-cnrhc -- env

# Test from inside the pod
kubectl exec microservice-1-d94466577-cnrhc -- curl -s localhost

# Check network policies
kubectl get networkpolicies


