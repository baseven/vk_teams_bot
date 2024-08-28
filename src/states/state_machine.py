from transitions import Machine
from services.database_service import DatabaseService
from models.user_state import UserState
from src.states.annual_vacation import annual_vacation_states, annual_vacation_transitions


# Экземпляр DatabaseService для работы с базами данных
database_service = DatabaseService()


# TODO:
#  1) Передача DatabaseService в качестве зависимости через конструктор улучшает тестируемость,
#  поскольку позволяет использовать заглушки или мок-объекты при тестировании.
#  2) Использование констант для состояний и переходов:
class BotStateMachine:
    # Определение состояний верхнего уровня
    states = [
        'main_menu',
        *annual_vacation_states,  # Подключение состояний для annual_vacation
        'unpaid_vacation',
        'view_limits_and_schedule',
        'reschedule_vacation',
        'cancel_vacation'
    ]

    # Определение переходов между состояниями
    transitions = [
        {'trigger': 'to_main_menu', 'source': '*', 'dest': 'main_menu'},
        {'trigger': 'to_annual_vacation_menu', 'source': 'main_menu', 'dest': 'annual_vacation_menu'},
        {'trigger': 'to_unpaid_vacation', 'source': 'main_menu', 'dest': 'unpaid_vacation'},
        {'trigger': 'to_view_limits_and_schedule', 'source': 'main_menu', 'dest': 'view_limits_and_schedule'},  # Переход в новое состояние
        {'trigger': 'to_reschedule_vacation', 'source': 'main_menu', 'dest': 'reschedule_vacation'},
        {'trigger': 'to_cancel_vacation', 'source': 'main_menu', 'dest': 'cancel_vacation'},
    ] + annual_vacation_transitions  # Добавление переходов для annual_vacation

    def __init__(self, user_id, initial_state='main_menu', last_message_id=None, start_date=None, end_date=None):
        self.user_id = user_id
        self.state = initial_state  # Инициализация состояния
        self.last_message_id = last_message_id  # Инициализация идентификатора последнего сообщения
        self.start_date = start_date
        self.end_date = end_date
        # Инициализация машины состояний
        self.machine = Machine(model=self,
                               states=BotStateMachine.states,
                               transitions=BotStateMachine.transitions,
                               initial=initial_state)

    def save_state(self):
        # Сохранение состояния в Redis и MongoDB через DatabaseService
        user_state = UserState(user_id=self.user_id, state=self.state, last_message_id=self.last_message_id,
                               start_date=self.start_date, end_date=self.end_date)
        database_service.save_state(user_state)

    @classmethod
    def load_state(cls, user_id):
        # Загрузка состояния из Redis или MongoDB через DatabaseService
        user_state = database_service.load_state(user_id)
        return cls(user_id=user_id, initial_state=user_state.state, last_message_id=user_state.last_message_id,
                   start_date=user_state.start_date, end_date=user_state.end_date)

    def set_vacation_dates(self, vacation_dates):
        """Устанавливает start_date и end_date на основе строки vacation_dates."""
        start_date, end_date = vacation_dates.split(" - ")
        self.start_date = start_date
        self.end_date = end_date
        print(f"Даты отпуска установлены: {self.start_date} по {self.end_date}")

    def get_vacation_dates(self) -> str:
        """Возвращает строку с датами отпуска в формате 'start_date - end_date'."""
        if self.start_date and self.end_date:
            return f"{self.start_date} - {self.end_date}"
        else:
            return "Даты отпуска не установлены"

    def reset_vacation_dates(self):
        """Сбрасывает start_date и end_date в None."""
        self.start_date = None
        self.end_date = None
        print("Даты отпуска сброшены до None.")
