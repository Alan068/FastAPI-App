from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# SQLAlchemy requires a base class that other models can inherit from.
# Empty class definition not allowed, so using 'pass' -> means do nothing, class is empty but still valid.
