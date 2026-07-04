import logging

from scripts.backup_manager import BackupManager
from scripts.get_backup_paths import GetBackupPaths
from scripts.logging_config import setup_logging


def main() -> None:
    """Exécute la logique de sauvegarde à partir du point d'entrée principal."""
    # Configure le système de logging avant toute opération importante.
    setup_logging()
    # Récupère le logger associé à ce module.
    logger = logging.getLogger(__name__)
    # Journalise le démarrage du programme.
    logger.info("Démarrage du programme de sauvegarde.")

    # Charge la configuration depuis le fichier JSON.
    loader = GetBackupPaths()
    # Signale que la configuration a bien été chargée.
    logger.info("Configuration chargée depuis le fichier de paramètres.")

    # Crée le gestionnaire de sauvegarde avec la configuration chargée.
    manager = BackupManager(loader.backup_paths)
    # Journalise le lancement de la procédure de sauvegarde.
    logger.info("Lancement de la procédure de sauvegarde.")
    # Exécute la sauvegarde.
    manager.perform_backup()
    # Journalise la fin de la procédure.
    logger.info("Fin de la procédure de sauvegarde.")


if __name__ == "__main__":
    main()
