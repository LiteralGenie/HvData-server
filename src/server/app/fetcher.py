from classes.parsers import LotteryParser, SuperParser, UserParser
from classes.models import Equip, Lottery, SuperAuction
from classes.models import LotteryItem, LotteryType

from sqlalchemy import select, func
from sqlalchemy.orm import Session, subqueryload

import attr, contextlib, time


def serialize(model):
    return {
        col.name: str(getattr(model, col.name))
        for col in model.__table__.columns
    }

class LotteryFetcher:
    db_session: Session
    lotto_parser: LotteryParser

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

        return lotto

    def lottery_latest(self, type: LotteryType):
        seconds_elapsed = time.time() - LotteryParser.START_DATES[type]
        days_elapsed = seconds_elapsed // 86400
                
        return dict(
            id = 1+days_elapsed,
            start = LotteryParser.START_DATES[type] + days_elapsed*86400
        )

class SuperFetcher:
    db_session: Session
    super_parser: SuperParser

    _last_list_scan: float = 0

    def super_auction(self, id: int):
        with self.db_session.begin() as session:
            stmt = select(SuperAuction).where(SuperAuction.id == id).options(subqueryload('*'))
            auc = session.execute(stmt).scalar()

            if auc is None:
                aucs = self.super_parser.fetch_list()
                [session.merge(x) for x in aucs]
                
                auc = next(x for x in aucs if x.id == id)
                if auc is None:
                    raise IndexError
            else:
                session.expunge_all()

            if len(auc.items) == 0:
                auc.items = self.super_parser.fetch_items(id=id)
                [session.merge(x) for x in auc.items]

        return auc
    
    @contextlib.contextmanager
    def super_list(self):
        with self.db_session.begin() as session:
            stmt = select(SuperAuction).order_by(SuperAuction.end_date.desc())
            latest: SuperAuction = session.execute(stmt).scalar()

            elapsed = time.time() - latest.end_date
            if elapsed > 6.25 * 86400:
                if time.time() - self._last_list_scan > 15*60:
                    aucs = self.super_parser.fetch_list()
                    [session.merge(x) for x in aucs]

                    self._last_list_scan = time.time()
            
            aucs = session.execute(stmt).scalars().all()
            yield aucs

@attr.s(auto_attribs=True)
class Fetcher(LotteryFetcher, SuperFetcher):
    db_session: Session
    lotto_parser: LotteryParser
    super_parser: SuperParser
    user_parser: UserParser