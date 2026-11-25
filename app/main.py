from fastapi import FastAPI, HTTPException, Depends
from app.dependencies import get_current_user
from app.database import get_db
from app.schemas import (
    ShipmentUpdate,
    ShipmentStatusUpdate,
    ShipmentCreate, 
    ShipmentResponse,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    )
from app.crud import(
    delete_shipment,
    create_shipment,
    get_shipment, 
    get_shipments,
    get_shipment_by_tracking_number,
    update_shipment_status, 
    update_shipment
    ) 


app = FastAPI(title="Belgium Delivery API")



@app.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return user



@app.get("/shipments", response_model=list[ShipmentResponse])
async def get_shipments_endpoint(
    destination: str | None = None,
    limit: int = 10,
    skip: int = 0,
    db: AsyncSession = Depends(get_db),
    ):

    results = await get_shipments(
    destination=destination,
    limit=limit,
    skip=skip,
    db=db
    )

    return results


@app.get("/shipments/{shipment_id}", response_model=ShipmentResponse)
async def get_shipment_endpoint(shipment_id: int, db: AsyncSession = Depends(get_db)):
    shipment = await get_shipment(db=db, shipment_id=shipment_id)
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@app.post("/shipments", response_model=ShipmentResponse, status_code=201)
async def create_ship(shipment: ShipmentCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_shipment = await create_shipment(
        db=db,
        shipment=shipment
        )

    return new_shipment

@app.get("/tracking/{tracking_number}", 
        response_model=ShipmentResponse,
        )

async def tracking_shipment_endpoint(
    tracking_number: str, 
    db: AsyncSession = Depends(get_db),
    ):

    shipment = await get_shipment_by_tracking_number(
        db=db, 
        tracking_number=tracking_number,
        )
    
    if not shipment:
        raise HTTPException(
            status_code=404, 
            detail="Shipment not found",
            )
    return shipment
    


@app.patch("/shipments/{shipment_id}/status", 
        response_model=ShipmentResponse
        )
async def update_shipment_status_endpoint(
    shipment_id: int, 
    update: ShipmentStatusUpdate, 
    db: AsyncSession = Depends(get_db)
    ):

    shipment = await update_shipment_status(
        db=db, 
        shipment_id=shipment_id, 
        status=update.status,
        )
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment
    




@app.put("/shipments/{shipment_id}", 
        response_model=ShipmentResponse,
        )
async def update_shipment_endpoint(
    shipment_id: int,
    shipment_update: ShipmentUpdate,
    db: AsyncSession = Depends(get_db),
    ):

    shipment = await update_shipment(
        db=db, 
        shipment_id=shipment_id, 
        update=shipment_update
        )

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment
    

    
            


@app.delete("/shipments/{shipment_id}")
async def delete_shipment_endpoint(shipment_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_shipment(shipment_id=shipment_id, db=db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return {"message": "Shipment deleted"}