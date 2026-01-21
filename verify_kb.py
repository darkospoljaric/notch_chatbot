#!/usr/bin/env python3
"""Quick script to verify knowledge base loads correctly."""

from src.notch_chatbot.knowledge_base import load_knowledge_base


def main():
    """Load and display knowledge base summary."""
    print("Loading knowledge base...")
    kb = load_knowledge_base()

    print(f"\n✓ Successfully loaded knowledge base!")
    print(f"\nServices: {len(kb.services)}")
    for service in kb.services:
        print(f"  - {service.name} ({service.category.value})")

    print(f"\nCase Studies: {len(kb.case_studies)}")
    for cs in kb.case_studies:
        print(f"  - {cs.client_name}: {cs.title}")

    print(f"\nUse Cases: {len(kb.use_cases)}")
    for uc in kb.use_cases:
        print(f"  - {uc.title}")

    print(f"\nExpertise Domains: {len(kb.expertise_domains)}")
    for domain in kb.expertise_domains:
        print(f"  - {domain}")

    print("\n✓ All knowledge base files loaded successfully!")


if __name__ == "__main__":
    main()
