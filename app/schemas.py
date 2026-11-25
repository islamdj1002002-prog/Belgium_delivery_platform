from pydantic import BaseModel, Field, ConfigDict


class ShipmentBase(BaseModel):
    tracking_number: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Трек-номер посылки",
    )

    destination: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Город доставки",


    )

class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(ShipmentBase):
    status: str = Field(
        ..., 
        min_length=3,
        max_length=30,
        description="Статус посылки",
    )



class ShipmentStatusUpdate(BaseModel):
    status: str = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Новый статус посылки",
    )


class ShipmentResponse(ShipmentBase):
    id: int
    status: str  

    model_config = ConfigDict(from_attributes=True)