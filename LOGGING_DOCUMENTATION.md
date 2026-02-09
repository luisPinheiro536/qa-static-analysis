# 📋 Logging Estruturado e Documentação Automática (v0.3.0+)

## Visão Geral

A partir da versão 0.3.0, o **robotframework-quality-scanner** captura automaticamente todos os erros, logs e traces (stack traces) de cada execução e gera documentação estruturada em Markdown e JSON.

## ✨ Características

### 1. **Captura Automática de Logs**
- ✅ Logs em tempo real durante a execução
- ✅ Captura de erros com stack traces completos
- ✅ Avisos e informações contextualizadas
- ✅ Timestamps para cada evento
- ✅ Identificação da origem (qual analisador/módulo)

### 2. **Estrutura de Dados Rica**
```python
LogEntry:
  - timestamp: ISO 8601
  - level: INFO | WARNING | ERROR | DEBUG
  - message: descrição do evento
  - source: qual módulo gerou o log
  - error_type: tipo de exceção (se houver)
  - traceback: stack trace completo
  - context: dados adicionais (dicionário)
```

### 3. **Relatórios Automáticos**

#### Markdown (`.md`)
- 📊 Sumário com contadores
- 🔴 Seção de erros com traces
- 🟡 Seção de avisos
- 📝 Tabela completa de logs
- 📅 Timestamp da geração

#### JSON (`.json`)
- Estrutura completa e programável
- Fácil integração com ferramentas externas
- Ideal para dashboards e análise automatizada

### 4. **Pasta `.docs/`**
- 📁 Criada automaticamente na primeira execução
- 📅 Armazena todos os relatórios com timestamp
- 🔍 Fácil localização e auditoria
- 📊 Histórico completo de execuções

## 🚀 Como Usar

### Uso Básico

```python
from robotframework_quality_scanner import QualityScanner

# Inicializar scanner (cria .docs/ automaticamente)
scanner = QualityScanner(docs_dir=".docs")

# Escanear com geração automática de logs
issues, reports = scanner.scan("./tests/", generate_reports=True)

# Logs são capturados automaticamente durante o scan
# Relatórios são gerados em .docs/scan_YYYYMMDD_HHMMSS_logs.*
```

### Acessar Logs em Memória

```python
# Verificar sumário
summary = scanner.logger.get_summary()
print(f"Total de logs: {summary['total_logs']}")
print(f"Erros: {summary['total_errors']}")
print(f"Avisos: {summary['total_warnings']}")

# Listar relatórios gerados
reports = scanner.logger.list_reports()
for report in reports:
    print(f"- {report['name']} ({report['size_bytes']} bytes)")
```

### Gerar Relatórios Manualmente

```python
# Markdown
md_report = scanner.logger.generate_markdown_report(filename="custom_name")

# JSON
json_report = scanner.logger.generate_json_report(filename="custom_name")
```

## 📁 Estrutura de Diretórios

```
seu_projeto/
├── .docs/
│   ├── scan_20260209_184112_logs.md
│   ├── scan_20260209_184112_logs.json
│   ├── scan_20260209_185530_logs.md
│   └── scan_20260209_185530_logs.json
├── tests/
│   └── *.robot
└── ...
```

## 📄 Exemplo de Relatório Markdown

```markdown
# 📋 Relatório de Execução - Logs e Erros

**Data/Hora:** 2026-02-09T18:41:12.585532

## 📊 Sumário

- **Total de Logs:** 5
- **Erros:** 1
- **Avisos:** 2

---

## 🔴 Erros Encontrados

### Erro 1: FileNotFoundError

**Timestamp:** 2026-02-09T18:41:12.590000

**Origem:** `scan_file`

**Mensagem:**
```
Arquivo não encontrado: tests/missing.robot
```

**Stack Trace:**
```python
Traceback (most recent call last):
  File "scanner.py", line 47, in scan_file
    with open(path, "r", encoding="utf-8") as f:
FileNotFoundError: [Errno 2] No such file or directory: 'tests/missing.robot'
```

---

## 🟡 Avisos

### Aviso 1

**Timestamp:** 2026-02-09T18:41:12.590000

**Origem:** `dependency_analyzer`

**Mensagem:** Cache hit não validado

---

## 📝 Log Completo

| Timestamp | Nível | Origem | Mensagem |
|-----------|-------|--------|----------|
| 2026-02-09T18:41:12.583122 | INFO | scan | Iniciando scan de examples/bad_web.robot |
| 2026-02-09T18:41:12.583361 | INFO | scan_file | Escaneando arquivo: bad_web.robot |
| 2026-02-09T18:41:12.590000 | ERROR | scan_file | Arquivo não encontrado: tests/missing.robot |
| ... | ... | ... | ... |
```

## 🔗 Integração com CI/CD

### GitHub Actions

```yaml
- name: Robot Framework Quality Scan
  run: |
    pip install robotframework-quality-scanner
    python -c "
      from robotframework_quality_scanner import QualityScanner
      scanner = QualityScanner()
      issues, reports = scanner.scan('./tests/')
      print(f'Scan concluído: {len(issues)} issues encontrados')
    "

- name: Upload Logs
  if: always()
  uses: actions/upload-artifact@v2
  with:
    name: quality-scanner-logs
    path: .docs/
```

## 📊 Análise Programática

```python
import json

# Ler relatório JSON
with open(".docs/scan_YYYYMMDD_HHMMSS_logs.json") as f:
    data = json.load(f)

# Analisar erros
for error in data['errors']:
    print(f"{error['error_type']}: {error['message']}")

# Verificar contexto
for log in data['all_logs']:
    if log['level'] == 'ERROR':
        print(f"Contexto: {log['context']}")
```

## 🎯 Casos de Uso

1. **Auditoria**: Manter histórico de todas as execuções
2. **Debugging**: Rastrear traces completos de erros
3. **Dashboard**: Integrar logs JSON em dashboards
4. **Alertas**: Automatizar notificações baseadas em erros
5. **Relatórios**: Gerar documentação automática das execuções
6. **Conformidade**: Documentar todas as verificações realizadas

## 🔧 Configuração Avançada

### Pasta Personalizada
```python
scanner = QualityScanner(docs_dir="custom/path/.docs")
```

### Limpeza de Logs
```python
scanner.logger.clear_logs()
```

### Nomes de Arquivo Customizados
```python
scanner.logger.generate_markdown_report(filename="my_custom_report")
```

## 📈 Ciclo de Vida do Log

1. **Captura**: Evento ocorre durante a execução
2. **Estruturação**: Convertido para `LogEntry`
3. **Armazenamento**: Armazenado em memória
4. **Geração**: Ao final do scan, relatórios são gerados
5. **Persistência**: Arquivos `.md` e `.json` salvos em `.docs/`

## 🔐 Boas Práticas

- ✅ Sempre faça commit da pasta `.docs/` no git para auditoria
- ✅ Use a integração com CI/CD para capturar logs de pipelines
- ✅ Analise relatórios JSON para automação
- ✅ Mantenha histórico de erros para tendências
- ✅ Revise traces antes de fazer alterações

---

**Documentação atualizada para v0.3.0+**
