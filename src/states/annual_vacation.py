# Определение состояний и переходов для annual_vacation

# Состояния, относящиеся к annual_vacation
annual_vacation_states = [
    'annual_vacation_menu',
    'annual_vacation_confirm_period',  # Подтверждение выбранного периода отпуска
    'annual_vacation_create_vacation',
]

# Переходы для состояний внутри annual_vacation
annual_vacation_transitions = [
    {'trigger': 'to_annual_vacation_confirm_period', 'source': 'annual_vacation_menu',
     'dest': 'annual_vacation_confirm_period'},
    {'trigger': 'to_annual_vacation_create_vacation', 'source': 'annual_vacation_menu',
     'dest': 'annual_vacation_create_vacation'},
    {'trigger': 'to_annual_vacation_create_vacation', 'source': 'annual_vacation_confirm_period',
     'dest': 'annual_vacation_create_vacation'},
]
