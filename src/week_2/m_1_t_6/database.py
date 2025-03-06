import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()


pg_dsn = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)


engine = create_engine(pg_dsn)

DbSession = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class TaskQueue(Base):
    __tablename__ = "task_queue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_name: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


def init_orm() -> None:
    with engine.begin() as conn:
        Base.metadata.create_all(conn)


def close_orm() -> None:
    engine.dispose()
