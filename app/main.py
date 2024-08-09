from fastapi import FastAPI, WebSocket, Query, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.websocket_manager import WebSocketManager
from app.exchange_clients import BinanceClient, KrakenClient
from typing import Optional
import asyncio

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

ws_manager = WebSocketManager()
binance_client = BinanceClient()
kraken_client = KrakenClient()


async def update_prices_periodically():
    while True:
        await binance_client.update_prices()
        await kraken_client.update_prices()
        await asyncio.sleep(60)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_prices_periodically())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_message(data)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


@app.get("/prices")
async def get_prices(pair: Optional[str] = Query(None), exchange: Optional[str] = Query(None)):
    binance_prices = binance_client.get_cached_prices()
    kraken_prices = kraken_client.get_cached_prices()

    all_prices = {**binance_prices, **kraken_prices}

    if not pair and not exchange:
        return all_prices

    if exchange:
        if exchange.lower() == "binance":
            exchange_prices = binance_prices
        elif exchange.lower() == "kraken":
            exchange_prices = kraken_prices
        else:
            return {"error": "Unknown exchange"}

        if pair:
            return {pair: exchange_prices.get(pair)}
        return exchange_prices

    if pair:
        return {pair: all_prices.get(pair)}

    return all_prices


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("frontend/index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)
