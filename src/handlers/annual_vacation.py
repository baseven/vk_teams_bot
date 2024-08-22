import json
import logging
from src.states.state_machine import BotStateMachine

# Настройка логгера для модуля
logger = logging.getLogger(__name__)


def handle_annual_vacation(bot, state_machine, user_id, event):
    logger.info(f"Starting annual vacation process for user {user_id}")
    state_machine.to_annual_vacation_process()
    state_machine.save_state()

    # Здесь будет запрос к БД для получения лимитов
    # лимиты = запрос к БД
    bot.send_text(
        chat_id=user_id,
        text="Ваши лимиты:",
        # Отображение лимитов пользователю
    )

    # Здесь будет запрос к БД для получения текущих отпусков
    # текущие_отпуска = запрос к БД
    bot.send_text(
        chat_id=user_id,
        text="Ваши текущие отпуска:",
        # Отображение текущих отпусков пользователю
    )

    bot.send_text(
        chat_id=user_id,
        text="Введите дату начала отпуска (в формате ДД.ММ.ГГГГ):"
    )


def handle_start_date(bot, state_machine, user_id, event):
    start_date = event.text
    # Проверка формата даты на валидность
    if not is_valid_date(start_date):
        bot.send_text(
            chat_id=user_id,
            text="Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ:"
        )
        return

    state_machine.start_date = start_date
    state_machine.save_state()
    bot.send_text(
        chat_id=user_id,
        text="Введите дату окончания отпуска (в формате ДД.ММ.ГГГГ):"
    )


def handle_end_date(bot, state_machine, user_id, event):
    end_date = event.text
    # Проверка формата даты на валидность
    if not is_valid_date(end_date):
        bot.send_text(
            chat_id=user_id,
            text="Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ:"
        )
        return

    state_machine.end_date = end_date
    state_machine.save_state()

    # Проверка лимитов и пересечения дат
    if not check_limits(state_machine.start_date, state_machine.end_date):
        bot.send_text(
            chat_id=user_id,
            text="Недостаточно дней. Пожалуйста, введите дату начала отпуска (в формате ДД.ММ.ГГГГ):"
        )
        return

    if dates_overlap(state_machine.start_date, state_machine.end_date):
        bot.send_text(
            chat_id=user_id,
            text="Даты пересекаются с текущими отпусками. Пожалуйста, введите дату начала отпуска (в формате ДД.ММ.ГГГГ):"
        )
        return

    # Создание заявки на отпуск
    create_vacation_request(user_id, state_machine.start_date, state_machine.end_date)
    bot.send_text(
        chat_id=user_id,
        text="Ваша заявка на отпуск сформирована."
    )
    state_machine.to_main_menu()
    state_machine.save_state()
    bot.send_text(
        chat_id=user_id,
        text="Вы возвращены в главное меню."
    )


def is_valid_date(date_str):
    # Проверка формата даты (ДД.ММ.ГГГГ)
    # Реализация функции проверки
    return True


def check_limits(start_date, end_date):
    # Проверка лимитов для выбранных дат
    # Реализация функции проверки
    return True


def dates_overlap(start_date, end_date):
    # Проверка пересечения дат
    # Реализация функции проверки
    return False


def create_vacation_request(user_id, start_date, end_date):
    # Создание заявки на отпуск
    # Реализация функции создания заявки
    pass
