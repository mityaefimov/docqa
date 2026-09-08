"""cli — интерфейс командной строки для docqa."""

import json
import sys
from pathlib import Path
from typing import List

import click

from .validators.structure import StructureValidator
from .validators.metadata import MetadataValidator
from .validators.links import LinksValidator

VALIDATORS = [StructureValidator, MetadataValidator, LinksValidator]


def run_validators(file_path: str) -> dict:
    """Запускает все валидаторы и возвращает результаты."""
    issues = []
    validator_stats = {}

    for validator_class in VALIDATORS:
        validator = validator_class(file_path)
        found_issues = validator.validate()
        issues.extend(found_issues)
        validator_stats[validator_class.__name__] = len(found_issues)

    critical = sum(1 for i in issues if i.severity == 'critical')
    warning = sum(1 for i in issues if i.severity == 'warning')
    info = sum(1 for i in issues if i.severity == 'info')

    return {
        'file': file_path,
        'total_issues': len(issues),
        'critical': critical,
        'warning': warning,
        'info': info,
        'issues': [
            {
                'severity': i.severity,
                'message': i.message,
                'location': i.location
            }
            for i in issues
        ],
        'validator_stats': validator_stats
    }


def format_text(results: dict) -> str:
    """Форматирует результаты в текст."""
    lines = []
    lines.append(f"\n📄 {Path(results['file']).name}")
    lines.append(f"   Всего проблем: {results['total_issues']}")
    lines.append(f"   Критичных: {results['critical']}")
    lines.append(f"   Предупреждений: {results['warning']}")
    lines.append(f"   Информационных: {results['info']}")

    if results['issues']:
        lines.append("\n   Детали:")
        for issue in results['issues']:
            severity = issue['severity'].upper()
            lines.append(f"      [{severity}] {issue['location']}: {issue['message']}")

    return '\n'.join(lines)


def format_json(results: dict) -> str:
    """Форматирует результаты в JSON."""
    return json.dumps(results, ensure_ascii=False, indent=2)


def format_html(results: dict) -> str:
    """Форматирует результаты в HTML."""
    html = ['<!DOCTYPE html>', '<html>', '<head>', '<meta charset="utf-8">']
    html.append(f'<title>DocQA Report: {Path(results["file"]).name}</title>')
    html.append('<style>')
    html.append('body { font-family: sans-serif; max-width: 800px; margin: 40px auto; }')
    html.append('.critical { color: red; font-weight: bold; }')
    html.append('.warning { color: orange; }')
    html.append('.info { color: blue; }')
    html.append('</style>')
    html.append('</head><body>')
    html.append(f'<h1>DocQA Report: {Path(results["file"]).name}</h1>')
    html.append(f'<p>Total issues: {results["total_issues"]}</p>')
    html.append(f'<p>Critical: {results["critical"]}, Warning: {results["warning"]}, Info: {results["info"]}</p>')

    if results['issues']:
        html.append('<h2>Details</h2>')
        html.append('<ul>')
        for issue in results['issues']:
            css_class = issue['severity']
            html.append(f'<li class="{css_class}">[{issue["severity"].upper()}] {issue["location"]}: {issue["message"]}</li>')
        html.append('</ul>')

    html.append('</body></html>')
    return '\n'.join(html)


@click.command()
@click.argument('file_path')
@click.option('--format', '-f', 'output_format', type=click.Choice(['text', 'json', 'html']), default='text',
              help='Формат вывода отчёта')
@click.option('--output', '-o', type=click.Path(), help='Сохранить отчёт в файл')
def main(file_path: str, output_format: str, output: str):
    """DocQA — автоматизированный анализ качества документов.

    FILE_PATH: путь к .docx файлу для проверки
    """
    if not Path(file_path).exists():
        click.echo(f"❌ Файл не найден: {file_path}", err=True)
        sys.exit(1)

    if not file_path.lower().endswith('.docx'):
        click.echo(f"❌ Файл должен быть в формате .docx", err=True)
        sys.exit(1)

    click.echo(f"🔍 Анализирую {file_path}...")

    results = run_validators(file_path)

    if output_format == 'text':
        formatted = format_text(results)
    elif output_format == 'json':
        formatted = format_json(results)
    elif output_format == 'html':
        formatted = format_html(results)

    if output:
        Path(output).write_text(formatted, encoding='utf-8')
        click.echo(f"✅ Отчёт сохранён: {output}")
    else:
        click.echo(formatted)

    # код выхода: 0 если нет критичных проблем, 1 если есть
    if results['critical'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()