#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

echo "[bootstrap] Updating apt..."
apt-get update -y

echo "[bootstrap] Installing base tools..."
apt-get install -y ca-certificates curl gnupg lsb-release git jq

echo "[bootstrap] Installing Docker..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

ARCH="$(dpkg --print-architecture)"
CODENAME="$(. /etc/os-release && echo "$VERSION_CODENAME")"

echo "deb [arch=${ARCH} signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu ${CODENAME} stable" \
  > /etc/apt/sources.list.d/docker.list

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "[bootstrap] Enabling Docker..."
systemctl enable --now docker

echo "[bootstrap] Adding vagrant user to docker group..."
usermod -aG docker vagrant || true

echo "[bootstrap] Done. Run 'vagrant reload' if docker needs sudo."
