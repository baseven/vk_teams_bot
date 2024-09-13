reschedule_vacation_states = [
    'reschedule_vacation_menu',
    'reschedule_vacation',
    'entering_new_vacation_dates',
    'confirm_reschedule_vacation',

]

reschedule_vacation_transitions = [
    {'trigger': 'to_reschedule_vacation', 'source': 'reschedule_vacation_menu',
     'dest': 'reschedule_vacation'},
    {'trigger': 'to_entering_new_vacation_dates', 'source': 'reschedule_vacation',
     'dest': 'entering_new_vacation_dates'},
    {'trigger': 'to_confirm_reschedule_vacation', 'source': 'entering_new_vacation_dates',
     'dest': 'confirm_reschedule_vacation'},
]
