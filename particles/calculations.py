from .models import Particle, PLANCK_CONSTANT, SPEED_OF_LIGHT

def calculate_specific_charge(particle: Particle) -> float:
    """Расчет удельного заряда (q/m)."""
    if particle.mass == 0:
        return 0.0
    return particle.charge / particle.mass

def calculate_compton_wavelength(particle: Particle) -> float:
    """Расчет комптоновской длины волны (λ = h / mc)."""
    return PLANCK_CONSTANT / (particle.mass * SPEED_OF_LIGHT)