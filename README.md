# pdf-platform
a microservice-based PDF platform
Repo layout
pdf-platform/
├─ infra/
│ ├─ k8s/
│ │ ├─ api-deployment.yaml
│ │ ├─ worker-deployment.yaml
│ │ ├─ minio-deployment.yaml
│ │ └─ postgres-pvc.yaml
│ └─ helm/ (optional Helm charts)
├─ services/
│ ├─ api/
│ │ ├─ app/
│ │ │ ├─ main.py
│ │ │ ├─ api/
│ │ │ │ ├─ routes.py
│ │ │ │ └─ jobs.py
│ │ │ ├─ models.py
│ │ │ └─ utils.py
│ │ ├─ Dockerfile
│ │ └─ requirements.txt
│ └─ worker/
│ ├─ worker.py
│ ├─ Dockerfile
│ └─ requirements.txt
├─ frontend/
│ ├─ web/
│ │ ├─ src/
│ │ │ ├─ App.jsx
│ │ │ ├─ components/Upload.jsx
│ │ │ └─ components/Viewer.jsx
│ │ ├─ package.json
│ │ └─ Dockerfile
├─ docker-compose.yml
├─ .github/workflows/ci-cd.yml
└─ README.md
