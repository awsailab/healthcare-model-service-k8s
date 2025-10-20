# healthcare-model-service-k8s

Kubernetes-Ready AI Model Service
This repository provides a production-grade blueprint for containerizing a machine learning model and deploying it as a scalable, orchestrated microservice on Kubernetes. It serves as a practical demonstration of cloud-native best practices for MLOps infrastructure.

The project encapsulates a simple FastAPI application within a Docker container and uses declarative Kubernetes manifests to manage its deployment, networking, and scalability.

Architecture Overview
The application is deployed using a standard Kubernetes Deployment to manage the lifecycle of the application Pods. A Service of type ClusterIP provides a stable internal network endpoint for the application, enabling reliable service discovery within the cluster.

This architecture ensures that the application is scalable, resilient, and decoupled from the underlying infrastructure.

Key Features
Containerized Application: The FastAPI service is packaged into a lightweight, portable Docker image.

Declarative Orchestration: Kubernetes manifests define the desired state of the application, enabling version-controlled, repeatable deployments.

Scalability & Resilience: The Deployment controller ensures the specified number of replicas are always running, automatically recovering from pod failures.

Service Discovery: A Service object provides a stable DNS name and IP address, abstracting away the ephemeral nature of pods.

Local Development Workflow: The entire stack can be tested locally using minikube, mirroring a production environment.

Tech Stack
Orchestration: Kubernetes (managed locally via Minikube)

Containerization: Docker

API Framework: FastAPI (Python 3.9)

Configuration: Kustomize

Local Deployment Guide
Follow these steps to run the application on a local Kubernetes cluster.

Prerequisites

Docker installed and running.

Minikube installed.

kubectl installed.

Steps

Clone the Repository:

Bash
git clone https://github.com/awsailab/healthcare-model-service-k8s.git
cd healthcare-model-service-k8s
Start the Local Cluster:

Bash
minikube start --driver=docker
Build the Docker Image:

Bash
docker build -t healthcare-model-service .
Load the Image into the Cluster: This step makes the locally-built image available to the Kubernetes cluster.

Bash
minikube image load healthcare-model-service:latest
Deploy the Application to Kubernetes: This command uses Kustomize to apply all manifests in the k8s/ directory.

Bash
kubectl apply -k k8s/
Verify the Deployment: Check that the pods are running successfully.

Bash
kubectl get pods
Access the Service: Use the Minikube tunnel to access the service and open it in your browser.

Bash
minikube service model-api-service
Navigate to the /docs endpoint on the opened URL to interact with the API.

API Endpoint
/predict

Method: POST

Description: Accepts patient data and returns a mock risk prediction.

Request Body:

JSON
{
  "patient_data": {
    "age": 65,
    "cholesterol": 240
  }
}
Success Response:

JSON
{
  "prediction": "High Risk",
  "confidence": 0.92,
  "model_version": "v1.0.0"
}


MLOps Monitoring & Observability
This project includes a complete, production-grade monitoring stack built on Prometheus and Grafana. This stack provides real-time observability into the API's performance, scraping key metrics like request latency, error rates, and traffic volume.

How It Works

The monitoring pipeline is configured using Kubernetes-native best practices:

Application Instrumentation: The FastAPI application uses prometheus-fastapi-instrumentator to automatically expose a /metrics endpoint with detailed performance data.

Monitoring Stack: The kube-prometheus-stack is deployed via Helm into its own monitoring namespace. This stack includes Prometheus (for data collection) and Grafana (for visualization).

Service Discovery: A ServiceMonitor resource is deployed. This is the key component that enables declarative, automated service discovery.

The ServiceMonitor is configured to watch the default namespace for any Service that has the label app: model-api.

Once it finds our service, it instructs Prometheus to automatically begin scraping metrics from the port named http at a 15-second interval.

This setup means monitoring is "zero-touch"—any new pod added to the deployment will be automatically discovered and monitored by Prometheus without any manual configuration.

Visualizing the Metrics (Local Demo)

You can access the live Grafana dashboard to see your API's performance.

Install the Monitoring Stack:

Bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
Get the Grafana Admin Password:

Bash
kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
Access the Grafana Dashboard: Run this command to open a secure tunnel to the Grafana service.

Bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
Now, go to the URL provided in your PORTS tab for port 3000.

Username: admin

Password: (Paste the password you retrieved)

Generate Traffic: To see data, you must generate requests. Open a new terminal and forward your API's port:

Bash
kubectl port-forward svc/model-api-service 8080:80
In a third terminal, run a curl loop (using the URL for port 8080 from your PORTS tab):

Bash
while true; do curl -k -X POST -H "Content-Type: application/json" -d '{"patient_data": {"age": 70}}' <URL_FROM_PORTS_TAB>/predict; sleep 0.5; done
Build a Panel: In Grafana, create a new dashboard and add a panel. Use the following PromQL query to see the live request rate:

Code snippet
rate(http_requests_total{job="serviceMonitor/default/model-api-servicemonitor/0"}[1m])
Set your dashboard's time range to "Last 5 minutes" to see the traffic.
