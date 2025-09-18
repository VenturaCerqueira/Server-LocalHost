from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify, session, make_response
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from servidor_app.models.user_model import User
from servidor_app.models.role_model import Role
from servidor_app.models.system_link_model import SystemLink
from servidor_app.services.server_info_service import get_server_info
import servidor_app.services.database_service as db_service
from servidor_app.services.metrics_service import metrics_service
from servidor_app.services.optimization_service import performance_optimizer
from servidor_app.controllers.permissions import require_access, AREAS
from servidor_app import db
import json
import graphviz
import os
import pymysql
import time
import traceback
import html
from decimal import Decimal



def lower_keys(d):
    if isinstance(d, dict):
        return {str(k).lower(): v for k, v in d.items()}
    return d

def format_number(num):
    if num is None:
        return "0"
    try:
        return f"{int(num):,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(num)

def decimal_to_float(obj):
    from decimal import Decimal
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(decimal_to_float(item) for item in obj)
    return obj

def get_table_color(table_name):
    table_name = table_name.lower()
    if any(word in table_name for word in ['user', 'usuario', 'auth', 'login', 'account', 'profile']):
        return '#E3F2FD'
    elif any(word in table_name for word in ['log', 'audit', 'history', 'track', 'visit']):
        return '#FFF3E0'
    elif any(word in table_name for word in ['config', 'setting', 'parametro', 'system', 'admin', 'option']):
        return '#F5F5F5'
    elif ('_' in table_name and len(table_name.split('_')) >= 2) or \
         any(word in table_name for word in ['relacionamento', 'pivot', 'junction']):
        return '#E8F5E9'
    else:
        return '#FFE0E6'

def get_table_category(table_name):
    table_name = table_name.lower()
    if any(word in table_name for word in ['user', 'usuario', 'auth', 'login', 'account', 'profile']):
        return 'authentication'
    elif any(word in table_name for word in ['log', 'audit', 'history', 'track', 'visit']):
        return 'logging'
    elif any(word in table_name for word in ['config', 'setting', 'parametro', 'system', 'admin', 'option']):
        return 'configuration'
    elif ('_' in table_name and len(table_name.split('_')) >= 2 and
          not any(kw in table_name for kw in ['user', 'log', 'config', 'parametro'])):
        return 'relationship'
    else:
        return 'business'

def get_column_icon(column_type):
    column_type = column_type.lower()
    if 'int' in column_type or 'bigint' in column_type or 'smallint' in column_type:
        return 'bi-hash'
    elif 'varchar' in column_type or 'text' in column_type or 'char' in column_type:
        return 'bi-textarea-t'
    elif 'date' in column_type or 'datetime' in column_type or 'timestamp' in column_type:
        return 'bi-calendar'
    elif 'decimal' in column_type or 'float' in column_type or 'double' in column_type:
        return 'bi-calculator'
    elif 'bool' in column_type or 'tinyint(1)' in column_type:
        return 'bi-toggle-on'
    else:
        return 'bi-code'



main_bp = Blueprint('main', __name__)



@main_bp.route('/')
@login_required
def index():
    # Use FileSystemModel to get directory listing with pagination
    from servidor_app.models.file_system_model import FileSystemModel

    current_path = request.args.get('path', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    fs_model = FileSystemModel(current_app.config['ROOT_DIR'])
    try:
        pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
    except Exception as e:
        flash(f"Erro ao listar diretório: {e}", "danger")
        pastas = []
        pagination = None
        parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('index.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@main_bp.route('/browse/<path:sub_path>')
@login_required
def browse(sub_path):
    # Use FileSystemModel to get directory listing with pagination
    from servidor_app.models.file_system_model import FileSystemModel

    current_path = sub_path
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    fs_model = FileSystemModel(current_app.config['ROOT_DIR'])

    # Check if folder is secure and always prompt for password
    if fs_model.is_folder_secure(current_path):
        # Always redirect to password prompt page
        return redirect(url_for('main.secure_folder_password', folder_path=current_path))

    try:
        pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
    except Exception as e:
        flash(f"Erro ao listar diretório: {e}", "danger")
        pastas = []
        pagination = None
        parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('index.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@main_bp.route('/dados_pessoais')
@login_required
@require_access(AREAS['dados_pessoais'])
def dados_pessoais():
    # Dados Pessoais management page
    from servidor_app.models.file_system_model import FileSystemModel
    import os

    current_path = request.args.get('path', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    # Use a specific directory for dados pessoais or create one
    root_dir = os.path.join(current_app.config['ROOT_DIR'], 'Dados_Pessoais')
    if not os.path.exists(root_dir):
        os.makedirs(root_dir, exist_ok=True)

    fs_model = FileSystemModel(root_dir)
    try:
        full_path = os.path.join(root_dir, current_path)
        if not os.path.exists(full_path):
            flash(f"Diretório não encontrado: {full_path}", "danger")
            pastas = []
            pagination = None
            parent_path = None
        else:
            pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
    except Exception as e:
        flash(f"Erro ao listar diretório: {e}", "danger")
        pastas = []
        pagination = None
        parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('documentos_privado.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@main_bp.route('/databases')
@login_required
@require_access(AREAS['banco_dados'])
def databases():
    # Database management page with MySQL databases from XAMPP and production
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    mysql_dbs_local = db_service.list_local_mysql_databases(current_app.config)
    mysql_dbs_prod = db_service.list_production_mysql_databases(current_app.config)
    return render_template('databases.html', dados_servidor=dados_servidor, mysql_dbs_local=mysql_dbs_local, mysql_dbs_prod=mysql_dbs_prod)

@main_bp.route('/databases/download/<db_name>')
@login_required
@require_access(AREAS['banco_dados'])
def download_database(db_name):
    # Download production database as SQL dump
    try:
        # Get database dump
        dump_result = db_service.dump_production_database(current_app.config, db_name)

        if not dump_result['success']:
            return jsonify({'error': dump_result['error']}), 500

        # Create response with SQL content
        response = make_response(dump_result['dump'])
        response.headers['Content-Type'] = 'application/sql'
        response.headers['Content-Disposition'] = f'attachment; filename={db_name}_{dump_result["timestamp"]}.sql'

        # Set cookie to indicate download started
        response.set_cookie('fileDownload', 'true', path='/')

        return response

    except Exception as e:
        current_app.logger.error(f"Error downloading database {db_name}: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@main_bp.route('/databases/compare/<db_name>')
@login_required
@require_access(AREAS['banco_dados'])
def compare_database(db_name):
    import os
    import pymysql
    import time
    import traceback
    import json
    import html
    from flask import render_template, current_app, request

    # Check if this is an AJAX request
    if request.headers.get('Content-Type') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        return compare_database_json(db_name)

    # Load environment variables from app config
    config = current_app.config

    # Connect to both local and production databases and compare
    local_connection = None
    prod_connection = None
    comparison_results = {}
    error_message = None

    try:
        # Connect to local MySQL database
        from servidor_app.services.database_service import get_local_mysql_connection
        local_connection = get_local_mysql_connection(config, db_name)

        # Connect to production MySQL database
        from servidor_app.services.database_service import get_production_mysql_connection
        prod_connection = get_production_mysql_connection(config, db_name)

        # Get tables from both databases
        with local_connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            local_tables = [row[f'Tables_in_{db_name}'] for row in cursor.fetchall()]

        with prod_connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            prod_tables = [row[f'Tables_in_{db_name}'] for row in cursor.fetchall()]

        # Compare tables
        missing_in_prod = [table for table in local_tables if table not in prod_tables]
        missing_in_local = [table for table in prod_tables if table not in local_tables]
        common_tables = [table for table in local_tables if table in prod_tables]

        comparison_results['tables'] = {
            'missing_in_prod': missing_in_prod,
            'missing_in_local': missing_in_local,
            'common': common_tables
        }

        # Compare columns for common tables
        column_differences = {}
        data_differences = {}

        for table in common_tables:
            # Get columns from local
            with local_connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE {table}")
                local_columns = cursor.fetchall()

            # Get columns from production
            with prod_connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE {table}")
                prod_columns = cursor.fetchall()

            # Compare columns
            local_col_names = [col['Field'] for col in local_columns]
            prod_col_names = [col['Field'] for col in prod_columns]

            missing_cols_in_prod = [col for col in local_col_names if col not in prod_col_names]
            missing_cols_in_local = [col for col in prod_col_names if col not in local_col_names]

            # Check for type differences in common columns
            type_differences = {}
            for col_name in set(local_col_names) & set(prod_col_names):
                local_col = next(col for col in local_columns if col['Field'] == col_name)
                prod_col = next(col for col in prod_columns if col['Field'] == col_name)

                if local_col['Type'] != prod_col['Type']:
                    type_differences[col_name] = {
                        'local': local_col['Type'],
                        'prod': prod_col['Type']
                    }

            if missing_cols_in_prod or missing_cols_in_local or type_differences:
                column_differences[table] = {
                    'missing_in_prod': missing_cols_in_prod,
                    'missing_in_local': missing_cols_in_local,
                    'type_differences': type_differences
                }

            # Compare row counts (simple data comparison)
            with local_connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                local_count = cursor.fetchone()['count']

            with prod_connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                prod_count = cursor.fetchone()['count']

            if local_count != prod_count:
                data_differences[table] = {
                    'local_count': local_count,
                    'prod_count': prod_count,
                    'difference': local_count - prod_count
                }

        comparison_results['columns'] = column_differences
        comparison_results['data'] = data_differences

        return render_template('database_comparison.html',
                             db_name=db_name,
                             comparison=comparison_results,
                             error=None)

    except Exception as e:
        error_message = f"Erro ao comparar bancos de dados: {str(e)}"
        current_app.logger.error(error_message)
        current_app.logger.error(traceback.format_exc())
        return render_template('database_comparison.html', error=error_message, db_name=db_name)
    finally:
        if local_connection and local_connection.open:
            local_connection.close()
        if prod_connection and prod_connection.open:
            prod_connection.close()

def compare_database_json(db_name):
    """Return JSON response for database comparison (used by AJAX requests)"""
    import os
    import pymysql
    import time
    import traceback
    import json
    import html
    from flask import current_app, jsonify

    # Load environment variables from app config
    config = current_app.config

    # Connect to both local and production databases and compare
    local_connection = None
    prod_connection = None

    try:
        # Connect to local MySQL database
        from servidor_app.services.database_service import get_local_mysql_connection
        local_connection = get_local_mysql_connection(config, db_name)

        # Connect to production MySQL database
        from servidor_app.services.database_service import get_production_mysql_connection
        prod_connection = get_production_mysql_connection(config, db_name)

        # Get tables from both databases
        with local_connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            local_tables = [row[f'Tables_in_{db_name}'] for row in cursor.fetchall()]

        with prod_connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            prod_tables = [row[f'Tables_in_{db_name}'] for row in cursor.fetchall()]

        # Compare tables
        missing_in_prod = [table for table in local_tables if table not in prod_tables]
        missing_in_local = [table for table in prod_tables if table not in local_tables]
        common_tables = [table for table in local_tables if table in prod_tables]

        # Prepare tables array for frontend
        tables_comparison = []

        # Add missing tables in production
        for table in missing_in_prod:
            tables_comparison.append({
                'name': table,
                'status': 'missing',
                'details': 'Tabela existe apenas no banco local'
            })

        # Add missing tables in local
        for table in missing_in_local:
            tables_comparison.append({
                'name': table,
                'status': 'missing',
                'details': 'Tabela existe apenas no banco de produção'
            })

        # Add common tables (initially marked as matching)
        for table in common_tables:
            tables_comparison.append({
                'name': table,
                'status': 'matching',
                'details': 'Tabela existe em ambos os bancos'
            })

        # Prepare columns and data arrays
        columns_comparison = []
        data_comparison = []

        # Compare columns for common tables
        for table in common_tables:
            # Get columns from local
            with local_connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE {table}")
                local_columns = cursor.fetchall()

            # Get columns from production
            with prod_connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE {table}")
                prod_columns = cursor.fetchall()

            # Compare columns
            local_col_names = [col['Field'] for col in local_columns]
            prod_col_names = [col['Field'] for col in prod_columns]

            missing_cols_in_prod = [col for col in local_col_names if col not in prod_col_names]
            missing_cols_in_local = [col for col in prod_col_names if col not in local_col_names]

            # Check for type differences in common columns
            type_differences = {}
            for col_name in set(local_col_names) & set(prod_col_names):
                local_col = next(col for col in local_columns if col['Field'] == col_name)
                prod_col = next(col for col in prod_columns if col['Field'] == col_name)

                if local_col['Type'] != prod_col['Type']:
                    type_differences[col_name] = {
                        'local': local_col['Type'],
                        'prod': prod_col['Type']
                    }

            # Add column differences
            for col in missing_cols_in_prod:
                columns_comparison.append({
                    'table': table,
                    'name': col,
                    'status': 'missing',
                    'details': 'Coluna existe apenas no banco local'
                })

            for col in missing_cols_in_local:
                columns_comparison.append({
                    'table': table,
                    'name': col,
                    'status': 'missing',
                    'details': 'Coluna existe apenas no banco de produção'
                })

            for col_name, types in type_differences.items():
                columns_comparison.append({
                    'table': table,
                    'name': col_name,
                    'status': 'different',
                    'details': f'Tipo diferente: Local={types["local"]}, Produção={types["prod"]}'
                })

            # If there are column differences, mark table as different
            if missing_cols_in_prod or missing_cols_in_local or type_differences:
                # Update table status
                for t in tables_comparison:
                    if t['name'] == table:
                        t['status'] = 'different'
                        t['details'] = 'Diferenças encontradas nas colunas'
                        break

            # Compare row counts (simple data comparison)
            with local_connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                local_count = cursor.fetchone()['count']

            with prod_connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                prod_count = cursor.fetchone()['count']

            if local_count != prod_count:
                data_comparison.append({
                    'table': table,
                    'local_count': local_count,
                    'production_count': prod_count,
                    'differences': abs(local_count - prod_count)
                })

                # Mark table as different if data differs
                for t in tables_comparison:
                    if t['name'] == table:
                        t['status'] = 'different'
                        t['details'] = 'Diferenças encontradas nos dados'
                        break

        # Calculate statistics
        total_tables = len(tables_comparison)
        matching_tables = len([t for t in tables_comparison if t['status'] == 'matching'])
        different_tables = len([t for t in tables_comparison if t['status'] == 'different'])
        missing_tables = len([t for t in tables_comparison if t['status'] == 'missing'])

        comparison_results = {
            'stats': {
                'tables_total': total_tables,
                'tables_matching': matching_tables,
                'tables_different': different_tables,
                'tables_missing': missing_tables
            },
            'tables': tables_comparison,
            'columns': columns_comparison,
            'data': data_comparison
        }

        return jsonify({
            'success': True,
            'comparison': comparison_results
        })

    except Exception as e:
        error_message = f"Erro ao comparar bancos de dados: {str(e)}"
        current_app.logger.error(error_message)
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': error_message
        }), 500
    finally:
        if local_connection and local_connection.open:
            local_connection.close()
        if prod_connection and prod_connection.open:
            prod_connection.close()

@main_bp.route('/databases/analyze/<db_name>')
@login_required
@require_access(AREAS['banco_dados'])
def analyze_database(db_name):
    import os
    import pymysql
    import time
    import traceback
    import json
    import html
    from flask import render_template, current_app

    # Load environment variables from app config
    config = current_app.config

    # Connect to database and gather metadata
    connection = None
    markdown_content = ""
    tables_with_details_for_diagrams_and_docs = []
    error_message = None

    try:
        from servidor_app.services.database_service import get_production_mysql_connection

        connection = get_production_mysql_connection(config, db_name)

        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name, engine, table_collation, table_comment, create_time, update_time, table_rows, ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name", (db_name,))
            tables_metadata_raw_list = cursor.fetchall()

            if not tables_metadata_raw_list:
                error_message = f"Nenhuma tabela encontrada no banco de dados '{db_name}'."
                return render_template('database_analysis.html', error=error_message, db_name=db_name)

            all_raw_table_data_for_processing = []
            for table_raw_meta_dict in tables_metadata_raw_list:
                table_meta_dict = lower_keys(table_raw_meta_dict)
                tname = table_meta_dict["table_name"]

                cursor.execute("SELECT c.column_name, c.column_type, c.column_key, c.is_nullable, c.column_default, c.column_comment, c.character_set_name, c.collation_name, kcu.referenced_table_name, kcu.referenced_column_name FROM information_schema.columns c LEFT JOIN information_schema.key_column_usage kcu ON c.table_schema = kcu.table_schema AND c.table_name = kcu.table_name AND c.column_name = kcu.column_name AND kcu.referenced_table_name IS NOT NULL WHERE c.table_schema = %s AND c.table_name = %s ORDER BY c.ordinal_position", (db_name, tname))
                columns_data_raw_list = [lower_keys(col_dict) for col_dict in cursor.fetchall()]

                # Add icon_class to columns
                for col in columns_data_raw_list:
                    col['icon_class'] = get_column_icon(col['column_type'])

                all_raw_table_data_for_processing.append({
                    "table_name": tname,
                    "table_info": decimal_to_float(table_meta_dict),
                    "columns": decimal_to_float(columns_data_raw_list)
                })

        # Create tables_data for template
        tables_data = []
        for table_bundle_dict in all_raw_table_data_for_processing:
            tname = table_bundle_dict["table_name"]
            table_info_dict = table_bundle_dict["table_info"]
            columns_list = table_bundle_dict["columns"]

            table_data = {
                "name": tname,
                "metadata": table_info_dict,
                "columns": columns_list,
                "color": get_table_color(tname),
                "category": get_table_category(tname)
            }
            tables_data.append(table_data)

        # AI Analysis Integration removed
        ai_insights = None

        # Generate markdown content for tables
        markdown_content = f"# Documentação do Banco de Dados: `{db_name}`\n\n"
        for table_bundle_dict in all_raw_table_data_for_processing:
            tname = table_bundle_dict["table_name"]
            table_info_dict = table_bundle_dict["table_info"]
            columns_list = table_bundle_dict["columns"]

            table_md_section = f"## Tabela: `{tname}`\n\n"
            table_md_section += f"- Motor (Engine): `{table_info_dict.get('engine', 'N/A')}`\n"
            table_md_section += f"- Total de Linhas (aprox.): {format_number(table_info_dict.get('table_rows', 0))}\n"
            table_md_section += f"- Tamanho em Disco (aprox.): {float(table_info_dict.get('size_mb', 0.0)):.2f} MB\n"
            if table_info_dict.get('table_collation'):
                table_md_section += f"- Collation: `{table_info_dict.get('table_collation')}`\n"
            if table_info_dict.get('create_time'):
                table_md_section += f"- Data de Criação: {table_info_dict.get('create_time')}\n"
            if table_info_dict.get('update_time'):
                table_md_section += f"- Última Atualização: {table_info_dict.get('update_time')}\n"
            if table_info_dict.get('table_comment'):
                table_md_section += f"- Comentário da Tabela: {html.escape(str(table_info_dict['table_comment']))}\n"
            table_md_section += "\n"

            # Group columns by type
            pk_columns = [col for col in columns_list if col.get('column_key') == 'PRI']
            fk_columns = [col for col in columns_list if col.get('referenced_table_name')]
            other_columns = [col for col in columns_list if col not in pk_columns and col not in fk_columns]

            def add_column_table(title, cols):
                if not cols:
                    return ""
                md = f"#### {title}\n| Nome da Coluna | Tipo de Dado | Charset | Collation | Chave | Nulo? | Padrão | Comentário da Coluna | Referência FK |\n|---|---|---|---|---|---|---|---|---|\n"
                for col in cols:
                    fk_info = f"→ `{html.escape(str(col['referenced_table_name']))}`.`{html.escape(str(col.get('referenced_column_name', '')))}`" if col.get('referenced_table_name') else ''
                    md += f"| `{html.escape(str(col['column_name']))}` | `{html.escape(str(col['column_type']))}` | {html.escape(str(col.get('character_set_name', '')))} | {html.escape(str(col.get('collation_name', '')))} | {html.escape(str(col.get('column_key', '')))} | {html.escape(str(col.get('is_nullable', '')))} | {html.escape(str(col.get('column_default', '')))} | {html.escape(str(col.get('column_comment', '')))} | {fk_info} |\n"
                md += "\n"
                return md


            table_md_section += "\n---\n\n"
            markdown_content += table_md_section

        # Convert markdown to HTML
        import markdown
        markdown_html = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])





        # Save files to static/diagrams directory
        static_diagrams_path = os.path.join(current_app.root_path, 'static', 'diagrams')
        if not os.path.exists(static_diagrams_path):
            os.makedirs(static_diagrams_path, exist_ok=True)

        # Save markdown content
        md_file_path = os.path.join(static_diagrams_path, f"{db_name}_schema_documentation.md")
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Save ERD diagram as PNG and SVG
        erd_png_path = os.path.join(static_diagrams_path, f"{db_name}_ERD")
        erd_svg_path = os.path.join(static_diagrams_path, f"{db_name}_ERD.svg")
        dot = graphviz.Digraph(comment=f"ERD for {db_name}")
        for table_bundle in all_raw_table_data_for_processing:
            table_name = table_bundle["table_name"]
            table_info = table_bundle["table_info"]
            label = f"{table_name}\\n{format_number(table_info.get('table_rows', 0))} rows\\n{float(table_info.get('size_mb', 0.0)):.2f} MB"
            dot.node(table_name, label=label, shape='box')
        for table_bundle in all_raw_table_data_for_processing:
            table_name = table_bundle["table_name"]
            for col in table_bundle["columns"]:
                if col.get('referenced_table_name'):
                    dot.edge(col['referenced_table_name'], table_name, label=col['column_name'])
        dot.render(erd_png_path, format='png', cleanup=True)
        with open(erd_svg_path, 'wb') as f:
            f.write(dot.pipe(format='svg'))

        # Save flow diagram as PNG and SVG
        flow_png_path = os.path.join(static_diagrams_path, f"{db_name}_DataFlow")
        flow_svg_path = os.path.join(static_diagrams_path, f"{db_name}_DataFlow.svg")
        dot_flow = graphviz.Digraph(comment=f"Data Flow for {db_name}")
        categories = {}
        for table_bundle in all_raw_table_data_for_processing:
            cat = get_table_category(table_bundle["table_name"])
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(table_bundle["table_name"])
        for cat, tables in categories.items():
            with dot_flow.subgraph(name=f'cluster_{cat}') as sub:
                sub.attr(label=cat)
                for table in tables:
                    sub.node(table, table)
        for table_bundle in all_raw_table_data_for_processing:
            table_name = table_bundle["table_name"]
            for col in table_bundle["columns"]:
                if col.get('referenced_table_name'):
                    dot_flow.edge(col['referenced_table_name'], table_name, label=col['column_name'])
        dot_flow.render(flow_png_path, format='png', cleanup=True)
        with open(flow_svg_path, 'wb') as f:
            f.write(dot_flow.pipe(format='svg'))

        # Generate URLs for template
        erd_png_url = f"/static/diagrams/{db_name}_ERD.png"
        erd_svg_url = f"/static/diagrams/{db_name}_ERD.svg"
        flow_png_url = f"/static/diagrams/{db_name}_DataFlow.png"
        flow_svg_url = f"/static/diagrams/{db_name}_DataFlow.svg"
        md_url = f"/static/diagrams/{db_name}_schema_documentation.md"

        return render_template('database_analysis.html',
                             db_name=db_name,
                             markdown_html=markdown_html,
                             markdown_url=md_url,
                             erd_png_url=erd_png_url,
                             erd_svg_url=erd_svg_url,
                             flow_png_url=flow_png_url,
                             flow_svg_url=flow_svg_url,
                             tables=tables_data,
                             ai_insights=ai_insights,
                             error=None)

    except Exception as e:
        error_message = f"Erro ao analisar banco de dados: {str(e)}"
        current_app.logger.error(error_message)
        current_app.logger.error(traceback.format_exc())
        return render_template('database_analysis.html', error=error_message, db_name=db_name)
    finally:
        if connection and connection.open:
            connection.close()

@main_bp.route('/databases/tables/<db_name>')
@login_required
@require_access(AREAS['banco_dados'])
def database_tables(db_name):
    import os
    import pymysql
    import time
    import traceback
    import json
    import html
    from flask import render_template, current_app

    # Load environment variables from app config
    config = current_app.config

    # Connect to database and gather metadata
    connection = None
    tables_data = []
    error_message = None

    try:
        from servidor_app.services.database_service import get_production_mysql_connection

        connection = get_production_mysql_connection(config, db_name)

        with connection.cursor() as cursor:
            cursor.execute("SELECT table_name, engine, table_collation, table_comment, create_time, update_time, table_rows, ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb FROM information_schema.tables WHERE table_schema = %s ORDER BY table_name", (db_name,))
            tables_metadata_raw_list = cursor.fetchall()

            if not tables_metadata_raw_list:
                error_message = f"Nenhuma tabela encontrada no banco de dados '{db_name}'."
                return render_template('database_tables.html', error=error_message, db_name=db_name)

            for table_raw_meta_dict in tables_metadata_raw_list:
                table_meta_dict = lower_keys(table_raw_meta_dict)
                tname = table_meta_dict["table_name"]

                cursor.execute("SELECT c.column_name, c.column_type, c.column_key, c.is_nullable, c.column_default, c.column_comment, c.character_set_name, c.collation_name, kcu.referenced_table_name, kcu.referenced_column_name FROM information_schema.columns c LEFT JOIN information_schema.key_column_usage kcu ON c.table_schema = kcu.table_schema AND c.table_name = kcu.table_name AND c.column_name = kcu.column_name AND kcu.referenced_table_name IS NOT NULL WHERE c.table_schema = %s AND c.table_name = %s ORDER BY c.ordinal_position", (db_name, tname))
                columns_data_raw_list = [lower_keys(col_dict) for col_dict in cursor.fetchall()]

                table_data = {
                    "name": tname,
                    "metadata": decimal_to_float(table_meta_dict),
                    "columns": decimal_to_float(columns_data_raw_list),
                    "color": get_table_color(tname),
                    "category": get_table_category(tname)
                }
                tables_data.append(table_data)

        return render_template('database_tables.html', db_name=db_name, tables=tables_data, error=None)

    except Exception as e:
        error_message = f"Erro ao analisar banco de dados: {str(e)}"
        current_app.logger.error(error_message)
        current_app.logger.error(traceback.format_exc())
        return render_template('database_tables.html', error=error_message, db_name=db_name)
    finally:
        if connection and connection.open:
            connection.close()

@main_bp.route('/sistemas')
@login_required
@require_access(AREAS['sistemas'])
def sistemas():
    # Systems management page pointing to XAMPP htdocs
    from servidor_app.models.file_system_model import FileSystemModel
    import os

    current_path = request.args.get('path', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    root_dir = current_app.config['SISTEMAS_DIR']
    fs_model = FileSystemModel(root_dir)
    try:
        full_path = os.path.join(root_dir, current_path)
        if not os.path.exists(full_path):
            flash(f"Diretório não encontrado: {full_path}", "danger")
            pastas = []
            pagination = None
            parent_path = None
        else:
            pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
    except Exception as e:
        flash(f"Erro ao listar diretório: {e}", "danger")
        pastas = []
        pagination = None
        parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('sistemas.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@main_bp.route('/portal')
@login_required
@require_access(AREAS['sistemas'])
def portal():
    # Portal page with blocks of system links
    links = SystemLink.query.all()
    # Group links by block
    blocks = {}
    for link in links:
        block = link.block or 'Geral'
        if block not in blocks:
            blocks[block] = []
        blocks[block].append(link)

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('portal.html', blocks=blocks, dados_servidor=dados_servidor)

@main_bp.context_processor
def inject_blocks():
    # Provide distinct blocks for use in templates like portal_add.html
    distinct_blocks = [row[0] for row in db.session.query(SystemLink.block).distinct().all() if row[0]]
    # Also include a default block 'Geral' if not present
    if 'Geral' not in distinct_blocks:
        distinct_blocks.append('Geral')
    return dict(distinct_blocks=distinct_blocks)

@main_bp.route('/portal/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
@require_access(AREAS['sistemas'])
def edit_system_link(link_id):
    link = SystemLink.query.get_or_404(link_id)

    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        block = request.form.get('block')
        icon = request.form.get('icon')

        if not name or not url:
            flash('Nome e URL são obrigatórios.', 'danger')
            return redirect(url_for('main.edit_system_link', link_id=link_id))

        link.name = name
        link.url = url
        link.block = block
        link.icon = icon

        db.session.commit()
        flash('Link atualizado com sucesso.', 'success')
        return redirect(url_for('main.portal'))

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('portal_add.html', link=link, dados_servidor=dados_servidor)

@main_bp.route('/portal/<int:link_id>/delete', methods=['POST'])
@login_required
@require_access(AREAS['sistemas'])
def delete_system_link(link_id):
    link = SystemLink.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link excluído com sucesso.', 'success')
    return redirect(url_for('main.portal'))

@main_bp.route('/portal/add', methods=['GET', 'POST'])
@login_required
@require_access(AREAS['sistemas'])
def add_system_link():
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        block = request.form.get('block')
        icon = request.form.get('icon')

        if not name or not url:
            flash('Nome e URL são obrigatórios.', 'danger')
            return redirect(url_for('main.add_system_link'))

        new_link = SystemLink(name=name, url=url, block=block, icon=icon)
        db.session.add(new_link)
        db.session.commit()
        flash('Link adicionado com sucesso.', 'success')
        return redirect(url_for('main.portal'))

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('portal_add.html', dados_servidor=dados_servidor)



@main_bp.route('/licitacoes')
@login_required
@require_access(AREAS['licitacoes'])
def licitacoes():
    # Licitações management page pointing to D:\Servidor\Licitações
    from servidor_app.models.file_system_model import FileSystemModel
    import os

    current_path = request.args.get('path', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    root_dir = current_app.config['LICITACOES_DIR']
    fs_model = FileSystemModel(root_dir)
    try:
        full_path = os.path.join(root_dir, current_path)
        if not os.path.exists(full_path):
            flash(f"Diretório não encontrado: {full_path}", "danger")
            pastas = []
            pagination = None
            parent_path = None
        else:
            pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
    except Exception as e:
        flash(f"Erro ao listar diretório: {e}", "danger")
        pastas = []
        pagination = None
        parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('licitacoes.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor)

@main_bp.route('/dropbox')
@login_required
@require_access(AREAS['dropbox'])
def dropbox():
    # Dropbox management page pointing to network path
    from servidor_app.models.file_system_model import FileSystemModel
    import os
    import logging

    current_path = request.args.get('path', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    root_dir = current_app.config['DROPBOX_DIR']
    error_message = None

    # Check if root directory exists before initializing FileSystemModel
    if not os.path.exists(root_dir):
        error_message = f"Diretório Dropbox não encontrado ou inacessível: {root_dir}"
        pastas = []
        pagination = None
        parent_path = None
    else:
        try:
            fs_model = FileSystemModel(root_dir)
            full_path = os.path.join(root_dir, current_path)
            if not os.path.exists(full_path):
                error_message = f"Diretório não encontrado: {full_path}"
                pastas = []
                pagination = None
                parent_path = None
            else:
                pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
                # Log debug info
                logging.debug(f"Dropbox list_directory called with current_path={current_path}, page={page}, per_page={per_page}")
                if pagination:
                    logging.debug(f"Pagination info: total_items={pagination.get('total_items')}, total_pages={pagination.get('total_pages')}")
        except Exception as e:
            error_message = f"Erro ao listar diretório: {e}"
            pastas = []
            pagination = None
            parent_path = None

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('dropbox.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor, error_message=error_message)

@main_bp.route('/metrics')
@login_required
@require_access(AREAS['metrics'])
def metrics():
    # Metrics monitoring page with real data
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    system_resources = performance_optimizer.get_system_resources()
    metrics_summary = metrics_service.get_metrics_summary()
    return render_template('metrics.html', dados_servidor=dados_servidor, system_resources=system_resources, metrics_summary=metrics_summary)

@main_bp.route('/performance')
@login_required
@require_access(AREAS['performance'])
def performance():
    # Performance monitoring page with real data
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    performance_stats = performance_optimizer.get_performance_stats()
    metrics_summary = metrics_service.get_metrics_summary()
    return render_template('performance.html', dados_servidor=dados_servidor, performance_stats=performance_stats, metrics_summary=metrics_summary)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')
            return redirect(url_for('main.login'))
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email:
            flash('Email é obrigatório.', 'danger')
            return redirect(url_for('main.register'))

        if password != confirm_password:
            flash('A senha e a confirmação não coincidem.', 'danger')
            return redirect(url_for('main.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nome de usuário já existe.', 'danger')
            return redirect(url_for('main.register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email já está em uso.', 'danger')
            return redirect(url_for('main.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso. Faça login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/perfil')
@login_required
def perfil():
    # Show logged-in user info
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('perfil.html', user=current_user, dados_servidor=dados_servidor)

@main_bp.route('/configuracoes', methods=['GET', 'POST'])
@login_required
def configuracoes():
    if request.method == 'POST':
        new_username = request.form.get('username')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Verify current password
        if not current_user.check_password(current_password):
            flash('Senha atual incorreta.', 'danger')
            return redirect(url_for('main.configuracoes'))

        # Check new password confirmation
        if new_password != confirm_password:
            flash('A nova senha e a confirmação não coincidem.', 'danger')
            return redirect(url_for('main.configuracoes'))

        # Update username and password
        if new_username:
            current_user.username = new_username
        if new_password:
            current_user.set_password(new_password)

        db.session.commit()
        flash('Configurações atualizadas com sucesso.', 'success')
        return redirect(url_for('main.perfil'))

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('configuracoes.html', user=current_user, dados_servidor=dados_servidor)

@main_bp.route('/admin')
@login_required
@require_access(AREAS['admin'])
def admin():
    # Get all users and roles for admin dashboard
    users = User.query.all()
    roles = Role.query.all()
    # Remove dados_servidor here to avoid conflict with global context processor
    return render_template('admin.html', users=users, roles=roles)

@main_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@require_access(AREAS['admin'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # Don't allow deleting self
    if user.id == current_user.id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect(url_for('main.admin'))

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    flash(f'Usuário {user.username} foi excluído com sucesso.', 'success')
    return redirect(url_for('main.admin'))

@main_bp.route('/admin/users/<int:user_id>/toggle', methods=['POST'])
@login_required
@require_access(AREAS['admin'])
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)

    # Don't allow blocking self
    if user.id == current_user.id:
        flash('Você não pode bloquear sua própria conta.', 'danger')
        return redirect(url_for('main.admin'))

    # Toggle active status
    user.is_active = not user.is_active
    db.session.commit()

    status = 'desbloqueado' if user.is_active else 'bloqueado'
    flash(f'Usuário {user.username} foi {status} com sucesso.', 'success')
    return redirect(url_for('main.admin'))

@main_bp.route('/admin/users/<int:user_id>/assign_role', methods=['POST'])
@login_required
@require_access(AREAS['admin'])
def assign_role(user_id):
    user = User.query.get_or_404(user_id)
    role_id = request.form.get('role_id')

    if role_id:
        role = Role.query.get_or_404(role_id)
        user.role = role
        db.session.commit()
        flash(f'Função {role.name} atribuída com sucesso ao usuário {user.username}.', 'success')
    else:
        # Remove role assignment
        user.role = None
        db.session.commit()
        flash(f'Função removida com sucesso do usuário {user.username}.', 'success')

    return redirect(url_for('main.admin'))

# Role Management Routes
@main_bp.route('/admin/roles')
@login_required
@require_access(AREAS['admin'])
def admin_roles():
    # Get all roles for admin dashboard
    roles = Role.query.all()
    return render_template('admin_roles.html', roles=roles)

@main_bp.route('/admin/roles/create', methods=['GET', 'POST'])
@login_required
@require_access(AREAS['admin'])
def create_role():
    if request.method == 'POST':
        name = request.form.get('name')
        allowed_areas = request.form.getlist('allowed_areas')

        if not name:
            flash('Nome da função é obrigatório.', 'danger')
            return redirect(url_for('main.create_role'))

        existing_role = Role.query.filter_by(name=name).first()
        if existing_role:
            flash('Nome da função já existe.', 'danger')
            return redirect(url_for('main.create_role'))

        new_role = Role(
            name=name,
            allowed_areas=json.dumps(allowed_areas)
        )
        db.session.add(new_role)
        db.session.commit()
        flash('Função criada com sucesso.', 'success')
        return redirect(url_for('main.admin_roles'))

    return render_template('admin_role_form.html', role=None)

@main_bp.route('/admin/roles/<int:role_id>/edit', methods=['GET', 'POST'])
@login_required
@require_access(AREAS['admin'])
def edit_role(role_id):
    role = Role.query.get_or_404(role_id)

    if request.method == 'POST':
        name = request.form.get('name')
        allowed_areas = request.form.getlist('allowed_areas')

        if not name:
            flash('Nome da função é obrigatório.', 'danger')
            return redirect(url_for('main.edit_role', role_id=role_id))

        existing_role = Role.query.filter_by(name=name).first()
        if existing_role and existing_role.id != role_id:
            flash('Nome da função já existe.', 'danger')
            return redirect(url_for('main.edit_role', role_id=role_id))

        role.name = name
        role.allowed_areas = json.dumps(allowed_areas)
        db.session.commit()
        flash('Função atualizada com sucesso.', 'success')
        return redirect(url_for('main.admin_roles'))

    return render_template('admin_role_form.html', role=role)

@main_bp.route('/admin/roles/<int:role_id>/delete', methods=['POST'])
@login_required
@require_access(AREAS['admin'])
def delete_role(role_id):
    role = Role.query.get_or_404(role_id)

    # Check if role is assigned to any users
    if role.users:
        flash('Não é possível excluir uma função que está atribuída a usuários.', 'danger')
        return redirect(url_for('main.admin_roles'))

    db.session.delete(role)
    db.session.commit()
    flash(f'Função {role.name} foi excluída com sucesso.', 'success')
    return redirect(url_for('main.admin_roles'))

@main_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    from servidor_app.models.file_system_model import FileSystemModel

    if 'file' not in request.files:
        return jsonify({'message': 'Nenhum arquivo enviado', 'success': False}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'Nome de arquivo vazio', 'success': False}), 400

    current_path = request.form.get('current_path', '')
    # Determine root_dir based on current_path context
    if current_path.startswith('Licitações') or request.referrer and '/licitacoes' in request.referrer:
        root_dir = current_app.config['LICITACOES_DIR']
    else:
        root_dir = current_app.config['ROOT_DIR']

    fs_model = FileSystemModel(root_dir)

    try:
        filename = fs_model.save_file(file, current_path, current_user)
        # Determine redirect URL based on context
        if request.referrer and '/licitacoes' in request.referrer:
            redirect_url = url_for('main.licitacoes', path=current_path) if current_path else url_for('main.licitacoes')
        else:
            redirect_url = url_for('main.browse', sub_path=current_path) if current_path else url_for('main.index')
        return jsonify({
            'message': f'Arquivo {filename} enviado com sucesso',
            'success': True,
            'redirect_url': redirect_url
        })
    except Exception as e:
        return jsonify({'message': f'Erro ao enviar arquivo: {str(e)}', 'success': False}), 500

@main_bp.route('/create_folder', methods=['POST'])
@login_required
def create_folder():
    from servidor_app.models.file_system_model import FileSystemModel
    from werkzeug.security import generate_password_hash

    folder_name = request.form.get('folder_name')
    current_path = request.form.get('current_path', '')
    folder_password = request.form.get('folder_password', None)

    if not folder_name:
        return jsonify({'message': 'Nome da pasta é obrigatório', 'success': False}), 400

    # Determine root_dir based on current_path context
    if current_path.startswith('Licitações') or (request.referrer and '/licitacoes' in request.referrer):
        root_dir = current_app.config['LICITACOES_DIR']
    else:
        root_dir = current_app.config['ROOT_DIR']

    fs_model = FileSystemModel(root_dir)

    try:
        password_hash = generate_password_hash(folder_password) if folder_password else None
        fs_model.create_folder(folder_name, current_path, current_user, password_hash=password_hash)
        # Determine redirect URL based on context
        if request.referrer and '/licitacoes' in request.referrer:
            redirect_url = url_for('main.licitacoes', path=current_path) if current_path else url_for('main.licitacoes')
        else:
            redirect_url = url_for('main.browse', sub_path=current_path) if current_path else url_for('main.index')
        return jsonify({
            'message': f'Pasta {folder_name} criada com sucesso',
            'success': True,
            'redirect_url': redirect_url
        })
    except Exception as e:
        return jsonify({'message': f'Erro ao criar pasta: {str(e)}', 'success': False}), 500

@main_bp.route('/move_item', methods=['POST'])
@login_required
def move_item():
    from servidor_app.models.file_system_model import FileSystemModel

    source_path = request.form.get('source_path')
    destination_path = request.form.get('destination_path')

    if not source_path or not destination_path:
        return jsonify({'message': 'Caminhos de origem e destino são obrigatórios', 'success': False}), 400

    fs_model = FileSystemModel(current_app.config['ROOT_DIR'])

    try:
        fs_model.move_item(source_path, destination_path, current_user)
        return jsonify({
            'message': 'Item movido com sucesso',
            'success': True,
            'redirect_url': url_for('main.index')
        })
    except Exception as e:
        return jsonify({'message': f'Erro ao mover item: {str(e)}', 'success': False}), 500

@main_bp.route('/download/<path:file_path>')
@login_required
def download(file_path):
    from servidor_app.models.file_system_model import FileSystemModel
    import os
    from flask import send_from_directory, send_file, jsonify, current_app

    # Determine root directory based on path prefix
    if file_path.startswith('Licitações/'):
        root_dir = current_app.config['LICITACOES_DIR']
        relative_path = file_path[len('Licitações/'):]
    elif file_path.startswith('Sistemas/'):
        root_dir = current_app.config['SISTEMAS_DIR']
        relative_path = file_path[len('Sistemas/'):]
    elif file_path.startswith('Dropbox/'):
        root_dir = current_app.config['DROPBOX_DIR']
        relative_path = file_path[len('Dropbox/'):]
    else:
        root_dir = current_app.config['ROOT_DIR']
        relative_path = file_path

    fs_model = FileSystemModel(root_dir)
    full_path = os.path.join(root_dir, relative_path)

    # Log the request
    current_app.logger.info(f"Download requested: file_path={file_path}, relative_path={relative_path}, full_path={full_path}")

    # Security check
    if not os.path.abspath(full_path).startswith(os.path.abspath(root_dir)):
        current_app.logger.warning(f"Security check failed for path: {full_path}")
        return jsonify({'message': 'Acesso negado', 'success': False}), 403

    if not os.path.exists(full_path):
        current_app.logger.warning(f"File not found: {full_path}")
        return jsonify({'message': 'Arquivo não encontrado', 'success': False}), 404

    if os.path.isdir(full_path):
        # If it's a directory, create a zip file
        memory_file, download_name = fs_model.create_zip_from_folder(relative_path)
        if memory_file:
            memory_file.seek(0)
            return send_file(
                memory_file,
                as_attachment=True,
                download_name=download_name,
                mimetype='application/zip'
            )
        else:
            current_app.logger.error(f"Error creating zip for folder: {full_path}")
            return jsonify({'message': 'Erro ao criar arquivo zip', 'success': False}), 500
    else:
        # If it's a file, send it directly
        directory = os.path.dirname(full_path)
        return send_from_directory(directory, os.path.basename(full_path), as_attachment=True)

@main_bp.route('/secure_folder_password/<path:folder_path>', methods=['GET', 'POST'])
@login_required
def secure_folder_password(folder_path):
    from servidor_app.models.file_system_model import FileSystemModel
    from werkzeug.security import check_password_hash

    fs_model = FileSystemModel(current_app.config['ROOT_DIR'])

    if not fs_model.is_folder_secure(folder_path):
        flash('Esta pasta não é segura.', 'warning')
        return redirect(url_for('main.browse', sub_path=folder_path))

    if request.method == 'POST':
        password = request.form.get('password')
        if fs_model.check_folder_password(folder_path, password):
            # Password correct, render the folder listing directly
            current_path = folder_path
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 50, type=int)
            try:
                pastas, current_path, parent_path, pagination = fs_model.list_directory(current_path, page, per_page)
            except Exception as e:
                flash(f"Erro ao listar diretório: {e}", "danger")
                pastas = []
                pagination = None
                parent_path = None
            dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
            flash('Acesso concedido à pasta segura.', 'success')
            response = make_response(render_template('index.html', current_path=current_path, pastas=pastas, pagination=pagination, parent_path=parent_path, dados_servidor=dados_servidor))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        else:
            flash('Senha incorreta.', 'danger')

    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    response = make_response(render_template('secure_folder_password.html', folder_path=folder_path, dados_servidor=dados_servidor))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@main_bp.app_errorhandler(404)
def page_not_found(e):
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    return render_template('404.html', dados_servidor=dados_servidor), 404
