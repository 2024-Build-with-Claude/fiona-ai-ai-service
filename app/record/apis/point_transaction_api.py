from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.infrastructure.dependencies import get_pageable_param
from app.infrastructure.schemas import PageableParamDTO, PageableResultDTO
from app.record.schemas import point_transaction_schema
from app.record.services import point_transaction_service
from app.user import models as user_model
from app.user.services import get_current_local_auth_user

router = APIRouter()


# @router.post("", response_model=point_transaction_schema.PointTransaction)
# def create_point_transaction(
#     transaction_data: point_transaction_schema.PointTransactionCreate,
#     db: Session = Depends(get_db),
# ):
#     return point_transaction_service.create_point_transaction(
#         transaction_data=transaction_data, db=db
#     )


@router.get(
    "/{transaction_id}", response_model=point_transaction_schema.PointTransaction
)
def get_point_transaction(transaction_id: str, db: Session = Depends(get_db)):
    transaction = point_transaction_service.get_point_transaction(transaction_id, db)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    return transaction


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=PageableResultDTO[point_transaction_schema.PointTransaction],
)
def point_transaction_list(
    page_params: PageableParamDTO = Depends(get_pageable_param),
    user: user_model.User = Depends(get_current_local_auth_user),
    db: Session = Depends(get_db),
):
    return point_transaction_service.get_point_transactions(
        page_params=page_params, user_id=user.id, db=db
    )


# @router.put(
#     path="/{transaction_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=point_transaction_schema.PointTransaction,
# )
# def update_point_transaction(
#     transaction_id: str,
#     transaction_update: point_transaction_schema.PointTransactionUpdate,
#     db: Session = Depends(get_db),
# ):
#     updated_transaction = point_transaction_service.update_point_transaction(
#         transaction_id=transaction_id, transaction_update=transaction_update, db=db
#     )
#     if not updated_transaction:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Transaction not found",
#         )
#     return updated_transaction


# @router.delete(
#     path="/{transaction_id}",
#     status_code=status.HTTP_200_OK,
# )
# def delete_point_transaction(
#     transaction_id: str,
#     db: Session = Depends(get_db),
# ):
#     message = point_transaction_service.delete_point_transaction(
#         transaction_id=transaction_id, db=db
#     )
#     if not message:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Transaction not found",
#         )
#     return {"message": message}
