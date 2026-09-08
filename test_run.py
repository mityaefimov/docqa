"""Быстрый тест валидатора на трёх документах."""

import sys
import os

# добавляем папку проекта в путь чтобы импорты работали
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docqa.validators.structure import StructureValidator


def test_file(file_path: str) -> None:
    """Запускает валидатор на одном файле."""
    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return

    validator = StructureValidator(file_path)
    issues = validator.validate()

    print(f"\n📄 {os.path.basename(file_path)}")
    print(f"   Найдено проблем: {len(issues)}")
    for issue in issues:
        print(f"   {issue}")


def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))

    print("🔍 Тестирую валидатор на трёх документах...")

    test_file(os.path.join(project_dir, 'test_sample.docx'))
    test_file(os.path.join(project_dir, 'test_clean.docx'))
    test_file(os.path.join(project_dir, 'test_orphans.docx'))


if __name__ == "__main__":
    main()