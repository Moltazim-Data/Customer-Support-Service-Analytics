CREATE TABLE agents (
  agent_id VARCHAR(10) PRIMARY KEY,
  agent_name VARCHAR(100) NOT NULL,
  team VARCHAR(30) NOT NULL,
  region VARCHAR(50) NOT NULL
);

CREATE TABLE support_tickets (
  ticket_id VARCHAR(10) PRIMARY KEY,
  customer_id VARCHAR(10) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  first_response_at TIMESTAMP NULL,
  closed_at TIMESTAMP NULL,
  status VARCHAR(20) NOT NULL,
  priority VARCHAR(10) NOT NULL,
  category VARCHAR(40) NOT NULL,
  channel VARCHAR(20) NOT NULL,
  agent_id VARCHAR(10) NOT NULL REFERENCES agents(agent_id),
  response_hours DECIMAL(10,2),
  resolution_hours DECIMAL(10,2),
  sla_eligible BOOLEAN NOT NULL,
  csat_score INTEGER,
  response_sla_hours DECIMAL(10,2),
  resolution_sla_hours DECIMAL(10,2),
  first_response_sla_met BOOLEAN,
  resolution_sla_met BOOLEAN,
  backlog_age_days DECIMAL(10,2),
  CHECK (csat_score IS NULL OR csat_score BETWEEN 1 AND 5),
  CHECK (response_hours IS NULL OR response_hours >= 0),
  CHECK (resolution_hours IS NULL OR resolution_hours >= 0)
);
