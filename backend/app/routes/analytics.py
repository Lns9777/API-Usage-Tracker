from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ApiUsage, Model, Project, Provider

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    rows = db.query(ApiUsage).all()
    count = len(rows)
    total_tokens = sum(r.total_tokens for r in rows)
    total_cost = sum(r.total_cost for r in rows)
    avg_latency = (sum(r.latency_ms for r in rows) / count) if count else 0
    error_rate = (
        ((sum(1 for r in rows if r.status != "success") / count) * 100) if count else 0
    )
    return {
        "requests": count,
        "tokens": total_tokens,
        "cost": total_cost,
        "average_latency_ms": avg_latency,
        "error_rate": error_rate,
    }


@router.get("/cost")
def cost(db: Session = Depends(get_db)):
    rows = (
        db.query(
            func.date(ApiUsage.timestamp).label("day"), func.sum(ApiUsage.total_cost)
        )
        .group_by("day")
        .all()
    )
    return [{"date": str(day), "cost": cost or 0} for day, cost in rows]


@router.get("/tokens")
def tokens(db: Session = Depends(get_db)):
    rows = (
        db.query(
            func.date(ApiUsage.timestamp).label("day"),
            func.sum(ApiUsage.input_tokens),
            func.sum(ApiUsage.output_tokens),
            func.sum(ApiUsage.thinking_tokens),
            func.sum(ApiUsage.cached_tokens),
        )
        .group_by("day")
        .all()
    )
    return [
        {
            "date": str(day),
            "input": i or 0,
            "output": o or 0,
            "thinking": t or 0,
            "cached": c or 0,
        }
        for day, i, o, t, c in rows
    ]


@router.get("/latency")
def latency(db: Session = Depends(get_db)):
    rows = [row.latency_ms for row in db.query(ApiUsage).all()]
    if not rows:
        return {"average": 0, "p50": 0, "p95": 0, "p99": 0}
    rows.sort()
    count = len(rows)
    return {
        "average": sum(rows) / count,
        "p50": rows[int(count * 0.5) - 1 if count > 1 else 0],
        "p95": rows[int(count * 0.95) - 1 if count > 1 else 0],
        "p99": rows[int(count * 0.99) - 1 if count > 1 else 0],
    }


@router.get("/errors")
def errors(db: Session = Depends(get_db)):
    rows = (
        db.query(ApiUsage.error_type, func.count(ApiUsage.id))
        .filter(ApiUsage.status != "success")
        .group_by(ApiUsage.error_type)
        .all()
    )
    return [
        {"error_type": error_type or "Unknown", "count": count}
        for error_type, count in rows
    ]


@router.get("/by-project")
def by_project(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Project.name,
            func.count(ApiUsage.id),
            func.sum(ApiUsage.total_tokens),
            func.sum(ApiUsage.total_cost),
            func.avg(ApiUsage.latency_ms),
        )
        .join(ApiUsage, ApiUsage.project_id == Project.id)
        .group_by(Project.name)
        .all()
    )
    return [
        {
            "project": name,
            "requests": req or 0,
            "tokens": tokens or 0,
            "cost": cost or 0,
            "latency_ms": latency or 0,
        }
        for name, req, tokens, cost, latency in rows
    ]


@router.get("/by-provider")
def by_provider(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Provider.name,
            func.count(ApiUsage.id),
            func.sum(ApiUsage.total_tokens),
            func.sum(ApiUsage.total_cost),
            func.avg(ApiUsage.latency_ms),
        )
        .join(ApiUsage, ApiUsage.provider_id == Provider.id)
        .group_by(Provider.name)
        .all()
    )
    return [
        {
            "provider": name,
            "requests": req or 0,
            "tokens": tokens or 0,
            "cost": cost or 0,
            "latency_ms": latency or 0,
        }
        for name, req, tokens, cost, latency in rows
    ]


@router.get("/by-model")
def by_model(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Model.model_name,
            func.count(ApiUsage.id),
            func.sum(ApiUsage.total_tokens),
            func.sum(ApiUsage.total_cost),
            func.avg(ApiUsage.latency_ms),
        )
        .join(ApiUsage, ApiUsage.model_id == Model.id)
        .group_by(Model.model_name)
        .all()
    )
    return [
        {
            "model": name,
            "requests": req or 0,
            "tokens": tokens or 0,
            "cost": cost or 0,
            "latency_ms": latency or 0,
        }
        for name, req, tokens, cost, latency in rows
    ]
