-- Base de données
CREATE DATABASE IF NOT EXISTS Logs;
USE Logs;

-- Table des conversations
CREATE TABLE conversations (
    id_conversation INT AUTO_INCREMENT PRIMARY KEY
);

-- Table des statuts
CREATE TABLE statuts (
    id_statut INT AUTO_INCREMENT PRIMARY KEY,
    label VARCHAR(20) NOT NULL
);

-- Table des échanges
CREATE TABLE echanges (
    id_echange INT AUTO_INCREMENT PRIMARY KEY,
    conversation INT NOT NULL,
    date DATETIME NOT NULL,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    statut INT NOT NULL,
    FOREIGN KEY (conversation) REFERENCES conversations(id_conversation),
    FOREIGN KEY (statut) REFERENCES statuts(id_statut)
);
