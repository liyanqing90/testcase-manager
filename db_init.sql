-- 创建 projects 表
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    maintainers VARCHAR(255) DEFAULT ''
);

-- 创建 test_cases 表
CREATE TABLE IF NOT EXISTS test_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_id VARCHAR(200) NOT NULL,
    title VARCHAR(255),
    description TEXT,
    preconditions TEXT,
    steps TEXT,
    expected_results TEXT,
    priority VARCHAR(50),
    category VARCHAR(100),
    status VARCHAR(50),
    created_at DATETIME,
    updated_at DATETIME,
    created_by VARCHAR(100),
    last_updated_by VARCHAR(100),
    project_id INT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- 添加项目内唯一约束，确保同一项目内case_id唯一
ALTER TABLE test_cases ADD UNIQUE INDEX unique_case_id_per_project (project_id, case_id);

-- 创建 project_cases 表
CREATE TABLE IF NOT EXISTS project_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    test_case_id INT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id)
);

-- 创建AI生成历史记录表
CREATE TABLE `ai_test_generation_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_types` json DEFAULT NULL,
  `priority_distribution` json DEFAULT NULL,
  `total_cases` int(11) DEFAULT '0',
  `functional_test_count` int(11) DEFAULT '0',
  `api_test_count` int(11) DEFAULT '0',
  `ui_auto_test_count` int(11) DEFAULT '0',
  `estimated_file_size` bigint(20) DEFAULT NULL,
  `generated_at` datetime DEFAULT NULL,
  `filename` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_filename` (`filename`),
  KEY `idx_generated_at` (`generated_at`),
  KEY `idx_filename` (`filename`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建AI配置表
CREATE TABLE IF NOT EXISTS `ai_configs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model_type` varchar(50) NOT NULL COMMENT 'AI模型类型',
  `api_key` text NOT NULL COMMENT 'AI模型API密钥',
  `model_url` text NOT NULL COMMENT 'AI模型URL地址',
  `model_version` varchar(100) NOT NULL COMMENT 'AI模型版本',
  `prompt_price_per_1k` DECIMAL(10,6) DEFAULT 0.001 COMMENT '每1000个prompt token的价格',
  `completion_price_per_1k` DECIMAL(10,6) DEFAULT 0.002 COMMENT '每1000个completion token的价格',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
