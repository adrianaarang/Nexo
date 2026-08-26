from typing import Any
from db.database import get_cursor
from modules.donaciones.schemas import DonationCreate, DonationStatus, DonationType


def list_donations(donation_type: DonationType | None = None) -> list[dict[str, Any]]:
    conditions: list[str] = []
    params: list[str] = []

    if donation_type is not None:
        conditions.append("tipo = ?")
        params.append(donation_type.value)

    query = "SELECT * FROM donaciones"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY id ASC"

    with get_cursor() as cursor:
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def get_donation(donation_id: int) -> dict[str, Any] | None:
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM donaciones WHERE id = ?", (donation_id,))
        row = cursor.fetchone()
        return dict(row) if row is not None else None


def create_donation(donation: DonationCreate) -> dict[str, Any]:
    with get_cursor() as cursor:
        cursor.execute(
            """INSERT INTO donaciones (tipo, recurso, cantidad, descripcion, contacto, estado)
               VALUES (?, ?, ?, ?, ?, 'activa')""",
            (
                donation.donation_type.value,
                donation.resource.value,
                donation.quantity,
                donation.description,
                donation.contact,
            ),
        )
        donation_id = cursor.lastrowid
        cursor.execute("SELECT * FROM donaciones WHERE id = ?", (donation_id,))
        return dict(cursor.fetchone())


def update_status(donation_id: int, status: DonationStatus) -> dict[str, Any] | None:
    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE donaciones SET estado = ? WHERE id = ?",
            (status.value, donation_id),
        )
        if cursor.rowcount == 0:
            return None
        cursor.execute("SELECT * FROM donaciones WHERE id = ?", (donation_id,))
        return dict(cursor.fetchone())