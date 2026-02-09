import os
import time
from .models.issue import Issue
from .analyzers.performance_analyzer import PerformanceAnalyzer
from .analyzers.duplication_analyzer import DuplicationAnalyzer
from .analyzers.dependency_analyzer import DependencyAnalyzer
from .analyzers.test_data_analyzer import TestDataAnalyzer
from .utils import AnalysisCache
from .utils.history import AnalysisHistory
from .utils.logger import StructuredLogger
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
      - Logs estruturados com erros e traces
    """

    def __init__(self, docs_dir: str = ".docs"):
        self.cache = AnalysisCache()
        self.history = AnalysisHistory()
        self.logger = StructuredLogger(docs_dir=docs_dir)
        self.perf_analyzer = PerformanceAnalyzer()
        self.dup_analyzer = DuplicationAnalyzer()
        self.dep_analyzer = DependencyAnalyzer()
        self.data_analyzer = TestDataAnalyzer()
        self.scan_time = 0
        self.files_analyzed = []
        self.reports = {}
        self.docs_dir = docs_dir

    def scan_file(self, path, use_cache=True):
        """Escaneia um arquivo individual."""
        try:
            # Verificar cache
            if use_cache:
                cached = self.cache.get(path)
                if cached is not None:
                    self.logger.debug(f"Cache hit para {path}", source="scan_file")
                    return cached

            issues = []
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            basename = os.path.basename(path)
            self.logger.info(f"Escaneando arquivo: {basename}", source="scan_file", 
                            context={"file": basename, "size": len(content)})

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
            try:
                issues.extend(self.perf_analyzer.analyze_file(basename, content))
            except Exception as e:
                self.logger.error(f"Erro no PerformanceAnalyzer para {basename}", 
                                source="performance_analyzer", exception=e,
                                context={"file": basename})
            
            try:
                issues.extend(self.dup_analyzer.analyze_file(basename, content))
            except Exception as e:
                self.logger.error(f"Erro no DuplicationAnalyzer para {basename}", 
                                source="duplication_analyzer", exception=e,
                                context={"file": basename})
            
            try:
                issues.extend(self.dep_analyzer.analyze_file(basename, content))
            except Exception as e:
                self.logger.error(f"Erro no DependencyAnalyzer para {basename}", 
                                source="dependency_analyzer", exception=e,
                                context={"file": basename})
            
            try:
                issues.extend(self.data_analyzer.analyze_file(basename, content))
            except Exception as e:
                self.logger.error(f"Erro no TestDataAnalyzer para {basename}", 
                                source="test_data_analyzer", exception=e,
                                context={"file": basename})

            # Cache + Histórico
            self.cache.set(path, issues)
            self.history.record_analysis(path, issues)
            
            self.logger.info(f"Arquivo {basename} escaneado: {len(issues)} issues encontrados", 
                            source="scan_file", context={"file": basename, "issues": len(issues)})

            return issues
        
        except FileNotFoundError as e:
            self.logger.error(f"Arquivo não encontrado: {path}", 
                            source="scan_file", exception=e,
                            context={"file": path})
            return []
        except Exception as e:
            self.logger.error(f"Erro ao escanear {path}", 
                            source="scan_file", exception=e,
                            context={"file": path})
            return []

    def scan(self, path, use_cache=True, generate_reports=True):
        """Escaneia arquivo ou diretório recursivamente e gera relatórios."""
        try:
            start_time = time.time()
            results = []
            self.files_analyzed = []
            
            self.logger.info(f"Iniciando scan de {path}", source="scan",
                            context={"path": path, "use_cache": use_cache})
            
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
            
            self.logger.info(f"Scan concluído: {len(results)} issues encontrados em {len(self.files_analyzed)} arquivos", 
                            source="scan", context={"total_issues": len(results), "files": len(self.files_analyzed)})

            # Gerar relatórios
            if generate_reports:
                self.reports = {
                    'executive': ExecutiveReport(results, self.scan_time),
                    'coverage': CoverageReport(self.files_analyzed)
                }
                
                # Gerar relatório de logs em markdown
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                self.logger.generate_markdown_report(filename=f"scan_{timestamp}_logs")
                self.logger.generate_json_report(filename=f"scan_{timestamp}_logs")
                
                self.logger.info(f"Relatórios gerados na pasta {self.docs_dir}", source="scan")
                
                return results, self.reports
            
            return results
        
        except Exception as e:
            self.logger.error(f"Erro fatal durante o scan", source="scan", exception=e,
                            context={"path": path})
            raise

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
