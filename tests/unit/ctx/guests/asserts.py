"""Вспомогательнае функции для сравнения объектов в домене guests."""
from wedding.ctx.guests.dto.data import GuestData
from wedding.ctx.guests.entity.guest import GuestEntity


def assert_guest_data_to_entity(
    data: GuestData,
    entity: GuestEntity,
):
    """Сравнивает данные гостя с его сущностью"""
    assert entity.first_name == data.first_name
    assert entity.middle_name == data.middle_name
    assert entity.last_name == data.last_name
    assert entity.male.value == data.male
