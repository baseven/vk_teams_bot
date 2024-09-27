from src.actions.annual_vacation import AnnualVacationActions as Actions
from src.styles import ButtonStyle

annual_vacation_buttons = [
    [{"text": Actions.CREATE_ANNUAL_VACATION.text, "callbackData": Actions.CREATE_ANNUAL_VACATION.value, "style": ButtonStyle.PRIMARY.value}],
    [{"text": Actions.BACK_TO_MAIN_MENU.text, "callbackData": Actions.BACK_TO_MAIN_MENU.value, "style": ButtonStyle.PRIMARY.value}]
]

confirm_period_keyboard = [
    [{"text": Actions.CONFIRM_ANNUAL_VACATION.text, "callbackData": Actions.CONFIRM_ANNUAL_VACATION.value, "style": ButtonStyle.PRIMARY.value}],
    [{"text": Actions.CREATE_ANNUAL_VACATION.text, "callbackData": Actions.CREATE_ANNUAL_VACATION.value, "style": ButtonStyle.PRIMARY.value}],
    [{"text": Actions.BACK_TO_MAIN_MENU.text, "callbackData": Actions.BACK_TO_MAIN_MENU.value, "style": ButtonStyle.PRIMARY.value}]
]

accept_period_keyboard = [
    [{"text": Actions.CONFIRM_ANNUAL_VACATION.text, "callbackData": Actions.CONFIRM_ANNUAL_VACATION.value, "style": ButtonStyle.PRIMARY.value}],
    [{"text": Actions.BACK_TO_MAIN_MENU.text, "callbackData": Actions.BACK_TO_MAIN_MENU.value, "style": ButtonStyle.PRIMARY.value}]
]
