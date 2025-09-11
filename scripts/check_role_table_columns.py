from sqlalchemy import create_engine, inspect
import os

try:
    # Check if database file exists
    db_path = 'servidor_app/app.db'
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found.")
        exit(1)

    engine = create_engine(f'sqlite:///{db_path}')

    inspector = inspect(engine)

    columns = inspector.get_columns('role')
    print("Columns in 'role' table:")
    for column in columns:
        print(f"- {column['name']} ({column['type']})")

    # Check if allowed_areas column exists
    column_names = [col['name'] for col in columns]
    if 'allowed_areas' in column_names:
        print("\nallowed_areas column exists.")
    else:
        print("\nallowed_areas column is MISSING!")

except Exception as e:
    print(f"Error: {e}")
