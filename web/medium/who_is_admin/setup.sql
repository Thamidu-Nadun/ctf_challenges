CREATE TABLE IF NOT EXISTS `users` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `config` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `key` VARCHAR(255) NOT NULL,
    `value` VARCHAR(255) NOT NULL
);

DELETE FROM `users`;
DELETE FROM `config`;

INSERT INTO users (username, password)
VALUES ('admin', 'admin123'), ('john', 'password1'), ('alex', 'password2');

INSERT INTO config (key, value)
VALUES ('FLAG', 'FLAG{B40KEN_AUTH}')