import random

from fastapi import APIRouter, Depends, HTTPException

from app.repositories.contact_repo import ContactRepository, get_contact_repo
from app.repositories.lead_repo import LeadRepository, get_lead_repo
from app.repositories.operator_repo import OperatorRepository, get_operator_repo
from app.repositories.source_repo import SourceRepository, get_source_repo
from app.schemas.contact import ContactResponse, ContactCreate
from app.schemas.operator import OperatorResponse, OperatorCreate
from app.schemas.source import SourceResponse, SourceWeightCreate, SourceCreateRequest

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/operators", response_model=OperatorResponse)
async def create_operator(
    op: OperatorCreate,
    repo: OperatorRepository = Depends(get_operator_repo),
):
    return await repo.create(op.name, op.max_load_limit)


@router.post("/sources", response_model=SourceResponse)
async def create_source(
    request_data: SourceCreateRequest,
    repo: SourceRepository = Depends(get_source_repo),
):
    w_dicts = [w.model_dump() for w in request_data.weights]

    return await repo.create_with_weights(name=request_data.name, weights=w_dicts)


@router.post("/contacts", response_model=ContactResponse)
async def register_contact(
    request: ContactCreate,
    lead_repo: LeadRepository = Depends(get_lead_repo),
    source_repo: SourceRepository = Depends(get_source_repo),
    contact_repo: ContactRepository = Depends(get_contact_repo),
):

    lead = await lead_repo.get_or_create(request.lead_external_id)

    source_weights = await source_repo.get_weights_for_source(request.source_id)
    if not source_weights:
        raise HTTPException(
            status_code=404, detail="Source not found or no operators assigned"
        )

    candidates = []
    weights = []

    for sw in source_weights:
        operator = sw.operator

        if not operator.is_active:
            continue

        current_load = await contact_repo.get_active_load(operator.id)
        if current_load < operator.max_load_limit:
            candidates.append(operator)
            weights.append(sw.weight)

    selected_operator_id = None

    if candidates:
        chosen_operator = random.choices(candidates, weights=weights, k=1)[0]
        selected_operator_id = chosen_operator.id

    contact = await contact_repo.create(
        lead_id=lead.id, source_id=request.source_id, operator_id=selected_operator_id
    )

    return contact
