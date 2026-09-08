"""metadata — проверка метаданных документа."""

from typing import List

import docx

from .base import BaseValidator, Issue


# значения которые считаются мусорными для поля автора
DEFAULT_AUTHORS = {
    '', 'author', 'автор', 'python-docx', 'microsoft word',
    'user', 'пользователь', 'admin', 'administrator', 'unknown',
}

# значения которые считаются мусорными для названия
DEFAULT_TITLES = {
    '', 'document', 'документ', 'untitled', 'без названия',
    'new document', 'новый документ', 'doc1', 'document1', 'title',
}


class MetadataValidator(BaseValidator):
    """Проверяет метаданные документа:

    - автор: не пустой и не дефолтный
    - название: не пустое и не дефолтное
    - дата создания: присутствует
    - язык: указан
    """

    def validate(self) -> List[Issue]:
        """Запускает все проверки метаданных."""
        doc = docx.Document(self.doc_path)
        props = doc.core_properties

        self._check_author(props)
        self._check_title(props)
        self._check_created(props)
        self._check_language(props)
        return self.issues

    def _check_author(self, props) -> None:
        """Проверяет что автор указан и не является мусорным значением."""
        author = (props.author or '').strip().lower()
        if author in DEFAULT_AUTHORS:
            self._add_issue(
                severity='warning',
                message='Автор не указан или содержит мусорное значение',
                location='Metadata: author'
            )

    def _check_title(self, props) -> None:
        """Проверяет что название указано и не является мусорным."""
        title = (props.title or '').strip().lower()
        if title in DEFAULT_TITLES:
            self._add_issue(
                severity='warning',
                message='Название не указано или содержит мусорное значение',
                location='Metadata: title'
            )

    def _check_created(self, props) -> None:
        """Проверяет что дата создания присутствует."""
        if props.created is None:
            self._add_issue(
                severity='info',
                message='Дата создания документа отсутствует',
                location='Metadata: created'
            )

    def _check_language(self, props) -> None:
        """Проверяет что язык документа указан."""
        language = (props.language or '').strip()
        if not language:
            self._add_issue(
                severity='info',
                message='Язык документа не указан',
                location='Metadata: language'
            )