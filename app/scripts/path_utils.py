import logging
from pathlib import Path, PureWindowsPath, PurePosixPath
from typing import Optional

# Logger spécifique à ce module pour tracer les conversions de chemins.
logger = logging.getLogger(__name__)


def normalize_path(path_str: str) -> Optional[Path]:
    """Normalise un chemin de chaîne de caractères en objet Path multiplateforme.

    Cette fonction détecte si le chemin fourni est au format Windows (ex: "D:\\...")
    ou au format POSIX (ex: "/home/user/...") et le convertit en un objet Path
    compatible avec la plateforme d'exécution actuelle.

    Args:
        path_str (str): Le chemin sous forme de chaîne de caractères à normaliser.

    Returns:
        Optional[Path]: Un objet Path normalisé, ou None si le chemin est vide ou invalide.

    Raises:
        ValueError: Si le chemin fourni ne peut pas être interprété correctement.
    """
    # Vérifie que le chemin n'est pas vide ou constitué uniquement d'espaces.
    if not path_str or not path_str.strip():
        logger.debug("Chemin vide ou invalide ignoré.")
        return None

    # Nettoie le chemin en supprimant les espaces inutiles.
    cleaned_path = path_str.strip()

    # Détecte si le chemin est au format Windows (contient une lettre suivie de ":")
    # Exemple: "D:\", "C:\Users\...", "\\server\share"
    if _is_windows_path(cleaned_path):
        try:
            # Convertit le chemin Windows en objet PureWindowsPath pour le parser.
            windows_path = PureWindowsPath(cleaned_path)
            # Convertit ensuite en Path natif de la plateforme courante.
            converted_path = Path(windows_path.as_posix())
            logger.debug("Chemin Windows '%s' converti en : %s", cleaned_path, converted_path)
            return converted_path
        except ValueError as error:
            # Lève une exception si le chemin Windows ne peut pas être parsé.
            logger.error("Impossible de parser le chemin Windows '%s' : %s", cleaned_path, error)
            raise ValueError(f"Chemin Windows invalide : {cleaned_path}") from error
    else:
        # Traite le chemin comme un chemin POSIX standard.
        try:
            # Convertit la chaîne en objet Path natif de la plateforme.
            posix_path = Path(cleaned_path)
            logger.debug("Chemin POSIX normalisé : %s", posix_path)
            return posix_path
        except ValueError as error:
            # Lève une exception si le chemin POSIX ne peut pas être parsé.
            logger.error("Impossible de parser le chemin POSIX '%s' : %s", cleaned_path, error)
            raise ValueError(f"Chemin POSIX invalide : {cleaned_path}") from error


def _is_windows_path(path: str) -> bool:
    """Détecte si une chaîne de caractères représente un chemin au format Windows.

    Identifie les formats Windows courants:
    - Chemins locaux: "C:\", "D:\Users\..."
    - Chemins UNC: "\\server\share", "\\\\server\\share"

    Args:
        path (str): La chaîne de caractères à analyser.

    Returns:
        bool: True si le chemin détecté est au format Windows, False sinon.
    """
    # Vérifie la présence d'une lettre de lecteur (ex: "C:", "D:")
    if len(path) >= 2 and path[1] == ":" and path[0].isalpha():
        return True

    # Vérifie la présence d'un chemin UNC (ex: "\\server\share" ou "\\\\server\\share")
    if path.startswith("\\"):
        return True

    # Pas un chemin Windows détectable
    return False


def validate_path_accessibility(path: Path) -> bool:
    """Vérifie si un chemin est accessible (existe ou peut être créé).

    Args:
        path (Path): Le chemin à vérifier.

    Returns:
        bool: True si le chemin existe ou est accessible, False sinon.
    """
    try:
        # Vérifie si le chemin ou son parent existe.
        if path.exists():
            return True
        # Vérifie si le parent du chemin existe (pour les destinations potentielles).
        if path.parent.exists():
            return True
        logger.warning("Le chemin '%s' et son parent n'existent pas.", path)
        return False
    except (OSError, PermissionError) as error:
        # En cas d'erreur d'accès ou de permissions, le chemin est considéré inaccessible.
        logger.error("Erreur lors de la vérification du chemin '%s' : %s", path, error)
        return False
