from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify, make_response
from flask_login import login_required
from servidor_app.services.server_info_service import get_server_info
import servidor_app.services.database_service as db_service
from servidor_app.controllers.permissions import require_access, AREAS
import json
import graphviz
import os
import pymysql
import time
import traceback
import html
from decimal import Decimal

database_bp = Blueprint('database', __name__)

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

@database_bp.route('/databases')
@login_required
@require_access(AREAS['banco_dados'])
def databases():
    # Database management page with MySQL databases from XAMPP and production
    dados_servidor = get_server_info(current_app.config['ROOT_DIR'])
    mysql_dbs_local = db_service.list_local_mysql_databases(current_app.config)
    mysql_dbs_prod = db_service.list_production_mysql_databases(current_app.config)
    return render_template('database/databases.html', dados_servidor=dados_servidor, mysql_dbs_local=mysql_dbs_local, mysql_dbs_prod=mysql_dbs_prod)

@database_bp.route('/databases/download/<db_name>')
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

@database_bp.route('/databases/compare/<db_name>')
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

        return render_template('database/database_comparison.html',
                             db_name=db_name,
                             comparison=comparison_results,
                             error=None)

    except Exception as e:
        error_message = f"Erro ao comparar bancos de dados: {str(e)}"
        current_app.logger.error(error_message)
        current_app.logger.error(traceback.format_exc())
        return render_template('database/database_comparison.html', error=error_message, db_name=db_name)
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

@database_bp.route('/databases/analyze/<db_name>')
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
                return render_template('database/database_analysis.html', error=error_message, db_name=db_name)

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

            table_md_section += add_column_table("Chaves Primárias", pk_columns)
            table_md_section += add_column_table("Chaves Estrangeiras", fk_columns)
            table_md_section += add_column_table("Outras Colunas", other_columns)

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

        return render_template('database/database_analysis.html',
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
        return render_template('database/database_analysis.html', error=error_message, db_name=db_name)
    finally:
        if connection and connection.open:
            connection.close()

@database_bp.route('/databases/delete/<db_name>', methods=['DELETE'])
@login_required
@require_access(AREAS['banco_dados'])
def delete_database(db_name):
    # Delete local MySQL database
    db_type = request.args.get('type', 'local')

    if db_type == 'local':
        result = db_service.delete_local_mysql_database(db_name, current_app.config)
    else:
        # For production databases, don't allow deletion
        return jsonify({
            'success': False,
            'error': 'Não é permitido deletar bancos de produção'
        }), 403

    if result['success']:
        return jsonify({
            'success': True,
            'message': result['message']
        })
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@database_bp.route('/databases/import/<db_name>', methods=['POST'])
@login_required
@require_access(AREAS['banco_dados'])
def import_database(db_name):
    # Import SQL file to local MySQL database
    if 'sql_file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'Nenhum arquivo SQL enviado'
        }), 400

    sql_file = request.files['sql_file']
    if sql_file.filename == '':
        return jsonify({
            'success': False,
            'error': 'Nome do arquivo vazio'
        }), 400

    # Validate file extension
    if not sql_file.filename.lower().endswith('.sql'):
        return jsonify({
            'success': False,
            'error': 'Apenas arquivos .sql são permitidos'
        }), 400

    # Save uploaded file temporarily
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode='wb', suffix='.sql', delete=False) as temp_file:
        temp_path = temp_file.name
        sql_file.save(temp_file)

    try:
        # Import the SQL file
        result = db_service.import_sql_file_to_mysql(temp_path, db_name, current_app.config)

        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message'],
                'analysis_results': result.get('analysis', {})
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error'],
                'analysis_results': result.get('analysis', {})
            }), 500

    except Exception as e:
        current_app.logger.error(f"Erro na importação do banco {db_name}: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        }), 500

    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@database_bp.route('/databases/tables/<db_name>')
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
                return render_template('database/database_tables.html', error=error_message, db_name=db_name)

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

        return render_template('database/database_tables.html', db_name=db_name, tables=tables_data, error=None)

    except Exception as e:
        error_message = f"Erro ao analisar banco de dados: {str(e)}"
        current_app.logger.error(error_message)
        current_app.logger.error(traceback.format_exc())
        return render_template('database/database_tables.html', error=error_message, db_name=db_name)
    finally:
        if connection and connection.open:
            connection.close()
