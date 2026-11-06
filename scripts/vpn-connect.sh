#!/usr/bin/env bash
# Connexion VPN Université de Corse (GlobalProtect) avec HIP report.
set -euo pipefail

VPN_HOST="${VPN_HOST:-vpn.univ-corse.fr}"
HIP_WRAPPER="${HIP_WRAPPER:-./hipreport.sh}"

if [[ ! -x "$HIP_WRAPPER" ]]; then
  echo "ERREUR: $HIP_WRAPPER introuvable ou non exécutable." >&2
  echo "Récupère hipreport.sh (ex: https://github.com/steven-murray/hipreport-openconnect)" >&2
  exit 1
fi

echo "Connexion à $VPN_HOST ..."
sudo openconnect --protocol=gp --csd-wrapper="$HIP_WRAPPER" "$VPN_HOST"

# Après connexion, depuis un autre terminal :
#   ip route get 193.48.31.6
#   curl -v --max-time 10 telnet://193.48.31.6:32297