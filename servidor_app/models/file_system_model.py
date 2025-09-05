# servidor_app/models/file_system_model.py
import os
import datetime
import zipfile
from io import BytesIO
from werkzeug.utils import secure_filename
from ..services.optimization_service import performance_optimizer
from .. import db
from .file_metadata_model import FileMetadata

class FileSystemModel:
    """
    Gerencia todas as operações do sistema de arquivos para a aplicação.
    """
    def __init__(self, root_dir):
        if not os.path.isdir(root_dir):
            raise FileNotFoundError(f"O diretório raiz especificado não existe: {root_dir}")
        self.root_dir = root_dir
        self.optimizer = performance_optimizer

    def _format_size(self, size_bytes):
        if size_bytes is None:
            return "N/A"
        if size_bytes >= 1024**3:
            return f"{round(size_bytes / (1024**3), 2)} GB"
        elif size_bytes >= 1024**2:
            return f"{round(size_bytes / (1024**2), 2)} MB"
        elif size_bytes >= 1024:
            return f"{round(size_bytes / 1024, 2)} KB"
        else:
            return f"{size_bytes} B"

    def get_folder_size(self, path):
        from ..services.cache_service import cache

        cache_key = f"folder_size_{path}"

        cached_size = cache.get(cache_key)
        if cached_size:
            return cached_size

        # Usar otimizador para cálculo assíncrono
        def calculate_size():
            try:
                total_size = self.optimizer.calculate_directory_size_optimized(path)
                formatted_size = self._format_size(total_size)
                cache.set(cache_key, formatted_size, ttl_seconds=300)
            except (PermissionError, FileNotFoundError):
                cache.set(cache_key, "N/A", ttl_seconds=300)

        # Iniciar cálculo otimizado em thread separada
        import threading
        thread = threading.Thread(target=calculate_size)
        thread.daemon = True
        thread.start()

        # Retornar mensagem indicando que está calculando
        return "calculando..."
    
    def list_directory(self, sub_path='', page=1, per_page=50):
        full_path = os.path.join(self.root_dir, sub_path)

        if not os.path.abspath(full_path).startswith(os.path.abspath(self.root_dir)):
            raise PermissionError("Acesso negado.")

        if not os.path.exists(full_path):
            raise FileNotFoundError("Caminho não encontrado.")

        items = sorted(os.listdir(full_path))
        filtered_items = [item for item in items if not item.startswith('.')]

        # Calcular paginação
        total_items = len(filtered_items)
        total_pages = (total_items + per_page - 1) // per_page  # Ceiling division
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_items = filtered_items[start_index:end_index]

        result_list = []

        for item in paginated_items:
            item_path = os.path.join(full_path, item)
            is_dir = os.path.isdir(item_path)

            # AJUSTE: Coleta ambas as datas, de modificação e de criação.
            modified_at = datetime.datetime.fromtimestamp(os.path.getmtime(item_path)).strftime('%d/%m/%Y %H:%M')
            created_at = datetime.datetime.fromtimestamp(os.path.getctime(item_path)).strftime('%d/%m/%Y %H:%M')

            # Get file metadata from database
            rel_path = os.path.join(sub_path, item).replace('\\', '/')
            metadata = FileMetadata.query.filter_by(path=rel_path).first()

            created_by = metadata.created_by.username if metadata and metadata.created_by else None
            updated_by = metadata.updated_by.username if metadata and metadata.updated_by else None

            item_data = {
                'nome': item,
                'path': rel_path,
                'is_dir': is_dir,
                'modified_at': modified_at,
                'created_at': created_at,
                'created_by': created_by,
                'updated_by': updated_by,
            }

            if is_dir:
                try:
                    contents = [name for name in os.listdir(item_path) if not name.startswith('.')]
                    item_data['file_count'] = sum(1 for name in contents if os.path.isfile(os.path.join(item_path, name)))
                    item_data['folder_count'] = sum(1 for name in contents if os.path.isdir(os.path.join(item_path, name)))
                except (PermissionError, FileNotFoundError):
                    item_data['file_count'] = "N/A"
                    item_data['folder_count'] = "N/A"
                item_data['size'] = 'calculando...'
            else:
                size_bytes = os.path.getsize(item_path)
                item_data['size'] = self._format_size(size_bytes)
                item_data['size_bytes'] = size_bytes
                item_data['type'] = item.split('.')[-1].lower() if '.' in item else 'file'

            result_list.append(item_data)

        parent_path = os.path.dirname(sub_path).replace('\\', '/') if sub_path else None

        pagination_info = {
            'page': page,
            'per_page': per_page,
            'total_items': total_items,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1,
            'next_page': page + 1 if page < total_pages else None,
            'prev_page': page - 1 if page > 1 else None
        }

        return result_list, sub_path, parent_path, pagination_info

    def search(self, query, page=1, per_page=50):
        results = []
        query_lower = query.lower()
        for root, dirs, files in os.walk(self.root_dir):
            for d in dirs:
                if query_lower in d.lower():
                    results.append(os.path.join(root, d))
            for f in files:
                if query_lower in f.lower():
                    results.append(os.path.join(root, f))
        # Paginação
        start = (page - 1) * per_page
        end = start + per_page
        paginated = results[start:end]
        return paginated, len(results)

    def create_zip_from_folder(self, folder_path):
        full_path = os.path.join(self.root_dir, folder_path)
        if not os.path.isdir(full_path):
            return None, None
            
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(full_path):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]
                
                for file in files:
                    file_full_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_full_path, full_path)
                    zf.write(file_full_path, arcname)

        memory_file.seek(0)
        download_name = f"{os.path.basename(full_path)}.zip"
        return memory_file, download_name

    def save_file(self, file, sub_path='', user=None):
        full_path = os.path.join(self.root_dir, sub_path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(self.root_dir)):
            raise PermissionError("Acesso negado.")

        filename = secure_filename(file.filename)
        file_path = os.path.join(full_path, filename)
        file.save(file_path)

        # Save or update file metadata with user info
        if user:
            rel_path = os.path.join(sub_path, filename).replace('\\', '/')
            metadata = FileMetadata.query.filter_by(path=rel_path).first()
            if not metadata:
                metadata = FileMetadata(path=rel_path, created_by=user, updated_by=user)
                db.session.add(metadata)
            else:
                metadata.updated_by = user
            db.session.commit()

        return filename

    def create_folder(self, folder_name, sub_path='', user=None):
        full_path = os.path.join(self.root_dir, sub_path)
        if not os.path.abspath(full_path).startswith(os.path.abspath(self.root_dir)):
            raise PermissionError("Acesso negado.")

        new_folder_path = os.path.join(full_path, secure_filename(folder_name))

        if os.path.exists(new_folder_path):
            raise FileExistsError(f'O caminho "{new_folder_path}" já existe.')

        os.makedirs(new_folder_path)

        # Save or update folder metadata with user info
        if user:
            rel_path = os.path.join(sub_path, secure_filename(folder_name)).replace('\\', '/')
            metadata = FileMetadata.query.filter_by(path=rel_path).first()
            if not metadata:
                metadata = FileMetadata(path=rel_path, created_by=user, updated_by=user)
                db.session.add(metadata)
            else:
                metadata.updated_by = user
            db.session.commit()

    def move_item(self, source_path, destination_path, user=None):
        """
        Move a file or folder from source_path to destination_path
        """
        full_source = os.path.join(self.root_dir, source_path)
        full_destination = os.path.join(self.root_dir, destination_path)

        # Security check
        if not (os.path.abspath(full_source).startswith(os.path.abspath(self.root_dir)) and
                os.path.abspath(full_destination).startswith(os.path.abspath(self.root_dir))):
            raise PermissionError("Acesso negado.")

        if not os.path.exists(full_source):
            raise FileNotFoundError(f"Item não encontrado: {source_path}")

        # Check if destination already exists
        if os.path.exists(full_destination):
            raise FileExistsError(f"Destino já existe: {destination_path}")

        # Move the item
        os.rename(full_source, full_destination)

        # Update metadata if user is provided
        if user:
            # Update the path in metadata
            metadata = FileMetadata.query.filter_by(path=source_path).first()
            if metadata:
                metadata.path = destination_path
                metadata.updated_by = user
                db.session.commit()

            # If it's a directory, update all child paths
            if os.path.isdir(full_destination):
                old_prefix = source_path + '/' if not source_path.endswith('/') else source_path
                new_prefix = destination_path + '/' if not destination_path.endswith('/') else destination_path

                # Update all child metadata paths
                child_metadata = FileMetadata.query.filter(FileMetadata.path.like(old_prefix + '%')).all()
                for child in child_metadata:
                    child.path = child.path.replace(old_prefix, new_prefix, 1)
                    child.updated_by = user
                db.session.commit()
