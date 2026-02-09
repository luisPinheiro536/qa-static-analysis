"""API REST para integração com ferramentas externas."""
import json
from pathlib import Path


class AnalysisAPI:
    """API simples para exposição de análises."""

    def __init__(self, scanner):
        self.scanner = scanner

    def analyze_file_api(self, filepath):
        """Analisa um arquivo e retorna JSON."""
        if not Path(filepath).exists():
            return {"error": f"Arquivo não encontrado: {filepath}"}, 404
        
        issues = self.scanner.scan_file(filepath)
        return {
            "file": filepath,
            "issue_count": len(issues),
            "issues": [i.to_dict() for i in issues]
        }, 200

    def analyze_directory_api(self, dirpath):
        """Analisa diretório e retorna JSON."""
        if not Path(dirpath).exists():
            return {"error": f"Diretório não encontrado: {dirpath}"}, 404
        
        issues = self.scanner.scan(dirpath)
        
        # Agrupar por arquivo
        by_file = {}
        for issue in issues:
            if issue.file not in by_file:
                by_file[issue.file] = []
            by_file[issue.file].append(issue.to_dict())
        
        return {
            "directory": dirpath,
            "total_issues": len(issues),
            "files_with_issues": len(by_file),
            "issues_by_file": by_file
        }, 200

    def generate_report(self, dirpath, report_format="json"):
        """Gera relatório em diferentes formatos."""
        if report_format == "json":
            data, code = self.analyze_directory_api(dirpath)
            return {
                "format": "json",
                "data": data,
                "code": code
            }
        
        elif report_format == "txt":
            issues = self.scanner.scan(dirpath)
            report = "QUALITY REPORT\n" + "=" * 50 + "\n\n"
            for issue in issues:
                report += f"[{issue.severity}] {issue.rule_id}\n"
                report += f"  File: {issue.file}:{issue.line}\n"
                report += f"  {issue.description}\n"
                report += f"  Recommendation: {issue.recommendation}\n\n"
            return {"format": "txt", "content": report}
        
        elif report_format == "html":
            issues = self.scanner.scan(dirpath)
            html = """<html><head><title>Quality Report</title>
            <style>body{font-family:Arial;margin:20px}
            .issue{margin:10px;padding:10px;border:1px solid #ccc}
            .HIGH{background:#ffcccc}.MEDIUM{background:#ffffcc}.LOW{background:#ccffcc}
            </style></head><body><h1>Quality Report</h1>"""
            
            for issue in issues:
                html += f'<div class="issue {issue.severity}">'
                html += f'<strong>[{issue.severity}] {issue.rule_id}</strong><br>'
                html += f'{issue.file}:{issue.line}<br>'
                html += f'{issue.description}<br>'
                html += f'<em>→ {issue.recommendation}</em>'
                html += '</div>'
            
            html += "</body></html>"
            return {"format": "html", "content": html}
        
        return {"error": "Unknown format"}, 400

    def get_summary(self):
        """Retorna sumário do cache/histórico."""
        cache_stats = self.scanner.cache.get_stats()
        return {
            "cache": cache_stats,
            "version": "0.1.0"
        }
