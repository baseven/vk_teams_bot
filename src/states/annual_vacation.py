# Определение состояний и переходов для annual_vacation

# Состояния, относящиеся к annual_vacation
annual_vacation_states = [
    'annual_vacation_menu',
    'annual_vacation_confirm_period',  # Подтверждение выбранного периода отпуска
    'annual_vacation_create_vacation',

    'annual_vacation_enter_start_date',
    'annual_vacation_enter_end_date',
    'annual_vacation_check_limits',
    'annual_vacation_check_overlap',
    'annual_vacation_create_vacation',
    'annual_vacation_completed'
]

# Переходы для состояний внутри annual_vacation
annual_vacation_transitions = [
    {'trigger': 'to_annual_vacation_confirm_period', 'source': 'annual_vacation_menu',
     'dest': 'annual_vacation_confirm_period'},
    {'trigger': 'to_annual_vacation_create_vacation', 'source': 'annual_vacation_menu',
     'dest': 'annual_vacation_create_vacation'},
    {'trigger': 'to_annual_vacation_create_vacation', 'source': 'annual_vacation_confirm_period',
     'dest': 'annual_vacation_create_vacation'},

    {'trigger': 'enter_end_date', 'source': 'annual_vacation_enter_start_date', 'dest': 'annual_vacation_enter_end_date'},
    {'trigger': 'check_limits', 'source': 'annual_vacation_enter_end_date', 'dest': 'annual_vacation_check_limits'},
    {'trigger': 'check_overlap', 'source': 'annual_vacation_check_limits', 'dest': 'annual_vacation_check_overlap'},
    {'trigger': 'create_vacation', 'source': 'annual_vacation_check_overlap', 'dest': 'annual_vacation_create_vacation'},
    {'trigger': 'complete', 'source': 'annual_vacation_create_vacation', 'dest': 'annual_vacation_completed'},
    {'trigger': 'finish_annual_vacation', 'source': 'annual_vacation_completed', 'dest': 'main_menu'}
]
