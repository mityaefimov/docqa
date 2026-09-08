"""тесты валидаторов docqa."""

from docqa.validators.structure import StructureValidator
from docqa.validators.metadata import MetadataValidator
from docqa.validators.links import LinksValidator


class TestStructureValidator:
    def test_clean_document_has_no_issues(self, clean_doc):
        issues = StructureValidator(clean_doc).validate()
        assert issues == []

    def test_detects_skipped_heading_level(self, bad_structure_doc):
        issues = StructureValidator(bad_structure_doc).validate()
        messages = ' '.join(i.message for i in issues)
        assert 'Пропущен уровень' in messages

    def test_detects_empty_paragraphs(self, bad_structure_doc):
        issues = StructureValidator(bad_structure_doc).validate()
        messages = ' '.join(i.message for i in issues)
        assert 'пустых параграфов' in messages

    def test_detects_orphaned_text(self, bad_structure_doc):
        issues = StructureValidator(bad_structure_doc).validate()
        messages = ' '.join(i.message for i in issues)
        assert 'короткий текст' in messages


class TestMetadataValidator:
    def test_clean_document_has_no_issues(self, clean_doc):
        issues = MetadataValidator(clean_doc).validate()
        assert issues == []

    def test_detects_missing_author(self, bad_metadata_doc):
        issues = MetadataValidator(bad_metadata_doc).validate()
        messages = ' '.join(i.message for i in issues)
        assert 'Автор' in messages

    def test_detects_missing_title(self, bad_metadata_doc):
        issues = MetadataValidator(bad_metadata_doc).validate()
        messages = ' '.join(i.message for i in issues)
        assert 'Название' in messages


class TestLinksValidator:
    def test_clean_document_has_no_issues(self, clean_doc):
        issues = LinksValidator(clean_doc).validate()
        assert issues == []

    def test_detects_link_without_scheme(self, bad_links_doc):
        issues = LinksValidator(bad_links_doc).validate()
        messages = ' '.join(i.message for i in issues)
        assert 'без корректной схемы' in messages

    def test_detects_broken_anchor(self, bad_links_doc):
        issues = LinksValidator(bad_links_doc).validate()
        messages = ' '.join(i.message for i in issues)
        assert 'несуществующую закладку' in messages