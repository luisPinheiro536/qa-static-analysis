"""Library Robot Framework para robotframework-quality-scanner.

Exemplo de uso:
    *** Settings ***
    Library    QualityAnalysisLibrary

    *** Test Cases ***
    Escanear Projeto
        ${issues}    Scan Quality    ./tests/
        Log    Encontrados ${issues} issues
        
    Gerar Relatórios
        ${issues}    ${reports}    Scan With Reports    ./tests/
        Log    Quality Score: ${reports}[executive]
"""

from robot.api.deco import keyword
from quality_scanner import QualityScanner


class QualityAnalysisLibrary:
    """Library Robot Framework para análise de qualidade."""

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.3.0'

    def __init__(self):
        """Inicializa a library."""
        self.scanner = QualityScanner(docs_dir=".docs")
        self.last_issues = []
        self.last_reports = {}

    @keyword
    def scan_quality(self, path, use_cache=True):
        """Escaneia arquivos e retorna número de issues.
        
        Args:
            path: Caminho para arquivo ou diretório
            use_cache: Usar cache (True/False)
            
        Returns:
            Número de issues encontrados
            
        Example:
            ${issues}    Scan Quality    ./tests/
            Should Be Equal As Numbers    ${issues}    0
        """
        issues = self.scanner.scan(path, use_cache=use_cache, generate_reports=False)
        self.last_issues = issues
        return len(issues)

    @keyword
    def scan_with_reports(self, path, use_cache=True):
        """Escaneia e gera relatórios completos.
        
        Args:
            path: Caminho para arquivo ou diretório
            use_cache: Usar cache (True/False)
            
        Returns:
            Lista com [número de issues, dicionário de relatórios]
            
        Example:
            ${result}    Scan With Reports    ./tests/
            ${issues}    Get From List    ${result}    0
            Should Be Equal As Numbers    ${issues}    0
        """
        issues, reports = self.scanner.scan(path, use_cache=use_cache, generate_reports=True)
        self.last_issues = issues
        self.last_reports = reports
        return [len(issues), reports]

    @keyword
    def get_issues_by_severity(self, severity):
        """Retorna issues de uma severidade específica.
        
        Args:
            severity: CRITICAL, HIGH, MEDIUM ou LOW
            
        Returns:
            Lista de issues com a severidade
            
        Example:
            ${high_issues}    Get Issues By Severity    HIGH
            Length Should Be    ${high_issues}    0
        """
        filtered = [i for i in self.last_issues if i.severity == severity]
        return filtered

    @keyword
    def get_issues_by_rule(self, rule_id):
        """Retorna issues de uma regra específica.
        
        Args:
            rule_id: ID da regra (WEB001, PERF001, etc)
            
        Returns:
            Lista de issues da regra
            
        Example:
            ${sleep_issues}    Get Issues By Rule    WEB001
            Length Should Be    ${sleep_issues}    0
        """
        filtered = [i for i in self.last_issues if i.rule_id == rule_id]
        return filtered

    @keyword
    def get_quality_score(self):
        """Retorna o score de qualidade (0-100).
        
        Returns:
            Score de qualidade
            
        Example:
            ${score}    Get Quality Score
            Should Be Greater Than    ${score}    80
        """
        if not self.last_reports or 'executive' not in self.last_reports:
            return None
        
        exec_report = self.last_reports['executive']
        report_dict = exec_report.to_dict()
        return report_dict['summary']['quality_score']

    @keyword
    def get_issues_summary(self):
        """Retorna sumário de issues.
        
        Returns:
            Dicionário com contadores por severidade
            
        Example:
            ${summary}    Get Issues Summary
            Should Be Equal As Numbers    ${summary}[HIGH]    0
        """
        summary = {
            'CRITICAL': len([i for i in self.last_issues if i.severity == 'CRITICAL']),
            'HIGH': len([i for i in self.last_issues if i.severity == 'HIGH']),
            'MEDIUM': len([i for i in self.last_issues if i.severity == 'MEDIUM']),
            'LOW': len([i for i in self.last_issues if i.severity == 'LOW']),
            'total': len(self.last_issues)
        }
        return summary

    @keyword
    def assert_no_critical_issues(self):
        """Falha se houver issues críticos.
        
        Example:
            Assert No Critical Issues
        """
        critical = [i for i in self.last_issues if i.severity == 'CRITICAL']
        if critical:
            raise AssertionError(f"Encontrados {len(critical)} issues CRITICAL")

    @keyword
    def assert_no_high_issues(self):
        """Falha se houver issues altos.
        
        Example:
            Assert No High Issues
        """
        high = [i for i in self.last_issues if i.severity == 'HIGH']
        if high:
            raise AssertionError(f"Encontrados {len(high)} issues HIGH")

    @keyword
    def assert_quality_score_above(self, minimum_score):
        """Falha se score de qualidade for menor que o mínimo.
        
        Args:
            minimum_score: Score mínimo esperado (0-100)
            
        Example:
            Assert Quality Score Above    80
        """
        score = self.get_quality_score()
        if score is None:
            raise AssertionError("Nenhum scan com relatório foi executado")
        
        if score < float(minimum_score):
            raise AssertionError(
                f"Quality score {score} é menor que {minimum_score}"
            )

    @keyword
    def get_total_issues(self):
        """Retorna o número total de issues.
        
        Returns:
            Total de issues
            
        Example:
            ${total}    Get Total Issues
            Should Be Equal As Numbers    ${total}    0
        """
        return len(self.last_issues)

    @keyword
    def print_issues(self):
        """Imprime todos os issues encontrados.
        
        Example:
            Print Issues
        """
        if not self.last_issues:
            print("\n✓ Nenhum issue encontrado!\n")
            return
        
        print(f"\n\n{'='*80}")
        print(f"{'ISSUES ENCONTRADOS':^80}")
        print(f"{'='*80}\n")
        
        for issue in sorted(self.last_issues, key=lambda x: x.severity):
            print(f"[{issue.severity}] {issue.rule_id} - {issue.file}:{issue.line}")
            print(f"  → {issue.description}")
            print(f"  ✓ {issue.recommendation}\n")
        
        print(f"{'='*80}\n")

    @keyword
    def print_quality_report(self):
        """Imprime o relatório de qualidade.
        
        Example:
            Print Quality Report
        """
        if not self.last_reports or 'executive' not in self.last_reports:
            print("\nNenhum relatório disponível. Execute scan_with_reports primeiro.\n")
            return
        
        report = self.last_reports['executive']
        print("\n\n" + report.to_text())
