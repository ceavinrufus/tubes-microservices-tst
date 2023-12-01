import datetime

def calculate_age(birthdate_str: str):
    birthdate = datetime.datetime.fromisoformat(birthdate_str)

    today = datetime.date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    return age
