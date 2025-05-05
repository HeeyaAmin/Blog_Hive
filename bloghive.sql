-- BlogHive Database SQL Code
-- Authors: Heeya Mineshkumar Amin and Shail Jayesh Patel

-- ==================================================
-- Step 1: Create Database
-- ==================================================

-- Written by Heeya Mineshkumar Amin
CREATE DATABASE IF NOT EXISTS bloghive;
USE bloghive;

-- ==================================================
-- Step 2: Create Tables
-- ==================================================

-- Written by Heeya Mineshkumar Amin
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Written by Heeya Mineshkumar Amin
CREATE TABLE IF NOT EXISTS keywords (
    keyword_id INT AUTO_INCREMENT PRIMARY KEY,
    keyword_name VARCHAR(100) UNIQUE NOT NULL
);

-- Written by Shail Jayesh Patel
CREATE TABLE IF NOT EXISTS user_favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    blog_title TEXT NOT NULL,
    blog_description TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

USE 
-- Written by Shail Jayesh Patel
CREATE TABLE IF NOT EXISTS adjectives (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vacation_destination VARCHAR(100),
    fitness VARCHAR(100),
    technology VARCHAR(100),
    food VARCHAR(100),
    fashion VARCHAR(100),
    finance VARCHAR(100),
    health VARCHAR(100),
    business VARCHAR(100),
    education VARCHAR(100),
    sports VARCHAR(100),
    seasons VARCHAR(100),
    entertainment VARCHAR(100),
    cooking VARCHAR(100),
    music_preference VARCHAR(100),
    hobbies VARCHAR(100),
    movies_preference VARCHAR(100),
    lifestyle_pace VARCHAR(100),
    nutrition VARCHAR(100),
    volunteering VARCHAR(100),
    house_style VARCHAR(100)
);

-- ==================================================
-- Step 3: Insert Sample Data
-- ==================================================

-- Written by Heeya Mineshkumar Amin
INSERT INTO keywords (keyword_name) VALUES
('vacation_destination'),
('fitness'),
('technology'),
('food'),
('fashion'),
('finance'),
('health'),
('business'),
('education'),
('sports'),
('seasons'),
('entertainment'),
('cooking'),
('music_preference'),
('hobbies'),
('movies_preference'),
('lifestyle_pace'),
('nutrition'),
('volunteering'),
('house_style');

-- ==================================================
-- Step 4: Sample Queries Relevant to Application
-- ==================================================

-- 4.1. Insert a new user
-- Written by Heeya Mineshkumar Amin
INSERT INTO user (first_name, last_name, email, password) 
VALUES ('John', 'Doe', 'john.doe@example.com', 'securepassword');

-- 4.2. Insert a blog favorite for a user
-- Written by Shail Jayesh Patel
INSERT INTO user_favorites (user_id, blog_title, blog_description) 
VALUES (1, 'Top Vacation Spots 2025', 'Explore the best destinations for your next vacation.');

-- 4.3. Retrieve all blogs saved by a specific user
-- Written by Shail Jayesh Patel
SELECT f.blog_title, f.blog_description
FROM user u
JOIN user_favorites f ON u.user_id = f.user_id
WHERE u.email = 'john.doe@example.com';

-- 4.4. Display all available keywords
-- Written by Heeya Mineshkumar Amin
SELECT keyword_name
FROM keywords
ORDER BY keyword_name ASC;

-- 4.5. Retrieve adjectives for a blog generation
-- Written by Shail Jayesh Patel
SELECT vacation_destination, food, fashion
FROM adjectives
ORDER BY id
LIMIT 5;

-- ==================================================
-- Step 5: Create Simple View
-- ==================================================

-- Written by Shail Jayesh Patel
CREATE VIEW user_fav_blogs AS
SELECT u.first_name, u.last_name, f.blog_title, f.blog_description
FROM user u
JOIN user_favorites f ON u.user_id = f.user_id;

-- To check the view
-- SELECT * FROM user_fav_blogs;

USE bloghive;

CREATE TABLE IF NOT EXISTS blog_generation_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    generated_title TEXT NOT NULL,
    generated_description TEXT NOT NULL,
    selected_data JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
);

SELECT generated_title, selected_data, created_at
FROM blog_generation_log
WHERE user_id = 3
ORDER BY created_at DESC
LIMIT 5;

USE bloghive;
# Updating User_favorites table to store image path
ALTER TABLE user_favorites ADD COLUMN image_url TEXT;



-- ==================================================
-- End of SQL Code
-- ==================================================
