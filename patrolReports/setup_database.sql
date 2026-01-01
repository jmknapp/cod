-- Database setup for USS Cod Patrol Reports
-- Run: mysql -u root -p < setup_database.sql

-- Create database
CREATE DATABASE IF NOT EXISTS cod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE cod;

-- Main attack table (one row per attack)
CREATE TABLE IF NOT EXISTS torpedo_attacks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patrol INT NOT NULL,
    attack_number INT NOT NULL,
    attack_date DATE NOT NULL,
    attack_time TIME,
    timezone VARCHAR(10),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    latitude_deg INT,
    latitude_min DECIMAL(5,2),
    latitude_hemisphere CHAR(1),
    longitude_deg INT,
    longitude_min DECIMAL(5,2),
    longitude_hemisphere CHAR(1),
    target_name VARCHAR(100),
    target_type VARCHAR(50),
    target_tonnage INT,
    target_description TEXT,
    target_course INT,
    target_speed DECIMAL(4,1),
    target_draft DECIMAL(4,1),
    target_range INT,
    target_bearing INT,
    angle_on_bow VARCHAR(20),
    own_course INT,
    own_speed DECIMAL(4,1),
    own_depth INT,
    attack_type VARCHAR(50),
    sea_condition VARCHAR(100),
    visibility VARCHAR(100),
    convoy_info TEXT,
    result VARCHAR(50),
    damage_description TEXT,
    pdf_page INT,
    remarks TEXT,
    UNIQUE KEY patrol_attack (patrol, attack_number)
);

-- Individual torpedo data
CREATE TABLE IF NOT EXISTS torpedoes_fired (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attack_id INT NOT NULL,
    tube_number INT NOT NULL,
    fire_sequence INT,
    track_angle INT,
    track_side CHAR(1),
    gyro_angle INT,
    depth_setting INT,
    power_setting VARCHAR(10),
    spread_type VARCHAR(20),
    firing_interval INT,
    mk_torpedo VARCHAR(10),
    torpedo_serial VARCHAR(20),
    mk_exploder VARCHAR(10),
    exploder_serial VARCHAR(20),
    actuation_set VARCHAR(20),
    mk_warhead VARCHAR(10),
    warhead_serial VARCHAR(20),
    explosive_type VARCHAR(20),
    hit_miss VARCHAR(10),
    erratic VARCHAR(10),
    actual_actuation VARCHAR(20),
    FOREIGN KEY (attack_id) REFERENCES torpedo_attacks(id) ON DELETE CASCADE
);

-- Convoy ships table
CREATE TABLE IF NOT EXISTS convoy_ships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attack_id INT NOT NULL,
    ship_letter CHAR(1),
    ship_name VARCHAR(100),
    ship_type VARCHAR(50),
    ship_class VARCHAR(100),
    tonnage INT,
    role VARCHAR(50),
    relative_bearing INT,
    relative_range INT,
    course INT,
    speed DECIMAL(4,1),
    was_hit BOOLEAN DEFAULT FALSE,
    was_sunk BOOLEAN DEFAULT FALSE,
    icon_type VARCHAR(20),
    FOREIGN KEY (attack_id) REFERENCES torpedo_attacks(id) ON DELETE CASCADE
);

-- Narrative page index
CREATE TABLE IF NOT EXISTS narrative_page_index (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patrol INT NOT NULL,
    page INT NOT NULL,
    observation_date DATE NOT NULL,
    observation_time VARCHAR(4),
    UNIQUE KEY unique_patrol_page (patrol, page),
    INDEX idx_patrol (patrol),
    INDEX idx_date (observation_date)
);

-- Ship contacts table
CREATE TABLE IF NOT EXISTS ship_contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patrol INT NOT NULL,
    contact_date DATE NOT NULL,
    contact_time TIME,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    ship_type VARCHAR(100),
    ship_name VARCHAR(100),
    tonnage INT,
    description TEXT,
    action_taken TEXT,
    result VARCHAR(50),
    pdf_page INT
);

-- Aircraft contacts table
CREATE TABLE IF NOT EXISTS aircraft_contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patrol INT NOT NULL,
    contact_date DATE NOT NULL,
    contact_time TIME,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    aircraft_type VARCHAR(100),
    description TEXT,
    action_taken TEXT,
    pdf_page INT
);

-- Position tracking table
CREATE TABLE IF NOT EXISTS positions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patrol INT NOT NULL,
    observation_date DATE NOT NULL,
    observation_time TIME,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    course INT,
    speed DECIMAL(4,1),
    notes TEXT,
    pdf_page INT
);

-- Additional indexes (only if not already defined inline)
-- These use CREATE INDEX IF NOT EXISTS pattern via stored procedure
DROP PROCEDURE IF EXISTS create_index_if_not_exists;
DELIMITER //
CREATE PROCEDURE create_index_if_not_exists()
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = 'torpedo_attacks' AND index_name = 'idx_attacks_patrol') THEN
        CREATE INDEX idx_attacks_patrol ON torpedo_attacks(patrol);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = 'torpedo_attacks' AND index_name = 'idx_attacks_date') THEN
        CREATE INDEX idx_attacks_date ON torpedo_attacks(attack_date);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = 'torpedoes_fired' AND index_name = 'idx_torpedoes_attack') THEN
        CREATE INDEX idx_torpedoes_attack ON torpedoes_fired(attack_id);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = 'convoy_ships' AND index_name = 'idx_convoy_attack') THEN
        CREATE INDEX idx_convoy_attack ON convoy_ships(attack_id);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = 'ship_contacts' AND index_name = 'idx_ship_contacts_patrol') THEN
        CREATE INDEX idx_ship_contacts_patrol ON ship_contacts(patrol);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = 'aircraft_contacts' AND index_name = 'idx_aircraft_contacts_patrol') THEN
        CREATE INDEX idx_aircraft_contacts_patrol ON aircraft_contacts(patrol);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = 'positions' AND index_name = 'idx_positions_patrol') THEN
        CREATE INDEX idx_positions_patrol ON positions(patrol);
    END IF;
END //
DELIMITER ;
CALL create_index_if_not_exists();
DROP PROCEDURE IF EXISTS create_index_if_not_exists;

-- Grant permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON cod.* TO 'codpatrols'@'localhost' IDENTIFIED BY 'your_password';
-- FLUSH PRIVILEGES;

SELECT 'Database cod created successfully!' AS status;
