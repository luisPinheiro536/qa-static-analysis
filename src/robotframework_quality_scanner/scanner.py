import os
import time
from .models.issue import Issue
from .analyzers.performance_analyzer import PerformanceAnalyzer
from .analyzers.duplication_analyzer import DuplicationAnalyzer
from .analyzers.dependency_analyzer import DependencyAnalyzer
from .analyzers.test_data_analyzer import TestDataAnalyzer
from .utils import AnalysisCache
from .utils.history import AnalysisHistory
from .reporters.executive_report import ExecutiveReport
from .reporters.coverage_report import CoverageReport


class QualityScanner:
    """Scanner de qualidade Robot Framework com múltiplos analisadores.

    Detecta:
      - Anti-patterns web (Sleep, XPath, URLs)
      - Performance (deep nesting, timeouts)
      - Código duplicado
      - Problemas de dependência
      - Dados hardcoded
      - Gera relatórios executivos e de cobertura
    """

    def __init__(self):
        self.cache = AnalysisCache()
        self.history = AnalysisHistory()
        self.perf_analyzer = PerformanceAnalyzer()
        self.dup_analyzer = DuplicationAnalyzer()
        self.dep_analyzer = DependencyAnalyzer()
        self.data_analyzer = TestDataAnalyzer()
        self.scan_time = 0
        self.files_analyzed = []
        self.reports = {}

    def scan_file(self, path, use_cache=True):
        """Escaneia um arquivo individual."""
        # Verificar cache
        if use_cache:
            cached = self.cache.get(path)
            if cached is not None:
                return cached

        issues = []
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        basename = os.path.basename(path)

        # Armazenar para cobertura
        self.files_analyzed.append((basename, content))

        # Web/Basic rules
        for i, line in enumerate(content.split('\n'), 1):
            if "Sleep" in line:
                issues.append(Issue(
                    rule_id="WEB001",
                    category="WEB",
                    severity="HIGH",
                    description="Uso de Sleep detectado.",
                    file=basename,
                    line=i,
                    recommendation="Use waits explícitos.",
                    reference="https://robotframework.org/SeleniumLibrary/"
                ))
            if "/html/" in line or (line.strip().startswith("/") and "xpath" in line.lower()):
                issues.append(Issue(
                    rule_id="WEB002",
                    category="WEB",
                    severity="MEDIUM",
                    description="XPath absoluto detectado.",
                    file=basename,
                    line=i,
                    recommendation="Use localizadores mais resilientes."
                ))
            if "http://" in line:
                issues.append(Issue(
                    rule_id="WEB003",
                    category="WEB",
                    severity="MEDIUM",
                    description="URL hardcoded.",
                    file=basename,
                    line=i,
                    recommendation="Extrair para variável."
                ))

        # Analisadores especializados
        issues.extend(self.perf_analyzer.analyze_file(basename, content))
        issues.extend(self.dup_analyzer.analyze_file(basename, content))
        issues.extend(self.dep_analyzer.analyze_file(basename, content))
        issues.extend(self.data_analyzer.analyze_file(basename, content))

        # Cache + Histórico
        self.cache.set(path, issues)
        self.history.record_analysis(path, issues)

        return issues

    def scan(self, path, use_cache=True, generate_reports=True):
        """Escaneia arquivo ou diretório recursivamente e gera relatórios."""
        start_time = time.time()
        results = []
        self.files_analyzed = []
        
        if os.path.isfile(path):
            if path.endswith(('.robot', '.resource')):
                results.extend(self.scan_file(path, use_cache))
        else:
            for root, _, files in os.walk(path):
                for f in files:
                    if f.endswith(('.robot', '.resource')):
                        full = os.path.join(root, f)
                        results.extend(self.scan_file(full, use_cache))
        
        self.scan_time = time.time() - start_time

        # Gerar relatórios
        if generate_reports:
            self.reports = {
                'executive': ExecutiveReport(results, self.scan_time),
                'coverage': CoverageReport(self.files_analyzed)
            }
            return results, self.reports
        
        return results

    def generate_executive_report(self, issues, format='text'):
        """Gera relatório executivo em diferentes formatos."""
        report = ExecutiveReport(issues, self.scan_time)
        
        if format == 'text':
            return report.to_text()
        elif format == 'json':
            return report.to_json()
        elif format == 'html':
            return report.to_html()
        else:
            return report.to_dict()

    def generate_coverage_report(self, format='text'):
        """Gera relatório de cobertura."""
        report = CoverageReport(self.files_analyzed)
        
        if format == 'text':
            return report.to_text()
        elif format == 'html':
            return report.to_html()
        else:
            return report.to_dict()

    def save_reports(self, output_dir='./quality-reports'):
        """Salva relatórios em arquivo."""
        os.makedirs(output_dir, exist_ok=True)

        # Salvar relatório executivo
        with open(os.path.join(output_dir, 'executive_report.html'), 'w') as f:
            f.write(self.reports['executive'].to_html())
        
        with open(os.path.join(output_dir, 'executive_report.txt'), 'w') as f:
            f.write(self.reports['executive'].to_text())
        
        with open(os.path.join(output_dir, 'executive_report.json'), 'w') as f:
            f.write(self.reports['executive'].to_json())

        # Salvar relatório de cobertura
        with open(os.path.join(output_dir, 'coverage_report.html'), 'w') as f:
            f.write(self.reports['coverage'].to_html())
        
        with open(os.path.join(output_dir, 'coverage_report.txt'), 'w') as f:
            f.write(self.reports['coverage'].to_text())

        return output_dir
