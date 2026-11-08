<?php

use Glpi\Plugin\Hooks;

define('PLUGIN_CHATBOT_VERSION', '0.1.0');
define('PLUGIN_CHATBOT_MIN_GLPI', '10.0.0');
define('PLUGIN_CHATBOT_MAX_GLPI', '10.1.99');

require_once __DIR__ . '/inc/menu.class.php';

function plugin_init_chatbot(): void
{
    global $PLUGIN_HOOKS;

    $PLUGIN_HOOKS['csrf_compliant']['chatbot'] = true;

    if (Session::getLoginUserID()) {
        // Menu visible dans la section "Self-Service"
        $PLUGIN_HOOKS['menu_toadd']['chatbot'] = [
            'helpdesk' => 'PluginChatbotMenu',
        ];
    }
}

function plugin_version_chatbot(): array
{
    return [
        'name'           => 'Chatbot IA',
        'version'        => PLUGIN_CHATBOT_VERSION,
        'author'         => 'Binôme M2',
        'license'        => 'GPLv2+',
        'homepage'       => '',
        'requirements'   => [
            'glpi' => [
                'min' => PLUGIN_CHATBOT_MIN_GLPI,
                'max' => PLUGIN_CHATBOT_MAX_GLPI,
            ],
        ],
    ];
}

function plugin_chatbot_check_prerequisites(): bool
{
    return true;
}

function plugin_chatbot_check_config($verbose = false): bool
{
    return true;
}