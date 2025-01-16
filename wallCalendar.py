### Big Calendar Component
# Produces a formatted list for use with an Excel script. Final product is a single-page 3' x 4' wall poster with room for every day of the year.
from datetime import date, timedelta

# Change this for each year being calculated.
year = 2025

dt = date(year, 1, 1)
# Set end date for list to last day of the year.
end_dt = date(year+1, 1, 1)-timedelta(days=1)

dates = []
days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

while dt <= end_dt:
    # Add header for each new month.
    if dt.day == 1:
        dates.append(months[dt.month-1])
    
    # Format each date as "# DAY" for the calendar.
    dates.append(
        str(dt.day) + " " + days[dt.isoweekday()-1]
        )

    dt += timedelta(days=1)

print(dates)