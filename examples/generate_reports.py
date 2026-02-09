#!/usr/bin/env python3
"""Exemplo de geração de relatórios ao final da execução."""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from robotframework_quality_scanner import QualityScanner

def main():
    """Gera relatórios executivo e de cobertura."""
    scanner = QualityScanner()

    # Exemplo 1: Escanear arquivo único com geração de relatórios
    print("=" * 70)
    print("EXEMPLO 1: Escanear arquivo único")
    print("=" * 70)
    
    file_path = os.path.join(os.path.dirname(__file__), 'bad_web.robot')
    if os.path.exists(file_path):
        print(f"\nEscaneando: {file_path}\n")
        results, reports = scanner.scan(file_path, use_cache=False)
        
        # Exibir estatísticas
        print(f"Total de problemas encontrados: {len(results)}")
        print(f"Tempo de execução: {scanner.scan_time:.4f}s\n")
        
        # Exibir relatório executivo em texto
        print("=" * 70)
        print("RELATÓRIO EXECUTIVO (TEXTO)")
        print("=" * 70)
        print(reports['executive'].to_text())
        
        # Exibir relatório de cobertura em texto
        print("\n" + "=" * 70)
        print("RELATÓRIO DE COBERTURA (TEXTO)")
        print("=" * 70)
        print(reports['coverage'].to_text())
        
        # Salvar relatórios em arquivos
        output_dir = os.path.join(os.path.dirname(__file__), 'quality-reports')
        scanner.save_reports(output_dir)
        print(f"\n✓ Relatórios salvos em: {output_dir}")
        print(f"  - executive_report.html")
        print(f"  - executive_report.txt")
        print(f"  - executive_report.json")
        print(f"  - coverage_report.html")
        print(f"  - coverage_report.txt")
        
        # Exemplo 2: Acessar dados estruturados (JSON)
        print("\n" + "=" * 70)
        print("EXEMPLO 2: Dados estruturados (JSON)")
        print("=" * 70)
        exec_dict = reports['executive'].to_dict()
        print(f"Qualidade: {exec_dict['summary']['quality_score']}/100")
        print(f"Problemas por severidade:")
        for severity, count in exec_dict['severity_breakdown'].items():
            print(f"  - {severity}: {count}")
        
        # Exemplo 3: Gerar formato específico
        print("\n" + "=" * 70)
        print("EXEMPLO 3: Formatos específicos")
        print("=" * 70)
        
        # Relatório executivo em HTML (primeiras 500 chars)
        html_report = scanner.generate_executive_report(results, format='html')
        print(f"HTML gerado ({len(html_report)} chars):")
        print(html_report[:300] + "...")
        
    else:
        print(f"Arquivo não encontrado: {file_path}")

if __name__ == '__main__':
    main()
