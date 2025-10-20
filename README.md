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
