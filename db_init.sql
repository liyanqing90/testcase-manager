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
    case_id VARCHAR(64) NOT NULL UNIQUE,
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
-- 创建 project_cases 表
CREATE TABLE IF NOT EXISTS project_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    test_case_id INT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id)
);