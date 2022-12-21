-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : mer. 14 déc. 2022 à 11:13
-- Version du serveur :  10.4.16-MariaDB
-- Version de PHP : 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `indicators`
--

-- --------------------------------------------------------

--
-- Structure de la table `partner`
--

CREATE TABLE `partner` (
  `id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `website` varchar(50) DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  `userId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `partner`
--

INSERT INTO `partner` (`id`, `name`, `website`, `active`, `userId`) VALUES
(3, 'USAID', 'www://usaid.us', 1, 2),
(4, 'CARITAS', 'www://caritas-congo.org', 0, 12);

-- --------------------------------------------------------

--
-- Structure de la table `sector`
--

CREATE TABLE `sector` (
  `id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `sector`
--

INSERT INTO `sector` (`id`, `name`) VALUES
(1, 'Cohesion social'),
(2, 'Santé'),
(4, 'WASH');

-- --------------------------------------------------------

--
-- Structure de la table `subscription`
--

CREATE TABLE `subscription` (
  `id` int(11) NOT NULL,
  `sectorId` int(11) DEFAULT NULL,
  `partnerId` int(11) DEFAULT NULL,
  `startDate` datetime DEFAULT current_timestamp(),
  `endDate` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `subscription`
--

INSERT INTO `subscription` (`id`, `sectorId`, `partnerId`, `startDate`, `endDate`) VALUES
(2, 1, 3, '2022-12-11 00:00:00', '2022-12-31 00:00:00'),
(3, 4, 3, '2022-12-08 00:00:00', '2022-12-31 00:00:00');

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`, `type`, `phone`) VALUES
(1, 'PRINCE Julien', 'julienprince6@gmail.com', '$2b$12$eoaw0GR8Ai7Gy8s6OaFRn.LLeTDjIwg6crBpgyX3yG1VzuC583P.S', 'Admin', '0995961907'),
(2, 'USAID', 'usaid@gmail.com', '$2b$12$Xq5ga.sUBkyYlYgZ9CQAOOm3einjfEzNgWtoqs7i0uDnXHs8/0xC.', 'Partner', '0990432480'),
(12, 'Albert for CARITAS', 'albert@gmail.com', '$2b$12$iueecvBU5OnGqt4zBlMfoeno3UdtEGFH1F1mSzDgTs3IDNLPpS46C', 'Partner', '+243 995 696 492');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `partner`
--
ALTER TABLE `partner`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user` (`userId`);

--
-- Index pour la table `sector`
--
ALTER TABLE `sector`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `subscription`
--
ALTER TABLE `subscription`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_indicator` (`sectorId`),
  ADD KEY `fk_partner` (`partnerId`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `partner`
--
ALTER TABLE `partner`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `sector`
--
ALTER TABLE `sector`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `subscription`
--
ALTER TABLE `subscription`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `partner`
--
ALTER TABLE `partner`
  ADD CONSTRAINT `fk_user` FOREIGN KEY (`userId`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `subscription`
--
ALTER TABLE `subscription`
  ADD CONSTRAINT `fk_indicator` FOREIGN KEY (`sectorId`) REFERENCES `sector` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_partner` FOREIGN KEY (`partnerId`) REFERENCES `partner` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
