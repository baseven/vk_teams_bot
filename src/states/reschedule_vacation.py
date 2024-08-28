reschedule_vacation_states = [
    'reschedule_vacation_menu',
    'reschedule_vacation_change_period',
    'reschedule_vacation_create_vacation',

]

reschedule_vacation_transitions = [
    {'trigger': 'to_reschedule_vacation_change_period', 'source': 'reschedule_vacation_menu',
     'dest': 'reschedule_vacation_change_period'},
    {'trigger': 'to_reschedule_vacation_create_vacation', 'source': 'reschedule_vacation_change_period',
     'dest': 'reschedule_vacation_create_vacation'},
]
