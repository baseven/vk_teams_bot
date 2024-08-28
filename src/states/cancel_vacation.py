cancel_vacation_states = [
    'cancel_vacation_menu',
    'cancel_vacation_delete_period',
]

cancel_vacation_transitions = [
    {'trigger': 'to_cancel_vacation_delete_period', 'source': 'cancel_vacation_menu',
     'dest': 'cancel_vacation_delete_period'},
]
