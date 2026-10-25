"""Generate deterministic synthetic customer-support ticket and agent data."""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
N_TICKETS = 2400
OUT = Path(__file__).resolve().parents[1] / "data"

def generate():
    rng = np.random.default_rng(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    agent_rows = [
        ("A001", "Ava Chen", "Tier 1", "North America"), ("A002", "Noah Patel", "Tier 1", "Europe"),
        ("A003", "Mia Garcia", "Tier 1", "North America"), ("A004", "Liam Wilson", "Tier 2", "Europe"),
        ("A005", "Sophia Brown", "Tier 2", "Asia Pacific"), ("A006", "Ethan Martin", "Tier 2", "North America"),
        ("A007", "Isabella Davis", "Specialist", "Europe"), ("A008", "Lucas Anderson", "Specialist", "Asia Pacific"),
        ("A009", "Amir Hassan", "Tier 1", "Middle East"), ("A010", "Ella Thompson", "Tier 2", "Europe"),
        ("A011", "Oliver Kim", "Tier 1", "Asia Pacific"), ("A012", "Grace Taylor", "Specialist", "North America"),
    ]
    agents = pd.DataFrame(agent_rows, columns=["agent_id", "agent_name", "team", "region"])
    agents.to_csv(OUT / "agents.csv", index=False)
    start, end = pd.Timestamp("2025-01-01"), pd.Timestamp("2025-12-31 23:59:59")
    seconds = int((end - start).total_seconds())
    created = pd.Series(start + pd.to_timedelta(rng.integers(0, seconds, N_TICKETS), unit="s")).sort_values().reset_index(drop=True)
    categories = np.array(["Billing", "Technical", "Account Access", "Shipping", "Product Question", "Returns"])
    channels = np.array(["Email", "Chat", "Web Form", "Phone", "Social"])
    priorities = np.array(["Low", "Normal", "High", "Urgent"])
    statuses = np.array(["Resolved", "Closed", "Open", "Pending", "Escalated"])
    category = rng.choice(categories, N_TICKETS, p=[.18,.24,.16,.14,.16,.12])
    channel = rng.choice(channels, N_TICKETS, p=[.30,.27,.22,.15,.06])
    priority = rng.choice(priorities, N_TICKETS, p=[.18,.48,.27,.07])
    status = rng.choice(statuses, N_TICKETS, p=[.42,.28,.13,.10,.07])
    agent_ids = rng.choice(agents.agent_id.to_numpy(), N_TICKETS)
    customer_ids = [f"C{v:05d}" for v in rng.integers(1, 1801, N_TICKETS)]
    response_target = {"Low":24,"Normal":8,"High":4,"Urgent":1}
    resolution_target = {"Low":120,"Normal":48,"High":24,"Urgent":8}
    response_hours, resolution_hours, eligible_list, csat, closed_at, first_response_at = [], [], [], [], [], []
    for i, p in enumerate(priority):
        response = float(np.clip(rng.gamma(1.7, response_target[p]/2.1), .05, 72))
        resolution = float(np.clip(rng.gamma(2.0, resolution_target[p]/2.3), response/2, 240))
        eligible = bool(rng.random() > .04)
        is_closed = status[i] in ("Resolved", "Closed")
        has_response = rng.random() > .035
        response_hours.append(round(response,2) if has_response else np.nan)
        eligible_list.append(eligible)
        first_response_at.append(created[i] + pd.to_timedelta(response, unit="h") if has_response else pd.NaT)
        if is_closed:
            closed_at.append(created[i] + pd.to_timedelta(resolution, unit="h"))
            resolution_hours.append(round(resolution,2))
            csat.append(int(np.clip(round(rng.normal(4.1-max(resolution-resolution_target[p],0)/180,.85)),1,5)) if rng.random()<.62 else np.nan)
        else:
            closed_at.append(pd.NaT); resolution_hours.append(np.nan); csat.append(np.nan)
    df = pd.DataFrame({
        "ticket_id":[f"T{n:06d}" for n in range(1,N_TICKETS+1)], "customer_id":customer_ids,
        "created_at":created, "first_response_at":first_response_at, "closed_at":closed_at,
        "status":status, "priority":priority, "category":category, "channel":channel, "agent_id":agent_ids,
        "response_hours":response_hours, "resolution_hours":resolution_hours, "sla_eligible":eligible_list,
        "csat_score":csat})
    df["response_sla_hours"] = df.priority.map(response_target)
    df["resolution_sla_hours"] = df.priority.map(resolution_target)
    df["first_response_sla_met"] = np.where(df.sla_eligible & df.response_hours.notna(), df.response_hours <= df.response_sla_hours, np.nan)
    df["resolution_sla_met"] = np.where(df.sla_eligible & df.resolution_hours.notna(), df.resolution_hours <= df.resolution_sla_hours, np.nan)
    df["backlog_age_days"] = np.where(df.closed_at.isna(), ((pd.Timestamp("2026-01-01")-df.created_at).dt.total_seconds()/86400).round(2), np.nan)
    df.to_csv(OUT/"support_tickets.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")
    print(f"Wrote {len(df):,} tickets and {len(agents):,} agents to {OUT}")

if __name__ == "__main__":
    generate()
