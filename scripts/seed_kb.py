"""Insère quelques Q/R de démo dans la base de connaissances."""
from chatbot.db.session import SessionLocal
from chatbot.services import kb

SEED = [
    (
        "Mon VPN ne se connecte pas",
        "Vérifiez votre connexion Internet puis relancez le client GlobalProtect. "
        "Si le problème persiste, contactez le support avec le code d'erreur affiché.",
    ),
    (
        "Comment changer mon mot de passe ENT ?",
        "Rendez-vous sur https://ent.univ-corse.fr, cliquez sur 'Mot de passe oublié' "
        "et suivez la procédure. Le mot de passe doit contenir au moins 12 caractères.",
    ),
    (
        "Imprimante du bâtiment Desanti ne fonctionne pas",
        "Vérifiez que vous êtes sur le réseau EDUROC. Si l'imprimante reste hors ligne, "
        "ouvrez un ticket avec le numéro de l'imprimante.",
    ),
    (
        "Comment accéder au WiFi Eduroam ?",
        "Sélectionnez le réseau Eduroam, identifiez-vous avec votre login ENT et votre "
        "mot de passe. Acceptez le certificat.",
    ),
    (
        "Réinitialiser mon mot de passe universitaire",
        "Utilisez le portail de réinitialisation à l'adresse https://mdp.univ-corse.fr. "
        "Une confirmation par SMS ou mail vous sera demandée.",
    ),
]


def main() -> None:
    with SessionLocal() as db:
        for q, a in SEED:
            kb.insert(db, question=q, answer=a, source="manual")
            print(f"inséré : {q}")
    print(f"\n{len(SEED)} entrées ajoutées.")


if __name__ == "__main__":
    main()