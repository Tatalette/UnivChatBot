<?php

class PluginChatbotMenu extends CommonGLPI
{
    static $rightname = 'ticket';  // droit ouvert aux utilisateurs self-service

    static function getMenuName(): string
    {
        return __('Chatbot IA', 'chatbot');
    }

    static function getMenuContent(): array
    {
        return [
            'title' => self::getMenuName(),
            'page'  => '/plugins/chatbot/front/chatbot.php',
            'icon'  => 'ti ti-robot',
        ];
    }
}