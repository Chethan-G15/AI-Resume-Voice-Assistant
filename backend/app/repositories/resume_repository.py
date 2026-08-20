from app.database.database import get_connection


def insert_resume(
    candidate_name,
    email,
    phone,
    filename,
    career_objective,
    skills,
    education,
    experience,
    projects,
    certifications
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO resumes (
            candidate_name,
            email,
            phone,
            filename,
            career_objective,
            skills,
            education,
            experience,
            projects,
            certifications
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            candidate_name,
            email,
            phone,
            filename,
            career_objective,
            skills,
            education,
            experience,
            projects,
            certifications
        )
    )

    connection.commit()

    resume_id = cursor.lastrowid

    connection.close()

    return resume_id


def get_resume_by_candidate(candidate_name):
    """
    Find a resume using the candidate name.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            candidate_name,
            email,
            phone,
            filename,
            career_objective,
            skills,
            education,
            experience,
            projects,
            certifications
        FROM resumes
        WHERE LOWER(candidate_name) LIKE LOWER(?)
        LIMIT 1
        """,
        (f"%{candidate_name}%",)
    )

    row = cursor.fetchone()

    connection.close()

    return row