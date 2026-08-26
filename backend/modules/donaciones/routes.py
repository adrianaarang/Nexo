from fastapi import APIRouter, HTTPException, Query
from modules.donaciones import models
from modules.donaciones.schemas import (
    DonationCreate,
    DonationResponse,
    DonationStatusUpdate,
    DonationType,
)

router = APIRouter(prefix="/api/donaciones", tags=["donaciones"])


@router.get("", response_model=list[DonationResponse])
def list_donations(donation_type: DonationType | None = Query(default=None, alias="tipo")):
    return models.list_donations(donation_type=donation_type)


@router.get("/{donation_id}", response_model=DonationResponse)
def get_donation(donation_id: int):
    donation = models.get_donation(donation_id)
    if donation is None:
        raise HTTPException(status_code=404, detail="Donación no encontrada")
    return donation


@router.post("", response_model=DonationResponse, status_code=201)
def create_donation(donation: DonationCreate):
    return models.create_donation(donation)


@router.patch("/{donation_id}/estado", response_model=DonationResponse)
def update_donation_status(donation_id: int, change: DonationStatusUpdate):
    donation = models.update_status(donation_id, change.status)
    if donation is None:
        raise HTTPException(status_code=404, detail="Donación no encontrada")
    return donation
