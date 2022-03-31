from typing import List

from fastapi import APIRouter, Depends
from alws import database

from alws.dependencies import get_db, JWTBearer
from alws.schemas import platform_flavors_schema as pf_schema
from alws.crud import platform_flavors as pf_crud

router = APIRouter(
    prefix='/platform_flavors',
    tags=['platform_flavors'],
    dependencies=[Depends(JWTBearer())]
)


@router.post('/', response_model=pf_schema.FlavourResponse)
async def create_flavour(
    flavour: pf_schema.CreateFlavour,
    db: database.Session = Depends(get_db)
):
    return await pf_crud.create_flavour(db, flavour)


@router.get('/', response_model=List[pf_schema.FlavourResponse])
async def get_flavours(
    db: database.Session = Depends(get_db)
):
    return await pf_crud.list_flavours(db)