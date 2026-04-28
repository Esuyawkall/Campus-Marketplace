-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Apr 28, 2026 at 07:52 PM
-- Server version: 8.0.34
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ia637_Marketplace`
--

-- --------------------------------------------------------

--
-- Table structure for table `favorites`
--

CREATE TABLE `favorites` (
  `user_id` int NOT NULL,
  `product_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `favorites`
--

INSERT INTO `favorites` (`user_id`, `product_id`) VALUES
(1, 1),
(1, 2),
(9, 2),
(3, 3),
(9, 3),
(10, 3),
(9, 4),
(9, 5);

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `image_id` int NOT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `product_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `images`
--

INSERT INTO `images` (`image_id`, `image_url`, `product_id`) VALUES
(1, 'images/playstation.jpg', 1),
(3, 'images/computer.jpg', 3),
(4, 'images/desk+chair.jpg', 4),
(8, 'images/1be07f39d3aa45aca6133605a780021e_book.jpg', 13),
(12, 'images/121bbff947af4b47b8b131e2bb975580_scooter.jpg', 17),
(15, 'images/desk+chair.jpg', 20);

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `message_id` int NOT NULL,
  `date_sent` datetime DEFAULT CURRENT_TIMESTAMP,
  `message_text` text NOT NULL,
  `sender_id` int DEFAULT NULL,
  `receiver_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`message_id`, `date_sent`, `message_text`, `sender_id`, `receiver_id`, `product_id`) VALUES
(1, '2026-04-02 15:22:27', 'Is this still available?', 9, 2, 1),
(2, '2026-04-02 15:22:27', 'Yes, it is!', 2, 1, 1),
(3, '2026-04-02 15:22:27', 'Can you lower the price?', 3, 9, 3),
(4, '2026-04-02 15:22:27', 'Price is firm.', 2, 3, 3),
(5, '2026-04-13 16:21:36', 'what', 9, 3, NULL),
(6, '2026-04-13 16:24:59', 'hello', 9, 9, NULL),
(7, '2026-04-13 16:27:06', 'No', 9, 3, NULL),
(8, '2026-04-13 16:54:01', 'yes it is', 9, 2, NULL),
(9, '2026-04-13 16:57:42', 'Hello', 9, 10, NULL),
(10, '2026-04-13 18:12:51', 'Hi', 10, 9, NULL),
(11, '2026-04-13 18:13:12', 'Is the item still available', 9, 10, NULL),
(12, '2026-04-13 18:13:29', 'Yes It is', 10, 9, NULL),
(13, '2026-04-14 14:32:22', 'wassup broe...are you on campu', 14, 4, NULL),
(14, '2026-04-14 14:47:38', 'yes i am', 14, 4, NULL),
(15, '2026-04-14 15:07:52', 'Hello', 9, 14, NULL),
(16, '2026-04-14 15:08:12', 'are you on campus', 14, 9, NULL),
(17, '2026-04-14 15:08:45', 'Yes I am', 9, 14, NULL),
(18, '2026-04-14 15:10:25', 'see you by the Snell entrance at  1pm sharp and we make the transaction', 14, 9, NULL),
(19, '2026-04-14 15:11:00', 'works for me', 9, 14, NULL),
(20, '2026-04-19 18:18:40', 'hi', 9, 14, NULL),
(21, '2026-04-19 19:15:33', 'broe wassup', 9, 14, NULL),
(22, '2026-04-22 14:16:21', 'How much for the desk only?', 9, 4, 3),
(23, '2026-04-22 14:34:12', 'what product is this', 9, 2, NULL),
(24, '2026-04-22 14:35:29', 'what product is this', 9, 2, 3),
(25, '2026-04-22 14:38:47', 'hello?', 9, 10, 8);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int NOT NULL,
  `quantity` int NOT NULL,
  `order_status` varchar(20) DEFAULT NULL,
  `date_completed` datetime DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `seller_id` int DEFAULT NULL,
  `buyer_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `quantity`, `order_status`, `date_completed`, `product_id`, `seller_id`, `buyer_id`) VALUES
(12, 1, 'Completed', '2026-04-16 15:49:05', 1, NULL, 9),
(19, 1, 'Completed', '2026-04-16 15:55:36', 2, NULL, 9),
(22, 1, 'Completed', '2026-04-16 16:02:05', 4, NULL, 9),
(24, 1, 'Completed', '2026-04-16 16:03:17', 8, NULL, 9);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int NOT NULL,
  `product_name` varchar(150) DEFAULT NULL,
  `description` text NOT NULL,
  `product_price` decimal(10,2) NOT NULL,
  `product_status` varchar(20) DEFAULT NULL,
  `date_posted` datetime DEFAULT CURRENT_TIMESTAMP,
  `product_condition` varchar(50) DEFAULT NULL,
  `seller_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_name`, `description`, `product_price`, `product_status`, `date_posted`, `product_condition`, `seller_id`) VALUES
(1, 'Play Station 4', 'Selling my sparingly used PlayStation 5 (Disc Edition). This console works perfectly and has been taken excellent care of. It has only been used for roughly 20-30 hours since I bought it new. No scratches, never dropped, and comes from a smoke-free, pet-free home.', 650.00, 'active', '2026-04-02 15:22:27', 'Used', 2),
(2, 'New product 2', 'Ergonomic gaming chair in like-new condition. Provides excellent back support for long study or gaming sessions. Comfortable, adjustable, and perfect for dorm or home setups.', 150.00, 'unavailable', '2026-04-02 15:22:27', 'Like New', 4),
(3, 'MacBook Air', 'MacBook Air with M1 chip and 16GB RAM. Lightweight and powerful laptop ideal for coding, schoolwork, and everyday use. Well maintained and performs smoothly.', 900.00, 'pending', '2026-04-02 15:22:27', 'Used', 2),
(4, 'Desk Lamp', 'LED desk lamp with adjustable brightness settings. Great for studying at night or working in low-light environments. Energy-efficient and in excellent condition.', 30.00, 'Sold', '2026-04-02 15:22:27', 'New', 4),
(5, 'New product', 'Affordable item in good condition, suitable for everyday student use. Simple, reliable, and available for quick pickup on campus.', 12.00, NULL, '2026-04-08 15:28:22', 'New', 9),
(6, 'Machine Learning Text Book', 'Machine Learning textbook, 2025 new version. Ideal for students taking AI or data science courses. Clean pages with minimal wear and very useful for academic reference.', 10.00, 'available', '2026-04-09 01:44:56', 'Used', 9),
(8, 'Gaming Chair', 'High-quality item in like-new condition. Great value for students looking for affordability and reliability. Ready for immediate use and pickup.', 100.00, 'available', '2026-04-09 15:16:20', 'Like New', 10),
(13, 'Machine Learning Text Book', 'Machine Learning text book', 1200.00, 'available', '2026-04-19 16:12:05', 'Like New', 9),
(17, 'Scooter', 'f', 45.00, 'available', '2026-04-19 16:54:07', 'For Parts', 9),
(20, 'Test 1', 'New DEsc', 123.00, 'available', '2026-04-23 15:53:08', 'New', 10);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `user_status` varchar(20) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `user_status`, `password`, `role`, `email`) VALUES
(1, 'John', 'Doe', 'Active', 'hash1', 'admin', 'john@example.com'),
(2, 'Alice', 'Smith', 'Active', 'hash2', 'participant', 'alice@example.com'),
(3, 'Michael', 'Brown', 'Active', 'hash3', 'participant', 'michael@example.com'),
(4, 'Sarah', 'Johnson', 'Active', 'hash4', 'participant', 'sarah@example.com'),
(9, 'esuyawkal', 'bereda', 'active', 'adf47922f0bdb6b9a520ed2d43622d14', 'admin', 'esuyawkal@clarkson.edu'),
(10, 'Esuyawkal', 'Bereda', 'Active', 'adf47922f0bdb6b9a520ed2d43622d14', 'participant', 'esuyawkal07@gmail.com'),
(11, 'esuyawkal', 'demisie', NULL, 'adf47922f0bdb6b9a520ed2d43622d14', 'admin', 'esuyawkal@gmail.com'),
(12, 'esuyawkal', 'bereda', 'active', 'adf47922f0bdb6b9a520ed2d43622d14', 'admin', 'esuyawkal@admin'),
(14, 'kuda', 'anderson', NULL, 'a4eb2e0f3e0cbac5c3e64ddc4d24f1df', 'participant', 'kuda@clarkson.edu');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`user_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`image_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`message_id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `receiver_id` (`receiver_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD UNIQUE KEY `unique_order` (`buyer_id`,`product_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `seller_id` (`seller_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `seller_id` (`seller_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `images`
--
ALTER TABLE `images`
  MODIFY `image_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `message_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `favorites`
--
ALTER TABLE `favorites`
  ADD CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);

--
-- Constraints for table `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `messages_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`seller_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`buyer_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
