#!/usr/bin/env python3
"""CLI para robotframework-quality-scanner."""

import sys
import argparse
from pathlib import Path
from robotframework_quality_scanner import QualityScanner


def main():
    """Entrada principal da CLI."""
    parser = argparse.ArgumentParser(
        description="Robot Framework Quality Scanner - Análise estática de testes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s ./tests/
  %(prog)s ./tests/ --format json
  %(prog)s ./tests/login.robot --no-cache
  %(prog)s ./tests/ --docs ./.docs --format markdown
        """
    )
    
    parser.add_argument(
        "path",
        help="Caminho para arquivo ou diretório .robot"
    )
    
    parser.add_argument(
        "-f", "--format",
        choices=["text", "json", "html"],
        default="text",
        help="Formato de saída (padrão: text)"
    )
    
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Desabilitar cache"
    )
    
    parser.add_argument(
        "--no-reports",
        action="store_true",
        help="Não gerar relatórios"
    )
    
    parser.add_argument(
        "--docs",
        default=".docs",
        help="Diretório para armazenar documentação (padrão: .docs)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verbose"
    )
    
    args = parser.parse_args()
    
    # Validar path
    path = Path(args.path)
    if not path.exists():
        print(f"❌ Erro: {path} não encontrado", file=sys.stderr)
        sys.exit(1)
    
    # Inicializar scanner
    scanner = QualityScanner(docs_dir=args.docs)
    
    if args.verbose:
        print(f"📁 Escaneando: {path}")
        print(f"📋 Cache: {'Desabilitado' if args.no_cache else 'Habilitado'}")
        print(f"📂 Documentação: {args.docs}")
        print()
    
    # Executar scan
    try:
        use_cache = not args.no_cache
        generate_reports = not args.no_reports
        
        if generate_reports:
            issues, reports = scanner.scan(str(path), use_cache=use_cache, generate_reports=True)
        else:
            issues = scanner.scan(str(path), use_cache=use_cache, generate_reports=False)
            reports = None
        
        # Exibir resultado
        if args.format == "text":
            print_text_output(issues, reports, scanner, args.verbose)
        elif args.format == "json":
            print_json_output(issues, reports)
        elif args.format == "html":
            print_html_output(issues, reports)
        
        # Status exit
        has_critical = any(i.severity == "CRITICAL" for i in issues)
        sys.exit(1 if has_critical else 0)
    
    except Exception as e:
        print(f"❌ Erro: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def print_text_output(issues, reports, scanner, verbose):
    """Exibe output em formato texto."""
    print("=" * 80)
    print(f"{'RELATÓRIO DE QUALIDADE':^80}")
    print("=" * 80)
    print()
    
    if reports:
        exec_report = reports['executive']
        print(exec_report.to_text())
        print()
    else:
        print(f"📊 Issues encontrados: {len(issues)}")
        print()
        
        if issues:
            print("Problemas encontrados:")
            for issue in sorted(issues, key=lambda x: x.severity):
                print(f"  [{issue.severity}] {issue.rule_id} - {issue.file}:{issue.line}")
                print(f"      {issue.description}")
        else:
            print("✅ Nenhum problema encontrado!")
    
    if verbose:
        print()
        print(f"⏱️  Tempo de execução: {scanner.scan_time:.4f}s")
        print(f"📁 Arquivos analisados: {len(scanner.files_analyzed)}")


def print_json_output(issues, reports):
    """Exibe output em formato JSON."""
    import json
    
    if reports:
        output = reports['executive'].to_dict()
    else:
        output = {
            "total_issues": len(issues),
            "issues": [
                {
                    "rule_id": i.rule_id,
                    "severity": i.severity,
                    "file": i.file,
                    "line": i.line,
                    "description": i.description
                }
                for i in issues
            ]
        }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))


def print_html_output(issues, reports):
    """Exibe output em formato HTML."""
    if reports:
        html = reports['executive'].to_html()
        print(html)
    else:
        print("<html><body>")
        print("<h1>Relatório de Qualidade</h1>")
        print(f"<p>Total de issues: {len(issues)}</p>")
        print("<ul>")
        for issue in issues:
            print(f"<li>[{issue.severity}] {issue.rule_id} - {issue.description}</li>")
        print("</ul>")
        print("</body></html>")


if __name__ == "__main__":
    main()
