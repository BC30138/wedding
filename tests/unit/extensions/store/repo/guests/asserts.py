"""Вспомогательные функции для сравнения гостей."""
from wedding.ctx.guests.entity.guest import GuestEntity
from wedding.extensions.store.repo.guests.models import Guests


def assert_guest_model_with_entity(
    model: Guests,
    entity: GuestEntity,
):
    """Сравнение модели гости с его сущностью."""
    assert model.id == entity.id
    assert model.male == entity.male.value
    assert model.first_name == entity.first_name
    assert model.middle_name == entity.middle_name
    assert model.last_name == entity.last_name
