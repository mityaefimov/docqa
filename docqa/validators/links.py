"""links — проверка гиперссылок и внутренних якорей документа."""

from typing import List
from urllib.parse import urlparse

import docx
from docx.oxml.ns import qn

from .base import BaseValidator, Issue

# схемы которые считаем корректными для внешних ссылок
VALID_SCHEMES = {'http', 'https', 'mailto', 'ftp'}

# content type части документа где хранятся сноски
FOOTNOTES_CT = (
    'application/vnd.openxmlformats-officedocument'
    '.wordprocessingml.footnotes+xml'
)


class LinksValidator(BaseValidator):
    """Проверяет ссылки в документе:

    - пустые гиперссылки (без адреса)
    - ссылки без корректной схемы (не http/https/mailto)
    - внутренние якоря (#anchor) на несуществующие закладки
    - ссылки на несуществующие сноски
    """

    def validate(self) -> List[Issue]:
        """Запускает все проверки ссылок."""
        doc = docx.Document(self.doc_path)
        bookmarks = self._collect_bookmarks(doc)

        for i, para in enumerate(doc.paragraphs):
            for hyperlink in para._p.findall(qn('w:hyperlink')):
                target = self._get_target(doc, hyperlink)
                text = self._get_link_text(hyperlink)
                self._check_one_link(target, text, i + 1, bookmarks)

        self._check_footnotes(doc)
        return self.issues

    def _collect_bookmarks(self, doc) -> set:
        """Собирает имена всех закладок в документе."""
        names = set()
        for para in doc.paragraphs:
            for bookmark in para._p.findall(qn('w:bookmarkStart')):
                name = bookmark.get(qn('w:name'))
                if name:
                    names.add(name)
        return names

    def _get_target(self, doc, hyperlink) -> str:
        """Достаёт адрес ссылки: внешний target или внутренний якорь."""
        r_id = hyperlink.get(qn('r:id'))
        anchor = hyperlink.get(qn('w:anchor'))

        if r_id:
            rel = doc.part.rels.get(r_id)
            if rel is None:
                return ''
            return str(rel.target_ref)

        if anchor:
            return '#' + anchor

        return ''

    def _get_link_text(self, hyperlink) -> str:
        """Достаёт видимый текст ссылки."""
        parts = []
        for t in hyperlink.iter(qn('w:t')):
            parts.append(t.text or '')
        return ''.join(parts).strip()

    def _check_one_link(self, target: str, text: str, paragraph_no: int,
                        bookmarks: set) -> None:
        """Проверяет одну ссылку на все виды проблем."""
        label = text or 'без текста'

        if not target:
            self._add_issue(
                severity='critical',
                message=f'Гиперссылка без адреса (текст: "{label}")',
                location=f'Paragraph {paragraph_no}'
            )
            return

        if target.startswith('#'):
            anchor = target[1:]
            if anchor not in bookmarks:
                self._add_issue(
                    severity='warning',
                    message=f'Внутренняя ссылка на несуществующую закладку: {anchor}',
                    location=f'Paragraph {paragraph_no}'
                )
            return

        scheme = urlparse(target).scheme.lower()
        if scheme not in VALID_SCHEMES:
            self._add_issue(
                severity='warning',
                message=f'Ссылка без корректной схемы (http/https/mailto): {target}',
                location=f'Paragraph {paragraph_no}'
            )

    def _check_footnotes(self, doc) -> None:
        """Проверяет что ссылки на сноски указывают на существующие сноски."""
        body = doc.element.body
        ref_ids = [r.get(qn('w:id')) for r in body.iter(qn('w:footnoteReference'))]
        if not ref_ids:
            return

        footnotes_part = None
        for part in doc.part.package.iter_parts():
            if part.content_type == FOOTNOTES_CT:
                footnotes_part = part
                break

        if footnotes_part is None:
            self._add_issue(
                severity='critical',
                message=f'Найдены ссылки на сноски ({len(ref_ids)}), но часть со сносками отсутствует',
                location='Document'
            )
            return

        defined_ids = {f.get(qn('w:id')) for f in footnotes_part.element.findall(qn('w:footnote'))}
        missing = [rid for rid in ref_ids if rid not in defined_ids]
        if missing:
            self._add_issue(
                severity='critical',
                message=f'Ссылки на несуществующие сноски: {missing}',
                location='Document'
            )