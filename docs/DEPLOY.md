# VayuBus — EKS Deployment Guide

## Prerequisites

| Tool    | Version | Install |
|---------|---------|---------|
| AWS CLI | ≥ 2.x   | https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html |
| Docker  | ≥ 24.x  | https://docs.docker.com/get-docker/ |
| kubectl | ≥ 1.28  | https://kubernetes.io/docs/tasks/tools/ |
| eksctl  | ≥ 0.175 | https://eksctl.io/installation/ |
| Helm    | ≥ 3.x   | https://helm.sh/docs/intro/install/ |

---

## Step 1 — Create EKS Cluster

```bash
eksctl create cluster \
  --name vayubus-eks-cluster \
  --region ap-south-1 \
  --nodegroup-name workers \
  --node-type t3.medium \
  --nodes 3 --nodes-min 2 --nodes-max 5 \
  --managed \
  --zones ap-south-1a,ap-south-1b,ap-south-1c
```

---

## Step 2 — Install AWS Load Balancer Controller

```bash
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy.json

aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam_policy.json

eksctl create iamserviceaccount \
  --cluster=vayubus-eks-cluster \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --attach-policy-arn=arn:aws:iam::ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve

helm repo add eks https://aws.github.io/eks-charts && helm repo update

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=vayubus-eks-cluster \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

---

## Step 3 — Deploy with deploy.sh

```bash
chmod +x deploy.sh
./deploy.sh \
  --account 123456789012 \
  --cluster vayubus-eks-cluster \
  --region  ap-south-1
```

---

## Step 4 — Verify

```bash
# Pods should be Running
kubectl get pods -n vayubus

# Get ALB URL (wait ~2 min)
kubectl get ingress -n vayubus
```

---

## Common Operations

```bash
# Scale
kubectl scale deployment vayubus -n vayubus --replicas=5

# Restart (zero-downtime)
kubectl rollout restart deployment/vayubus -n vayubus

# Rollback
kubectl rollout undo deployment/vayubus -n vayubus

# Logs
kubectl logs -l app=vayubus -n vayubus --tail=50

# Delete all
kubectl delete namespace vayubus
```
