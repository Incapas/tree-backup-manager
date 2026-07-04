import json
import logging
from pathlib import Path
from typing import Any, Mapping

# Logger spécifique à ce module pour suivre les opérations de chargement.
logger = logging.getLogger(__name__)

# Chemin absolu vers le fichier JSON contenant la configuration des chemins de sauvegarde.
BACKUP_PATHS: Path = Path(__file__).resolve().parents[1] / "config" / "backup_paths.json"


class GetBackupPaths:
    """Charge et expose la configuration des chemins de sauvegarde."""

    def __init__(self) -> None:
        """Initialise l’instance avec la configuration chargée."""
        # Charge immédiatement la configuration au moment de l'instanciation.
        self.backup_paths: Mapping[str, Any] = self.load_backup_paths()

    def load_backup_paths(self) -> Mapping[str, Any]:
        """Charge la configuration JSON depuis le fichier de chemins de sauvegarde.

        Returns:
            Mapping[str, Any]: La configuration chargée sous forme de mapping.

        Raises:
            ValueError: Si le contenu JSON n’est pas un objet de type dictionnaire.
        """
        try:
            # Tente d'ouvrir directement le fichier JSON sans vérification préalable.
            with BACKUP_PATHS.open(mode="r", encoding="utf-8") as fichier:
                # Charge les données JSON lues depuis le fichier.
                paths: Any = json.load(fichier)
        except FileNotFoundError:
            # Journalise une erreur si le fichier de configuration est absent.
            logger.error("Le fichier de chemins de sauvegarde est introuvable : %s", BACKUP_PATHS)
            return {}
        except json.JSONDecodeError as erreur:
            # Journalise une erreur si le contenu JSON est invalide.
            logger.error("Le fichier de chemins de sauvegarde contient un JSON invalide : %s", erreur)
            return {}

        # Vérifie que la configuration chargée est bien un objet JSON de type dictionnaire.
        if not isinstance(paths, dict):
            # Journalise une erreur si la structure n'est pas attendue.
            logger.error("La configuration de sauvegarde n'est pas un objet JSON valide.")
            raise ValueError("La configuration de sauvegarde doit être un objet JSON valide.")

        # Enregistre un message de succès si la configuration est valide.
        logger.info("Configuration des chemins de sauvegarde chargée avec succès.")
        return paths
