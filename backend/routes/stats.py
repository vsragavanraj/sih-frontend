from fastapi import APIRouter
from database import get_dashboard_stats
from models.scan_models import DashboardStatsResponse

router = APIRouter(tags=["Dashboard Analytics"])

@router.get("/stats", response_model=DashboardStatsResponse)
async def get_stats():
    """
    GET /stats - Dashboard Analytics API Endpoint
    
    Returns total scans count, compliant count, non-compliant count,
    and accuracy score calculated from SQLite scan history.
    
    Example Output:
    {
       "total_scans": 100,
       "compliant": 82,
       "non_compliant": 18,
       "accuracy": 96
    }
    """
    stats_data = get_dashboard_stats()
    return DashboardStatsResponse(**stats_data)
