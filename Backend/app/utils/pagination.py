from sqlalchemy.sql import Select


def paginate(query: Select, page: int, size: int):
    offset = (page - 1) * size
    return query.offset(offset).limit(size)
