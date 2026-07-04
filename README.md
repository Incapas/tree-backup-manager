# 📦 Tree Backup Manager

## Description du Projet

Ce projet est un outil Python dédié à la gestion de sauvegardes automatisées via des chemins de sauvegarde configurables. Il permet de charger une configuration JSON, de tenter une sauvegarde via un chemin principal, puis de basculer automatiquement vers un chemin secondaire si le premier est indisponible.

Le programme est conçu pour fonctionner de manière autonome et peut être planifié via un cron, un anacron ou un planificateur de tâches afin d’exécuter des sauvegardes périodiques sans intervention manuelle.

Un autre objectif de ce projet est de démontrer la capacité à construire un programme complet avec l’aide de GitHub Copilot, depuis la conception jusqu’à la mise en œuvre fonctionnelle.

## ✨ Fonctionnalités Clés

- Chargement de la configuration depuis un fichier JSON.
- Tentative de sauvegarde via un chemin principal.
- Basculement automatique vers un chemin secondaire en cas d’indisponibilité.
- Journalisation des opérations dans un fichier de log.
- Structure modulaire adaptée à une exécution automatisée.

---

## 👥 Contributions au Projet

### 👩 Développeur Initial

Contribution résidant dans la définition des objectifs du projet, l’organisation de la structure et l’implémentation de la logique métier.

| Catégorie                  | Description de la contribution                                                             |
| :------------------------- | :----------------------------------------------------------------------------------------- |
| **Architecture du Projet** | Définition de la structure globale et séparation des responsabilités entre les modules.    |
| **Logique de Sauvegarde**  | Mise en place de la logique de fallback entre le chemin principal et le chemin secondaire. |
| **Configuration**          | Définition et alimentation du fichier de configuration JSON.                               |
| **Validation**             | Vérification du comportement attendu dans un contexte d’exécution automatisé.              |

### 🧑 Assistant IA GitHub Copilot

Contribution résidant dans l’aide à l’implémentation, la structuration du code et la documentation du projet.

| Catégorie                 | Description de la Contribution                                                             |
| :------------------------ | :----------------------------------------------------------------------------------------- |
| **Structuration du Code** | Aide à la séparation du code en modules distincts pour la lisibilité et la maintenabilité. |
| **Gestion des Erreurs**   | Proposition et mise en place d’une logique robuste pour les erreurs de sauvegarde.         |
| **Journalisation**        | Mise en place de la configuration des logs vers un fichier dédié.                          |
| **Documentation**         | Rédaction et amélioration du contenu du README.                                            |

---

## 🛠️ Structure du Projet

- app/ : code applicatif principal ;
- app/scripts/ : modules Python pour la gestion des chemins et de la sauvegarde ;
- app/config/ : configuration JSON du projet ;
- app/logs/ : fichiers de logs générés par l’application.

---

## 🚀 Démarrage

Pour lancer le projet, après avoir renseigner les différents chemins dans "app/config/backup_paths.json", exécutez :

```bash
python app/main.py
```

---

## 📝 Fonctionnement

Le programme charge la configuration depuis le fichier de configuration, puis exécute la sauvegarde en suivant cet ordre :

1. tentative via le chemin principal ;
2. si le chemin principal est indisponible, bascule sur le chemin secondaire ;
3. enregistre les événements dans un fichier de log.
