import time
from datetime import datetime


class TimestampMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, attrs)


class A(metaclass=TimestampMeta):
    pass


time.sleep(0.1)


class B(metaclass=TimestampMeta):
    pass


assert type(A.created_at) is type(B.created_at) is datetime
assert A.created_at != B.created_at
