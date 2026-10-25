import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from bot.logging_config import logger
from bot.service import place_order

load_dotenv()


class OrderRequest(BaseModel):
    market: str = Field(default="FUTURES")
    symbol: str
    side: str
    type: str
    quantity: float
    price: Optional[float] = None


app = FastAPI(title="Primetrade Bot API", version="1.0.0")

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")
origins = [origin.strip() for origin in cors_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    details = [
        {
            "field": ".".join(str(item) for item in error.get("loc", []) if item != "body"),
            "message": error.get("msg", "Invalid value"),
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "message": "Invalid request payload",
                "details": details,
            },
        },
    )


@app.get("/health")
def health():
    return {"success": True, "data": {"status": "ok"}}


@app.post("/api/orders")
def create_order(payload: OrderRequest):
    try:
        summary = place_order(
            market=payload.market,
            symbol=payload.symbol,
            side=payload.side,
            order_type=payload.type,
            quantity=payload.quantity,
            price=payload.price,
        )
        return {"success": True, "data": summary}
    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": {"message": str(exc)}},
        )
    except Exception as exc:
        logger.error(f"API execution error: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": {"message": "Internal server error"}},
        )
