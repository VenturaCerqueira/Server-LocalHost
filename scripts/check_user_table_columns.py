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

    columns = inspector.get_columns('user')
    print("Columns in 'user' table:")
    for column in columns:
        print(f"- {column['name']} ({column['type']})")

    # Check if role_id column exists
    column_names = [col['name'] for col in columns]
    if 'role_id' in column_names:
        print("\nrole_id column exists.")
    else:
        print("\nrole_id column is MISSING!")

except Exception as e:
    print(f"Error: {e}")
