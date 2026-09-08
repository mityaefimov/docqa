"""Быстрый тест всех валидаторов на трёх документах."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docqa.validators.structure import StructureValidator
from docqa.validators.metadata import MetadataValidator
from docqa.validators.links import LinksValidator

VALIDATORS = [StructureValidator, MetadataValidator, LinksValidator]

def test_file(file_path: str) -> None:
    """Запускает все валидаторы на одном файле."""
    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return

    print(f"\n📄 {os.path.basename(file_path)}")

    for validator_class in VALIDATORS:
        validator = validator_class(file_path)
        issues = validator.validate()

        print(f"   {validator_class.__name__}: {len(issues)} проблем")
        for issue in issues:
            print(f"      {issue}")


def main():
    project_dir = os.path.dirname(os.path.abspath(__file__))

    print("🔍 Тестирую валидаторы на трёх документах...")

    test_file(os.path.join(project_dir, 'test_sample.docx'))
    test_file(os.path.join(project_dir, 'test_clean.docx'))
    test_file(os.path.join(project_dir, 'test_orphans.docx'))


if __name__ == "__main__":
    main()