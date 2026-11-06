#!/usr/bin/env bash
set -euo pipefail

API="${API:-http://localhost:8000}"

echo "=== 1. health ==="
curl -s "$API/health" | jq

echo
echo "=== 2. question connue (doit matcher la KB) ==="
curl -s -X POST "$API/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Mon VPN ne se connecte pas","glpi_user_id":1}' | jq

echo
echo "=== 3. question nouvelle (web + LLM) ==="
RESP=$(curl -s -X POST "$API/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Comment réserver une salle de réunion ?","glpi_user_id":1}')
echo "$RESP" | jq
CONV_ID=$(echo "$RESP" | jq -r '.conversation_id')

echo
echo "=== 4. validation (ajout à la KB) ==="
curl -s -X POST "$API/validate" \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\":$CONV_ID}" | jq

echo
echo "=== 5. nouvelle question + rejet (création ticket GLPI) ==="
RESP2=$(curl -s -X POST "$API/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"Le projecteur de l amphi Fesch est en panne","glpi_user_id":1}')
echo "$RESP2" | jq
CONV2=$(echo "$RESP2" | jq -r '.conversation_id')

curl -s -X POST "$API/reject" \
  -H "Content-Type: application/json" \
  -d "{\"conversation_id\":$CONV2}" | jq