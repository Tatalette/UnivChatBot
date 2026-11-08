<?php
/**
 * URL du service FastAPI depuis le conteneur GLPI.
 * Les deux sont sur le réseau Docker `glpi-net`, donc `chatbot` est résolu
 * automatiquement par Docker DNS.
 */
return [
    'api_url' => getenv('CHATBOT_API_URL') ?: 'http://chatbot:8000',
];