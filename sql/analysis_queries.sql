-- KPI summary
SELECT COUNT(DISTINCT ticket_id) AS total_tickets,
       SUM(CASE WHEN status NOT IN ('Resolved','Closed') THEN 1 ELSE 0 END) AS open_backlog,
       AVG(response_hours) AS avg_response_hours,
       AVG(resolution_hours) AS avg_resolution_hours,
       AVG(csat_score) AS avg_csat
FROM support_tickets;

-- SLA rates use only eligible tickets with a recorded result.
SELECT
  AVG(CASE WHEN first_response_sla_met THEN 1.0 ELSE 0.0 END) AS first_response_sla_rate,
  AVG(CASE WHEN resolution_sla_met THEN 1.0 ELSE 0.0 END) AS resolution_sla_rate
FROM support_tickets
WHERE sla_eligible = TRUE;

-- Category performance
SELECT category, COUNT(*) AS ticket_count,
       AVG(resolution_hours) AS avg_resolution_hours,
       AVG(CASE WHEN resolution_sla_met THEN 1.0 ELSE 0.0 END) AS resolution_sla_rate
FROM support_tickets
WHERE sla_eligible = TRUE AND resolution_sla_met IS NOT NULL
GROUP BY category ORDER BY ticket_count DESC;

-- Backlog aging
SELECT priority,
       COUNT(*) AS open_tickets,
       AVG(backlog_age_days) AS avg_backlog_age_days
FROM support_tickets
WHERE status NOT IN ('Resolved','Closed')
GROUP BY priority ORDER BY open_tickets DESC;

-- Agent workload and CSAT; compare with caution because ticket mix differs.
SELECT a.agent_name, a.team, COUNT(t.ticket_id) AS assigned_tickets,
       AVG(t.resolution_hours) AS avg_resolution_hours, AVG(t.csat_score) AS avg_csat
FROM agents a LEFT JOIN support_tickets t ON a.agent_id=t.agent_id
GROUP BY a.agent_id, a.agent_name, a.team
ORDER BY assigned_tickets DESC;
