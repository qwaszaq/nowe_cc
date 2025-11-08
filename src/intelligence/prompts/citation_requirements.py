"""
Citation Requirements Module for Intelligence Reports

This module provides aggressive citation enforcement for all analysis agents.
It is prepended to comprehensive mode prompts to ensure minimum citation counts.

Target: 40+ total citations across 6 agents = 8+ citations per agent minimum
"""

# Citation enforcement text that gets prepended to all comprehensive system prompts
CITATION_ENFORCEMENT = """
═══════════════════════════════════════════════════════════════════
🚨 CRITICAL CITATION REQUIREMENT 🚨
═══════════════════════════════════════════════════════════════════

**YOU MUST INCLUDE AT LEAST 8 CITATIONS WITH PAGE NUMBERS IN YOUR ANALYSIS**

This is MANDATORY. Your analysis will be rejected if it contains fewer than 8 citations.

CITATION FORMAT (use EXACTLY this format):
[Source 1: Grupa_Azoty_Financial_Statements_2024.pdf, Page 15]
[Source 2: Grupa_Azoty_Directors_Report_2024.pdf, Page 87]

EXAMPLES OF PROPER CITATIONS:

Good ✅:
"Total assets declined 12% to PLN 24,162 million [Source 1: Financial_Statements_2024.pdf, Page 8],
driven primarily by inventory write-downs of PLN 2.1 billion [Source 2: Directors_Report_2024.pdf, Page 34]."

Good ✅:
"Management attributed the PLN 4.2 billion loss to three factors: energy costs (PLN 1.8B),
raw material inflation (PLN 1.3B), and demand contraction (PLN 1.1B) [Source 3: Directors_Report_2023.pdf, Page 45-47]."

Good ✅:
"The company's debt-to-equity ratio deteriorated from 0.65 in 2021 to 2.31 in 2024
[Source 4: Financial_Statements_2024.pdf, Page 12], signaling severe financial distress."

BAD ❌:
"Total assets declined significantly." (no citation, no specific number)

BAD ❌:
"According to the annual report, losses were substantial." (vague, no page number, no document name)

═══════════════════════════════════════════════════════════════════
WHERE TO FIND CITATION-WORTHY INFORMATION:
═══════════════════════════════════════════════════════════════════

Your analysis has access to TWO sources of information:

1. **Financial Data Tables** (provided in the prompt below)
   - These do NOT need citations (they are extracted data)
   - Use these for baseline metrics and ratios

2. **Additional Context from Company Documents** (RAG-retrieved context)
   - THIS REQUIRES CITATIONS
   - When you see sections labeled "Additional Context from Company Documents"
   - Every factual claim from this context MUST include [Source X: filename.pdf, Page Y]
   - Examples of citation-worthy claims:
     * Management explanations ("Management stated...", "The company attributed...")
     * Strategic initiatives ("The Board approved...", "Management launched...")
     * Market conditions ("Demand fell by...", "Competitors reported...")
     * Operational challenges ("Production was halted...", "Energy costs rose...")
     * Forward guidance ("Management expects...", "The company projects...")

═══════════════════════════════════════════════════════════════════
CITATION CHECKLIST (Review before submitting your analysis):
═══════════════════════════════════════════════════════════════════

Before you finalize your analysis, COUNT YOUR CITATIONS and verify:

✓ [ ] I have included AT LEAST 8 citations
✓ [ ] Each citation includes filename AND page number
✓ [ ] Citations use EXACT format: [Source N: filename.pdf, Page X]
✓ [ ] Each major claim from RAG context has a citation
✓ [ ] Management quotes/explanations are cited
✓ [ ] Specific operational details are cited
✓ [ ] Strategic initiatives mentioned are cited
✓ [ ] Forward-looking statements are cited

If you cannot find 8 citation-worthy facts in the RAG context, then:
- Request more context ("More details needed on...")
- Focus on areas where RAG context is rich
- Prioritize management discussion sections
- Look for year-over-year explanations

═══════════════════════════════════════════════════════════════════
MINIMUM CITATION TARGETS BY SECTION:
═══════════════════════════════════════════════════════════════════

For a comprehensive analysis, distribute citations as follows:

- Section 1 (Executive Summary): 0-1 citations (summary doesn't need heavy citations)
- Section 2 (Deep Dive Analysis): 3-4 citations (cite management explanations)
- Section 3 (Trend Analysis): 2-3 citations (cite strategic initiatives, market conditions)
- Section 4 (Additional Analysis): 2-3 citations (cite operational details, challenges)
- Section 5 (Scoring/Conclusion): 0-1 citations (conclusions based on analysis)

TOTAL: 8+ citations minimum

═══════════════════════════════════════════════════════════════════

**REMINDER: Your analysis MUST include at least 8 properly formatted citations.**

If RAG context is limited, you may see sections like:
"Additional Context from Company Documents: No relevant context found."

In this case, acknowledge the limitation but still aim for maximum citations from
available context. If truly no context is available, note this explicitly in your analysis.

═══════════════════════════════════════════════════════════════════
"""


def add_citation_enforcement(system_prompt: str) -> str:
    """
    Prepend citation enforcement to a system prompt

    Args:
        system_prompt: Original system prompt

    Returns:
        Enhanced prompt with citation requirements
    """
    return CITATION_ENFORCEMENT + "\n\n" + system_prompt


def get_citation_examples() -> str:
    """
    Get citation examples for reference

    Returns:
        String with citation format examples
    """
    return """
CITATION FORMAT EXAMPLES:

1. Single source:
   [Source 1: Grupa_Azoty_Financial_Statements_2024.pdf, Page 15]

2. Multiple pages from same source:
   [Source 1: Grupa_Azoty_Directors_Report_2024.pdf, Pages 34-37]

3. Two sources supporting same claim:
   [Source 1: FS_2024.pdf, Page 8; Source 2: Directors_Report_2024.pdf, Page 12]

4. Quote with citation:
   "The company expects to return to profitability by Q3 2025" [Source 3: Directors_Report_2024.pdf, Page 156].

5. Multiple facts, one citation:
   Management attributed the loss to three factors: energy costs, raw materials, and demand contraction
   [Source 2: Directors_Report_2023.pdf, Pages 45-47].
"""


# Test/validation function
if __name__ == "__main__":
    print("Citation Requirements Module")
    print("=" * 80)
    print("\nThis module enforces minimum citation counts in intelligence reports.")
    print("\nTarget: 8+ citations per agent (6 agents = 48+ total citations)")
    print("\nUsage:")
    print("  from src.intelligence.prompts.citation_requirements import add_citation_enforcement")
    print("  enhanced_prompt = add_citation_enforcement(original_system_prompt)")
    print("\n" + "=" * 80)
    print("\nCitation Enforcement Text Preview:")
    print("=" * 80)
    print(CITATION_ENFORCEMENT[:500] + "...\n")
