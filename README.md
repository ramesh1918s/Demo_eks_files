# 🚌 VayuBus — Smart Bus Booking

> A production-grade static bus seat booking application with full EKS deployment support.

---

## File Structure

```
vayubus/
│
├── src/                          # Application source code
│   ├── index.html                # Main HTML entry point
│   │
│   ├── css/                      # Stylesheets (loaded in order)
│   │   ├── reset.css             # CSS reset + utility classes
│   │   ├── variables.css         # Design tokens (colours, spacing, radius)
│   │   ├── layout.css            # Header, main grid, bus cards, route map
│   │   ├── components.css        # Buttons, toast, seat legend, controls
│   │   ├── seats.css             # Bus chassis + individual seat styles
│   │   ├── summary.css           # Right panel: summary, passenger form
│   │   ├── modal.css             # Confirmation overlay & ticket
│   │   └── responsive.css        # Media queries (tablet, mobile)
│   │
│   ├── js/                       # JavaScript modules (loaded in order)
│   │   ├── data.js               # Static data: buses, routes, cities
│   │   ├── utils.js              # Shared helpers: format, toast, type helpers
│   │   ├── routeMap.js           # Canvas route renderer + stop timeline
│   │   ├── seatMap.js            # Seat map builder + toggle/selection logic
│   │   ├── summary.js            # Summary panel + passenger form builder
│   │   └── app.js                # Main controller — orchestrates all modules
│   │
│   └── assets/
│       └── logo.svg              # Standalone SVG bus logo
│
├── k8s/                          # Kubernetes manifests
│   ├── 00-namespace.yaml         # Namespace: vayubus
│   ├── 01-configmap.yaml         # App config (env vars)
│   ├── 02-deployment.yaml        # Deployment: 3 replicas, rolling update
│   ├── 03-service.yaml           # ClusterIP service (port 80 → 8080)
│   ├── 04-ingress.yaml           # AWS ALB Ingress (internet-facing)
│   └── 05-hpa-sa-pdb.yaml        # HPA + ServiceAccount + PodDisruptionBudget
│
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions CI/CD pipeline
│
├── docs/
│   └── DEPLOY.md                 # Step-by-step EKS deployment guide
│
├── Dockerfile                    # nginx:alpine, non-root, port 8080
├── nginx.conf                    # Custom nginx with /health endpoint
├── deploy.sh                     # One-command build + deploy script
├── .dockerignore                 # Docker build exclusions
├── .gitignore                    # Git exclusions
└── README.md                     # This file
```

---

## Features

| Feature | Description |
|---------|-------------|
| 🚌 Unique Logo | Custom SVG bus icon with speed lines & headlight glow |
| 🗺️ Route Map | Canvas-drawn route with stop timeline & city labels |
| 🎨 Seat Types | Male (Blue) / Female (Pink) / Child (Amber) with distinct colours |
| 🔢 Seat Counter | +/- control (1–5 seats) with live enforcement |
| 👥 Passenger Form | Per-seat passenger details with ID proof selection |
| 💰 Smart Pricing | Children get 40% discount automatically |
| ✅ PNR Confirmation | Animated booking confirmation with generated PNR |
| 📱 Responsive | Works on mobile, tablet, and desktop |

---

## Quick Start

### Run locally
```bash
# Any static file server works
python3 -m http.server 3000 --directory src
# Open: http://localhost:3000
```

### Docker
```bash
docker build -t vayubus .
docker run -p 8080:8080 vayubus
# Open: http://localhost:8080
```

### Deploy to EKS
```bash
chmod +x deploy.sh
./deploy.sh \
  --account YOUR_AWS_ACCOUNT_ID \
  --cluster YOUR_EKS_CLUSTER \
  --region  ap-south-1
```

See `docs/DEPLOY.md` for full step-by-step EKS setup including cluster creation and ALB controller installation.

---

## Architecture

```
Internet
   │
   ▼
AWS ALB (internet-facing, HTTPS)
   │
ClusterIP Service (port 80 → 8080)
   │
Pods ×3 — nginx serving static files
   │
HPA: auto-scale 2–10 pods on CPU/Memory
PDB: min 1 pod always available
```

---

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JS (no framework, no build step needed)
- **Server**:   nginx 1.25 Alpine
- **Container**: Docker (non-root, port 8080)
- **Orchestration**: Kubernetes on AWS EKS
- **CI/CD**: GitHub Actions → ECR → EKS
- **Fonts**: Syne, Outfit, JetBrains Mono (Google Fonts)
