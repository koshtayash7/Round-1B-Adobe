# embedder.py

def rank_sections_by_relevance(sections, persona, job):
    """
    Rank sections based on the presence of focus keywords.
    
    Parameters:
    - sections: List of dicts with keys: 'document', 'section_title', 'text', 'page_number'
    - persona: Dict with user role (not used in current scoring logic but passed for future use)
    - job: Dict with keys 'task' and optional 'focus_keywords'
    
    Returns:
    - top_sections: List of top 5 sections with highest keyword match
    - top_subsections: Detailed analysis of subsections corresponding to top sections
    """

    # Extract keywords in lowercase
    keywords = [k.lower() for k in job.get("focus_keywords", [])]
    ranked_sections = []
    subsection_analysis = []

    for section in sections:
        text_lower = section["text"].lower()
        # Score: count how many keywords are present
        score = sum(k in text_lower for k in keywords) if keywords else 1

        ranked_sections.append({
            "document": section["document"],
            "section_title": section["section_title"],
            "importance_rank": score,
            "page_number": section["page_number"]
        })

        subsection_analysis.append({
            "document": section["document"],
            "refined_text": section["text"],
            "page_number": section["page_number"]
        })

    # Sort by score (desc), then by doc and page for consistency
    ranked_sections = sorted(
        ranked_sections,
        key=lambda x: (-x["importance_rank"], x["document"], x["page_number"])
    )

    # Take top 5 ranked sections
    top_sections = ranked_sections[:5]
    for i, sec in enumerate(top_sections):
        sec["importance_rank"] = i + 1  # Re-rank 1 through 5

    # Filter subsection analysis to only include top sections
    top_docs_pages = {(s["document"], s["page_number"]) for s in top_sections}
    top_subsections = [
        s for s in subsection_analysis
        if (s["document"], s["page_number"]) in top_docs_pages
    ]

    return top_sections, top_subsections
