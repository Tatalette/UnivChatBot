<?php

include('../../../inc/includes.php');

if (!Session::getLoginUserID()) {
    Html::redirect($CFG_GLPI['root_doc'] . '/index.php');
}

Html::header(
    __('Chatbot IA', 'chatbot'),
    $_SERVER['PHP_SELF'],
    'helpdesk',
    'PluginChatbotMenu'
);

TemplateRenderer::getInstance()->display('@chatbot/chatbot.html.twig', [
    'csrf_token'   => Session::getNewCSRFToken(),
    'ajax_url'     => $CFG_GLPI['root_doc'] . '/plugins/chatbot/ajax',
    'glpi_user_id' => (int) Session::getLoginUserID(),
]);

Html::footer();