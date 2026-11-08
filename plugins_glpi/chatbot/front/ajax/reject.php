<?php

include('../../../inc/includes.php');
require_once __DIR__ . '/../inc/helpers.php';

chatbot_require_auth();

$convId = (int) ($_POST['conversation_id'] ?? 0);
if ($convId <= 0) {
    chatbot_json_response(['error' => 'conversation_id manquant'], 400);
}

$data = chatbot_api_call('/reject', ['conversation_id' => $convId]);

if (isset($data['_error'])) {
    chatbot_json_response(['error' => $data['_error']], 502);
}

chatbot_json_response($data);