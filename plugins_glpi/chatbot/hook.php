<?php

function plugin_chatbot_install(): bool
{
    // Pas de table à créer (l'état vit dans le FastAPI / PostgreSQL)
    return true;
}

function plugin_chatbot_uninstall(): bool
{
    return true;
}