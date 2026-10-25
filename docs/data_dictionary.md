# Data Dictionary

## support_tickets.csv
| Field | Description |
|---|---|
| ticket_id | Unique synthetic ticket identifier |
| customer_id | Synthetic customer identifier; not real personal data |
| created_at | Ticket creation timestamp |
| first_response_at | First response timestamp; may be missing |
| closed_at | Close timestamp for Resolved/Closed tickets |
| status | Resolved, Closed, Open, Pending, Escalated |
| priority | Low, Normal, High, Urgent |
| category | Billing, Technical, Account Access, Shipping, Product Question, Returns |
| channel | Email, Chat, Web Form, Phone, Social |
| agent_id | Foreign key to agents |
| response_hours / resolution_hours | Durations; may be missing |
| sla_eligible | Whether ticket is eligible for SLA measurement |
| csat_score | Optional customer rating from 1 to 5 |
| response_sla_hours / resolution_sla_hours | Illustrative priority targets |
| first_response_sla_met / resolution_sla_met | SLA result; null when no eligible outcome |
| backlog_age_days | Age for open tickets at synthetic reporting cutoff |

## agents.csv
| Field | Description |
|---|---|
| agent_id | Unique synthetic agent ID |
| agent_name | Synthetic agent name |
| team | Tier 1, Tier 2, or Specialist |
| region | Assigned operating region |
