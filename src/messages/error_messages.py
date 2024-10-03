# TODO: Move to constants.py?
#  Enum for error messages
class ErrorMessages:
    DATE_FORMAT_ERROR = "Неверный формат даты. Пожалуйста, используйте формат ДД.ММ.ГГГГ - ДД.ММ.ГГГГ."
    DATE_ORDER_ERROR = "Дата начала не может быть позже даты окончания."
    PAST_DATE_ERROR = "Дата не может быть в прошлом."
    OVERLAP_ERROR = "Ваш отпуск пересекается с существующим отпуском."
