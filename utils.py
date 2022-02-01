from datetime import datetime


def get_time_now():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time

def admin_is_auth(senha: str):
    return senha == 'batatinha'
