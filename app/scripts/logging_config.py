import logging
from pathlib import Path


def setup_logging() -> None:
    """Configure le système de logging pour écrire dans logs/app.log."""
    # Détermine le dossier de logs à partir du chemin du module actuel.
    log_dir = Path(__file__).resolve().parents[1] / "logs"
    # Crée le dossier de logs s'il n'existe pas déjà.
    log_dir.mkdir(parents=True, exist_ok=True)
    # Définit le fichier de logs principal.
    log_file = log_dir / "app.log"

    # Formate chaque message avec la date, le niveau et le nom du module.
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Récupère le logger racine pour y appliquer la configuration globale.
    root_logger = logging.getLogger()

    # Supprime les anciens gestionnaires pour éviter les doublons à chaque exécution.
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)
        handler.close()

    # Crée un gestionnaire de log vers le fichier app.log.
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    # Enregistre tous les niveaux de log dans le fichier.
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Crée un gestionnaire de log vers la sortie standard.
    stream_handler = logging.StreamHandler()
    # Affiche les messages de niveau INFO et supérieurs dans la console.
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Définit le niveau minimum global du système de logging.
    root_logger.setLevel(logging.DEBUG)
    # Ajoute les deux gestionnaires au logger racine.
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)
