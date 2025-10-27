from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}

# TODO: Add more routes for balances, cycles, controls, etc.
