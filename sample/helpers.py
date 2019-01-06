import datetime

def get_answer():
    """Get an answer."""
    return True

def get_offset(time_str: str) -> datetime.timedelta:
    t: datetime = datetime.datetime.strptime(time_str + 'm', '%I:%M%p')
    midnight = datetime.datetime.strptime("12:00a" + 'm', '%I:%M%p')
    offset_midnight: datetime.timedelta = t - midnight
    return offset_midnight

def parse_course(subject_course, rows:dict): 
    for row in rows:
        time_str: str = row["Time"]
        time_many = time_str.split("-")
        start_str: str = time_many[0]
        end_str: str = time_many[1]
        # ref: https://stackoverflow.com/questions/41308016/python-converting-time-format-1200a-to-24hour
        start_offset = get_offset(start_str)
        end_offset = get_offset(end_str)