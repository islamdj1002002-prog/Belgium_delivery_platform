from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Shipment
from app.schemas import ShipmentCreate, ShipmentUpdate

from typing import Optional, Sequence

async def get_shipments(
        db: AsyncSession,
        destination: Optional[str] = None, 
        skip: int = 0,
        limit: int = 10,
    ) -> Sequence[Shipment]:
    stmt = select(Shipment)

    if destination:
        stmt = stmt.where(Shipment.destination == destination)
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_shipment(
        db: AsyncSession,
        shipment_id: int
) -> Optional[Shipment]:
    stmt = select(Shipment).where(Shipment.id == shipment_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_shipment(
        db: AsyncSession,
        shipment: ShipmentCreate,
) -> Shipment:
    new_shipment = Shipment(**shipment.model_dump())
    db.add(new_shipment)
    await db.commit()
    await db.refresh(new_shipment)

    return new_shipment


async def delete_shipment(
        db: AsyncSession,
        shipment_id: int,

) -> bool:
    shipment = await get_shipment(db=db, shipment_id=shipment_id)
    if shipment:
        await db.delete(shipment)
        await db.commit()
        return True
    return False



async def get_shipment_by_tracking_number(
    db: AsyncSession,
    tracking_number: str,
) -> Optional[Shipment]:
    stmt = select(Shipment).where(
        Shipment.tracking_number == tracking_number
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def update_shipment_status(
    db: AsyncSession,
    shipment_id: int,
    status: str,
    ) -> Optional[Shipment]:

    shipment = await get_shipment(
        db=db, 
        shipment_id=shipment_id
        )
    if not shipment:
        return None

    shipment.status = status

    await db.commit()
    await db.refresh(shipment)

    return shipment


async def update_shipment(db: AsyncSession, shipment_id: int, update: ShipmentUpdate) -> Optional[Shipment]:
    shipment = await get_shipment(db=db, shipment_id=shipment_id)
    
    if not shipment:
        return None
    
    shipment.tracking_number = update.tracking_number
    shipment.destination = update.destination
    shipment.status = update.status

    await db.commit()
    await db.refresh(shipment)

    return shipment
    
    