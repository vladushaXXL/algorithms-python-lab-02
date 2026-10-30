class Particle:
    """Базовый класс для элементарной частицы."""
    def __init__(self, name: str, mass: float, charge: float):
        self.name = name
        self.mass = mass      # Масса в кг
        self.charge = charge  # Заряд в Кулонах

    def __str__(self):
        return f"Частица: {self.name}"

# Физические константы (СИ)
PLANCK_CONSTANT = 6.62607015e-34  # Дж·с
SPEED_OF_LIGHT = 299792458        # м/с

# Справочные данные (для автозаполнения)
REFERENCE_PARTICLES = {
    "Электрон": {"mass": 9.1093837e-31, "charge": -1.60217663e-19},
    "Протон": {"mass": 1.67262192e-27, "charge": 1.60217663e-19},
    "Нейтрон": {"mass": 1.67492750e-27, "charge": 0.0}
}