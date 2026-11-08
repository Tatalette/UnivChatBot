<?php

include('../../../inc/includes.php');
require_once __DIR__ . '/../inc/helpers.php';

$userId = chatbot_require_auth();

$question = trim($_POST['question'] ?? '');
if ($question === '') {
    chatbot_json_response(['error' => 'question vide'], 400);
}

// On utilise l'ID GLPI réel de la session, pas le paramètre POST
$data = chatbot_api_call('/ask', [
    'question'     => $question,
    'glpi_user_id' => $userId,
]);

if (isset($data['_error'])) {
    chatbot_json_response(['error' => $data['_error']], 502);
}

chatbot_json_response($data);