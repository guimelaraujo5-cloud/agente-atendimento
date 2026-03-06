from fastapi import FastAPI

app = FastAPI(title="guimel-assist", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "guimel-assist"}


@app.post("/webhooks/whatsapp")
def whatsapp_webhook() -> dict:
    return {"received": True}


@app.get("/webhooks/whatsapp/verify")
def whatsapp_verify() -> dict:
    return {"verify": "ok"}


@app.post("/webhooks/instagram")
def instagram_webhook() -> dict:
    return {"received": True}


@app.get("/webhooks/instagram/verify")
def instagram_verify() -> dict:
    return {"verify": "ok"}
