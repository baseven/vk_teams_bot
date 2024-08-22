from transitions import Machine
from services.database_service import DatabaseService
from models.user_state import UserState

# Экземпляр DatabaseService для работы с базами данных
database_service = DatabaseService()


# TODO:
#  1) Передача DatabaseService в качестве зависимости через конструктор улучшает тестируемость,
#  поскольку позволяет использовать заглушки или мок-объекты при тестировании.
#  2) Использование констант для состояний и переходов:
class BotStateMachine:
    states = ['main_menu', 'annual_vacation', 'unpaid_vacation', 'limits_and_schedule', 'reschedule_vacation',
              'cancel_vacation']

    transitions = [
        {'trigger': 'to_annual_vacation', 'source': 'main_menu', 'dest': 'annual_vacation'},
        {'trigger': 'to_unpaid_vacation', 'source': 'main_menu', 'dest': 'unpaid_vacation'},
        {'trigger': 'to_limits_and_schedule', 'source': 'main_menu', 'dest': 'limits_and_schedule'},
        {'trigger': 'to_reschedule_vacation', 'source': 'main_menu', 'dest': 'reschedule_vacation'},
        {'trigger': 'to_cancel_vacation', 'source': 'main_menu', 'dest': 'cancel_vacation'},
        {'trigger': 'to_main_menu', 'source': '*', 'dest': 'main_menu'},
    ]

    def __init__(self, user_id, initial_state='main_menu', last_message_id=None):
        self.user_id = user_id
        self.state = initial_state  # Инициализация состояния
        self.last_message_id = last_message_id  # Инициализация идентификатора последнего сообщения
        # Инициализация машины состояний
        self.machine = Machine(model=self,
                               states=BotStateMachine.states,
                               transitions=BotStateMachine.transitions,
                               initial=initial_state)

    def save_state(self):
        # Сохранение состояния в Redis и MongoDB через DatabaseService
        user_state = UserState(user_id=self.user_id, state=self.state, last_message_id=self.last_message_id)
        database_service.save_state(user_state)

    @classmethod
    def load_state(cls, user_id):
        # Загрузка состояния из Redis или MongoDB через DatabaseService
        user_state = database_service.load_state(user_id)
        return cls(user_id, user_state.state, user_state.last_message_id)
