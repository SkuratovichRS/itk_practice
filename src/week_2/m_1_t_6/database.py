from datetime import datetime

from sqlalchemy import DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine(
    "postgresql://postgres:postgres@127.0.0.1:5432/m_1_t_6",
)

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
