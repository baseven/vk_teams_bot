annual_vacation_states = [
    'annual_vacation_menu',
    'handle_annual_vacation',
    'create_annual_vacation',
    'confirm_annual_vacation',
]

annual_vacation_transitions = [
    {'trigger': 'to_handle_annual_vacation', 'source': 'annual_vacation_menu',
     'dest': 'handle_annual_vacation'},
    {'trigger': 'to_create_annual_vacation', 'source': 'annual_vacation_menu',
     'dest': 'create_annual_vacation'},
    {'trigger': 'to_create_annual_vacation', 'source': 'handle_annual_vacation',
     'dest': 'create_annual_vacation'},
    {'trigger': 'to_confirm_annual_vacation', 'source': 'create_annual_vacation',
     'dest': 'confirm_annual_vacation'},
]
