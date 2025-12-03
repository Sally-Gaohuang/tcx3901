# file: api/services/insurer_service.py
from sqlmodel import Session, select
from api.database.database import engine
from api.models import PolicyCategory, Bid, BiddingRound

def get_required_categories():
    with Session(engine) as session:
        categories = session.exec(
            select(PolicyCategory)
        ).all()
        return categories


def submit_bid(insurer_id: int, category_id: int, round_id: int, premium: float):
    with Session(engine) as session:
        bid = Bid(
            insurer_id=insurer_id,
            category_id=category_id,
            round_id=round_id,
            premium=premium
        )
        session.add(bid)
        session.commit()
        return bid


def update_bid(bid_id: int, premium: float):
    with Session(engine) as session:
        bid = session.get(Bid, bid_id)
        if not bid:
            return {"error": "Bid not found"}

        bid.premium = premium
        session.commit()
        return bid
