# Metric Definitions

| Metric | Definition | Interpretation |
|---|---|---|
| Total Tickets | Count of unique ticket IDs | One generated row per ticket |
| Open Backlog | Status is not Resolved or Closed | Snapshot, not a live queue |
| First Response SLA Rate | SLA-met eligible tickets with outcome / eligible tickets with outcome | Blanks are excluded |
| Resolution SLA Rate | SLA-met eligible closed tickets / eligible closed tickets with outcome | Open tickets are not failures |
| Average First Response | Mean of non-null response_hours | Pair with median/percentiles when possible |
| Average Resolution | Mean of non-null resolution_hours | Closed tickets only |
| Average CSAT | Mean of available csat_score values | Missing ratings are not zero |
| Backlog Aging | Days since creation for tickets not closed at cutoff | Synthetic cutoff: 2026-01-01 |
| Tickets Created | Count by created date | Not the same as tickets closed |
