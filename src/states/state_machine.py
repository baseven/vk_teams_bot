from transitions import Machine
from services.database_service import DatabaseService
from models.user_state import UserState

# Экземпляр DatabaseService для работы с базами данных
database_service = DatabaseService()


class BotStateMachine:
    states = ['main_menu', 'vacations', 'certificates']

    transitions = [
        {'trigger': 'to_vacations', 'source': 'main_menu', 'dest': 'vacations'},
        {'trigger': 'to_main_menu', 'source': '*', 'dest': 'main_menu'},
        {'trigger': 'to_certificates', 'source': 'main_menu', 'dest': 'certificates'}
    ]

    def __init__(self, user_id, initial_state='main_menu'):
        self.user_id = user_id
        self.state = initial_state  # Инициализация состояния
        # Инициализация машины состояний
        self.machine = Machine(model=self,
                               states=BotStateMachine.states,
                               transitions=BotStateMachine.transitions,
                               initial=initial_state)

    def save_state(self):
        # Сохранение состояния в Redis и MongoDB через DatabaseService
        user_state = UserState(user_id=self.user_id, state=self.state)
        database_service.save_state(user_state)

    @classmethod
    def load_state(cls, user_id):
        # Загрузка состояния из Redis или MongoDB через DatabaseService
        user_state = database_service.load_state(user_id)
        return cls(user_id, user_state.state)
