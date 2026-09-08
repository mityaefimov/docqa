"""create_test_docs — генератор тестовых документов для docqa."""

import docx
from docx.shared import Pt
import os


def create_document_with_issues(path: str) -> None:
    """Создаёт документ с разными проблемами структуры."""
    doc = docx.Document()

    # обычный заголовок H1
    doc.add_heading('Глава 1', level=1)

    # сразу заголовок H3 — пропуск уровня! (должно вызвать предупреждение)
    doc.add_heading('Подглава', level=3)

    # немного обычного текста
    doc.add_paragraph('Это обычный текст между заголовками.')

    # несколько пустых параграфов подряд (больше 3 — должно вызвать предупреждение)
    for _ in range(5):
        doc.add_paragraph('')

    # короткая одинокая строка (меньше 3 символов — предупреждение)
    doc.add_paragraph('Х.')

    # ещё один текст
    doc.add_paragraph('Продолжение главы после короткой строки.')

    # нормальный переход заголовков (H1 -> H2, проблем нет)
    doc.add_heading('Глава 2', level=1)
    doc.add_heading('Подглава 2.1', level=2)
    doc.add_paragraph('Обычный текст во второй главе.')

    doc.save(path)
    print(f"✅ Создан: {path}")


def create_clean_document(path: str) -> None:
    """Создаёт чистый документ без проблем (для сравнения)."""
    doc = docx.Document()

    # правильная иерархия заголовков
    doc.add_heading('Введение', level=1)
    doc.add_paragraph('Это введение в документ.')

    doc.add_heading('Раздел 1', level=2)
    doc.add_paragraph('Текст первого раздела с достаточной длиной.')

    doc.add_heading('Подраздел 1.1', level=3)
    doc.add_paragraph('Текст подраздела с нормальной структурой.')

    doc.add_heading('Раздел 2', level=2)
    doc.add_paragraph('Текст второго раздела, тоже нормальный.')

    doc.save(path)
    print(f"✅ Создан: {path}")


def create_document_with_orphans(path: str) -> None:
    """Создаёт документ с множеством коротких одиноких строк."""
    doc = docx.Document()

    doc.add_heading('Глава с артефактами', level=1)
    doc.add_paragraph('Нормальный текст в начале.')

    # несколько коротких строк подряд
    doc.add_paragraph('1.')
    doc.add_paragraph('а')
    doc.add_paragraph('-')

    doc.add_paragraph('После артефактов идёт нормальный текст достаточной длины.')

    doc.save(path)
    print(f"✅ Создан: {path}")


def main():
    """Создаёт все тестовые документы в папке проекта."""
    # папка где лежит этот скрипт (корень проекта)
    project_dir = os.path.dirname(os.path.abspath(__file__))

    print("🔨 Создаю тестовые документы...")
    print()

    create_document_with_issues(os.path.join(project_dir, 'test_sample.docx'))
    create_clean_document(os.path.join(project_dir, 'test_clean.docx'))
    create_document_with_orphans(os.path.join(project_dir, 'test_orphans.docx'))

    print()
    print("🎉 Готово! Три тестовых документа созданы.")
    print("Теперь можешь запустить валидатор на них.")


if __name__ == "__main__":
    main()