import arrow
import ics


class TimeEntry:
    def __init__(self, date, start: float, end: float):
        self.date = date
        self.start = start
        self.end = end
        self.duration = end - start
        print(str(start) + " -> " + str(end) + ": " + str(self.duration))

    def __repr__(self):
        return "TimeEntry(date=" + self.date.format() + ", duration=" + str(self.duration) + ")"


def create_time_entry(date: arrow.Arrow, start_hour: int, start_minute: int, end_hour: int, end_minute: int):
    if end_hour == 0 and end_minute == 0:
        end_hour = 24

    if end_hour < start_hour:  # Create two separate time entries if the recorded time is winds back due to midnight
        print("TWO ENTRIES FOR MIDNIGHT")
        print(date)
        print(str(start_hour) + ":" + str(start_minute))
        print(str(end_hour) + ":" + str(end_minute))
        return [create_time_entry(date, start_hour, start_minute, 24, 0)[0],
                create_time_entry(date.shift(days=1), 0, 0, end_hour, end_minute)[0]]

    start = start_hour + (start_minute / 60.0)
    end = end_hour + (end_minute / 60.0)

    return [TimeEntry(date, start, end)]


def parse_time_string(time_str: str):
    time_split = time_str.split(":", 1)

    return int(time_split[0]), int(time_split[1])


def parse_work_times(data: set):
    time_entry_list = []

    for time_entry in data:
        time_entry: ics.Todo

        if "-" not in time_entry.name:
            print("Invalid time entry " + time_entry.name + " on " + time_entry.due)
            continue

        time_split = time_entry.name.split("-", 1)
        start_time = time_split[0]
        end_time = time_split[1]

        if ":" not in start_time or ":" not in end_time:
            print("Invalid time entry " + time_entry.name + " on " + time_entry.due)
            continue

        (start_hour, start_minute) = parse_time_string(start_time)
        (end_hour, end_minute) = parse_time_string(end_time)

        time_entry_list.extend(create_time_entry(time_entry.due, start_hour, start_minute, end_hour, end_minute))

    return time_entry_list
