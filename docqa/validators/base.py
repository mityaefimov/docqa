"""base — базовый класс для всех валидаторов."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Issue:
    """Найденная проблема в документе."""
    severity: str      # 'critical', 'warning', 'info'
    message: str       # описание проблемы
    location: str      # где найдена (параграф, страница)

    def __str__(self):
        return f"[{self.severity.upper()}] {self.location}: {self.message}"


class BaseValidator(ABC):
    """Базовый класс для всех валидаторов.
    
    Каждый валидатор наследуется от этого класса и реализует метод validate().
    """

    def __init__(self, doc_path: str):
        self.doc_path = doc_path
        self.issues: List[Issue] = []

    @abstractmethod
    def validate(self) -> List[Issue]:
        """Запускает валидацию. Возвращает список найденных проблем."""
        raise NotImplementedError

    def _add_issue(self, severity: str, message: str, location: str) -> None:
        """Добавляет найденную проблему в список."""
        self.issues.append(Issue(severity=severity, message=message, location=location))