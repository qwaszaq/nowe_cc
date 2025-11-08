"""
Enhanced Prompts for Phase 1: Prompt Engineering Optimization

This module wraps existing comprehensive prompts with:
1. Stronger RAG citation requirements for OSS-20B
2. Better formatting/structure requirements for Gemma-27B

Implements immediate quality improvements without architectural changes.
"""

# =============================================================================
# CITATION ENFORCEMENT ADDITIONS (For OSS-20B weakness)
# =============================================================================

CITATION_ENFORCEMENT_PREFIX = """
═══════════════════════════════════════════════════════════════════════════
⚠️  CRITICAL RAG CITATION REQUIREMENTS (ENFORCED)
═══════════════════════════════════════════════════════════════════════════

You MUST achieve these MINIMUM citation counts in your analysis:

📊 CITATION TARGETS (MANDATORY):
   • Financial Health Section: Minimum 6 citations
   • Risk Assessment Section: Minimum 5 citations
   • Industry Context Section: Minimum 4 citations
   • Strategic Evaluation Section: Minimum 4 citations
   • Market Intelligence Section: Minimum 3 citations

   🎯 TOTAL MINIMUM: 22 source citations across all sections

📝 CITATION FORMAT (Use EXACTLY this format):
   ✅ CORRECT: "Revenue declined 15% year-over-year (Source: Annual Report 2024, p. 12)"
   ✅ CORRECT: "Management cited supply chain disruptions as primary driver (Source: Directors' Report 2023, p. 45)"
   ✅ CORRECT: "The company's debt-to-equity ratio increased to 3.2x (Source: Financial Statements 2024, Note 15)"

   ❌ INCORRECT: "Revenue declined" (no citation)
   ❌ INCORRECT: "According to the report..." (vague, no specific source)

🔍 WHEN TO CITE (You MUST cite in these scenarios):
   ✓ Every quantitative claim that comes from retrieved documents
   ✓ Every risk factor mentioned in company disclosures
   ✓ Every strategic initiative described in directors' reports
   ✓ Every market trend from industry context documents
   ✓ Every management statement or outlook comment

⚡ QUALITY CONTROL:
   • If you don't have 22+ citations, your report will be REJECTED
   • Generic statements without citations indicate you didn't use RAG properly
   • Each citation must include: Document name + Year + Page number

═══════════════════════════════════════════════════════════════════════════
"""

CITATION_ENFORCEMENT_SUFFIX = """

═══════════════════════════════════════════════════════════════════════════
📋 PRE-SUBMISSION CHECKLIST (Complete before finalizing):
═══════════════════════════════════════════════════════════════════════════

Before you submit your analysis, verify:

□ Financial Health section has 6+ citations with specific page numbers
□ Risk Assessment section has 5+ citations to disclosed risks
□ Industry Context section has 4+ citations to market/competitive data
□ Strategic Evaluation section has 4+ citations to management discussions
□ Market Intelligence section has 3+ citations to forward-looking statements

□ Every citation uses format: (Source: [Doc Name] [Year], p. [XX])
□ Total citation count is 22 or higher
□ No vague references like "the report states" without specific citation

If ANY checkbox is unchecked, revise your analysis before submission.

═══════════════════════════════════════════════════════════════════════════
"""

# =============================================================================
# FORMATTING ENFORCEMENT ADDITIONS (For Gemma-27B weakness)
# =============================================================================

FORMATTING_ENFORCEMENT_PREFIX = """
═══════════════════════════════════════════════════════════════════════════
⚠️  CRITICAL FORMATTING & STRUCTURE REQUIREMENTS (ENFORCED)
═══════════════════════════════════════════════════════════════════════════

Your analysis MUST follow professional formatting standards:

📊 MANDATORY TABLES (You MUST include these):

1. EXECUTIVE SUMMARY TABLE (Required at top of every section):
```markdown
| Key Metric | Value | Trend | Assessment |
|------------|-------|-------|------------|
| Metric 1   | XX.X  | ↑/↓/→ | [Brief]    |
| Metric 2   | XX.X  | ↑/↓/→ | [Brief]    |
| Metric 3   | XX.X  | ↑/↓/→ | [Brief]    |
```

2. QUANTITATIVE COMPARISON TABLE (Required for multi-year data):
```markdown
| Metric | 2022 | 2023 | 2024 | CAGR | Trend |
|--------|------|------|------|------|-------|
| Revenue (PLN m) | XXX | XXX | XXX | X.X% | ↑/↓ |
| EBIT (PLN m) | XXX | XXX | XXX | X.X% | ↑/↓ |
| Net Income | XXX | XXX | XXX | X.X% | ↑/↓ |
```

3. RISK MATRIX TABLE (Required for risk sections):
```markdown
| Risk Category | Probability | Impact | Severity | Trend |
|--------------|-------------|---------|----------|-------|
| Risk 1       | High/Med/Low| High/Med| Critical | ↑/→   |
| Risk 2       | High/Med/Low| Med/Low | High     | ↓/→   |
```

📐 SECTION STRUCTURE (Mandatory hierarchy):
   ## SECTION TITLE (H2)

   [Executive Summary Table here]

   ### Subsection 1 (H3)
   #### Analysis Point 1 (H4)
   - Bullet point with specific data
   - Bullet point with comparison

   #### Analysis Point 2 (H4)
   - Supporting evidence
   - Quantitative metrics

🎨 FORMATTING RULES:
   ✅ Use **bold** for key metrics and findings
   ✅ Use *italics* for emphasis on critical points
   ✅ Use bullet points for lists (never numbered lists for metrics)
   ✅ Use tables for ALL quantitative comparisons
   ✅ Use horizontal rules (---) between major sections
   ✅ Use blockquotes (>) for direct quotations only

═══════════════════════════════════════════════════════════════════════════
"""

FORMATTING_ENFORCEMENT_SUFFIX = """

═══════════════════════════════════════════════════════════════════════════
📋 FORMATTING CHECKLIST (Complete before finalizing):
═══════════════════════════════════════════════════════════════════════════

Before you submit your analysis, verify:

□ Executive summary table present at start of each major section
□ All multi-year data presented in comparative tables (not prose)
□ Risk matrix table included if discussing multiple risks
□ Clear ## / ### / #### heading hierarchy throughout
□ **Bold** used for all key metrics and scores
□ Tables use proper markdown formatting with aligned columns
□ Minimum 3 tables in comprehensive sections
□ No long paragraphs without bullet points (max 4-5 sentences)

If ANY checkbox is unchecked, reformat your analysis before submission.

═══════════════════════════════════════════════════════════════════════════
"""

# =============================================================================
# ENHANCED PROMPT WRAPPERS
# =============================================================================

def enhance_prompt_for_oss(base_prompt: str) -> str:
    """
    Enhance prompt for OSS-20B to enforce stronger RAG citations

    Args:
        base_prompt: Original comprehensive prompt

    Returns:
        Enhanced prompt with citation requirements
    """
    return f"""{CITATION_ENFORCEMENT_PREFIX}

{base_prompt}

{CITATION_ENFORCEMENT_SUFFIX}"""


def enhance_prompt_for_gemma(base_prompt: str) -> str:
    """
    Enhance prompt for Gemma-27B to enforce better formatting/structure

    Args:
        base_prompt: Original comprehensive prompt

    Returns:
        Enhanced prompt with formatting requirements
    """
    return f"""{FORMATTING_ENFORCEMENT_PREFIX}

{base_prompt}

{FORMATTING_ENFORCEMENT_SUFFIX}"""


def get_enhanced_prompt(base_prompt: str, model_name: str) -> str:
    """
    Apply model-specific enhancements based on detected weaknesses

    Args:
        base_prompt: Original prompt
        model_name: Model identifier (e.g., "openai/gpt-oss-20b", "gemma-3-27b-it")

    Returns:
        Enhanced prompt optimized for the specific model
    """
    if "oss" in model_name.lower():
        # OSS models need stronger citation enforcement
        return enhance_prompt_for_oss(base_prompt)
    elif "gemma" in model_name.lower():
        # Gemma models need better formatting structure
        return enhance_prompt_for_gemma(base_prompt)
    else:
        # Unknown model - apply both enhancements
        enhanced = enhance_prompt_for_oss(base_prompt)
        return enhance_prompt_for_gemma(enhanced)


# =============================================================================
# EXAMPLE CITATION SECTION (To be injected when RAG context is available)
# =============================================================================

CITATION_EXAMPLES = """

═══════════════════════════════════════════════════════════════════════════
💡 CITATION EXAMPLES (Study these patterns):
═══════════════════════════════════════════════════════════════════════════

EXAMPLE 1 - Financial Metric:
"Total assets decreased from PLN 25,866 thousand in 2022 to PLN 24,162 thousand in 2024,
representing a -3.3% CAGR (Source: Consolidated Financial Statements 2024, Statement of
Financial Position, p. 8). This decline was primarily driven by reductions in property,
plant and equipment, which decreased by 4.0% annually (Source: Financial Statements 2023,
Note 12, p. 34)."

EXAMPLE 2 - Risk Disclosure:
"Management identified foreign exchange risk as a material exposure, noting that approximately
45% of revenues are denominated in EUR while 70% of costs are in PLN (Source: Directors' Report
2024, Risk Factors section, p. 67). The company estimates that a 10% depreciation of PLN
against EUR would improve EBIT by approximately PLN 150 million (Source: Annual Report 2024,
Sensitivity Analysis, p. 89)."

EXAMPLE 3 - Strategic Initiative:
"The company announced a three-year digital transformation program with planned investments
of PLN 200 million focused on production automation and supply chain optimization (Source:
Directors' Report 2024, Strategic Initiatives, p. 23). Management expects these investments
to yield annual cost savings of PLN 50-60 million starting in 2026 (Source: Management
Discussion & Analysis 2024, p. 45)."

═══════════════════════════════════════════════════════════════════════════
"""
