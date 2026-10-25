# Power BI Dashboard Build Guide

## 1. Generate data
Run `python src/generate_data.py` and `python src/analyze_support.py` from the repository root.

## 2. Import
In Power BI Desktop, choose **Get data → Text/CSV** and import `data/support_tickets.csv` and `data/agents.csv`. Set timestamp, numeric, boolean, and categorical types explicitly.

## 3. Model
Create a one-to-many relationship from `agents[agent_id]` to `support_tickets[agent_id]`. Create a calendar/date table and relate its date column to the ticket creation date. Mark it as the date table.

## 4. Measures
Add measures from `measures.dax`. Format SLA rates as percentages, CSAT to two decimals, and durations in hours.

## 5. Pages
- **Executive Overview:** total tickets, open backlog, response SLA, resolution SLA, average resolution, average CSAT.
- **Demand & Mix:** tickets over time; breakdown by channel, category, and priority.
- **SLA & Efficiency:** SLA rates by priority/category; average response and resolution durations.
- **Backlog & Team:** backlog age bands, open tickets by priority and agent, CSAT by team.

## 6. Validate
Reconcile ticket totals and backlog with Python output. SLA denominators should include eligible records with recorded outcomes only. Missing CSAT is not zero. Avoid publishing customer IDs in screenshots.

This repository includes DAX and a build guide, not a native `.pbix` or a deployed Power BI report.