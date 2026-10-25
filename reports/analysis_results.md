# Analysis Results — Customer Support & Service Operations

## Dataset
- Tickets: 2,400
- Synthetic agents: 12
- Reporting period: 2025; backlog age cutoff: 2026-01-01
- Validation: 5 unit tests passed

## KPI snapshot

| KPI | Result |
|---|---:|
| Open backlog | 725 tickets |
| First-response SLA rate | 69.4% |
| Resolution SLA rate | 68.1% |
| Average resolution time | 42.9 hours |
| Average CSAT | 4.02 / 5 |

## Interpretation
About 30% of eligible tickets with recorded outcomes miss the first-response SLA. Resolution SLA attainment is slightly lower than first-response attainment. Investigate results by priority, category, and channel before recommending staffing or process changes. Average CSAT reflects rated tickets only.

## Caveats
All results come from deterministic synthetic data. SLA rates exclude ineligible tickets and missing outcomes; missing CSAT is not zero. The HTML dashboard is a browser preview, not a native Power BI report.

## Reproduce
Run: python src/generate_data.py
Then: python src/analyze_support.py
Tests: python -m unittest discover -s tests -v
