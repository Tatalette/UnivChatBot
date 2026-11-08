<?php

/**
 * Appel HTTP vers le service chatbot FastAPI.
 * Retourne le JSON décodé ou ['_error' => '...'] en cas de problème.
 */
function chatbot_api_call(string $path, array $payload): array
{
    $config = require __DIR__ . '/config.php';
    $url = rtrim($config['api_url'], '/') . $path;

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => json_encode($payload, JSON_UNESCAPED_UNICODE),
        CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 130,  // > timeout LLM
        CURLOPT_CONNECTTIMEOUT => 5,
    ]);

    $response  = curl_exec($ch);
    $http_code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err       = curl_error($ch);
    curl_close($ch);

    if ($response === false) {
        return ['_error' => 'Connexion impossible au chatbot : ' . $err];
    }

    $data = json_decode($response, true);
    if (!is_array($data)) {
        return ['_error' => 'Réponse non-JSON du chatbot (HTTP ' . $http_code . ')'];
    }
    if ($http_code >= 400) {
        return ['_error' => $data['detail'] ?? ('HTTP ' . $http_code)];
    }
    return $data;
}

/**
 * Réponse JSON standardisée + fin d'exécution.
 */
function chatbot_json_response(array $data, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

/**
 * Vérifie session + CSRF dans les handlers AJAX.
 */
function chatbot_require_auth(): int
{
    if (!Session::getLoginUserID()) {
        chatbot_json_response(['error' => 'unauthenticated'], 401);
    }
    if (!Session::validateCSRF($_POST)) {
        chatbot_json_response(['error' => 'csrf'], 403);
    }
    return (int) Session::getLoginUserID();
}