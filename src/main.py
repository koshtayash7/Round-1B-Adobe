import os
import sys
import json
from datetime import datetime
from extract_sections import extract_sections_from_pdfs
from embedder import rank_sections_by_relevance

def main(input_json_path, input_pdf_dir, output_json_path):
    # Load input JSON
    with open(input_json_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    # Extract document filenames
    input_documents = [doc["filename"] for doc in input_data.get("documents", [])]

    # Extract persona and task
    persona = input_data.get("persona", {})
    job_to_be_done = input_data.get("job_to_be_done", {})

    print("Persona:", persona.get("role", "N/A"))
    print("Task:", job_to_be_done.get("task", "N/A"))

    print("[INFO] Extracting sections from PDFs...")
    section_data = extract_sections_from_pdfs(input_pdf_dir, input_documents)

    print("[INFO] Ranking sections based on persona and job-to-be-done...")
    ranked_sections, ranked_subsections = rank_sections_by_relevance(
        section_data, persona, job_to_be_done
    )

    # Prepare output
    output_json = {
        "metadata": {
            "input_documents": input_documents,
            "persona": persona.get("role", ""),
            "job_to_be_done": job_to_be_done.get("task", ""),
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": ranked_sections,
        "subsection_analysis": ranked_subsections
    }

    # Ensure output directory exists
    output_dir = os.path.dirname(output_json_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Write output
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Output written to {output_json_path}")


if __name__ == "__main__":
    # Defaults
    input_json_path = sys.argv[1] if len(sys.argv) > 1 else "challenge1b_input.json"
    input_pdf_dir = sys.argv[2] if len(sys.argv) > 2 else "PDFs"
    output_json_path = sys.argv[3] if len(sys.argv) > 3 else "challenge1b_output.json"

    main(input_json_path, input_pdf_dir, output_json_path)
