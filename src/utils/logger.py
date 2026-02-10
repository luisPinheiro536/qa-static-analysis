"""Sistema de logging estruturado com geração de relatórios em Markdown."""

import os
import json
import traceback
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class LogEntry:
    """Entrada de log estruturada."""
    timestamp: str
    level: str
    message: str
    source: str
    error_type: Optional[str] = None
    traceback: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return asdict(self)


class StructuredLogger:
    """Logger estruturado que captura erros, warnings e informações."""

    def __init__(self, docs_dir: str = ".docs"):
        """Inicializa o logger.
        
        Args:
            docs_dir: Diretório para armazenar documentos
        """
        self.docs_dir = Path(docs_dir)
        self.docs_dir.mkdir(exist_ok=True)
        
        self.logs: List[LogEntry] = []
        self.errors: List[LogEntry] = []
        self.warnings: List[LogEntry] = []
        
        # Configurar logging Python
        self.logger = logging.getLogger("robotframework_quality_scanner")
        self.logger.setLevel(logging.DEBUG)
        
        # Handler para capturar logs
        self._setup_handlers()

    def _setup_handlers(self):
        """Configura handlers de logging."""
        # Remover handlers existentes
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def info(self, message: str, source: str = "scanner", context: Optional[Dict] = None):
        """Log de informação."""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level="INFO",
            message=message,
            source=source,
            context=context
        )
        self.logs.append(entry)
        self.logger.info(message)

    def warning(self, message: str, source: str = "scanner", context: Optional[Dict] = None):
        """Log de aviso."""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level="WARNING",
            message=message,
            source=source,
            context=context
        )
        self.logs.append(entry)
        self.warnings.append(entry)
        self.logger.warning(message)

    def error(self, message: str, source: str = "scanner", 
              exception: Optional[Exception] = None, context: Optional[Dict] = None):
        """Log de erro com trace."""
        tb_str = None
        error_type = None
        
        if exception:
            error_type = type(exception).__name__
            tb_str = traceback.format_exc()
        
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level="ERROR",
            message=message,
            source=source,
            error_type=error_type,
            traceback=tb_str,
            context=context
        )
        self.logs.append(entry)
        self.errors.append(entry)
        self.logger.error(message, exc_info=exception)

    def debug(self, message: str, source: str = "scanner", context: Optional[Dict] = None):
        """Log de debug."""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level="DEBUG",
            message=message,
            source=source,
            context=context
        )
        self.logs.append(entry)
        self.logger.debug(message)

    def get_summary(self) -> Dict[str, Any]:
        """Retorna sumário dos logs."""
        return {
            "total_logs": len(self.logs),
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
            "timestamp": datetime.now().isoformat(),
            "duration": "N/A",  # Será calculado pelo scanner
        }

    def generate_markdown_report(self, filename: Optional[str] = None) -> str:
        """Gera relatório em Markdown com todos os logs.
        
        Args:
            filename: Nome do arquivo (sem extensão). Se None, usa timestamp.
            
        Returns:
            Conteúdo do arquivo markdown
        """
        if not filename:
            filename = datetime.now().strftime("%Y%m%d_%H%M%S_logs")
        
        # Gerar conteúdo
        report = self._build_markdown_report()
        
        # Salvar arquivo
        file_path = self.docs_dir / f"{filename}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        return report

    def _build_markdown_report(self) -> str:
        """Constrói o relatório em Markdown."""
        summary = self.get_summary()
        
        md = "# 📋 Relatório de Execução - Logs e Erros\n\n"
        md += f"**Data/Hora:** {summary['timestamp']}\n\n"
        
        # Sumário
        md += "## 📊 Sumário\n\n"
        md += f"- **Total de Logs:** {summary['total_logs']}\n"
        md += f"- **Erros:** {summary['total_errors']}\n"
        md += f"- **Avisos:** {summary['total_warnings']}\n\n"
        
        # Erros (se houver)
        if self.errors:
            md += "---\n\n"
            md += "## 🔴 Erros Encontrados\n\n"
            for i, error in enumerate(self.errors, 1):
                md += f"### Erro {i}: {error.error_type}\n\n"
                md += f"**Timestamp:** {error.timestamp}\n\n"
                md += f"**Origem:** `{error.source}`\n\n"
                md += f"**Mensagem:**\n```\n{error.message}\n```\n\n"
                
                if error.context:
                    md += f"**Contexto:**\n```json\n{json.dumps(error.context, indent=2)}\n```\n\n"
                
                if error.traceback:
                    md += f"**Stack Trace:**\n```python\n{error.traceback}\n```\n\n"
        
        # Avisos (se houver)
        if self.warnings:
            md += "---\n\n"
            md += "## 🟡 Avisos\n\n"
            for i, warning in enumerate(self.warnings, 1):
                md += f"### Aviso {i}\n\n"
                md += f"**Timestamp:** {warning.timestamp}\n\n"
                md += f"**Origem:** `{warning.source}`\n\n"
                md += f"**Mensagem:** {warning.message}\n\n"
                
                if warning.context:
                    md += f"**Contexto:**\n```json\n{json.dumps(warning.context, indent=2)}\n```\n\n"
        
        # Todos os logs
        md += "---\n\n"
        md += "## 📝 Log Completo\n\n"
        md += "| Timestamp | Nível | Origem | Mensagem |\n"
        md += "|-----------|-------|--------|----------|\n"
        
        for log in self.logs:
            msg = log.message.replace("|", "\\|")[:50]
            md += f"| {log.timestamp} | {log.level} | {log.source} | {msg}... |\n"
        
        md += "\n---\n\n"
        md += "_Relatório gerado automaticamente pelo robotframework-quality-scanner_\n"
        
        return md

    def generate_json_report(self, filename: Optional[str] = None) -> str:
        """Gera relatório em JSON.
        
        Args:
            filename: Nome do arquivo (sem extensão).
            
        Returns:
            Conteúdo do arquivo JSON
        """
        if not filename:
            filename = datetime.now().strftime("%Y%m%d_%H%M%S_logs")
        
        report_data = {
            "summary": self.get_summary(),
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings],
            "all_logs": [l.to_dict() for l in self.logs],
        }
        
        file_path = self.docs_dir / f"{filename}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return json.dumps(report_data, indent=2, ensure_ascii=False)

    def list_reports(self) -> List[Dict[str, Any]]:
        """Lista todos os relatórios gerados."""
        reports = []
        if self.docs_dir.exists():
            for file in sorted(self.docs_dir.glob("*.md")):
                size = file.stat().st_size
                mtime = datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                reports.append({
                    "name": file.name,
                    "path": str(file),
                    "size_bytes": size,
                    "modified": mtime,
                })
        return reports

    def clear_logs(self):
        """Limpa os logs em memória."""
        self.logs.clear()
        self.errors.clear()
        self.warnings.clear()
