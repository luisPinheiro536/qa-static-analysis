from difflib import SequenceMatcher
from ..models.issue import Issue


class DuplicationAnalyzer:
    """Detecta código duplicado em testes."""

    def analyze_file(self, filepath, content):
        issues = []
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        
        # Detectar linhas repetidas
        seen = {}
        for i, line in enumerate(lines):
            if line in seen and not line.startswith('***'):
                issues.append(Issue(
                    rule_id="DUP001",
                    category="DUPLICATION",
                    severity="MEDIUM",
                    description=f"Linha duplicada (apareceu em linha {seen[line] + 1}).",
                    file=filepath,
                    line=i + 1,
                    recommendation="Consolide em uma keyword reutilizável."
                ))
            seen[line] = i
        
        # Detectar testes com alta similaridade
        test_lines = [l for l in lines if 'Test Cases' in l or l.startswith('***')]
        for i in range(len(test_lines)):
            for j in range(i + 1, len(test_lines)):
                ratio = SequenceMatcher(None, test_lines[i], test_lines[j]).ratio()
                if 0.8 <= ratio < 1.0:
                    issues.append(Issue(
                        rule_id="DUP002",
                        category="DUPLICATION",
                        severity="LOW",
                        description=f"Testes similares detectados ({int(ratio*100)}% match).",
                        file=filepath,
                        line=i + 1,
                        recommendation="Use [Template] ou data-driven tests."
                    ))
        
        return issues
