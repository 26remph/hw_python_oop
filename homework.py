#
# Notice
# -------
#
# About using PEP257 (Multi-line Docstring) into original say:
# [---skip---]
# Insert a blank line after all docstrings (one-line or multi-line)
# that document a class -- generally speaking, the class's methods
# are separated from each other by a single blank line, and the docstring
# needs to be offset from the first method by a blank line.
# [---end skip]
#
# In standard lib as 'pip' and 'flake8' (/lib/flake8) mudules use blank line
#  after all docstrings

from abc import abstractmethod
from typing import Optional


class InfoMessage:
    """Информационное сообщение о тренировке.

    Выводит: имя класса тренировки, длительность тренировки в часах,
    дистанция в километрах, среднюю скорость в км/ч, количество килокалорий
    в килокалориях.
    """

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки.

    Содержит аттрибуты:
    - :attr: 'LEN_STEP' - коэфф. перевода действий (шагов, гребков) в метры'
    - :attr: 'M_IN_KM' - константа для перевода километров в метры'
    - :attr: 'training_type' - тип тренировки
    - :attr: 'calories' - количество потраченных калорий'
    """

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

        self.training_type: str = self.__class__.__name__
        self.calories: float = 0

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    @abstractmethod
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        value_dict = {'training_type': self.training_type,
                      'duration': self.duration,
                      'distance': self.get_distance(),
                      'speed': self.get_mean_speed(),
                      'calories': self.get_spent_calories()}

        return InfoMessage(**value_dict)


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self):
        """ Расчет калорий = (18 * средняя_скорость - 20) * вес_спортсмена /
        M_IN_KM * время_тренировки_в_минутах"""
        CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
        CALORIES_MEAN_SPEED_SHIFT: float = 20

        mean_speed = self.get_mean_speed()
        weight = self.weight
        duration_minutes = self.duration * 60

        return ((CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                 - CALORIES_MEAN_SPEED_SHIFT)
                * weight
                / self.M_IN_KM
                * duration_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    Содержит дополнительный аттрибут:
    - :attr: 'height' - рост человека
    """

    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)

        self.height = height

    def get_spent_calories(self) -> float:
        """ Расчет калорий =
        (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
        * время_тренировки_в_минутах
        """
        FIRST_CALORIE_MULTIPLIER: float = 0.035
        SECOND_CALORIE_MULTIPLIER: float = 0.029
        weight: float = self.weight
        mean_speed: float = self.get_mean_speed()
        height: float = self.height
        duration_minutes: float = self.duration * 60

        return ((FIRST_CALORIE_MULTIPLIER * weight
                 + (mean_speed ** 2 // height)
                 * SECOND_CALORIE_MULTIPLIER * weight)
                * duration_minutes)


class Swimming(Training):
    """Тренировка: плавание.

    Содержит дополнительный аттрибут:
    - :attr: 'length_pool' - длинна бассейна
    - :attr: 'count_pool' - сколько раз пользователь переплыл бассейн

    Для расчета средней скорости использует переопределенный алгоритм.
    """

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)

        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_spent_calories(self) -> float:
        """Расчет калорий = (средняя_скорость + 1.1) * 2 * вес"""
        CALORIE_MULTIPLIER = 1.1
        return (self.get_mean_speed() + CALORIE_MULTIPLIER) * 2 * self.weight

    def get_mean_speed(self) -> float:
        """Ср. скорость =
        длина_бассейна * count_pool / M_IN_KM / время_тренировки"""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)


def read_package(workout_type: str, data: list) -> Optional[Training]:
    """
    Прочитать данные полученные от датчиков.

    Гарантируется что пакет данных отфильтрован и строго содержит данные
    определенной длинны, типов и значений.

    """
    class_links = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    try:
        obj: Training = class_links[workout_type](*data)
    except KeyError:
        print(f"Error. Processing of receive code '{workout_type}' "
              f"not implemented in module.")
        return None
    else:
        return obj


def main(training: Optional[Training]) -> None:
    """Главная функция."""
    if training is not None:
        info = training.show_training_info()
        print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('XXX', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
