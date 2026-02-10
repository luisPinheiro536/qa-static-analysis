import re
from ..models.issue import Issue


class TestDataAnalyzer:
    """Valida separação entre dados e lógica."""

    def analyze_file(self, filepath, content):
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Dados hardcoded
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            url_pattern = r'https?://[^\s]+'
            phone_pattern = r'\(\d{2}\)\s?9?\d{4}-\d{4}'
            
            if re.search(email_pattern, line):
                issues.append(Issue(
                    rule_id="DATA001",
                    category="TEST_DATA",
                    severity="MEDIUM",
                    description="Email hardcoded detectado.",
                    file=filepath,
                    line=i,
                    recommendation="Extraia para variável ou arquivo de dados."
                ))
            
            if re.search(url_pattern, line) and 'http' not in line.split('#')[0]:
                continue  # Skip comentários
            
            if re.search(url_pattern, line):
                issues.append(Issue(
                    rule_id="DATA002",
                    category="TEST_DATA",
                    severity="MEDIUM",
                    description="URL hardcoded detectada.",
                    file=filepath,
                    line=i,
                    recommendation="Use variável de ambiente ou arquivo de configuração."
                ))
            
            if re.search(phone_pattern, line):
                issues.append(Issue(
                    rule_id="DATA003",
                    category="TEST_DATA",
                    severity="MEDIUM",
                    description="Telefone hardcoded detectado.",
                    file=filepath,
                    line=i,
                    recommendation="Extraia para dados de teste."
                ))
            
            # Data-driven pattern sugestão
            if 'Test Cases' in line:
                # Heurística: 3+ testes similares → sugerir [Template]
                test_count = sum(1 for l in lines if l.strip() and not l.startswith('    ') and l not in ['*** Test Cases ***', '*** Keywords ***', '*** Settings ***'])
                if test_count >= 3:
                    issues.append(Issue(
                        rule_id="DATA004",
                        category="TEST_DATA",
                        severity="LOW",
                        description="Oportunidade de data-driven tests detectada.",
                        file=filepath,
                        line=i,
                        recommendation="Considere usar [Template] com multiple test cases."
                    ))
                    break
        
        return issues
