# Approach Explanation

## Objective

Build an offline, CPU-only system to extract and prioritize relevant sections from PDF documents, tailored to a specific persona and their task (job-to-be-done).

---

## Architecture Overview

1. **PDF Parsing (PyMuPDF)**:
   - Extracts text blocks, font sizes, and page numbers.
   - Uses font size and boldness heuristics to detect hierarchy:
     - Largest font: Title
     - Next largest: H1
     - Smaller sizes: H2, H3

2. **Semantic Embedding (MiniLM)**:
   - Embeddings generated using `all-MiniLM-L6-v2` from Sentence Transformers (~85MB).
   - Converts both:
     - Document sections
     - Query (persona + job-to-be-done)
     into vector representations.

3. **Relevance Scoring**:
   - Uses cosine similarity between query embedding and section embeddings.
   - Sections and sub-sections are ranked by similarity score.

4. **Output Formatting**:
   - Top N sections are selected and output in structured JSON format:
     - Document, Page, Title, Importance Rank
     - Subsection refined texts
   - Includes metadata such as persona, job, timestamp, etc.

---

## Optimization Choices

- **CPU-only**: No GPU acceleration required.
- **Model size < 1GB**: Embedding model is ~85MB.
- **Fast processing**: Designed to work within 60s for 3–5 PDFs.
- **Offline Mode**: All dependencies (including model) loaded at Docker image build-time.

---

## Dockerization

- Docker image installs dependencies and pre-downloads the model.
- At runtime, PDFs are read from `input_pdfs/`, and JSON output is saved to `output/output.json`.

---

## Generalization

This solution supports various domains by relying on:
- Font-based heading detection (structure)
- Embedding-based semantic similarity (content relevance)
- Simple modular design (for easy extension or tuning)
