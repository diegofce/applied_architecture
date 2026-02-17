from uuid import uuid4

from todo_app.domain.services.id_generator import IdGenerator


class UUIDGenerator(IdGenerator):
    def next_id(self) -> str:
        return str(uuid4())
