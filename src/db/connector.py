import hashlib
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import select

from db.engine import PostgresSession
from db.models.record import Record, RecordModel
from db.models.user import User, UserData


class RecordQuery(BaseModel):
    device_id: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None


class DBConnector:
    def __init__(self, postgres_session: PostgresSession) -> None:
        self._session = postgres_session

    async def register_user(self, user_data: UserData) -> None:
        password_hash = self.calculate_password_hash(password=user_data.password)
        user = User(
            login=user_data.login,
            password_hash=password_hash,
            devices=[],
        )
        self._session.add(user)
        await self._session.commit()

    async def user_exists(self, user_data: UserData) -> bool:
        password_hash = self.calculate_password_hash(password=user_data.password)
        result = await self._session.scalars(
            select(User).where(
                User.login == user_data.login,
                User.password_hash == password_hash,
            )
        )
        user = result.first()
        return user is not None

    @staticmethod
    def calculate_password_hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    async def get_records(
        self,
        record_query: RecordQuery,
    ) -> list[RecordModel]:
        query = select(Record)

        if record_query.device_id:
            query = query.where(Record.device_id == record_query.device_id)

        if record_query.start_date:
            query = query.where(Record.when >= record_query.start_date)

        if record_query.end_date:
            query = query.where(Record.when <= record_query.end_date)

        results = await self._session.execute(query).all()
        records = results.scalars().all()
        return [record.cast_to_model() for record in records]

    async def save_record(self, record: Record) -> None:
        self._session.add(record)
        await self._session.commit()


def create_db_connector() -> DBConnector:
    session = PostgresSession()
    try:
        yield DBConnector(postgres_session=session)
    finally:
        session.close()
