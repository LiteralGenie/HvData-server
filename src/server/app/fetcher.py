from classes.parsers import LotteryParser, SuperParser, UserParser
from classes.models import Equip, Lottery, SuperAuction
from classes.models import LotteryItem, LotteryType

from sqlalchemy import select
from sqlalchemy.orm import Session, subqueryload

import attr


def serialize(model):
    return {
        col.name: str(getattr(model, col.name))
        for col in model.__table__.columns
    }

@attr.s(auto_attribs=True)
class Fetcher:
    db_session: Session
    lotto_parser: LotteryParser
    super_parser: SuperParser
    user_parser: UserParser

    def lottery(self, id: int, type: LotteryType):
        with self.db_session.begin() as session:
            stmt = select(Lottery).where(Lottery.id == id, Lottery.type == type).options(subqueryload('*'))
            lotto = session.execute(stmt).scalar()
            
            if lotto is None:
                lotto = self.lotto_parser.fetch_one(type=type, id=id)
                self.lotto_parser.initialize_winners()
                session.merge(lotto)
            else:
                session.expunge_all()

            print(type, lotto.type)

        return lotto