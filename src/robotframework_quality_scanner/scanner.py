import os
from .models.issue import Issue

class QualityScanner:
    """Scanner simples que aplica regras básicas em arquivos .robot

    Atualmente detecta:
      - Uso de Sleep
      - XPath absoluto ("/html/")
      - Hardcoded HTTP (http://)
    """

    def __init__(self):
        pass

    def scan_file(self, path):
        issues = []
        with open(path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, start=1):
                if "Sleep" in line:
                    issues.append(Issue(
                        rule_id="WEB001",
                        category="WEB",
                        severity="HIGH",
                        description="Uso de Sleep detectado.",
                        file=os.path.basename(path),
                        line=i,
                        recommendation="Use waits explícitos como Wait Until Element Is Visible.",
                        reference="https://robotframework.org/SeleniumLibrary/"
                    ))
                if "/html/" in line or line.strip().startswith("/") and "xpath" in line.lower():
                    issues.append(Issue(
                        rule_id="WEB002",
                        category="WEB",
                        severity="MEDIUM",
                        description="XPath absoluto detectado.",
                        file=os.path.basename(path),
                        line=i,
                        recommendation="Use localizadores mais resilientes (ids, data-attributes).",
                    ))
                if "http://" in line:
                    issues.append(Issue(
                        rule_id="WEB003",
                        category="WEB",
                        severity="MEDIUM",
                        description="URL hardcoded com http detected.",
                        file=os.path.basename(path),
                        line=i,
                        recommendation="Extrair URL para variável de configuração.",
                    ))
        return issues

    def scan(self, path):
        results = []
        if os.path.isfile(path):
            if path.endswith('.robot') or path.endswith('.resource'):
                results.extend(self.scan_file(path))
            return results

        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith('.robot') or f.endswith('.resource'):
                    full = os.path.join(root, f)
                    results.extend(self.scan_file(full))
        return results
