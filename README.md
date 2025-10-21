
# Kubernetes-Ready AI Model Service

[](https://kubernetes.io/)
[](https://www.docker.com/)
[](https://fastapi.tiangolo.com/)
[](https://prometheus.io/)
[](https://grafana.com/)

This repository provides a production-grade blueprint for containerizing a machine learning model and deploying it as a scalable, observable microservice on Kubernetes. It serves as a practical, end-to-end demonstration of cloud-native best practices for MLOps infrastructure.

The project encapsulates a simple FastAPI application within a Docker container and uses declarative Kubernetes manifests to manage its deployment, networking, scalability, and real-time monitoring.

-----

## Architecture Overview

The application is deployed using a standard Kubernetes `Deployment` to manage the lifecycle of the application `Pods`. A `Service` of type `ClusterIP` provides a stable internal network endpoint for the application, enabling reliable service discovery within the cluster.

This architecture ensures that the application is scalable, resilient, and decoupled from the underlying infrastructure.

-----

## Tech Stack

  * **Orchestration:** Kubernetes (managed locally via Minikube)
  * **Containerization:** Docker
  * **API Framework:** FastAPI (Python 3.9)
  * **Monitoring:** Prometheus & Grafana
  * **Service Discovery:** Kubernetes `ServiceMonitor`
  * **Package Management:** Helm
  * **Configuration:** Kustomize

-----

## Local Deployment Guide

Follow these steps to run the application on a local Kubernetes cluster.

### Prerequisites

  * Docker installed and running
  * Minikube installed
  * `kubectl` installed
  * Helm installed

### 1\. Start the Local Cluster

```bash
minikube start --driver=docker
```

### 2\. Build the Docker Image

From the root of this repository, build the application's Docker image:

```bash
docker build -t healthcare-model-service .
```

### 3\. Load the Image into the Cluster

Make the locally-built image available to the Minikube cluster:

```bash
minikube image load healthcare-model-service:latest
```

### 4\. Deploy the Application

This command uses Kustomize to find and apply all manifests in the `k8s/` directory, including the `ServiceMonitor` for monitoring.

```bash
kubectl apply -k k8s/
```

### 5\. Verify the Deployment

Check that the pods are running successfully (it may take a moment for them to be in the `Running` state):

```bash
kubectl get pods
```

-----

## API Endpoint

### Accessing the API

To interact with the API, first open a secure tunnel from your machine to the service running in the cluster:

```bash
kubectl port-forward svc/model-api-service 8080:80
```

You can now access the API at `http://localhost:8080`. The interactive documentation is available at **`http://localhost:8080/docs`**.

### `/predict`

  * **Method:** `POST`
  * **Description:** Accepts patient data and returns a mock risk prediction.
  * **Request Body:**
    ```json
    {
      "patient_data": {
        "age": 65,
        "cholesterol": 240
      }
    }
    ```
  * **Success Response:**
    ```json
    {
      "prediction": "High Risk",
      "confidence": 0.92,
      "model_version": "v1.0.0"
    }
    ```

-----

## MLOps Monitoring & Observability

This project includes a complete, production-grade monitoring stack built on **Prometheus** and **Grafana**. This stack provides real-time observability into the API's performance, scraping key metrics like request latency, error rates, and traffic volume.

### How It Works

1.  **Application Instrumentation:** The FastAPI application uses `prometheus-fastapi-instrumentator` to automatically expose a `/metrics` endpoint with detailed performance data.
2.  **Monitoring Stack:** The `kube-prometheus-stack` is deployed via **Helm** into its own `monitoring` namespace.
3.  **Service Discovery:** A `ServiceMonitor` resource is deployed. This is the key component that enables declarative, automated service discovery.
      * The `ServiceMonitor` is configured to watch the `default` namespace for any `Service` that has the label `app: model-api`.
      * Once it finds our service, it instructs Prometheus to automatically begin scraping metrics from the port named `http` at a 15-second interval.

This setup means monitoring is "zero-touch"—any new pod added to the deployment will be automatically discovered and monitored by Prometheus.

### Visualizing the Metrics (Local Demo)

1.  **Install the Monitoring Stack:**

    ```bash
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update
    helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
    ```

2.  **Get the Grafana Admin Password:**

    ```bash
    kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode
    ```

3.  **Access the Grafana Dashboard:**
    Run this command to open a secure tunnel to the Grafana service:

    ```bash
    kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
    ```

    Access the dashboard in your browser at `http://localhost:3000`.

      * **Username:** `admin`
      * **Password:** (Paste the password you retrieved)

4.  **Generate Traffic & Build a Panel:**
    With your API running and forwarded (on port `8080`), use a `curl` loop to generate traffic. In Grafana, create a new panel with the following PromQL query and set the time range to **"Last 5 minutes"**:

    ```promql
    rate(http_requests_total{job="serviceMonitor/default/model-api-servicemonitor/0"}[1m])
    ```

    You will see a live graph of your API's request rate.
