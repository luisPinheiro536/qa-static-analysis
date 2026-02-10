import re
from ..models.issue import Issue


class PerformanceAnalyzer:
    """Detecta problemas de performance em testes Robot Framework."""

    def analyze_file(self, filepath, content):
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Deep nesting (>4 níveis)
            indent = len(line) - len(line.lstrip())
            if indent > 16:  # 4+ níveis de indentação
                issues.append(Issue(
                    rule_id="PERF001",
                    category="PERFORMANCE",
                    severity="MEDIUM",
                    description="Deep nesting detectado (>4 níveis).",
                    file=filepath,
                    line=i,
                    recommendation="Refatore keywords para reduzir nesting."
                ))
            
            # Sleep excessivo
            if 'Sleep' in line:
                sleep_match = re.search(r'Sleep\s+(\d+)([smh]?)', line, re.IGNORECASE)
                if sleep_match:
                    val = int(sleep_match.group(1))
                    unit = sleep_match.group(2) or 's'
                    total_sec = val * (1 if unit == 's' else 60 if unit == 'm' else 3600)
                    if total_sec > 5:
                        issues.append(Issue(
                            rule_id="PERF002",
                            category="PERFORMANCE",
                            severity="HIGH",
                            description=f"Sleep muito longo detectado ({val}{unit}).",
                            file=filepath,
                            line=i,
                            recommendation="Use waits explícitos ao invés de Sleep."
                        ))
            
            # Linha muito longa (>120 chars)
            if len(line) > 120:
                issues.append(Issue(
                    rule_id="PERF003",
                    category="PERFORMANCE",
                    severity="LOW",
                    description="Linha muito longa detectada (>120 caracteres).",
                    file=filepath,
                    line=i,
                    recommendation="Quebre a linha ou refatore a lógica."
                ))
        
        return issues
