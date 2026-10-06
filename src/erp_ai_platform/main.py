from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class PurchaseOrderItem(BaseModel):
    item_code: str
    qty: float = Field(gt=0)
    rate: float = Field(gt=0)

class PurchaseOrderCreate(BaseModel):
    supplier: str
    transaction_date: date
    items: list[PurchaseOrderItem] = Field(min_length=1)

class PurchaseOrder(PurchaseOrderCreate):
    id: int


purchase_orders: dict [int, PurchaseOrder] = {}


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "ERP AI Platform is running"}


@app.post("/purchase-orders", status_code=201)
def create_purchase_order(po: PurchaseOrderCreate) -> PurchaseOrder:
    global next_id
    new_po = PurchaseOrder(id=next_id, **po.model_dump())
    purchase_orders[next_id] = new_po
    next_id += 1
    return new_po


@app.get("/purchase-orders")
def list_purchase_orders() -> list[PurchaseOrder]:
    return list(purchase_orders.values())


@app.get("/purchase-orders/{po_id}")
def read_purchase_order(po_id: int) -> PurchaseOrder:
    if po_id not in purchase_orders:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return purchase_orders[po_id]

@app.delete("/purchase-orders/{po_id}")
def delete_purchase_order(po_id: int) -> dict[str, str]:
    if po_id not in purchase_orders:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    del purchase_orders[po_id]
    return {"message": f"Purchase Order {po_id} deleted"}