# Servidor LocalHost - Flask Application

This is a Flask-based web application for local server management, database analysis, and file system operations.

## Project Structure

- `entrypoints/`: Entry points and scripts
  - `run_flask.py`: Main Flask application runner
  - `run.py`: Alternative runner
  - `create_roles_fixed.py`: Role creation script
- `servidor_app/`: Main application package
  - `controllers/`: Flask blueprints for different domains
  - `models/`: Database models
  - `services/`: Business logic services
  - `static/`: CSS, JS, images
  - `templates/`: Jinja2 templates organized by domain
  - `tests/`: Unit and integration tests
- `scripts/`: Utility scripts organized by category
  - `database/`: Database setup and maintenance
  - `user/`: User management
  - `system/`: System configuration
- `docs/`: Documentation and project files
- `diagrams/`: Database and system diagrams

## Running the Application

### Option 1: Flask Runner
```bash
python entrypoints/run_flask.py
```

### Option 2: Alternative Runner
```bash
python entrypoints/run.py
```

The application will start on `http://localhost:5000` by default.

## Configuration

Configuration is handled in `servidor_app/config.py`. Environment variables can be set in a `.env` file.

## Database

The application uses SQLite by default. Database files are stored in the `servidor_app/` directory.

## Testing

Run tests from the `servidor_app/tests/` directory.

## Scripts

Utility scripts are organized in the `scripts/` directory by category. Run them with Python from the project root.
