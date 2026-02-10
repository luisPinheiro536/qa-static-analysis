"""Relatório de cobertura de testes."""
import re
from collections import defaultdict


class CoverageReport:
    """Analisa cobertura de testes em arquivos Robot Framework."""

    def __init__(self, files_analyzed):
        """
        Args:
            files_analyzed: Lista de tuplas (filepath, content)
        """
        self.files_analyzed = files_analyzed
        self.coverage_data = self._analyze_coverage()

    def _analyze_coverage(self):
        """Analisa cobertura em cada arquivo."""
        coverage = defaultdict(lambda: {
            "total_keywords": 0,
            "documented_keywords": 0,
            "used_keywords": 0,
            "unused_keywords": [],
            "test_count": 0,
            "keyword_count": 0,
            "documentation_coverage": 0,
            "keyword_usage_coverage": 0,
        })

        for filepath, content in self.files_analyzed:
            file_key = filepath if isinstance(filepath, str) else filepath.name

            # Parse sections
            in_keywords = False
            in_tests = False
            keywords_defined = []
            keywords_used = set()
            documented_kw = 0
            test_count = 0

            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Detectar seções
                if '*** Keywords ***' in line:
                    in_keywords = True
                    in_tests = False
                    continue
                elif '*** Test Cases ***' in line:
                    in_tests = True
                    in_keywords = False
                    continue
                elif '*** Settings ***' in line or '*** Variables ***' in line:
                    in_keywords = False
                    in_tests = False
                    continue

                # Contar keywords definidas
                if in_keywords and line.strip() and not line.startswith('    '):
                    keywords_defined.append(line.strip())
                    # Verificar se tem documentation
                    if i + 1 < len(lines) and '[Documentation]' in lines[i + 1]:
                        documented_kw += 1

                # Contar testes
                if in_tests and line.strip() and not line.startswith('    '):
                    test_count += 1

                # Coletar keywords usadas (heurística)
                for kw in keywords_defined:
                    if kw in line and not in_keywords:
                        keywords_used.add(kw)

            # Calcular métricas
            total_kw = len(keywords_defined)
            used_kw = len(keywords_used)
            unused_kw = [kw for kw in keywords_defined if kw not in keywords_used]

            coverage[file_key] = {
                "total_keywords": total_kw,
                "documented_keywords": documented_kw,
                "used_keywords": used_kw,
                "unused_keywords": unused_kw,
                "test_count": test_count,
                "documentation_coverage": (documented_kw / total_kw * 100) if total_kw > 0 else 0,
                "keyword_usage_coverage": (used_kw / total_kw * 100) if total_kw > 0 else 0,
            }

        return dict(coverage)

    def get_overall_stats(self):
        """Estatísticas gerais de cobertura."""
        total_files = len(self.coverage_data)
        total_keywords = sum(d["total_keywords"] for d in self.coverage_data.values())
        total_documented = sum(d["documented_keywords"] for d in self.coverage_data.values())
        total_used = sum(d["used_keywords"] for d in self.coverage_data.values())
        total_tests = sum(d["test_count"] for d in self.coverage_data.values())

        return {
            "files": total_files,
            "total_keywords": total_keywords,
            "documented_keywords": total_documented,
            "used_keywords": total_used,
            "total_tests": total_tests,
            "documentation_coverage_percent": (total_documented / total_keywords * 100) if total_keywords > 0 else 0,
            "keyword_usage_coverage_percent": (total_used / total_keywords * 100) if total_keywords > 0 else 0,
        }

    def to_dict(self):
        """Exporta como dicionário."""
        return {
            "overall": self.get_overall_stats(),
            "by_file": self.coverage_data,
        }

    def to_text(self):
        """Exporta como texto."""
        stats = self.get_overall_stats()

        text = "╔" + "=" * 78 + "╗\n"
        text += "║" + " RELATÓRIO DE COBERTURA DE TESTES ".center(78) + "║\n"
        text += "╚" + "=" * 78 + "╝\n\n"

        # Resumo geral
        text += "📊 RESUMO GERAL\n"
        text += "-" * 80 + "\n"
        text += f"Arquivos Analisados:          {stats['files']}\n"
        text += f"Total de Keywords:            {stats['total_keywords']}\n"
        text += f"Keywords Documentadas:        {stats['documented_keywords']} ({stats['documentation_coverage_percent']:.1f}%)\n"
        text += f"Keywords Utilizadas:          {stats['used_keywords']} ({stats['keyword_usage_coverage_percent']:.1f}%)\n"
        text += f"Total de Testes:              {stats['total_tests']}\n\n"

        # Por arquivo
        text += "📄 POR ARQUIVO\n"
        text += "-" * 80 + "\n"
        for file, data in sorted(self.coverage_data.items()):
            text += f"\n{file}\n"
            text += f"  Keywords: {data['total_keywords']} (Docs: {data['documentation_coverage']:.0f}%, Uso: {data['keyword_usage_coverage']:.0f}%)\n"
            text += f"  Testes: {data['test_count']}\n"

            if data['unused_keywords']:
                text += f"  ⚠️  Keywords não utilizadas: {', '.join(data['unused_keywords'][:5])}\n"

        text += "\n" + "=" * 80 + "\n"

        return text

    def to_html(self):
        """Exporta como HTML."""
        stats = self.get_overall_stats()

        doc_color = "#27ae60" if stats["documentation_coverage_percent"] >= 80 else "#f39c12" if stats["documentation_coverage_percent"] >= 60 else "#e74c3c"
        usage_color = "#27ae60" if stats["keyword_usage_coverage_percent"] >= 80 else "#f39c12" if stats["keyword_usage_coverage_percent"] >= 60 else "#e74c3c"

        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório de Cobertura</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #9b59b6;
                    padding-bottom: 10px;
                }}
                .metrics {{
                    display: grid;
                    grid-template-columns: repeat(5, 1fr);
                    gap: 15px;
                    margin: 20px 0;
                }}
                .metric-card {{
                    background: #ecf0f1;
                    padding: 20px;
                    border-radius: 5px;
                    text-align: center;
                }}
                .metric-card h3 {{
                    margin: 0;
                    color: #7f8c8d;
                    font-size: 12px;
                    text-transform: uppercase;
                }}
                .metric-card .value {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .coverage-bar {{
                    width: 100%;
                    height: 30px;
                    background: #ecf0f1;
                    border-radius: 4px;
                    overflow: hidden;
                    margin: 10px 0;
                }}
                .coverage-fill {{
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 12px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ecf0f1;
                }}
                th {{
                    background: #34495e;
                    color: white;
                }}
                tr:hover {{
                    background: #f8f9fa;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Relatório de Cobertura de Testes</h1>

                <div class="metrics">
                    <div class="metric-card">
                        <h3>Arquivos</h3>
                        <div class="value">{stats['files']}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Keywords</h3>
                        <div class="value">{stats['total_keywords']}</div>
                    </div>
                    <div class="metric-card">
                        <h3>Documentação</h3>
                        <div class="value">{stats['documentation_coverage_percent']:.0f}%</div>
                    </div>
                    <div class="metric-card">
                        <h3>Utilização</h3>
                        <div class="value">{stats['keyword_usage_coverage_percent']:.0f}%</div>
                    </div>
                    <div class="metric-card">
                        <h3>Testes</h3>
                        <div class="value">{stats['total_tests']}</div>
                    </div>
                </div>

                <h2>Cobertura Geral</h2>
                <div>
                    <strong>Documentação</strong>
                    <div class="coverage-bar">
                        <div class="coverage-fill" style="width: {stats['documentation_coverage_percent']}%; background: {doc_color};">
                            {stats['documentation_coverage_percent']:.1f}%
                        </div>
                    </div>
                </div>

                <div>
                    <strong>Utilização de Keywords</strong>
                    <div class="coverage-bar">
                        <div class="coverage-fill" style="width: {stats['keyword_usage_coverage_percent']}%; background: {usage_color};">
                            {stats['keyword_usage_coverage_percent']:.1f}%
                        </div>
                    </div>
                </div>

                <h2>Cobertura por Arquivo</h2>
                <table>
                    <tr>
                        <th>Arquivo</th>
                        <th>Keywords</th>
                        <th>Documentação</th>
                        <th>Utilização</th>
                        <th>Testes</th>
                    </tr>
        """

        for file, data in sorted(self.coverage_data.items()):
            html += f"""
                    <tr>
                        <td>{file}</td>
                        <td>{data['total_keywords']}</td>
                        <td>{data['documentation_coverage']:.0f}%</td>
                        <td>{data['keyword_usage_coverage']:.0f}%</td>
                        <td>{data['test_count']}</td>
                    </tr>
            """

        html += """
                </table>
            </div>
        </body>
        </html>
        """

        return html
