"""Relatório executivo com sumário de análises."""
import json
from datetime import datetime
from collections import defaultdict


class ExecutiveReport:
    """Gera relatório executivo com estatísticas e insights."""

    def __init__(self, issues, scan_time=0):
        self.issues = issues
        self.scan_time = scan_time
        self.timestamp = datetime.now().isoformat()

    def _get_stats(self):
        """Calcula estatísticas gerais."""
        stats = {
            "total_issues": len(self.issues),
            "by_severity": defaultdict(int),
            "by_category": defaultdict(int),
            "by_rule": defaultdict(int),
            "by_file": defaultdict(int),
        }

        for issue in self.issues:
            stats["by_severity"][issue.severity] += 1
            stats["by_category"][issue.category] += 1
            stats["by_rule"][issue.rule_id] += 1
            stats["by_file"][issue.file] += 1

        return {k: dict(v) if isinstance(v, defaultdict) else v for k, v in stats.items()}

    def _get_quality_score(self):
        """Calcula score de qualidade (0-100)."""
        if not self.issues:
            return 100

        severity_weight = {
            "CRITICAL": 10,
            "HIGH": 5,
            "MEDIUM": 2,
            "LOW": 1,
        }

        total_weight = sum(severity_weight.get(i.severity, 1) for i in self.issues)
        max_weight = len(self.issues) * 10  # Max seria todos CRITICAL

        score = max(0, 100 - (total_weight / max_weight * 100))
        return round(score, 1)

    def _get_top_issues(self, limit=10):
        """Top N issues mais frequentes."""
        from collections import Counter

        issue_counts = Counter(i.rule_id for i in self.issues)
        return issue_counts.most_common(limit)

    def _get_top_files(self, limit=5):
        """Top N arquivos com mais issues."""
        from collections import Counter

        file_counts = Counter(i.file for i in self.issues)
        return file_counts.most_common(limit)

    def to_dict(self):
        """Exporta relatório como dicionário."""
        stats = self._get_stats()

        return {
            "timestamp": self.timestamp,
            "summary": {
                "total_issues": stats["total_issues"],
                "quality_score": self._get_quality_score(),
                "scan_time_seconds": self.scan_time,
                "files_analyzed": len(stats.get("by_file", {})),
            },
            "severity_breakdown": stats.get("by_severity", {}),
            "category_breakdown": stats.get("by_category", {}),
            "top_issues": [{"rule": r, "count": c} for r, c in self._get_top_issues()],
            "top_files": [{"file": f, "count": c} for f, c in self._get_top_files()],
            "recommendations": self._get_recommendations(stats),
        }

    def _get_recommendations(self, stats):
        """Gera recomendações baseadas em análise."""
        recs = []

        critical = stats.get("by_severity", {}).get("CRITICAL", 0)
        high = stats.get("by_severity", {}).get("HIGH", 0)

        if critical > 0:
            recs.append(f"🔴 CRÍTICO: {critical} issue(s) crítica(s) encontrada(s). Resolva imediatamente.")

        if high > 0:
            recs.append(f"🟠 ALTA: {high} issue(s) de alta severidade. Prioritize na próxima sprint.")

        perf_issues = stats.get("by_category", {}).get("PERFORMANCE", 0)
        if perf_issues > 5:
            recs.append(f"⚡ Performance: {perf_issues} issues detectadas. Considere refatoração.")

        dup_issues = stats.get("by_category", {}).get("DUPLICATION", 0)
        if dup_issues > 3:
            recs.append(f"🔄 Duplicação: {dup_issues} issues. Consolide código repetido.")

        if len(self.issues) == 0:
            recs.append("✅ Excelente! Nenhum issue encontrado. Mantena a qualidade!")

        return recs

    def to_json(self):
        """Exporta como JSON."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    def to_text(self):
        """Exporta como texto estruturado."""
        report = self.to_dict()

        text = "╔" + "=" * 78 + "╗\n"
        text += "║" + " RELATÓRIO EXECUTIVO - ANÁLISE DE QUALIDADE ".center(78) + "║\n"
        text += "╚" + "=" * 78 + "╝\n\n"

        # Sumário
        text += "📊 SUMÁRIO\n"
        text += "-" * 80 + "\n"
        summary = report["summary"]
        text += f"Total de Issues:        {summary['total_issues']}\n"
        text += f"Score de Qualidade:     {summary['quality_score']}/100\n"
        text += f"Arquivos Analisados:    {summary['files_analyzed']}\n"
        text += f"Tempo de Análise:       {summary['scan_time_seconds']:.2f}s\n\n"

        # Severidade
        text += "⚠️  DISTRIBUIÇÃO POR SEVERIDADE\n"
        text += "-" * 80 + "\n"
        for sev, count in sorted(report["severity_breakdown"].items()):
            icon = "🔴" if sev == "CRITICAL" else "🟠" if sev == "HIGH" else "🟡" if sev == "MEDIUM" else "🔵"
            text += f"{icon} {sev:<12}: {count:>3} issues\n"
        text += "\n"

        # Categorias
        text += "📁 DISTRIBUIÇÃO POR CATEGORIA\n"
        text += "-" * 80 + "\n"
        for cat, count in sorted(report["category_breakdown"].items(), key=lambda x: -x[1]):
            text += f"  {cat:<20}: {count:>3} issues\n"
        text += "\n"

        # Top Issues
        if report["top_issues"]:
            text += "🎯 TOP 10 ISSUES MAIS FREQUENTES\n"
            text += "-" * 80 + "\n"
            for i, (rule, count) in enumerate(report["top_issues"], 1):
                text += f"  {i:2}. {rule:<15}: {count:>3} occorrências\n"
            text += "\n"

        # Top Files
        if report["top_files"]:
            text += "📄 TOP 5 ARQUIVOS COM MAIS ISSUES\n"
            text += "-" * 80 + "\n"
            for i, (file, count) in enumerate(report["top_files"], 1):
                text += f"  {i}. {file:<40}: {count:>3} issues\n"
            text += "\n"

        # Recomendações
        if report["recommendations"]:
            text += "💡 RECOMENDAÇÕES\n"
            text += "-" * 80 + "\n"
            for rec in report["recommendations"]:
                text += f"  {rec}\n"
            text += "\n"

        text += "=" * 80 + "\n"
        text += f"Gerado em: {report['timestamp']}\n"

        return text

    def to_html(self):
        """Exporta como HTML."""
        report = self.to_dict()
        summary = report["summary"]

        score_color = "#27ae60" if summary["quality_score"] >= 80 else "#f39c12" if summary["quality_score"] >= 60 else "#e74c3c"
        score_percent = summary["quality_score"]

        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Relatório Executivo - Análise de Qualidade</title>
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
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 30px;
                }}
                .summary {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 20px;
                    margin: 20px 0;
                }}
                .summary-card {{
                    background: #ecf0f1;
                    padding: 15px;
                    border-radius: 5px;
                    text-align: center;
                }}
                .summary-card h3 {{
                    margin: 0;
                    color: #7f8c8d;
                    font-size: 12px;
                    text-transform: uppercase;
                }}
                .summary-card .value {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .score {{
                    background: {score_color};
                    color: white;
                    padding: 30px;
                    border-radius: 8px;
                    text-align: center;
                    font-size: 48px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .severity {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 15px;
                    margin: 15px 0;
                }}
                .severity-item {{
                    padding: 15px;
                    border-radius: 5px;
                    border-left: 4px solid;
                }}
                .critical {{ border-left-color: #e74c3c; background: #fadbd8; }}
                .high {{ border-left-color: #f39c12; background: #fdebd0; }}
                .medium {{ border-left-color: #f1c40f; background: #fef5e7; }}
                .low {{ border-left-color: #27ae60; background: #d5f4e6; }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
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
                .recommendation {{
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #3498db;
                    background: #ebf5fb;
                    border-radius: 4px;
                }}
                .timestamp {{
                    color: #7f8c8d;
                    font-size: 12px;
                    text-align: right;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Relatório Executivo - Análise de Qualidade</h1>

                <div class="score">
                    {score_percent}/100
                </div>

                <div class="summary">
                    <div class="summary-card">
                        <h3>Total de Issues</h3>
                        <div class="value">{summary['total_issues']}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Arquivos Analisados</h3>
                        <div class="value">{summary['files_analyzed']}</div>
                    </div>
                    <div class="summary-card">
                        <h3>Tempo de Análise</h3>
                        <div class="value">{summary['scan_time_seconds']:.1f}s</div>
                    </div>
                    <div class="summary-card">
                        <h3>Data</h3>
                        <div class="value" style="font-size: 14px;">{report['timestamp'][:10]}</div>
                    </div>
                </div>

                <h2>⚠️ Severidade</h2>
                <div class="severity">
                    <div class="severity-item critical">
                        <strong>🔴 CRITICAL:</strong> {report['severity_breakdown'].get('CRITICAL', 0)} issues
                    </div>
                    <div class="severity-item high">
                        <strong>🟠 HIGH:</strong> {report['severity_breakdown'].get('HIGH', 0)} issues
                    </div>
                    <div class="severity-item medium">
                        <strong>🟡 MEDIUM:</strong> {report['severity_breakdown'].get('MEDIUM', 0)} issues
                    </div>
                    <div class="severity-item low">
                        <strong>🔵 LOW:</strong> {report['severity_breakdown'].get('LOW', 0)} issues
                    </div>
                </div>

                <h2>📁 Categorias</h2>
                <table>
                    <tr><th>Categoria</th><th>Issues</th></tr>
        """

        for cat, count in sorted(report["category_breakdown"].items(), key=lambda x: -x[1]):
            html += f"<tr><td>{cat}</td><td>{count}</td></tr>"

        html += """
                </table>

                <h2>🎯 Top Issues</h2>
                <table>
                    <tr><th>Rule ID</th><th>Ocorrências</th></tr>
        """

        for rule, count in report["top_issues"][:10]:
            html += f"<tr><td>{rule}</td><td>{count}</td></tr>"

        html += """
                </table>

                <h2>📄 Top Arquivos</h2>
                <table>
                    <tr><th>Arquivo</th><th>Issues</th></tr>
        """

        for file, count in report["top_files"][:5]:
            html += f"<tr><td>{file}</td><td>{count}</td></tr>"

        html += """
                </table>

                <h2>💡 Recomendações</h2>
        """

        for rec in report["recommendations"]:
            html += f'<div class="recommendation">{rec}</div>'

        html += f"""
                <div class="timestamp">Gerado em: {report['timestamp']}</div>
            </div>
        </body>
        </html>
        """

        return html
