# Test Case Management System

[中文版](README_zh.md)

A modern test case management system built with Flask and Vue 3, supporting Excel file batch upload, project management, and test case viewing functionalities.

## Project Features

### Core Functionality
- Project Management: Create, edit, and delete projects with descriptions and maintainer information
- Excel Batch Upload: Support for .xlsx format file uploads with intelligent Excel content parsing
- Duplicate Detection: Automatic detection of duplicates within files and in the database
- Smart Import: Selective import support with ability to assign new IDs to duplicate cases
- Test Case Viewing: View associated test cases by project with detailed case information display
- Responsive Interface: Modern UI design with sidebar navigation support

### Technical Features
- Separation of Frontend and Backend: Flask RESTful API with Vue 3 SPA
- Database Support: MySQL database with support for complex queries and associations
- File Processing: Excel file parsing and validation capabilities
- Error Handling: Comprehensive exception handling with user-friendly error messages
- Component Communication: Event-based inter-component communication mechanism

## Technology Stack

### Backend
- Python 3.8+
- Flask: Web framework
- Flask-CORS: Cross-origin support
- Flask-MySQLdb: MySQL database connection
- openpyxl: Excel file processing
- Werkzeug: File upload handling

### Frontend
- Vue 3: Progressive JavaScript framework
- Vue Router: Routing management
- Element Plus: UI component library
- Axios: HTTP client
- Vite: Build tool

### Database
- MySQL 5.7+: Relational database

## Project Structure

```
JoinTestCase/
├── backend/                 # Backend code
│   ├── app.py              # Flask application main file
│   ├── models/             # Data models
│   │   ├── __init__.py
│   │   └── db.py          # Database connection
│   ├── routes/             # Routing modules
│   │   ├── __init__.py
│   │   ├── project.py     # Project management routes
│   │   ├── test_case.py   # Test case routes
│   │   └── upload.py      # File upload routes
│   └── uploads/           # Uploaded file storage directory
├── frontend/              # Frontend code
│   ├── src/
│   │   ├── api/           # API interfaces
│   │   │   └── case.js    # Test case related APIs
│   │   ├── assets/        # Static resources
│   │   ├── components/    # Vue components
│   │   ├── views/         # Page components
│   │   │   ├── ManageCase.vue    # Project management page
│   │   │   └── UploadCase.vue    # Test case upload page
│   │   ├── App.vue        # Root component
│   │   ├── main.js        # Application entry point
│   │   └── router.js      # Routing configuration
│   ├── index.html         # HTML template
│   ├── package.json       # Dependency configuration
│   └── vite.config.js     # Vite configuration
├── config.py              # Database configuration
├── db_init.sql           # Database initialization script
├── read_excel.py         # Excel reading tool
└── 登录测试用例.xlsx      # Sample Excel file
```

## Database Design

### Core Table Structures

#### projects table (Project table)
```sql
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    maintainers VARCHAR(255) DEFAULT ''
);
```

#### test_cases table (Test case table)
```sql
CREATE TABLE test_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    case_id VARCHAR(64) NOT NULL,
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

-- Add unique constraint within project to ensure case_id uniqueness within the same project
ALTER TABLE test_cases ADD UNIQUE INDEX unique_case_id_per_project (project_id, case_id);
```

#### project_cases table (Project-test case association table)
```sql
CREATE TABLE project_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    test_case_id INT,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (test_case_id) REFERENCES test_cases(id)
);
```

## Quick Start

### Environment Requirements
- Python 3.8+
- Node.js 20.19.0+
- MySQL 5.7+

### 1. Clone the Project
```bash
git clone <repository-url>
cd JoinTestCase
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
pip install flask flask-cors flask-mysqldb openpyxl werkzeug
```

#### Database Configuration
1. Create MySQL database
```sql
CREATE DATABASE testcase_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Modify database configuration in `config.py`
```python
class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'your_username'
    MYSQL_PASSWORD = 'your_password'
    MYSQL_DB = 'testcase_manager'
    MYSQL_CURSORCLASS = 'DictCursor'
```

3. Initialize database
```bash
mysql -u your_username -p testcase_manager < db_init.sql
```

#### Start Backend Service
```bash
cd backend
python app.py
```
Backend service will start at `http://localhost:5000`

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### Start Development Server
```bash
npm run dev
```
Frontend application will start at `http://localhost:5173`

## Usage Instructions

### Project Management
1. Create Project: Click the "Create Project" button and fill in project name, description, and maintainers
2. Edit Project: Click the "Edit" button in the project list to modify project information
3. Delete Project: Click the "Delete" button and confirm to delete the project (also deletes associated test cases)

### Test Case Upload
1. Select Project: Choose the project to import test cases into on the upload page
2. Upload File: Click the "Select File" button and choose an Excel file in .xlsx format
3. Preview Data: The system will automatically parse the Excel content and display a preview
4. Handle Duplicates: 
   - The system automatically detects duplicate case IDs
   - Duplicate cases will be highlighted with a red background
   - New IDs can be assigned to duplicate cases
5. Select Import: Check the cases to import and click "Import Selected Cases"

### Test Case Viewing
1. View Project Cases: Click the "View Cases" button on the project management page
2. View Case Details: Click the "View" button in the case list to see complete case information

## API Interfaces

### Project Management
- `GET /project` - Get all projects
- `POST /project` - Create a new project
- `PUT /project/{id}` - Update a project
- `DELETE /project/{id}` - Delete a project
- `GET /project/{id}/testcases` - Get test cases associated with a project

### File Upload
- `POST /upload_case` - Upload Excel file and parse
- `POST /import_case` - Import selected test cases

## UI Features

### Design Style
- Modern UI: Modern interface design based on Element Plus
- Responsive Layout: Adapts to different screen sizes
- Sidebar Navigation: Clear navigation structure
- Card Layout: Well-organized information hierarchy

### Interaction Experience
- Smart Tables: Adaptive column widths with sorting and filtering support
- Modal Operations: Modal dialog-based create, update, and delete operations
- Real-time Feedback: Immediate feedback on operations
- Error Messages: User-friendly error information display

## Function Details

### Excel File Processing
- Format Support: Supports only .xlsx format
- Column Mapping: Automatically identifies Excel headers and maps to database fields
- Data Cleaning: Automatically handles null values and special characters
- Duplicate Detection: Intelligent detection of duplicates within files and in the database

### Data Validation
- File Format Validation: Ensures uploaded files are valid Excel format
- Data Integrity: Validates the presence of required fields
- ID Uniqueness: Ensures test case ID uniqueness

### Error Handling
- File Upload Errors: Handles file format errors and upload failures
- Database Errors: Handles database connection and operation exceptions
- Network Errors: Handles API request timeouts and network exceptions

## Deployment Instructions

### Production Deployment
1. Backend Deployment: Deploy Flask application using Gunicorn or uWSGI
2. Frontend Build: Run `npm run build` to build production version
3. Static File Serving: Use Nginx to serve frontend static files
4. Database Optimization: Configure MySQL performance parameters and indexes

### Environment Variable Configuration
```bash
# Database configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=testcase_manager

# Flask configuration
FLASK_ENV=production
FLASK_SECRET_KEY=your_secret_key
```

## Contribution Guidelines

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Changelog

### v1.0.0 (2025-08-01)
- Basic project management functionality
- Excel file upload and parsing
- Test case batch import
- Duplicate data detection and handling
- Responsive web interface

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Contact

For issues or suggestions, please contact through the following channels:
- Project Issues: [GitHub Issues](https://github.com/your-repo/issues)
- Email: maz9366@163.com

---

Note: Ensure to modify default database passwords and other sensitive configuration information in production environments.