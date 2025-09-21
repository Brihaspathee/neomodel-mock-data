from collections import defaultdict

from models.portico import PPProvLocOfHours
import logging

log = logging.getLogger(__name__)


def format_time(code: str):
    # "A0800" -> "8:00", "P04:30" -> "16:30"
    meridian = code[0] # A or P
    hhmm = code[1:] # 0800 or 0430
    hour = int(hhmm[:2])
    minute = int(hhmm[2:])
    if meridian == "A":
        if hour == 12: # 12 AM -> 00
            hour = 0
    elif meridian == "P":
        if hour != 12: # add 12 except for 12 PM
            hour += 12
    return f"{hour:02}:{minute:02}"

def format_office_hours(prov_loc_office_hours: list[PPProvLocOfHours]):
    log.debug(f"prov_loc_office_hours - {prov_loc_office_hours}")
    day_map = {
        "MO": "MON",
        "TU": "TUE",
        "WE": "WED",
        "TH": "THU",
        "FR": "FRI",
        "SA": "SAT",
        "SU": "SUN"
    }

    # Group events by day
    grouped_events = defaultdict(list)
    for off_hour in prov_loc_office_hours:
        day = day_map.get(off_hour.dayofweek, off_hour.dayofweek) # Second argument is the default value of the map does not have the key
        grouped_events[day].append((off_hour.event, off_hour.time))

    log.debug(f"grouped_events - {grouped_events}")
    converted_office_hours = {}
    for day, events in grouped_events.items():
        # sort events by time
        events.sort(key=lambda x: (x[1][0], int(x[1][1:])))
        log.debug(f"sorted events - {events}")
        intervals = []
        open_time = None
        for event, time in events:
            if event == "O":
                open_time = f"{day} {format_time(time)}"
            elif event == "C" and open_time:
                close_time = f"{day} {format_time(time)}"
                intervals.append({"open": open_time, "close": close_time})
                open_time = None
            log.debug(f"intervals - {intervals}")
        converted_office_hours[day] = intervals
    log.debug(f"converted_office_hours - {converted_office_hours}")
    return converted_office_hours
