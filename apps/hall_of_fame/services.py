from .models import HallOfFame
import requests


def get_all_architects():
    return HallOfFame.objects.all()


def send_message_to_architect(architect_id, message):
    try:
        architect = HallOfFame.objects.get(id=architect_id)
        payload = {
            "topic": "Message from current Architect",
            "text": message,
            "target_emails": [architect.email],
        }
        try:
            response = requests.post(
                "http://docker_go:8080/send_letter",
                json=payload,
                timeout=3,
            )
            if response.status_code != 200:
                print(f"Mailer error: {response.text}")
            else:
                print(f"Message successfully sent to {architect.email}")
        except Exception as e:
            print(f"Failed to send mail via Go service: {e}")

        return True

    except HallOfFame.DoesNotExist:
        return False
