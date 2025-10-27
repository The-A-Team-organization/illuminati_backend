from .models import Record


def get_all_records():
    return Record.objects.all()


def create_record(data):
    record = Record.objects.create(**data)
    return record
