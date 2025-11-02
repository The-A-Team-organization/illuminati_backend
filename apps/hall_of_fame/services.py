from .models import HallOfFame


def get_all_architects():
    return HallOfFame.objects.all()


def send_message_to_architect(architect_id, message):
    try:
        architect = HallOfFame.objects.get(id=architect_id)
        print(f"[MOCK] Sent message to {architect.email}: {message}")
        return True
    except HallOfFame.DoesNotExist:
        return False
