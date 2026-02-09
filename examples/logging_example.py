#!/usr/bin/env python3
"""Exemplo de uso com logging estruturado e geração de documentação."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from robotframework_quality_scanner import QualityScanner


def main():
    """Demonstra o sistema de logging e geração de documentação."""
    
    print("=" * 80)
    print("robotframework-quality-scanner v0.3.0 - Logging e Documentação")
    print("=" * 80)
    print()
    
    # Inicializar scanner com pasta .docs
    scanner = QualityScanner(docs_dir=".docs")
    
    print("📁 Pasta de documentação: .docs/")
    print()
    
    # Escanear arquivo
    print("🔍 Escaneando arquivo...")
    issues, reports = scanner.scan("examples/bad_web.robot", use_cache=False)
    
    print(f"✓ Scan concluído em {scanner.scan_time:.4f}s")
    print(f"✓ {len(issues)} issues encontrados")
    print()
    
    # Exibir resumo de logs
    print("=" * 80)
    print("📊 Resumo de Logs")
    print("=" * 80)
    summary = scanner.logger.get_summary()
    print(f"Total de logs: {summary['total_logs']}")
    print(f"Erros capturados: {summary['total_errors']}")
    print(f"Avisos capturados: {summary['total_warnings']}")
    print()
    
    # Listar relatórios gerados
    print("=" * 80)
    print("📄 Relatórios Gerados")
    print("=" * 80)
    reports_list = scanner.logger.list_reports()
    if reports_list:
        for report in reports_list:
            size_kb = report['size_bytes'] / 1024
            print(f"✓ {report['name']} ({size_kb:.1f} KB)")
            print(f"  Caminho: {report['path']}")
            print(f"  Modificado: {report['modified']}")
            print()
    else:
        print("Nenhum relatório encontrado ainda")
        print()
    
    # Exibir preview do relatório markdown
    if scanner.logger.logs:
        print("=" * 80)
        print("📝 Preview do Relatório Markdown")
        print("=" * 80)
        md_report = scanner.logger._build_markdown_report()
        lines = md_report.split('\n')[:30]
        print('\n'.join(lines))
        print("...")
        print()
    
    print("=" * 80)
    print("✓ Demonstração concluída com sucesso!")
    print("=" * 80)


if __name__ == '__main__':
    main()
