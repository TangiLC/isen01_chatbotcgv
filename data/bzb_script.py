import mysql.connector
from mysql.connector import Error

DB_HOST = "localhost"
DB_ROOT = "root"
DB_ROOT_PASSWORD = "example"
DB_NAME = "bz_bus"
DB_USER = "exemple"
DB_PASSWORD = "exemple"


def main():
    try:
        # Connexion admin pour création base et utilisateur
        admin_cnx = mysql.connector.connect(
            host=DB_HOST, user=DB_ROOT, password=DB_ROOT_PASSWORD
        )
        admin_cursor = admin_cnx.cursor()

        admin_cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        print(f"Base `{DB_NAME}` créée ou déjà existante.")

        admin_cursor.execute(
            f"CREATE USER IF NOT EXISTS '{DB_USER}'@'%' IDENTIFIED BY '{DB_PASSWORD}'"
        )
        admin_cursor.execute(
            f"GRANT ALL PRIVILEGES ON `{DB_NAME}`.* TO '{DB_USER}'@'%'"
        )
        admin_cursor.execute("FLUSH PRIVILEGES")
        admin_cnx.commit()
        admin_cursor.close()
        admin_cnx.close()
        print(f"Utilisateur `{DB_USER}`@`%` créé/mis à jour.")

    except Error as err:
        print(f"[Erreur admin] {err}")
        return

    try:
        # Connexion utilisateur sur la base
        user_cnx = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        user_cursor = user_cnx.cursor()

        statements = [
            # Création des tables
            """# create_table_arret
            CREATE TABLE IF NOT EXISTS `arrets` (
                `id` int(11) NOT NULL PRIMARY KEY,
                `nom` varchar(20) NOT NULL,
                `adresse` varchar(50) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """# create_table_lignes
            CREATE TABLE IF NOT EXISTS `lignes` (
                `id` int(11) NOT NULL PRIMARY KEY,
                `nom` varchar(20) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """# create_table_bus
            CREATE TABLE IF NOT EXISTS `bus` (
                `id` int(11) NOT NULL PRIMARY KEY,
                `numero` varchar(4) NOT NULL,
                `immatriculation` varchar(7) NOT NULL,
                `nombre_place` int(11) NOT NULL,
                `ligne` int(11) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            """# create_table_arrets_lignes
            CREATE TABLE IF NOT EXISTS `arrets_lignes` (
                `ligne` int(11) NOT NULL,
                `arret` int(11) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """,
            # Alter des clés primaires et auto_increment
            "ALTER TABLE `arrets` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;",
            "ALTER TABLE `lignes` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;",
            "ALTER TABLE `bus` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;",
            # "ALTER TABLE `arrets_lignes` ADD CONSTRAINT `arrets_lignes_ibfk_1` FOREIGN KEY (`ligne`) REFERENCES `lignes` (`id`);",
            # "ALTER TABLE `arrets_lignes` ADD CONSTRAINT `arrets_lignes_ibfk_2` FOREIGN KEY (`arret`) REFERENCES `arrets` (`id`);",
            # Insertion : lignes → arrets → arrets_lignes → bus
            """# insert_into_lignes
            INSERT INTO `lignes` (`id`, `nom`) VALUES
            (1, 'Rouge'), (2, 'Vert'), (3, 'Bleu');
            """,
            """# insert_into_arrets
            INSERT INTO `arrets` (`id`, `nom`, `adresse`) VALUES
            (1, 'Guénolé', '6 rue de Saint Guénolé'),
            (2, 'Korrigan', '1 impasse du Korrigan'),
            (3, 'Morgana', '2 plage de Morgana'),
            (4, 'L''Ankou', '3 place de la Morgue'),
            (5, 'Ys', '4 rue de l''ile d''Ys'),
            (6, 'Viviane', '5 avenue de Viviane');
            """,
            """# insert_into_arrets_lignes
            INSERT INTO `arrets_lignes` (`ligne`, `arret`) VALUES
            (1, 2), (1, 4), (1, 3),
            (2, 3), (2, 1), (2, 5),
            (3, 5), (3, 6), (3, 1), (3, 2);
            """,
            """# insert_into_bus
            INSERT INTO `bus` (`id`, `numero`, `immatriculation`, `nombre_place`, `ligne`) VALUES
            (1, 'BB01', 'CA123DO', 20, 1),
            (2, 'BB02', 'NO123EL', 30, 2),
            (3, 'BB03', 'JE123UX', 20, 3),
            (4, 'BB04', 'RE123PA', 30, 1);
            """,
        ]

        for stmt in statements:
            user_cursor.execute(stmt)
            print("→ OK :", stmt.strip().split()[0], stmt.strip().split()[1])

        user_cnx.commit()
        user_cursor.close()
        user_cnx.close()
        print("Initialisation de la base terminée avec succès.")

    except Error as err:
        print(f"[Erreur user] {err}")


if __name__ == "__main__":
    main()
