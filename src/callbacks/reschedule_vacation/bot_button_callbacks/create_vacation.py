import logging

from bot.event import Event, EventType

from src.sessions import UserSession

logger = logging.getLogger(__name__)

CREATE_NEW_VACATION_TEXT = "Введите период. Пожалуйста, укажите период в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ"


# TODO: Rename, because there should be a correspondence between the state and the name of the function.
# TODO: It is necessary to indicate what type of leave is being created, or we use the type of leave that was.
def create_new_vacation_cb(
        bot,
        user_session: UserSession,
        user_id: str,
        event: Event,
        callback_data_value: str
) -> None:
    logger.info(f"Create annual vacation callback for {user_id}")
    user_session.state_machine.to_entering_new_vacation_dates()
    user_session.save_session()

    bot.edit_text(
        chat_id=user_id,
        msg_id=user_session.get_last_bot_message_id(),
        text=CREATE_NEW_VACATION_TEXT
    )
