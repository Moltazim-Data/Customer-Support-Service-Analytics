# Customer Support & Service Operations Analytics

A portfolio-ready analytics project using **Python, SQL, and Power BI** to monitor ticket demand, SLA performance, resolution efficiency, backlog, and customer satisfaction.

> **Data note:** All records are synthetic. The HTML dashboard is a lightweight preview, not a native Power BI `.pbix` report.

## Business questions
1. How does ticket demand change by time, channel, category, and priority?
2. What percentage of eligible tickets meet first-response and resolution SLAs?
3. Which categories and priorities have the longest resolution times?
4. How large and old is the open backlog?
5. How do workload and customer satisfaction vary across teams?

## Repository structure
- `src/generate_data.py` — deterministic synthetic ticket and agent data
- `src/analyze_support.py` — data validation and KPI outputs
- `sql/` — relational schema and analysis queries
- `powerbi/` — DAX measures, build guide, HTML preview
- `docs/` — dictionary, metric definitions, insight playbook, limitations
- `tests/` — unit tests
- `.github/workflows/` — automated validation

## Quick start
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python src/generate_data.py
python src/analyze_support.py
python -m unittest discover -s tests -v
```

## Power BI
Run the scripts, import `data/support_tickets.csv` and `data/agents.csv` in Power BI Desktop, create the agent relationship and date table, then add measures from `powerbi/measures.dax`. Follow `powerbi/dashboard_build_guide.md`.

Suggested pages: Executive Overview; Demand & Mix; SLA & Efficiency; Backlog & Team.

## Interpretation and limitations
- SLA rates use eligible tickets with recorded outcomes; blanks are not treated as failures.
- CSAT is a 1–5 score and exists only for a subset of closed tickets.
- Backlog age uses a synthetic reporting cutoff of 2026-01-01.
- Data and SLA targets are illustrative, not representative of a real organization.
- This repository does not include a native `.pbix` or deployed Power BI report.

MIT License. See `LICENSE`.
