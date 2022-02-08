"""
Фитнес трекер. Модуль расчёта и отображения полной информации о тренировках
по данным от блока датчиков. Работает с такими видами тренировок:

* бег (реализована классом Running)
* спортивная ходьба (реализована классом SportsWalking)
* плавание (реализована классом Swimming)

Как это работает?
-------------
Принимается от блока датчиков информацию о прошедшей тренировке. Определяет вид
тренировки.

Функция:
read_package(workout_type: str, data: list) -> Training:

Далее рассчитывается результат. Для этого реализован метод базового класса
Training.show_training_info(self)

Для вывода сообщение о результатах тренировок предусмотрен отдельный класс
InfoMessage

Особенности реализации.
----------------------
Каждый вид тренировки имеет свой клас, все свойства и методы без изменений
наследуются от базового класса Training. Метод расчёта калорий, является
переопределяемым для наследуемых классов.
"""

from abc import abstractmethod


class InfoMessage:
    """
    Информационное сообщение о тренировке.
    Выводит: имя класса тренировки, длительность тренировки в часах,
    дистанция в километрах, средняя скорость, количество килокалорий
    """

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type: str = training_type  # бег, ходьба, плавание
        self.duration: float = duration  # длительность в часах

        # дистанция, которую преодолел пользователь, в километрах
        self.distance: float = distance
        self.speed: float = speed  # средняя скорость в км/ч
        self.calories: float = calories  # расход энергии, в килокалориях.

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки.
    Принимает три основных параметра тренировки:
    * action, количество совершённых действий
    * duration, длительность тренировки
    * weight, вес спортсмена.
    """

    # При типе тренировки "спортивной ходьба", данный показатель
    # имеет значение 0.65м, а во время плавания значение равное 1.38м
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000  # метров в километре

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
        pass

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
        M_IN_KM * время_тренировки_в_минутах
        """

        # коэффициенты для расчета калорий
        coeff_calorie_1: float = 18
        coeff_calorie_2: float = 20

        mean_speed = self.get_mean_speed()  # средняя скорость
        weight = self.weight  # вес_спортсмена
        duration_minutes = self.duration * 60  # время_тренировки_в_минутах

        return ((coeff_calorie_1 * mean_speed - coeff_calorie_2)
                * weight
                / self.M_IN_KM
                * duration_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба. Принимает дополнительно:
    * height, рост человека"""

    # При типе тренировки "спортивной ходьба", длина шага равна 0.65м
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)

        self.height = height

    def get_spent_calories(self) -> float:
        """
        Расчет калорий = (0.035 * вес + (средняя_скорость**2 // рост) * 0.029
        * вес) * время_тренировки_в_минутах
        """
        coeff_calorie_1: float = 0.035  # Коэффициент калорий
        coeff_calorie_2: float = 0.029  # Коэффициент калорий
        weight: float = self.weight  # вес
        mean_speed: float = self.get_mean_speed()  # квадрат средней скорости
        height: float = self.height  # рост
        # время_тренировки_в_минутах
        duration_minutes: float = self.duration * 60

        return ((coeff_calorie_1 * weight + (mean_speed ** 2 // height)
                 * coeff_calorie_2 * weight)
                * duration_minutes)


class Swimming(Training):
    """Тренировка: плавание. Принимает дополнительно:
    * length_pool, длинна бассейна
    * count_pool, сколько раз пользователь переплыл бассейн
    для расчета средней скорости использует переопределенный алгоритм.
    """

    # При типе тренировки "плавание", длина гребка равна 1.38м
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)

        self.LEN_STEP = 1.38

        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_spent_calories(self) -> float:
        """
        Расчет калорий = (средняя_скорость + 1.1) * 2 * вес
        """
        coeff_calorie_1 = 1.1
        return (self.get_mean_speed() + coeff_calorie_1) * 2 * self.weight

    def get_mean_speed(self) -> float:
        """
        Ср. скорость = длина_бассейна * count_pool / M_IN_KM / время_тренировки
        """
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """
    Прочитать данные полученные от датчиков.
    Гарантируется что пакет данных отфильтрован и строго содержит данные
    определенной длинны, типов и значений. Также, что в пакете будет получен
    код класса, определенный в справочнике class_links:
    Структура пакета:

    """
    class_links = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    try:
        obj: Training = class_links[workout_type](*data)
    except KeyError:
        raise
    else:
        return obj


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
