import re
from ..models.issue import Issue


class DependencyAnalyzer:
    """Valida imports e dependências."""

    def analyze_file(self, filepath, content):
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Library não é String
            if 'Library' in line and not any(x in line for x in ['Builtin', 'String', 'Collections']):
                if 'Library    http://' in line or 'Library    C:\\' in line:
                    issues.append(Issue(
                        rule_id="DEP001",
                        category="DEPENDENCY",
                        severity="HIGH",
                        description="Library com URL ou path absoluto.",
                        file=filepath,
                        line=i,
                        recommendation="Use imports relativos ou instale como package."
                    ))
            
            # Resource não encontrado (heurística: arquivo com extensão rara)
            if 'Resource' in line:
                res_match = re.search(r'Resource\s+(.+)', line)
                if res_match:
                    res_file = res_match.group(1).strip()
                    if res_file.endswith(('.py', '.txt', '.json')):
                        issues.append(Issue(
                            rule_id="DEP002",
                            category="DEPENDENCY",
                            severity="MEDIUM",
                            description="Resource com extensão não-robot.",
                            file=filepath,
                            line=i,
                            recommendation="Use arquivos .robot ou .resource."
                        ))
            
            # Import organizado (Libraries antes de Resources)
            if i > 1 and 'Resource' in lines[i-2] and 'Library' in line:
                issues.append(Issue(
                    rule_id="DEP003",
                    category="DEPENDENCY",
                    severity="LOW",
                    description="Library após Resource detectado.",
                    file=filepath,
                    line=i,
                    recommendation="Organize: Libraries primeiro, depois Resources."
                ))
        
        return issues
