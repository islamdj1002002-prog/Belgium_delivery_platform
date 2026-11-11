from fastapi import FastAPI
from app.schemas import (
    ShipmentUpdate,
    ShipmentStatusUpdate,
    ShipmentCreate, 
    ShipmentResponse,
    ShipmentBase
)

shipments = [
    {
        "id": 1, 
        "tracking_number": "BE1001",
        "status": "registered",
        "destination": "Brussels",
    },
    {
        "id": 2, 
        "tracking_number": "BE1002",
        "status": "registered",
        "destination": "Antwerp",
    },
]

app = FastAPI(title="Belgium Delivery API")



@app.get("/shipments", response_model=list[ShipmentResponse])
def get_shipments(destination: str = None, limit: int = 10):
    results = shipments

    if destination:
        results = [
            shipment for shipment in results
            if shipment["destination"] == destination
        ]

    return results[:limit]


@app.get("/shipment/{shipment_id}")
def get_shipment(shipment_id: int):
    for shipment in shipments:
        if shipment["id"] == shipment_id:
            return shipment

    return {"error": "Shipment not found"}


@app.post("/shipments", response_model=ShipmentResponse, status_code=201)
def create_ship(shipment: ShipmentCreate):
    new_id = max(item["id"] for item in shipments) + 1

    new_shipment = {
        "id": new_id,
        "tracking_number": shipment.tracking_number,
        "destination": shipment.destination,
        "status": "registered"
    }

    shipments.append(new_shipment)
    return new_shipment

@app.get("/tracking/{tracking_number}")
def tracking_shipment(tracking_number: str):
    for shipment in shipments:
        if shipment["tracking_number"] == tracking_number:
            return shipment

    return {"error": "Shipment not found"}   


@app.patch("/shipments/{shipment_id}/status")
def update_shipment_status(shipment_id: int, update: ShipmentStatusUpdate):
    for shipment in shipments:
        if shipment["id"] == shipment_id:
            shipment["status"] = update.status
            return shipment

    return {"error": "Shipment not found"}



@app.put("/shipments/{shipment_id}")
def update_shipment(
    shipment_id: int,
    shipment_update: ShipmentUpdate
    ):
    for shipment in shipments:
        if shipment["id"] == shipment_id:
            shipment["tracking_number"] = shipment_update.tracking_number
            shipment["status"] = shipment_update.status
            shipment["destination"] = shipment_update.destination
            return shipment

    return {"error": "Shipment not found"}
            


@app.delete("/shipments/{shipment_id}")
def delete_shipment(shipment_id: int):
    for shipment in shipments:
        if shipment["id"] == shipment_id:
            shipments.remove(shipment)
            return {"message": "Shipment deleted"}

    return {"error": "Shipment not found"}