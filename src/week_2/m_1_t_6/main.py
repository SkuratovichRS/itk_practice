import threading as th

from database import DbSession, TaskQueue, close_orm, init_orm
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

print_lock = th.Lock()


def create_test_data(session: Session) -> None:
    with session:
        objects = [
            TaskQueue(task_name=f"task_{i}", status="pending") for i in range(1, 6)
        ]
        session.add_all(objects)
        session.commit()


def remove_test_data(session: Session) -> None:
    with session:
        session.execute(delete(TaskQueue))
        session.commit()


def fetch_task(session: Session) -> None:
    with session:
        with print_lock:
            print(f"Fetching task: {th.current_thread().name}")
        stmt = (
            select(TaskQueue)
            .where(TaskQueue.status == "pending")
            .order_by(TaskQueue.id)
            .limit(1)
            .with_for_update(skip_locked=True)
        )
        result = session.execute(stmt)
        task = result.scalar_one_or_none()
        if task is None:
            with print_lock:
                print(f"No tasks to process: {th.current_thread().name}")
            return
        with print_lock:
            print(
                f"Processing task: {task.task_name}, current status: {task.status}: {th.current_thread().name}"
            )
        task.status = "processing"
        session.commit()
        session.refresh(task)
    with print_lock:
        print(
            f"Task processed: {task.task_name}, current status: {task.status}: {th.current_thread().name}"
        )


def run_threads() -> None:
    threads = []
    for _ in range(10):
        session = DbSession()
        thread = th.Thread(target=fetch_task, args=(session,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print("All tasks processed")


def main() -> None:
    session = DbSession()
    try:
        init_orm()
        create_test_data(session)
        run_threads()
    except Exception as e:
        print(e)
    finally:
        remove_test_data(session)
        close_orm()
        print("Done")


if __name__ == "__main__":
    main()
