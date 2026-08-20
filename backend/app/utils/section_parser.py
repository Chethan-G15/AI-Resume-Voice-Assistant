import re

# here we have created dictonary with one section can have different names
SECTION_ALIASES = {
    "career_objective": [
        "career objective",
        "objective",
        "career summary",
        "professional summary",
        "profile summary",
        "summary"
    ],

    "skills": [
        "skills",
        "technical skills",
        "key skills",
        "technical expertise"
    ],

    "education": [
        "education",
        "educational qualification",
        "academic qualification",
        "academic details"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience"
    ],

    "certifications": [
        "Awards and Certificate",
        "Awards and Certifications",
        "certifications",
        "certificates",
        "certification"
    ]
}


def normalize_heading(line: str) -> str:
    """
    Clean a possible section heading.
    """

    line = line.strip()

    # Remove common punctuation
    line = re.sub(r"[:\-]+$", "", line)

    return line.lower().strip()


# check each line suppose the extracted pdf contains title in the dictonary
def detect_section(line: str):
    """
    Check whether a line represents a known resume section.

    Returns:
        section name if recognized
        None otherwise
    """

    normalized_line = normalize_heading(line)

    for section_name, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            if normalized_line == alias:
                return section_name

    return None

# here it will receives the entire extraced resume text 
# this below format will store inside the SQLite
def parse_resume_sections(text: str) -> dict:
    """
    Divide resume text into recognized sections.
    """

    sections = {
        "career_objective": "",
        "skills": "",
        "education": "",
        "experience": "",
        "projects": "",
        "certifications": ""
    }

    current_section = None

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        detected_section = detect_section(line)

        if detected_section:
            current_section = detected_section
            continue

        if current_section:
            sections[current_section] += line + "\n"

    # Remove extra whitespace
    for section_name in sections:
        sections[section_name] = sections[section_name].strip()

    return sections

def extract_candidate_name(text: str) -> str:
    """
    Extract the first meaningful line as the candidate name.
    """

    for line in text.splitlines():

        line = line.strip()

        if line:
            return line

    return "Unknown Candidate"
def extract_email(text: str) -> str:
    """
    Extract email address from resume text.
    """

    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(email_pattern, text)

    if match:
        return match.group(0)

    return ""


def extract_phone(text: str) -> str:
    """
    Extract phone number from resume text.
    Supports common Indian phone number formats.
    """

    phone_pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    match = re.search(phone_pattern, text)

    if match:
        return match.group(0)

    return ""