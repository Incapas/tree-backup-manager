import logging
import shutil
from typing import Any, Mapping

# Logger spécifique à ce module pour tracer les événements de sauvegarde.
logger = logging.getLogger(__name__)


class BackupManager:
    """Gère les opérations de sauvegarde des fichiers et dossiers."""

    def __init__(self, backup_paths: Mapping[str, Any]) -> None:
        """Initialise l’instance avec la configuration des chemins de sauvegarde.

        Args:
            backup_paths (Mapping[str, Any]): La configuration des chemins de sauvegarde.
        """
        # Conserve la configuration complète fournie par le chargeur.
        self.backup_paths = backup_paths
        # Extrait la configuration du chemin principal pour une utilisation directe.
        self.primary_backup = backup_paths.get("primary_backup_path", {})
        # Extrait la configuration du chemin secondaire pour la sauvegarde de secours.
        self.secondary_backup = backup_paths.get("secondary_backup_path", {})

    def perform_backup(self) -> None:
        """Effectue la sauvegarde en essayant d’abord le chemin principal."""
        # Récupère le chemin source du backup principal à partir de la configuration.
        primary_source = self.primary_backup.get("src")
        # Récupère la destination du backup principal.
        primary_destination = self.primary_backup.get("dest")
        # Récupère le chemin source du backup secondaire.
        secondary_source = self.secondary_backup.get("src")
        # Récupère la destination du backup secondaire.
        secondary_destination = self.secondary_backup.get("dest")

        # Tente la sauvegarde via le chemin principal si les deux informations sont présentes.
        if primary_source and primary_destination:
            try:
                # Exécute la copie vers le chemin principal.
                self._copy_backup(primary_source, primary_destination, "primary")
                return
            except (FileNotFoundError, NotADirectoryError, PermissionError) as erreur:
                # Enregistre un avertissement si le chemin principal est indisponible.
                logger.warning(
                    "Le chemin principal est indisponible, utilisation du chemin secondaire : %s",
                    erreur,
                )

        # Si le chemin principal est indisponible, bascule automatiquement vers le secondaire.
        if secondary_source and secondary_destination:
            # Exécute la copie vers le chemin secondaire.
            self._copy_backup(secondary_source, secondary_destination, "secondary")
            return

        # Signale l'absence de chemin de sauvegarde exploitable.
        logger.error("Aucun chemin de sauvegarde disponible.")

    def _copy_backup(self, source: str, destination: str, label: str) -> None:
        """Copie un dossier vers une destination en utilisant le chemin fourni."""
        # Copie le contenu du dossier source vers la destination demandée.
        shutil.copytree(source, destination, dirs_exist_ok=True)
        # Enregistre un message de succès avec l'étiquette du chemin utilisé.
        logger.info("Sauvegarde réussie via %s : %s -> %s", label, source, destination)
