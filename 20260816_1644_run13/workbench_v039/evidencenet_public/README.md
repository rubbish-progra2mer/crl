# EvidenceNet three-disease evidence records and companion graphs

This Figshare release contains disease-specific evidence-record collections and companion graph files for hepatocellular carcinoma (HCC), colorectal cancer (CRC) and systemic lupus erythematosus (SLE).

## Released file groups

- `records/`: primary evidence-record JSON files
- `graphs/`: derived companion graph JSON files
- `schema/`: JSON schemas and field dictionary for file interpretation
- `validation/`: audit samples, integrity checks, record-lookup outputs, external-concordance summaries and metadata-QC records
- `prompts/`: extraction, aggregation and relation-verification prompt templates
- `checksums_sha256.txt`: SHA-256 checksums for file-integrity verification

## Primary data files

- `records/evidence_records_hcc.json` (7872 records)
- `records/evidence_records_crc.json` (6622 records)
- `records/evidence_records_sle.json` (4261 records)

These record-level JSON files are the primary data objects. Each file is keyed by `evidence_id` and stores article provenance, source text, study context, entities, quality-related fields and relation annotations.

## Companion graph files

- `graphs/evidence_graph_hcc.json` (10328 nodes, 49756 edges)
- `graphs/evidence_graph_crc.json` (8795 nodes, 39361 edges)
- `graphs/evidence_graph_sle.json` (6342 nodes, 21645 edges)

Graph files are derived companion representations for network loading and visualization. The graph layer preserves `evidence_id` values so users can return from graph nodes to the corresponding record-level JSON entries.

## Validation files

The `validation/` directory includes aligned validation outputs used in the manuscript: component-level manual audit files, graph-integrity checks, record-lookup prompts and retrieval results, external-concordance summaries, a metadata-year outlier table, and an aggregated validation summary.

## Reuse notes

The score and grade fields are computational quality indicators for filtering and prioritization. They are not clinical guideline recommendations. Evidence relations indicate semantic relationships between extracted records and should not be interpreted as clinical treatment advice without manual inspection of the linked source text, study design and disease context.

Lower coverage of quantitative fields indicates that a value is not directly extractable or not confidently attributable to the record. Missing values should not be interpreted as negative biomedical evidence.

## Metadata quality control

`validation/metadata_year_outliers.csv` records manually reviewed metadata-year outliers used during release QC. The SLE subset includes manually corrected source-metadata cases verified against source PDFs and repository records.
