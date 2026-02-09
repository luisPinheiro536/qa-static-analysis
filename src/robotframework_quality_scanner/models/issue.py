class Issue:
    def __init__(self, rule_id, category, severity, description, file, line, recommendation, reference=None):
        self.rule_id = rule_id
        self.category = category
        self.severity = severity
        self.description = description
        self.file = file
        self.line = line
        self.recommendation = recommendation
        self.reference = reference

    def to_dict(self):
        return {
            "rule_id": self.rule_id,
            "category": self.category,
            "severity": self.severity,
            "description": self.description,
            "file": self.file,
            "line": self.line,
            "recommendation": self.recommendation,
            "reference": self.reference,
        }
