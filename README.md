# Nirmaan Suraksha - DevOps Project (v1)

This is an end-to-end DevOps project implementing a secure and scalable Todo application with modern DevOps practices and security measures.

## Project Overview

Nirmaan Suraksha is a Flask-based Todo application with user authentication, containerized using Docker, and deployed on Kubernetes using KIND (Kubernetes IN Docker). The project implements a complete CI/CD pipeline with security scanning, policy enforcement, and automated deployment.

## Features

### Application Features
- User registration and authentication
- Todo task management (Add, Complete, Delete tasks)
- Session management
- SQLite database for data persistence

### DevOps Features
- Containerization with Docker
- CI/CD pipeline using Jenkins
- SonarQube for code quality analysis
- Trivy for container security scanning
- Artifactory for container registry
- Kubernetes deployment using KIND
- Kyverno policies for security enforcement
- Cloud Provider KIND for local load balancer simulation
- Nginx Ingress Controller

## Tech Stack

- **Backend**: Python 3.9, Flask 3.1.0
- **Database**: SQLite3
- **Container**: Docker (Alpine-based)
- **CI/CD**: Jenkins
- **Security**: 
  - Trivy (Container scanning)
  - Kyverno (Policy enforcement)
  - SonarQube (Code quality)
- **Container Registry**: JFrog Artifactory
- **Orchestration**: Kubernetes (KIND)
- **Ingress**: Nginx Ingress Controller

## Project Structure

```
python-todoapp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
├── Jenkinsfile          # CI/CD pipeline
├── k8s/                 # Kubernetes manifests
├── kyverno-policies/    # Security policies
├── kind-cluster-setup/  # Local cluster setup
├── templates/           # HTML templates
└── static/             # Static assets
```

## Security Features

1. **Container Security**:
   - Non-root user execution
   - Resource limits enforcement
   - Latest tag prevention
   - Regular security scanning

2. **Application Security**:
   - User authentication
   - Session management
   - SQL injection prevention
   - Input validation

3. **Infrastructure Security**:
   - Kyverno policies enforcement
   - Resource limits
   - Security context constraints
   - Health checks

## Setup Instructions

1. **Prerequisites**:
   - Docker
   - KIND
   - Go (for cloud-provider-kind)
   - Jenkins
   - SonarQube
   - JFrog Artifactory

2. **Local Development**:
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd python-todoapp

   # Install dependencies
   pip install -r requirements.txt

   # Run the application
   python app.py
   ```

3. **Container Build**:
   ```bash
   docker build -t todo-app:latest .
   ```

4. **KIND Cluster Setup**:
   ```bash
   # Create cluster
   kind create cluster --name local-cluster

   # Install cloud-provider-kind
   go install sigs.k8s.io/cloud-provider-kind@latest

   # Setup ingress controller
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
   ```

## CI/CD Pipeline

The Jenkins pipeline includes the following stages:
1. Code checkout
2. SonarQube analysis
3. Docker image build
4. Trivy security scan
5. Push to Artifactory
6. Deploy to KIND cluster

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
