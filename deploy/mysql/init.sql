# MySQL 初始化脚本
CREATE TABLE IF NOT EXISTS skills (
    id          VARCHAR(36)  PRIMARY KEY,
    name        VARCHAR(64)  NOT NULL UNIQUE,
    version     VARCHAR(16)  NOT NULL DEFAULT '0.1.0',
    author      VARCHAR(64)  NOT NULL,
    description TEXT         NOT NULL,
    tags        JSON         NOT NULL,
    downloads   INT          DEFAULT 0,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_author (author),
    INDEX idx_downloads (downloads),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
