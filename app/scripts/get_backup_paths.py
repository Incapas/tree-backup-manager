import json
import logging
from pathlib import Path
from typing import Any, Mapping

from scripts.path_utils import normalize_path

# Logger for this module to track loading operations.
logger = logging.getLogger(__name__)

# Absolute path to the JSON file containing the backup path configuration.
BACKUP_PATHS: Path = Path(__file__).resolve().parents[1] / "config" / "backup_paths.json"


class GetBackupPaths:
    """Charge et expose la configuration des chemins de sauvegarde."""

    def __init__(self) -> None:
        """Initialise l'instance avec la configuration chargée."""
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
        
        # Normalise tous les chemins de la configuration pour la plateforme courante.
        self._normalize_configuration_paths(paths)
        
        return paths

    def _normalize_configuration_paths(self, paths: dict) -> None:
        """Normalise tous les chemins présents dans la configuration pour la plateforme actuelle.

        Convertit les chemins au format Windows ou POSIX vers le format de la plateforme
        d'exécution courante en utilisant la fonction de normalisation.

        Args:
            paths (dict): La configuration contenant des clés "src" et "dest" à normaliser.
        """
        # Itère sur chaque clé de configuration (primary_backup_path, secondary_backup_path, etc.)
        for config_key, config_value in paths.items():
            # Vérifie que la valeur est un dictionnaire contenant "src" et "dest".
            if not isinstance(config_value, dict):
                continue

            # Normalise le chemin source s'il est présent.
            if "src" in config_value and isinstance(config_value["src"], str):
                normalized_source = normalize_path(config_value["src"])
                if normalized_source:
                    # Remplace la chaîne par un objet Path normalisé.
                    config_value["src"] = normalized_source
                    logger.debug("Chemin source normalisé pour '%s' : %s", config_key, normalized_source)

            # Normalise le chemin destination s'il est présent.
            if "dest" in config_value and isinstance(config_value["dest"], str):
                normalized_dest = normalize_path(config_value["dest"])
                if normalized_dest:
                    # Remplace la chaîne par un objet Path normalisé.
                    config_value["dest"] = normalized_dest
                    logger.debug("Chemin destination normalisé pour '%s' : %s", config_key, normalized_dest)
