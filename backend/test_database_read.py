from app.database.database import get_connection


connection = get_connection()

cursor = connection.cursor()

cursor.execute("""
    SELECT
        id,
        candidate_name,
        filename,
        career_objective,
        skills,
        education,
        experience,
        projects,
        certifications
    FROM resumes
""")

rows = cursor.fetchall()

for row in rows:

    print("\n" + "=" * 70)

    print(f"Resume ID: {row[0]}")
    print(f"Candidate Name: {row[1]}")
    print(f"Filename: {row[2]}")

    print("\n--- Career Objective ---")
    print(row[3])

    print("\n--- Skills ---")
    print(row[4])

    print("\n--- Education ---")
    print(row[5])

    print("\n--- Experience ---")
    print(row[6])

    print("\n--- Projects ---")
    print(row[7])

    print("\n--- Certifications ---")
    print(row[8])

    print("=" * 70)


connection.close()