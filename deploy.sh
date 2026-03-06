#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
#  VayuBus — Build & Deploy to EKS
#
#  Usage:
#    ./deploy.sh --account 123456789012 --cluster my-cluster
#
#  Options:
#    --region     AWS region           (default: ap-south-1)
#    --account    AWS Account ID       (required)
#    --cluster    EKS cluster name     (required)
#    --tag        Image tag            (default: git short SHA)
#    --skip-build Skip Docker build
#    --dry-run    Print without applying
# ═══════════════════════════════════════════════════════════
set -euo pipefail

R='\033[0;31m'; G='\033[0;32m'; Y='\033[1;33m'; C='\033[0;36m'; B='\033[1m'; X='\033[0m'
log()  { echo -e "${C}[INFO]${X}  $*"; }
ok()   { echo -e "${G}[OK]${X}    $*"; }
warn() { echo -e "${Y}[WARN]${X}  $*"; }
err()  { echo -e "${R}[ERROR]${X} $*"; exit 1; }
sep()  { echo -e "${B}────────────────────────────────────────${X}"; }

AWS_REGION="ap-south-1"
AWS_ACCOUNT_ID=""
CLUSTER_NAME=""
IMAGE_TAG=$(git rev-parse --short HEAD 2>/dev/null || echo "1.0.0")
APP_NAME="vayubus"
NAMESPACE="vayubus"
SKIP_BUILD=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --region)    AWS_REGION="$2";     shift 2 ;;
    --account)   AWS_ACCOUNT_ID="$2"; shift 2 ;;
    --cluster)   CLUSTER_NAME="$2";   shift 2 ;;
    --tag)       IMAGE_TAG="$2";      shift 2 ;;
    --skip-build) SKIP_BUILD=true;    shift   ;;
    --dry-run)   DRY_RUN=true;        shift   ;;
    *) err "Unknown option: $1" ;;
  esac
done

[[ -z "$AWS_ACCOUNT_ID" ]] && err "--account is required"
[[ -z "$CLUSTER_NAME"   ]] && err "--cluster is required"

ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
IMAGE_FULL="${ECR_REGISTRY}/${APP_NAME}:${IMAGE_TAG}"
IMAGE_LATEST="${ECR_REGISTRY}/${APP_NAME}:latest"

sep; log "VayuBus EKS Deploy"
sep
log "Region:   ${AWS_REGION}"
log "Account:  ${AWS_ACCOUNT_ID}"
log "Cluster:  ${CLUSTER_NAME}"
log "Image:    ${IMAGE_FULL}"
log "Dry-run:  ${DRY_RUN}"
sep

for cmd in aws docker kubectl; do
  command -v "$cmd" &>/dev/null || err "Missing: $cmd"
done
ok "Tools check passed"

sep; log "STEP 1 — ECR Login"
aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$ECR_REGISTRY"
ok "ECR authenticated"

sep; log "STEP 2 — Ensure ECR repository"
aws ecr describe-repositories --repository-names "$APP_NAME" --region "$AWS_REGION" &>/dev/null \
  || aws ecr create-repository --repository-name "$APP_NAME" --region "$AWS_REGION" \
       --image-scanning-configuration scanOnPush=true \
       --tags Key=App,Value=vayubus
ok "ECR repository ready"

if [ "$SKIP_BUILD" = false ]; then
  sep; log "STEP 3 — Docker Build & Push"
  docker build --platform linux/amd64 \
    -t "${IMAGE_FULL}" -t "${IMAGE_LATEST}" .
  docker push "${IMAGE_FULL}"
  docker push "${IMAGE_LATEST}"
  ok "Image pushed: ${IMAGE_FULL}"
else
  warn "Skipping build (--skip-build)"
fi

sep; log "STEP 4 — Update kubeconfig"
aws eks update-kubeconfig --region "$AWS_REGION" --name "$CLUSTER_NAME"
ok "kubeconfig updated"

sep; log "STEP 5 — Patch & Apply manifests"
sed -i "s|YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/vayubus:1.0.0|${IMAGE_FULL}|g" \
  k8s/02-deployment.yaml

KCMD="kubectl apply -f"
[ "$DRY_RUN" = true ] && KCMD="kubectl apply --dry-run=client -f" && warn "DRY RUN"

$KCMD k8s/
ok "Manifests applied"

if [ "$DRY_RUN" = false ]; then
  sep; log "STEP 6 — Wait for rollout"
  kubectl rollout status deployment/${APP_NAME} -n "$NAMESPACE" --timeout=300s
  ok "Rollout complete"

  sep; log "STEP 7 — Status"
  kubectl get pods    -n "$NAMESPACE" -l app=${APP_NAME}
  kubectl get svc     -n "$NAMESPACE"
  kubectl get ingress -n "$NAMESPACE"
  sep

  ALB=$(kubectl get ingress vayubus-ingress -n "$NAMESPACE" \
    -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null || echo "provisioning...")
  ok "🚌 VayuBus deployed!"
  log "URL: http://${ALB}"
fi
