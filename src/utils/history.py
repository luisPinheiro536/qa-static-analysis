import json
from pathlib import Path
from datetime import datetime


class AnalysisHistory:
    """Rastreia histórico de análises com tendências."""

    def __init__(self, history_dir=".analysis_history"):
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(exist_ok=True)

    def _get_history_file(self, filepath):
        """Arquivo JSON de histórico para um arquivo Robot."""
        return self.history_dir / f"{Path(filepath).stem}_history.json"

    def record_analysis(self, filepath, issues, analysis_type="all"):
        """Registra resultado de análise."""
        history_file = self._get_history_file(filepath)
        
        # Carregar histórico existente
        if history_file.exists():
            with open(history_file) as f:
                history = json.load(f)
        else:
            history = {"file": filepath, "runs": []}
        
        # Adicionar novo resultado
        run = {
            "timestamp": datetime.now().isoformat(),
            "analysis_type": analysis_type,
            "issue_count": len(issues),
            "issues_by_severity": {
                "CRITICAL": sum(1 for i in issues if i.severity == "CRITICAL"),
                "HIGH": sum(1 for i in issues if i.severity == "HIGH"),
                "MEDIUM": sum(1 for i in issues if i.severity == "MEDIUM"),
                "LOW": sum(1 for i in issues if i.severity == "LOW"),
            }
        }
        
        # Manter apenas últimas 100 análises
        history["runs"].append(run)
        history["runs"] = history["runs"][-100:]
        
        # Salvar
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)

    def get_history(self, filepath):
        """Retorna histórico completo."""
        history_file = self._get_history_file(filepath)
        if history_file.exists():
            with open(history_file) as f:
                return json.load(f)
        return {"file": filepath, "runs": []}

    def get_trends(self, filepath):
        """Analisa tendências."""
        history = self.get_history(filepath)
        if len(history["runs"]) < 2:
            return None
        
        latest = history["runs"][-1]
        previous = history["runs"][-2]
        
        current_count = latest["issue_count"]
        prev_count = previous["issue_count"]
        
        if current_count < prev_count:
            trend = "📈 melhorando"
        elif current_count > prev_count:
            trend = "📉 degradando"
        else:
            trend = "➡️ estável"
        
        return {
            "trend": trend,
            "current_count": current_count,
            "previous_count": prev_count,
            "change": current_count - prev_count
        }

    def export_json(self, filepath):
        """Exporta histórico em JSON."""
        return self.get_history(filepath)

    def clear(self):
        """Limpa todo o histórico."""
        import shutil
        shutil.rmtree(self.history_dir, ignore_errors=True)
        self.history_dir.mkdir()
