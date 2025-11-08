-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 08, 2025 at 06:22 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `isecure`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin_audit_logs`
--

CREATE TABLE `admin_audit_logs` (
  `id` int(11) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `action` text NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin_audit_logs`
--

INSERT INTO `admin_audit_logs` (`id`, `user_id`, `action`, `ip_address`, `user_agent`, `created_at`) VALUES
(1, 'admin@example.com', 'Failed login attempt', '::1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-05 16:57:08'),
(2, '690b82279e279', 'User logged in', '::1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-05 17:02:58'),
(3, '690b82279e279', 'User logged in', '::1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-07 21:22:02'),
(4, '690b82279e279', 'User logged in', '::1', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36', '2025-11-08 01:24:10'),
(5, '690b82279e279', 'Cancelled visitation request ID: 1', '::1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-08 01:48:28'),
(6, '690b82279e279', 'User logged out', '::1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-08 02:08:50'),
(7, '690b82279e279', 'User logged in', '::1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-08 02:09:16'),
(8, '690b82279e279', 'User logged in', '::1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-08 03:24:33'),
(9, '690b82279e279', 'User logged in', '::1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-08 04:03:37');

-- --------------------------------------------------------

--
-- Table structure for table `clearance_badges`
--

CREATE TABLE `clearance_badges` (
  `id` int(11) NOT NULL,
  `visitor_id` int(11) NOT NULL,
  `clearance_level` varchar(255) NOT NULL,
  `key_card_number` varchar(50) NOT NULL,
  `validity_start` datetime NOT NULL,
  `validity_end` datetime NOT NULL,
  `status` enum('active','inactive','terminated','expired') DEFAULT 'active',
  `issued_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `contact_messages`
--

CREATE TABLE `contact_messages` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `deleted_users`
--

CREATE TABLE `deleted_users` (
  `id` char(36) NOT NULL,
  `full_name` text NOT NULL,
  `email` text NOT NULL,
  `rank` text DEFAULT NULL,
  `status` text DEFAULT NULL,
  `role` text DEFAULT NULL,
  `password_hash` text DEFAULT NULL,
  `joined_date` datetime DEFAULT NULL,
  `last_active` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `landing_audit_logs`
--

CREATE TABLE `landing_audit_logs` (
  `id` int(11) NOT NULL,
  `user_id` varchar(255) DEFAULT NULL,
  `action` text NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `landing_audit_logs`
--

INSERT INTO `landing_audit_logs` (`id`, `user_id`, `action`, `ip_address`, `user_agent`, `created_at`) VALUES
(1, 'b526cc1d4c2c019d00f09bbad84615dee5464c5a4ea8c2a2d6501a1d7cda5f76', 'Submitted visitation request form', '::1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-07 21:21:38'),
(2, '783dfcb4aa6ac47421cff7584fccea1051d5f3d71b0dca5e920dea79bd9625d4', 'Submitted visitation request form', '::1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', '2025-11-08 01:53:33');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` int(11) NOT NULL,
  `user_id` char(36) NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `read_status` enum('Read','Unread') DEFAULT 'Unread'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `message`, `created_at`, `read_status`) VALUES
(1, '690b82279e279', 'Visitor John Carlo Bisnar Boadilla (Email: j.c.boadilla2024@gmail.com, Contact: 09368001943) has submitted a visitation request. This visitor has previous visit history.', '2025-11-07 21:21:38', 'Unread'),
(2, '690b82279e279', 'Visitor John Carlo Bisnar Boadilla (Email: j.c.boadilla2024@gmail.com, Contact: 09368001943) has submitted a visitation request. This visitor has previous visit history.', '2025-11-08 01:53:33', 'Unread');

-- --------------------------------------------------------

--
-- Table structure for table `password_resets`
--

CREATE TABLE `password_resets` (
  `id` int(11) NOT NULL,
  `user_id` char(36) NOT NULL,
  `reset_token` varchar(64) NOT NULL,
  `expires_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `personnel_sessions`
--

CREATE TABLE `personnel_sessions` (
  `id` char(36) NOT NULL,
  `user_id` char(36) NOT NULL,
  `token` varchar(64) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `expires_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `personnel_sessions`
--

INSERT INTO `personnel_sessions` (`id`, `user_id`, `token`, `created_at`, `expires_at`) VALUES
('690ec1199ab73', '690b82279e279', '31267a7bedf3b9b9710d5467c133dea8765385f7d1deddd57fa69473a5472c27', '2025-11-08 12:03:37', '2025-11-08 13:03:37');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` char(36) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `rank` varchar(50) NOT NULL,
  `status` enum('Active','Inactive','Banned','Pending','Suspended') DEFAULT 'Active',
  `password_hash` varchar(255) NOT NULL,
  `role` enum('Admin','User','Moderator','Guest') DEFAULT 'User',
  `joined_date` datetime DEFAULT current_timestamp(),
  `last_active` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `full_name`, `email`, `rank`, `status`, `password_hash`, `role`, `joined_date`, `last_active`) VALUES
('690b82279e279', 'System Admin', 'admin@example.com', 'Captain', 'Active', '$2y$10$qFlN/pa.jLW3gqHCw6X6DeB6abZvjUy4/8ZZrnw4W/n/KEM1AAyIy', 'Admin', '2025-11-06 00:58:15', '2025-11-06 00:58:15');

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `id` int(11) NOT NULL,
  `visitation_id` int(11) DEFAULT NULL,
  `vehicle_owner` varchar(100) NOT NULL,
  `vehicle_brand` varchar(100) NOT NULL,
  `vehicle_model` varchar(100) DEFAULT NULL,
  `vehicle_color` varchar(50) DEFAULT NULL,
  `plate_number` varchar(50) NOT NULL,
  `vehicle_photo_path` varchar(255) DEFAULT NULL,
  `vehicle_photo_compressed` longblob DEFAULT NULL,
  `entry_time` datetime DEFAULT current_timestamp(),
  `exit_time` datetime DEFAULT NULL,
  `status` enum('Expected','Inside','Exited') DEFAULT 'Expected'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`id`, `visitation_id`, `vehicle_owner`, `vehicle_brand`, `vehicle_model`, `vehicle_color`, `plate_number`, `vehicle_photo_path`, `vehicle_photo_compressed`, `entry_time`, `exit_time`, `status`) VALUES
(1, 1, 'John Carlo Bisnar Boadilla', 'Honda', 'Car', 'Red', 'YEC 652', NULL, NULL, NULL, NULL, ''),
(2, 2, 'John Carlo Bisnar Boadilla', 'Honda', 'Car', 'Red', 'YEC 652', NULL, NULL, NULL, NULL, 'Expected'),
(3, 2, 'John Carlo Bisnar Boadilla', 'Honda', 'Car', 'Red', 'YEC 652', NULL, NULL, NULL, NULL, 'Expected'),
(4, 2, 'John Carlo Bisnar Boadilla', 'Honda', 'Car', 'Red', 'YEC 652', NULL, NULL, NULL, NULL, 'Expected');

-- --------------------------------------------------------

--
-- Table structure for table `visitation_requests`
--

CREATE TABLE `visitation_requests` (
  `id` int(11) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `home_address` varchar(255) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `valid_id_path` varchar(255) NOT NULL,
  `selfie_photo_path` varchar(255) NOT NULL,
  `vehicle_owner` varchar(100) DEFAULT NULL,
  `vehicle_brand` varchar(100) DEFAULT NULL,
  `plate_number` varchar(50) DEFAULT NULL,
  `vehicle_color` varchar(50) DEFAULT NULL,
  `vehicle_model` varchar(100) DEFAULT NULL,
  `vehicle_photo_path` varchar(255) DEFAULT NULL,
  `reason` text NOT NULL,
  `personnel_related` varchar(100) DEFAULT NULL,
  `visit_date` date NOT NULL,
  `visit_time` time NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` enum('Pending','Approved','Rejected') NOT NULL DEFAULT 'Pending',
  `office_to_visit` enum('ICT Facility','Training Facility','Personnels Office') DEFAULT NULL,
  `driver_name` varchar(255) DEFAULT NULL,
  `driver_id` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `visitation_requests`
--

INSERT INTO `visitation_requests` (`id`, `first_name`, `middle_name`, `last_name`, `home_address`, `contact_number`, `email`, `valid_id_path`, `selfie_photo_path`, `vehicle_owner`, `vehicle_brand`, `plate_number`, `vehicle_color`, `vehicle_model`, `vehicle_photo_path`, `reason`, `personnel_related`, `visit_date`, `visit_time`, `created_at`, `status`, `office_to_visit`, `driver_name`, `driver_id`) VALUES
(1, 'John Carlo', 'Bisnar', 'Boadilla', 'San Simon, Pampanga', '09368001943', 'j.c.boadilla2024@gmail.com', 'uploads/1762550498_id.jfif', 'public/uploads/selfies/b526cc1d4c2c019d00f09bbad84615dee5464c5a4ea8c2a2d6501a1d7cda5f76.jpg', 'John Carlo Bisnar Boadilla', 'Honda', 'YEC 652', 'Red', 'Car', NULL, 'Visitation', 'John Doe', '2025-11-08', '13:20:00', '2025-11-07 21:21:38', '', 'ICT Facility', NULL, NULL),
(2, 'John Carlo', 'Bisnar', 'Boadilla', 'San Simon, Pampanga', '09368001943', 'j.c.boadilla2024@gmail.com', 'public/uploads/ids/1762566813_id.jfif', 'public/uploads/selfies/783dfcb4aa6ac47421cff7584fccea1051d5f3d71b0dca5e920dea79bd9625d4.jpg', 'John Carlo Bisnar Boadilla', 'Honda', 'YEC 652', 'Red', 'Car', NULL, 'Visitation', 'John Doe', '2025-11-09', '13:00:00', '2025-11-08 01:53:33', 'Approved', 'ICT Facility', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `visitors`
--

CREATE TABLE `visitors` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `middle_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `id_photo_path` varchar(255) DEFAULT NULL,
  `id_photo_compressed` longblob DEFAULT NULL,
  `selfie_photo_path` varchar(255) DEFAULT NULL,
  `selfie_photo_compressed` longblob DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `date` date NOT NULL,
  `time_in` time DEFAULT NULL,
  `time_out` time DEFAULT NULL,
  `status` enum('Expected','Inside','Exited','Cancelled') DEFAULT NULL,
  `key_card_number` varchar(255) DEFAULT NULL,
  `office_to_visit` enum('ICT Facility','Training Facility','Personnels Office') DEFAULT NULL,
  `personnel_related` varchar(100) DEFAULT NULL,
  `visitation_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `visitors`
--

INSERT INTO `visitors` (`id`, `first_name`, `middle_name`, `last_name`, `contact_number`, `email`, `address`, `id_photo_path`, `id_photo_compressed`, `selfie_photo_path`, `selfie_photo_compressed`, `reason`, `date`, `time_in`, `time_out`, `status`, `key_card_number`, `office_to_visit`, `personnel_related`, `visitation_id`) VALUES
(1, 'John Carlo', 'Bisnar', 'Boadilla', '09368001943', 'j.c.boadilla2024@gmail.com', 'San Simon, Pampanga', 'public/uploads/ids/1762566813_id.jfif', NULL, 'public/uploads/selfies/783dfcb4aa6ac47421cff7584fccea1051d5f3d71b0dca5e920dea79bd9625d4.jpg', NULL, 'Visitation', '2025-11-09', NULL, NULL, 'Expected', NULL, 'ICT Facility', 'John Doe', 2),
(2, 'John Carlo', 'Bisnar', 'Boadilla', '09368001943', 'j.c.boadilla2024@gmail.com', 'San Simon, Pampanga', 'public/uploads/ids/1762566813_id.jfif', NULL, 'public/uploads/selfies/783dfcb4aa6ac47421cff7584fccea1051d5f3d71b0dca5e920dea79bd9625d4.jpg', NULL, 'Visitation', '2025-11-09', NULL, NULL, 'Expected', NULL, 'ICT Facility', 'John Doe', 2),
(3, 'John Carlo', 'Bisnar', 'Boadilla', '09368001943', 'j.c.boadilla2024@gmail.com', 'San Simon, Pampanga', 'public/uploads/ids/1762566813_id.jfif', NULL, 'public/uploads/selfies/783dfcb4aa6ac47421cff7584fccea1051d5f3d71b0dca5e920dea79bd9625d4.jpg', NULL, 'Visitation', '2025-11-09', NULL, NULL, 'Expected', NULL, 'ICT Facility', 'John Doe', 2);

-- --------------------------------------------------------

--
-- Table structure for table `visitor_sessions`
--

CREATE TABLE `visitor_sessions` (
  `user_token` char(64) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `expires_at` datetime NOT NULL,
  `selfie_photo_path` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `visitor_sessions`
--

INSERT INTO `visitor_sessions` (`user_token`, `created_at`, `expires_at`, `selfie_photo_path`) VALUES
('489c33dcb89c55a6c33e0ed96cf9a8ae2647e936ab2b87c5250150dc4c198d15', '2025-11-08 03:10:59', '2025-11-08 04:55:59', NULL),
('48ab2ff18f1bc5105c2fcc21f7f76521af470428819a299e1dfaabc2b31285bd', '2025-11-07 06:03:34', '2025-11-07 07:48:34', NULL),
('783dfcb4aa6ac47421cff7584fccea1051d5f3d71b0dca5e920dea79bd9625d4', '2025-11-08 01:29:47', '2025-11-08 03:14:47', 'public/uploads/selfies/783dfcb4aa6ac47421cff7584fccea1051d5f3d71b0dca5e920dea79bd9625d4.jpg'),
('8113546c0ec0b66840b61172a8e01ec30dc351d4c6cbac7055d98fdd15ef77a4', '2025-11-08 02:22:13', '2025-11-08 04:07:13', NULL),
('ad01a88a7e1d4a411bd135cbc7708cfb18ea821c3c2e8ab5eedfa24adc9e79b0', '2025-11-05 17:37:19', '2025-11-05 19:22:19', NULL),
('b526cc1d4c2c019d00f09bbad84615dee5464c5a4ea8c2a2d6501a1d7cda5f76', '2025-11-07 15:26:39', '2025-11-07 17:11:39', 'public/uploads/selfies/b526cc1d4c2c019d00f09bbad84615dee5464c5a4ea8c2a2d6501a1d7cda5f76.jpg'),
('dd1e813228a869fb299b650df789b863c4e18bebb97a2b6e97b961a32e7053df', '2025-11-06 18:49:55', '2025-11-06 20:34:55', NULL),
('fb76bdd704aef108b11618bd5c6666808746c25f4836d7c7d8cb4dbeeb714214', '2025-11-07 04:01:36', '2025-11-07 05:46:36', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin_audit_logs`
--
ALTER TABLE `admin_audit_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `clearance_badges`
--
ALTER TABLE `clearance_badges`
  ADD PRIMARY KEY (`id`),
  ADD KEY `visitor_id` (`visitor_id`);

--
-- Indexes for table `contact_messages`
--
ALTER TABLE `contact_messages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `deleted_users`
--
ALTER TABLE `deleted_users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `landing_audit_logs`
--
ALTER TABLE `landing_audit_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_landing_session` (`user_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `password_resets`
--
ALTER TABLE `password_resets`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reset_token` (`reset_token`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `personnel_sessions`
--
ALTER TABLE `personnel_sessions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `visitation_id` (`visitation_id`);

--
-- Indexes for table `visitation_requests`
--
ALTER TABLE `visitation_requests`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `visitors`
--
ALTER TABLE `visitors`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_visitors_visitation` (`visitation_id`);

--
-- Indexes for table `visitor_sessions`
--
ALTER TABLE `visitor_sessions`
  ADD PRIMARY KEY (`user_token`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin_audit_logs`
--
ALTER TABLE `admin_audit_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `clearance_badges`
--
ALTER TABLE `clearance_badges`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `contact_messages`
--
ALTER TABLE `contact_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `landing_audit_logs`
--
ALTER TABLE `landing_audit_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `password_resets`
--
ALTER TABLE `password_resets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `visitation_requests`
--
ALTER TABLE `visitation_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `visitors`
--
ALTER TABLE `visitors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `clearance_badges`
--
ALTER TABLE `clearance_badges`
  ADD CONSTRAINT `clearance_badges_ibfk_1` FOREIGN KEY (`visitor_id`) REFERENCES `visitors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `landing_audit_logs`
--
ALTER TABLE `landing_audit_logs`
  ADD CONSTRAINT `fk_landing_session` FOREIGN KEY (`user_id`) REFERENCES `visitor_sessions` (`user_token`) ON DELETE CASCADE;

--
-- Constraints for table `password_resets`
--
ALTER TABLE `password_resets`
  ADD CONSTRAINT `password_resets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `personnel_sessions`
--
ALTER TABLE `personnel_sessions`
  ADD CONSTRAINT `personnel_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`visitation_id`) REFERENCES `visitation_requests` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `visitors`
--
ALTER TABLE `visitors`
  ADD CONSTRAINT `fk_visitors_visitation` FOREIGN KEY (`visitation_id`) REFERENCES `visitation_requests` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
