import os
from fastapi import FastAPI, HTTPException
from typing import Optional
import httpx
import asyncio

app = FastAPI()

# Fetch the URL from environment variable, fallback to default
DATA_SERVICE_URL = os.getenv("DATA_SERVICE_URL", "http://data/client-libraries/")


@app.get("/")
async def iqm_client_metadata(client_key: Optional[str] = None):
    try:
        response = httpx.get(DATA_SERVICE_URL, timeout=5.0)
        response.raise_for_status()
        await asyncio.sleep(0.1)
        all_data = response.json()

        if client_key:
            if client_key in all_data:
                return {client_key: all_data[client_key]}
        else:
            return all_data

    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Error connecting to data service")

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=502, detail="Invalid response from data service"
        )

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
