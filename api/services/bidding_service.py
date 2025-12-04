# file: api/services/bidding_service.py
from sqlmodel import Session, select
from api.database.database import engine
from api.models import Bid, BiddingRound, PolicyCategory, User
# from api.database.database import SessionLocal

def get_bids_for_round(round_id: int):
    with Session(engine) as session:
        bids = session.exec(
            select(Bid).where(Bid.round_id == round_id)
        ).all()
        return bids


def compare_bids(round_id: int):
    with Session(engine) as session:
        bids = session.exec(
            select(Bid, User)
            .join(User, User.user_id == Bid.insurer_id)
            .where(Bid.round_id == round_id)
        ).all()

        result = []
        for bid, insurer in bids:
            result.append({
                "insurer": insurer.username,
                "category": bid.category_id,
                "premium": bid.premium
            })
        return result
