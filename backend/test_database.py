from app.database.database import create_tables, DATABASE_PATH


create_tables()

print("Database created successfully.")
print(f"Database location: {DATABASE_PATH}")