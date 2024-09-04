from src.models.vacation import Limit, VacationType

vacation_limits = [
    Limit(vacation_type=VacationType.ANNUAL_PAID, available_days=28),
    Limit(vacation_type=VacationType.UNPAID, available_days=14),
]

vacation_limits_dict = {limit.vacation_type: limit for limit in vacation_limits}
