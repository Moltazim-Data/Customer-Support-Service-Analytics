"""Validate support data and produce KPI summaries."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"

def safe_rate(numerator, denominator):
    return numerator/denominator if denominator else None

def validate(tickets, agents):
    errors=[]
    if "ticket_id" not in tickets or tickets.ticket_id.duplicated().any(): errors.append("ticket_id must be unique")
    if "agent_id" not in agents or agents.agent_id.duplicated().any(): errors.append("agent_id must be unique")
    if not set(tickets.agent_id.dropna()).issubset(set(agents.agent_id)): errors.append("ticket agent_id must exist in agents")
    for col in ["created_at","status","priority","category","channel","agent_id"]:
        if col not in tickets or tickets[col].isna().any(): errors.append(f"{col} must be populated")
    if (tickets.response_hours.dropna()<0).any() or (tickets.resolution_hours.dropna()<0).any(): errors.append("durations must be non-negative")
    closed=tickets.status.isin(["Resolved","Closed"])
    if (closed != tickets.closed_at.notna()).any(): errors.append("status/closed_at consistency check failed")
    return errors

def main():
    tickets=pd.read_csv(DATA/"support_tickets.csv",parse_dates=["created_at","first_response_at","closed_at"])
    agents=pd.read_csv(DATA/"agents.csv")
    errors=validate(tickets,agents)
    if errors: raise ValueError("\n".join(errors))
    tickets["created_date"]=tickets.created_at.dt.date.astype(str)
    daily=tickets.groupby("created_date").agg(tickets_created=("ticket_id","nunique"),avg_response_hours=("response_hours","mean"),avg_resolution_hours=("resolution_hours","mean"),open_backlog=("status",lambda s:(~s.isin(["Resolved","Closed"])).sum()),avg_csat=("csat_score","mean")).reset_index()
    eligible_response=tickets.sla_eligible & tickets.first_response_sla_met.notna()
    eligible_resolution=tickets.sla_eligible & tickets.resolution_sla_met.notna()
    category=tickets.groupby("category").agg(ticket_count=("ticket_id","nunique"),avg_response_hours=("response_hours","mean"),avg_resolution_hours=("resolution_hours","mean"),avg_csat=("csat_score","mean")).reset_index()
    category.to_csv(DATA/"category_kpis.csv",index=False)
    daily.to_csv(DATA/"daily_kpis.csv",index=False)
    print(f"Tickets: {len(tickets):,}; open backlog: {(~tickets.status.isin(['Resolved','Closed'])).sum():,}")
    print(f"First-response SLA: {tickets.loc[eligible_response,'first_response_sla_met'].astype(float).mean():.1%}")
    print(f"Resolution SLA: {tickets.loc[eligible_resolution,'resolution_sla_met'].astype(float).mean():.1%}")
if __name__=="__main__": main()
