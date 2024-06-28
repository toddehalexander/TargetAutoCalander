import re
from datetime import datetime, time, timedelta
from ics import Calendar, Event
import pytz
import os

# Define the Pacific Time Zone
pacific_tz = pytz.timezone('US/Pacific')

def parse_schedule(schedule_text):
    lines = schedule_text.split('\n')
    current_year = None
    current_month = None
    current_day = None
    shifts = []
    temp_shift = {}

    for i, line in enumerate(lines):
        # Parse month and year
        month_year_match = re.match(r'(\w+)\s+(\d{4})', line)
        if month_year_match:
            current_month = datetime.strptime(month_year_match.group(1), '%B').month
            current_year = int(month_year_match.group(2))
        
        # Parse day
        day_match = re.match(r'(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday), (\w+) (\d+)', line)
        if day_match:
            current_day = int(day_match.group(3))
            month = datetime.strptime(day_match.group(2), '%B').month
            if month != current_month:
                current_month = month
                if current_month == 1 and current_year is not None:
                    current_year += 1
        
        # Parse shift
        time_match = re.match(r'(\d{2}):(\d{2})(AM|PM)', line)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))
            am_pm = time_match.group(3)
            
            # Convert to 24-hour format
            if am_pm == 'PM' and hour != 12:
                hour += 12
            elif am_pm == 'AM' and hour == 12:
                hour = 0
            
            shift_time = time(hour, minute)
            
            if 'start_time' not in temp_shift:
                temp_shift = {
                    'date': pacific_tz.localize(datetime(current_year, current_month, current_day)),
                    'start_time': shift_time
                }
            else:
                temp_shift['end_time'] = shift_time
                # Calculate shift duration
                start_datetime = temp_shift['date'].replace(hour=temp_shift['start_time'].hour, minute=temp_shift['start_time'].minute)
                end_datetime = temp_shift['date'].replace(hour=shift_time.hour, minute=shift_time.minute)
                if end_datetime <= start_datetime:
                    end_datetime += timedelta(days=1)
                duration = end_datetime - start_datetime
                temp_shift['duration'] = duration

                # Check for role
                role = 'Unknown'
                for j in range(i, min(i+5, len(lines))):  # Check next 4 lines for the role
                    if lines[j].strip() in ['Starbucks', 'Checkout Advocate']:
                        role = lines[j].strip()
                        break
                temp_shift['role'] = role

                shifts.append(temp_shift)
                temp_shift = {}

    return shifts

def get_schedule_range(shifts):
    if not shifts:
        return None, None
    start_date = min(shift['date'] for shift in shifts)
    end_date = max(shift['date'] for shift in shifts)
    return start_date, end_date

def create_ics_file(shifts, output_dir=''):
    if not shifts:
        return "No shifts to create a calendar for."

    start_date, end_date = get_schedule_range(shifts)
    year = start_date.year
    filename = f"work_schedule_{start_date.strftime('%b%d')}-{end_date.strftime('%b%d')}_{year}.ics"
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, filename)

    cal = Calendar()
    for shift in shifts:
        event = Event()
        event.name = f"Shift - {shift['role']}"
        
        start_datetime = shift['date'].replace(hour=shift['start_time'].hour, minute=shift['start_time'].minute)
        end_datetime = shift['date'].replace(hour=shift['end_time'].hour, minute=shift['end_time'].minute)
        
        if end_datetime <= start_datetime:
            end_datetime += timedelta(days=1)
        
        event.begin = start_datetime
        event.end = end_datetime
        
        event.description = f"Role: {shift['role']}\nDuration: {shift['duration']}"
        cal.events.add(event)

    with open(filename, 'w') as f:
        f.write(str(cal))
    return f"ICS file '{filename}' has been created."