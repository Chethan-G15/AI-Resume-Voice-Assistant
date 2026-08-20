import ollama
import json


MODEL_NAME = "llama3.2"


def understand_query(query: str) -> dict:

    prompt = f"""
You are a resume information retrieval assistant.

Analyze the user's query and identify:

1. candidate_name
2. requested_section

Allowed sections are ONLY:

- career_objective
- skills
- education
- experience
- projects
- certifications

The candidate name must come from the user's query.
Do not assume a fixed candidate name.

Examples:

"What are Rahul's skills?"
=> candidate_name: "RAHUL"
=> requested_section: "skills"

"Where did Priya study?"
=> candidate_name: "PRIYA"
=> requested_section: "education"

"What projects has Arjun worked on?"
=> candidate_name: "ARJUN"
=> requested_section: "projects"

"Where has Sneha worked?"
=> candidate_name: "SNEHA"
=> requested_section: "experience"

Return ONLY valid JSON.
Do not provide explanations.
Do not invent resume information.

User query:
{query}

Return exactly:

{{
    "candidate_name": "candidate name",
    "requested_section": "one allowed section"
}}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response["message"]["content"].strip()

    print("Ollama raw response:")
    print(content)

    # Remove Markdown code fences if Ollama adds them
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(
            f"Ollama did not return valid JSON. Response was: {content}"
        )

    return result