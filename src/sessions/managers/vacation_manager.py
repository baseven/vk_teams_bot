import logging
from typing import List, Optional, Tuple
from datetime import datetime

from src.models import Limit, UserData, Vacation, VacationType, VacationStatus
from src.utils.vacation_utils import get_vacation_dates

logger = logging.getLogger(__name__)


class VacationManager:
    """Class responsible for managing user's vacations."""

    def __init__(self, user_data: UserData):
        """
        Initializes the VacationManager with user's data.

        Args:
            user_data (UserData): The user's data.
        """
        self.user_data = user_data

    @property
    def new_vacation(self) -> Optional[Vacation]:
        return self.user_data.new_vacation

    @new_vacation.setter
    def new_vacation(self, vacation: Vacation) -> None:
        self.user_data.new_vacation = vacation

    @property
    def current_vacation(self) -> Optional[Vacation]:
        return self.user_data.current_vacation

    @current_vacation.setter
    def current_vacation(self, vacation: Vacation) -> None:
        self.user_data.current_vacation = vacation

    @property
    def current_limit(self) -> Optional[Limit]:
        return self.user_data.current_limit

    @current_limit.setter
    def current_limit(self, limit: Limit) -> None:
        self.user_data.current_limit = limit

    @property
    def vacations(self) -> List[Vacation]:
        return self.user_data.vacations

    @property
    def limits(self) -> List[Limit]:
        return self.user_data.limits

    def create_new_vacation(
        self,
        vacation_type: VacationType,
        start_date: datetime,
        end_date: datetime,
        status: VacationStatus = VacationStatus.PLANNED
    ) -> Vacation:
        """
        Creates a new vacation and assigns it to new_vacation.

        Args:
            vacation_type (VacationType): The type of vacation.
            start_date (datetime): The start date of the vacation.
            end_date (datetime): The end date of the vacation.
            status (VacationStatus): The status of the vacation (default is PLANNED).

        Returns:
            Vacation: The newly created vacation.
        """
        new_vacation = Vacation(
            vacation_type=vacation_type,
            start_date=start_date,
            end_date=end_date,
            status=status
        )
        self.new_vacation = new_vacation
        logger.info(f"New vacation created for user {self.user_data.user_id}: {new_vacation}")
        return new_vacation

    def set_current_vacation_and_limit(self, vacation_id: str) -> None:
        """
        Sets the current vacation and current limit based on the vacation ID.

        Args:
            vacation_id (str): The ID of the vacation to set as current.

        Raises:
            ValueError: If the vacation is not found.
        """
        vacation = self.get_vacation_by_id(vacation_id)
        if vacation:
            self.current_vacation = vacation
            limit = self.get_limit_by_type(vacation.vacation_type)
            if limit:
                self.current_limit = limit
            else:
                self.current_limit = None
                logger.warning(f"No limit found for vacation type {vacation.vacation_type}")
        else:
            self.current_vacation = None
            self.current_limit = None
            logger.error(f"Vacation {vacation_id} not found for user {self.user_data.user_id}")

    def get_new_vacation_dates(self) -> Optional[Tuple[datetime, datetime]]:
        """
        Returns the dates of the new vacation.

        Returns:
            Optional[Tuple[datetime, datetime]]: Tuple of (start_date, end_date) or None if not set.
        """
        return get_vacation_dates(self.new_vacation)

    def get_current_vacation_dates(self) -> Optional[Tuple[datetime, datetime]]:
        """
        Returns the dates of the current vacation.

        Returns:
            Optional[Tuple[datetime, datetime]]: Tuple of (start_date, end_date) or None if not set.
        """
        return get_vacation_dates(self.current_vacation)

    def get_vacation_by_id(self, vacation_id: str) -> Optional[Vacation]:
        """
        Retrieves a vacation by its ID.

        Args:
            vacation_id (str): The ID of the vacation to retrieve.

        Returns:
            Optional[Vacation]: The vacation if found, else None.
        """
        return next(
            (vacation for vacation in self.vacations if vacation.vacation_id == vacation_id),
            None
        )

    def get_vacations_by_type(self, vacation_type: VacationType) -> List[Vacation]:
        """
        Returns a list of vacations corresponding to the given vacation type.

        Args:
            vacation_type (VacationType): The type of vacation to filter.

        Returns:
            List[Vacation]: List of vacations of the given type.
        """
        return [vacation for vacation in self.vacations if vacation.vacation_type == vacation_type]

    def get_limit_by_type(self, vacation_type: VacationType) -> Optional[Limit]:
        """
        Returns the limit corresponding to the given vacation type.

        Args:
            vacation_type (VacationType): The type of vacation.

        Returns:
            Optional[Limit]: The limit or None if not found.
        """
        return next(
            (limit for limit in self.limits if limit.vacation_type == vacation_type),
            None
        )

    def reset_vacation_state(self) -> None:
        """
        Resets the current vacation, current limit, and new vacation to None.
        """
        self.current_vacation = None
        self.current_limit = None
        self.new_vacation = None
        logger.info(f"Vacation state reset for user {self.user_data.user_id}")
