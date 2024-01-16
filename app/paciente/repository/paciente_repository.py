from app.paciente.models.paciente_model import Paciente
from core.repository.base import BaseRepo


class PacienteRepository(BaseRepo):

    def __init__(self):
        super().__init__(Paciente)