import os
from .models.issue import Issue
from .analyzers.performance_analyzer import PerformanceAnalyzer
from .analyzers.duplication_analyzer import DuplicationAnalyzer
from .analyzers.dependency_analyzer import DependencyAnalyzer
from .analyzers.test_data_analyzer import TestDataAnalyzer
from .utils import AnalysisCache
from .utils.history import AnalysisHistory


class QualityScanner:
    """Scanner de qualidade Robot Framework com múltiplos analisadores.

    Detecta:
      - Anti-patterns web (Sleep, XPath, URLs)
      - Performance (deep nesting, timeouts)
      - Código duplicado
      - Problemas de dependência
      - Dados hardcoded
    """

    def __init__(self):
        self.cache = AnalysisCache()
        self.history = AnalysisHistory()
        self.perf_analyzer = PerformanceAnalyzer()
        self.dup_analyzer = DuplicationAnalyzer()
        self.dep_analyzer = DependencyAnalyzer()
        self.data_analyzer = TestDataAnalyzer()

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

    def scan(self, path, use_cache=True):
        """Escaneia arquivo ou diretório recursivamente."""
        results = []
        
        if os.path.isfile(path):
            if path.endswith(('.robot', '.resource')):
                results.extend(self.scan_file(path, use_cache))
            return results

        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(('.robot', '.resource')):
                    full = os.path.join(root, f)
                    results.extend(self.scan_file(full, use_cache))
        
        return results
