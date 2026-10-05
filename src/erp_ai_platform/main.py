from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root() -> dict[str, str]:
    return {"message":"ERP AI Platform is running"}


@app.get("/purchase-orders/{po_id}")
def read_purchase_order(po_id: int)-> dict[str, int]:
    return {"po_id": po_id}

