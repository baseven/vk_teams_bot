from datetime import datetime
from src.models.vacation import Limit,Vacation, VacationType, VacationStatus

vacations = [
    Vacation(
        vacation_id="1",
        vacation_type=VacationType.ANNUAL_PAID,
        start_date=datetime.strptime("01.01.2025", "%d.%m.%Y"),
        end_date=datetime.strptime("15.01.2025", "%d.%m.%Y"),
        status=VacationStatus.PLANNED
    ),
    Vacation(
        vacation_id="3",
        vacation_type=VacationType.ANNUAL_PAID,
        start_date=datetime.strptime("10.06.2025", "%d.%m.%Y"),
        end_date=datetime.strptime("20.06.2025", "%d.%m.%Y"),
        status=VacationStatus.PLANNED
    ),
    Vacation(
        vacation_id="2",
        vacation_type=VacationType.UNPAID,
        start_date=datetime.strptime("01.03.2025", "%d.%m.%Y"),
        end_date=datetime.strptime("05.03.2025", "%d.%m.%Y"),
        status=VacationStatus.PLANNED
    ),
]

limits = [
    Limit(vacation_type=VacationType.ANNUAL_PAID, available_days=28),
    Limit(vacation_type=VacationType.UNPAID, available_days=14),
]

limits_dict = {limit.vacation_type: limit for limit in limits}
