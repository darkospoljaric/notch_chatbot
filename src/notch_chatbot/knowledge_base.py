"""Knowledge base loader for Notch chatbot."""

import json
from pathlib import Path

from .models import CaseStudy, KnowledgeBase, Service, UseCase


def load_knowledge_base(data_dir: Path | str | None = None) -> KnowledgeBase:
    """Load knowledge base from JSON files.

    Args:
        data_dir: Directory containing JSON data files.
                  Defaults to 'data' directory in project root.

    Returns:
        Loaded KnowledgeBase instance.

    Raises:
        FileNotFoundError: If data directory or required files don't exist.
        json.JSONDecodeError: If JSON files are invalid.
    """
    if data_dir is None:
        # Default to data directory in project root
        data_dir = Path(__file__).parent.parent.parent / "data"
    else:
        data_dir = Path(data_dir)

    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    # Load services
    services_file = data_dir / "services.json"
    with open(services_file, "r", encoding="utf-8") as f:
        services_data = json.load(f)
        services = [Service(**s) for s in services_data]

    # Load case studies
    case_studies_file = data_dir / "case_studies.json"
    with open(case_studies_file, "r", encoding="utf-8") as f:
        case_studies_data = json.load(f)
        case_studies = [CaseStudy(**cs) for cs in case_studies_data]

    # Load use cases
    use_cases_file = data_dir / "use_cases.json"
    with open(use_cases_file, "r", encoding="utf-8") as f:
        use_cases_data = json.load(f)
        use_cases = [UseCase(**uc) for uc in use_cases_data]

    # Load expertise domains
    expertise_file = data_dir / "expertise.json"
    with open(expertise_file, "r", encoding="utf-8") as f:
        expertise_domains = json.load(f)

    return KnowledgeBase(
        services=services,
        case_studies=case_studies,
        use_cases=use_cases,
        expertise_domains=expertise_domains,
    )
