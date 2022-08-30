import typing

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from alws import database
from alws.auth import get_current_superuser
from alws.crud import user as user_crud
from alws.dependencies import get_db
from alws.errors import UserError
from alws.schemas import user_schema


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get(
    '/all_users',
    response_model=typing.List[user_schema.User],
)
async def get_all_users(db: database.Session = Depends(get_db)):
    return await user_crud.get_all_users(db)

@router.put(
    '/{user_id}',
    response_model=user_schema.UserOpResult
)
async def modify_user(user_id: int, payload: user_schema.UserUpdate,
                      db: database.Session = Depends(get_db),
                      _=Depends(get_current_superuser)
                      ) -> user_schema.UserOpResult:
    await user_crud.update_user(db, user_id, payload)
    return user_schema.UserOpResult(success=True)

# TODO: Delete route
@router.patch('/{user_id}/activate')
async def activate_user(user_id: int, db: database.Session = Depends(get_db),
                      _=Depends(get_current_superuser)
                      ) -> user_schema.UserOpResult:
    await user_crud.activate_user(user_id, db)
    return user_schema.UserOpResult(success=True)


# TODO: Delete route
@router.patch('/{user_id}/deactivate')
async def deactivate_user(user_id: int, db: database.Session = Depends(get_db),
                          _=Depends(get_current_superuser)
                          ) -> user_schema.UserOpResult:
    await user_crud.deactivate_user(user_id, db)
    return user_schema.UserOpResult(success=True)


# TODO: Delete route
@router.patch('/{user_id}/grant-superuser')
async def activate_user(user_id: int, db: database.Session = Depends(get_db),
                      _=Depends(get_current_superuser)
                      ) -> user_schema.UserOpResult:
    await user_crud.make_superuser(user_id, db)
    return user_schema.UserOpResult(success=True)


# TODO: Delete route
@router.patch('/{user_id}/revoke-superuser')
async def activate_user(user_id: int, db: database.Session = Depends(get_db),
                      _=Depends(get_current_superuser)
                      ) -> user_schema.UserOpResult:
    await user_crud.make_usual_user(user_id, db)
    return user_schema.UserOpResult(success=True)


@router.delete('/{user_id}/remove')
async def remove_user(user_id: int, db: database.Session = Depends(get_db),
                      _=Depends(get_current_superuser)
                      ) -> user_schema.UserOpResult:
    try:
        await user_crud.remove_user(user_id, db)
        return user_schema.UserOpResult(
            success=True,
            message=f'Successfully removed user with id {user_id}')
    except UserError as err:
        raise HTTPException(
            detail=str(err),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
