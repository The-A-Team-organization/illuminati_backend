from .models import Record


def get_all_records():
    return Record.objects.all()


def create_record(data):
    record = Record.objects.create(**data)
    return record


def get_record_by_id(record_id):
    record = Record.objects.get(id=record_id)
    return record
