# Document Input Folder

This folder is for dropping any documents you want to ingest into the RAG system.

## Usage

### 1. Add Documents

**ANY FILENAME WORKS!** Just copy or drag files into this folder.

```
✅ report.pdf
✅ Company Report 2024.pdf
✅ my-analysis.docx
✅ financial-data.txt
✅ anything_you_want.pdf
```

**No specific format required!**
- ✅ Use any filename you want
- ✅ Year is optional (will auto-extract if present: 1900-2099)
- ✅ Any file type supported by document loader
- ✅ Spaces, underscores, dashes - all work

**Examples:**
- `report.pdf` → Company: "report", Year: None
- `Grupa Azoty 2024.pdf` → Company: "Grupa Azoty", Year: 2024
- `PKN_Orlen_Annual_Report_2023.pdf` → Company: "PKN Orlen Annual Report", Year: 2023
- `my company data.pdf` → Company: "my company data", Year: None

The script will:
- Use filename as company name (cleaned up)
- Auto-extract year if present in filename
- Group documents by company name
- Create collection: `company_name_multi_year`

### 2. Run Ingestion

```bash
python3 scripts/ingest_from_input_folder.py
```

The script will:
1. Scan this folder for PDFs
2. Parse filenames to extract company and year
3. Group PDFs by company
4. Ask for confirmation
5. Ingest all PDFs into Qdrant
6. Create separate collections for each company

### 3. View Results

After ingestion completes, you'll see:
- Total PDFs processed
- Total chunks created
- Collection names created
- Success/failure status per file

### Example Workflow

```bash
# 1. Copy PDFs to input folder
cp ~/Downloads/Grupa_Azoty_*.pdf data/documents/input/

# 2. Run ingestion
python3 scripts/ingest_from_input_folder.py

# Output:
# Found 3 PDFs for Grupa Azoty (2022-2024)
# Proceed with ingestion? (y/n): y
# ✅ Ingested 4,840 chunks into collection: grupa_azoty_multi_year

# 3. Generate reports
python3 scripts/test_multi_agent_multi_year.py
```

## Features

✅ **Auto-detection** - Automatically extracts company name and year from filenames
✅ **Multi-company** - Processes multiple companies in one run
✅ **Collection per company** - Each company gets its own Qdrant collection
✅ **Error handling** - Skips files that can't be parsed, continues with others
✅ **Summary report** - Shows detailed results after ingestion

## Collection Naming

Collections are named: `{company_name}_multi_year`

Examples:
- `grupa_azoty_multi_year`
- `pkn_orlen_multi_year`
- `tesla_multi_year`

## Notes

- The script creates collections automatically
- If a collection already exists, new PDFs will be added to it
- Each PDF should have a unique year to avoid duplicates
- Supported file format: PDF only
- Recommended: 2-10 PDFs per company (covering multiple years)

## Troubleshooting

**"Could not parse filename"**
→ Check filename format: `CompanyName_Report_YYYY.pdf`

**"No PDFs found"**
→ Make sure PDFs are directly in this folder (not in subfolders)

**"Ingestion failed"**
→ Check PDF is valid and readable
→ Check Qdrant is running: `http://localhost:6333`

**"Collection already exists"**
→ This is normal! New PDFs will be added to existing collection
