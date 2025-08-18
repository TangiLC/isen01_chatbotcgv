# Chatbot CGV – PoC Python

## 🧾 Présentation

Ce projet est un **Proof of Concept (POC)** académique développé dans le cadre de la formation *Développeur IA* à l'**ISEN/Simplon**. Il s’agit d’un **chatbot terminal** capable de répondre automatiquement aux questions liées aux **Conditions Générales de Vente (CGV)** d'une entreprise e-commerce fictive (*MonEshop*), en s'appuyant sur un modèle OpenAI **fine-tuné** à partir d’un fichier JSONL d’entraînement.

- **Nom du projet** : Chatbot CGV
- **Objectif** : Simuler un assistant interne répondant aux questions sur les CGV (paiement, rétractation, livraison, garantie, données personnelles)
- **Livrable** : MVP fonctionnant en **ligne de commande** (sans interface graphique)

## 🛠️ Fonctionnalités

- Chargement d’un pré-prompt métier.
- Utilisation d’un modèle fine-tuné via l’API OpenAI.
- Interaction utilisateur en console (prompt/réponse).
- Enregistrement des échanges dans une base SQLite (via Docker).

## 🧑‍💻 Stack technique

- **Python ≥ 3.12**
- **Ubuntu 24.04 (via WSL2 recommandé)**
- **Base de données SQLite** (conteneur Docker + Adminer pour visualisation)
- **API OpenAI** pour fine-tuning
- **VSCode** (avec environnement virtuel Python)
- **Fichier d’entraînement JSONL** pour affiner le modèle GPT

## ⚙️ Installation et préparation

### 1. Fork et clonage du projet

```bash
git clone https://github.com/TangiLC/isen01_chatbotcgv.git
cd chatbot-cgv
```

### 2. Création d’un environnement virtuel Python

Sous Linux (Ubuntu recommandé) :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration des variables d’environnement

Créer un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4.1-nano-2025-04-14
OPENAI_FILE_ID=file-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

```

Ces clés sont nécessaires pour utiliser le modèle fine-tuné via l’API OpenAI.

## 🧪 Lancement de l'application

```bash
python chatbot.py
```

Une interaction en console vous permettra de poser vos questions, et d’obtenir les réponses générées par le modèle.

## 🧬 Fine-tuning (optionnel, si vous ne disposez pas encore d’un modèle)

Les scripts suivants peuvent être utilisés **une seule fois**, pour uploader vos données d’entraînement et générer un modèle personnalisé :

```bash
# upload du fichier JSONL
python train/addfile.py

# lancement du fine-tuning
python train/finetuning.py
```

👉 N'oubliez pas de mettre à jour `OPENAI_FILE_ID` et le nom du modèle dans vos appels.

## 🧩 Structure du projet

```
chatbot-cgv/
├── chatbot.py              # Script principal d'interaction
├── .env                    # Fichier de configuration des clés
├── /train/
│   ├── addfile.py          # Script pour upload du fichier JSONL
│   └── train.jsonl         # Fichier jsonl de fine-tuning
├── /data/                  
│   ├── diag.png            # Schéma de la BDD
│   ├── docker-compose.yml  # fichier compose pour conteneuriser SQLite
│   └── script.sql          # Fichier sql de création de la BDD
├── finetuning.py           # Script de création du modèle fine-tuné
├── requirements.txt        # Liste des packages nécessaires
├── cgv.md                  # Conditions générales de ventes
├── organigramme.png        # Schéma de l'algorithme
└── README.md
```

# Diagramme de fonctionnement - chatbot.py

```
                      ┌────────────┐
                      │   Début    │
                      └────┬───────┘
                    ┌──────▼───────┐
                    │ Saisie       │
                    │ utilisateur  │
                    └──────┬───────┘
          ┌────────────────▼────────────────┐
          │ La question existe-t-elle       │
          │ déjà en BDD (SQLite) ?          │
          └──────┬───────────────┬──────────┘
               [oui]           [non]
        ┌────────▼─────┐   ┌─────▼───────────┐
        │ Affichage de │   │ Envoi requête   │
        │ la réponse   │   │ à l’API OpenAI  │
        └────────┬─────┘   └─────┬───────────┘
            ┌────▼──────┐     ┌──▼───────────┐
            │ Autre     │     │ Attente de   │
            │ question ?│     │ la réponse   │
            └────┬──────┘     └──┬───────────┘
               [oui]             │
                 │        ┌──────▼───────┐
                 │        │ Réponse de   │
                 │        │ l’API valide?│
                 │        └────┬─────────┘
                 │           [oui]
                 │   ┌─────────▼────────────┐
                 │   │ Stockage Q/R dans la │
                 │   │ base de données      │
                 │   └────────┬─────────────┘
                 │     ┌──────▼─────┐
                 │     │ Affichage  │
                 │     │ réponse    │
                 │     └───────┬────┘
                 │       ┌─────▼─────┐
                 │       │ Autre     │
                 ─[oui]─ │ question ?│
                 │       └────┬──────┘
                 │          [non]
           ┌─────▼────┐  ┌────▼─────┐
           │  Retour  │  │   Fin    │
           └──────────┘  └──────────┘
```


## 🐳 Base de données (SQLite via Docker)

Dans le dossier `/data`, exécutez :

```bash
docker-compose up -d
```

Puis accédez à Adminer via [http://localhost:8080](http://localhost:8080) pour visualiser les logs des interactions.

---

## 🎓 Équipe pédagogique

- Travail réalisé en binôme (<a href="https://github.com/go2375" target="_blank">
  <img src="https://avatars.githubusercontent.com/go2375" width="40" height="40" style="border-radius: 50%;" alt="Gosia" />
</a>)
- Développement encadré pour du module *Fine-tuning GPT et prototypage IA* Prairie 01
- Formation ISEN - Simplon.co – 2025
- PS: les clés API OpenAPI initiales ont été révoquées, de nouvelles clés doivent être ajoutées au fichier .env

## TO DO

- Création de fichier jsonl de fine tuning plus conséquent
- Reprise des commentaires des fonctions au format docstring
- factorisation et sécurisation, notamment bdd=mysql.connect()
- optimisation des exceptions, retry en cas d'echec etc...

---

**Bon développement !**
