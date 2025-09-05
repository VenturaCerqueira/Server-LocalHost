# TODO: Implement MySQL Production to Local Sync Function

- [x] Add `sync_mysql_production_to_local` function to servidor_app/services/database_service.py
- [x] Implement mysqldump from production using provided credentials
- [x] Implement mysql restore to local XAMPP database
- [x] Handle errors and logging
- [x] Test the function (optional, if user provides test DB) - Added API endpoint /api/sync_db/<db_name> for testing
- [x] Fixed config access issue - Changed from attribute access to dictionary access for Flask config

# TODO: Adjust Sistemas Page Git Pull Functionality

- [x] Remove "Lista" button from sistemas.html
- [x] Remove "Atualizar Projeto (Git Pull)" button from sistemas.html
- [x] Update JavaScript to handle per-folder git pull buttons
- [x] Open modal showing git pull process for selected folder
- [x] Notify user of success or failure in modal
- [x] Test the updated functionality
