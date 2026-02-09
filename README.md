# robotframework-quality-scanner

Uma **Robot Framework Library** para escanear projetos de automação **Web, Mobile e API**, identificar **más práticas**, gerar **logs estruturados**, **relatórios** e **sugestões de correção baseadas em boas práticas oficiais**.

**Versão**: 0.2.0  
**Status**: Beta com suporte para caching, histórico, 4 analisadores especializados e API REST.

---

## 🎯 Objetivo

* Analisar arquivos `.robot` e `.resource`
* Detectar anti-patterns comuns em automação
* Classificar problemas por severidade (CRITICAL, HIGH, MEDIUM, LOW)
* Explicar impacto técnico e sugerir soluções
* **Cache 10x mais rápido** para análises repetidas
* Rastrear **histórico e tendências** de qualidade
* Gerar **múltiplos relatórios** (JSON, HTML, TXT)
* Integrar facilmente com **CI/CD e ferramentas externas** via API REST

---

## ✨ Features v0.2.0

### ✅ Implementado

1. **4 Analisadores Especializados**
   - `PerformanceAnalyzer`: Deep nesting, Sleep longo, linhas muito longas
   - `DuplicationAnalyzer`: Código duplicado, testes similares
   - `DependencyAnalyzer`: Validação de imports, organização
   - `TestDataAnalyzer`: Dados hardcoded, padrões data-driven

2. **Cache de Análises** (10x performance)
   - Invalidação por hash de arquivo
   - Armazenamento em pickle

3. **Histórico com Tendências**
   - Rastreia 100 últimas análises por arquivo
   - Detecta: 📈 melhorando, ➡️ estável, 📉 degradando
   - Exporta em JSON

4. **Auto-Fix Automático**
   - Remove trailing whitespace
   - Normaliza indentação (tabs → spaces)
   - Adiciona [Documentation]
   - Capitaliza keywords

5. **API REST**
   - Endpoints para análise de arquivo/diretório
   - Geração de relatórios (JSON, HTML, TXT)
   - Health check e sumário

6. **Relatórios Múltiplos**
   - Console (estruturado)
   - JSON (programável)
   - HTML (visual)
   - TXT (simples)

---

## 📦 Instalação

```bash
pip install robotframework-quality-scanner
```

---

## 🚀 Uso Rápido

### Python

```python
from robotframework_quality_scanner import QualityScanner

scanner = QualityScanner()

# Escanear com geração automática de relatórios
issues, reports = scanner.scan("./tests/", generate_reports=True)

# Exibir relatório executivo
print(reports['executive'].to_text())

# Salvar todos os relatórios em arquivos
scanner.save_reports("./quality-reports")
```

### Relatórios Automáticos

Ao final da execução, a biblioteca gera automaticamente dois relatórios:

1. **Relatório Executivo** - Sumário de qualidade com:
   - Score de qualidade (0-100)
   - Distribuição por severidade
   - Distribuição por categoria
   - Top 10 issues mais frequentes
   - Top 5 arquivos com mais problemas
   - Recomendações automáticas

2. **Relatório de Cobertura** - Análise de testes com:
   - Cobertura de documentação de keywords
   - Cobertura de uso de keywords
   - Detecção de keywords não utilizadas
   - Métricas por arquivo

```python
# Gerar formatos específicos
exec_text = scanner.generate_executive_report(issues, format='text')
exec_html = scanner.generate_executive_report(issues, format='html')
exec_json = scanner.generate_executive_report(issues, format='json')

cov_text = scanner.generate_coverage_report(format='text')
cov_html = scanner.generate_coverage_report(format='html')

# Salvar em diretório específico
scanner.save_reports("./output/reports")
# Cria:
#   ├── executive_report.html
#   ├── executive_report.txt
#   ├── executive_report.json
#   ├── coverage_report.html
#   └── coverage_report.txt
```

### Exemplo Completo

```python
from robotframework_quality_scanner import QualityScanner

scanner = QualityScanner()
issues, reports = scanner.scan("./tests/", use_cache=False, generate_reports=True)

print(f"[SUMÁRIO] {len(issues)} problemas encontrados")
print(f"[QUALIDADE] {reports['executive'].to_dict()['summary']['quality_score']}/100")

# Salvar relatórios
output = scanner.save_reports("./quality-reports")
print(f"✓ Relatórios salvos em: {output}")
```


---

## 🔍 Analisadores

| Analisador | Regra | Severidade | Descrição |
|-----------|-------|-----------|-----------|
| Web | WEB001 | HIGH | Sleep detectado |
| Web | WEB002 | MEDIUM | XPath absoluto |
| Web | WEB003 | MEDIUM | URL hardcoded |
| Performance | PERF001 | MEDIUM | Deep nesting (>4 níveis) |
| Performance | PERF002 | HIGH | Sleep muito longo (>5s) |
| Performance | PERF003 | LOW | Linha muito longa (>120 chars) |
| Duplication | DUP001 | MEDIUM | Linha duplicada |
| Duplication | DUP002 | LOW | Testes similares (80%+) |
| Dependency | DEP001 | HIGH | Library com URL/path |
| Dependency | DEP002 | MEDIUM | Resource com extensão não-robot |
| Dependency | DEP003 | LOW | Library após Resource |
| TestData | DATA001 | MEDIUM | Email hardcoded |
| TestData | DATA002 | MEDIUM | URL hardcoded |
| TestData | DATA003 | MEDIUM | Telefone hardcoded |
| TestData | DATA004 | LOW | Oportunidade data-driven |

---

## 🧪 Testes

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

---

## 🚀 CI/CD

```yaml
- run: pip install robotframework-quality-scanner
- run: python -c "
    from robotframework_quality_scanner import QualityScanner
    s = QualityScanner()
    issues = s.scan('./tests')
    high = [i for i in issues if i.severity in ['CRITICAL', 'HIGH']]
    exit(len(high) if high else 0)
  "
```

---

## 📞 Suporte

- 📄 [GitHub Issues](https://github.com/luisPinheiro536/qa-static-analysis/issues)
- 📧 luis@example.com

---

**Desenvolvido com ❤️ para a comunidade de QA Automation**

---

## 📦 Estrutura do Projeto

```text
robotframework-quality-scanner/
├── robotframework_quality_scanner/
│   ├── __init__.py
│   ├── scanner.py
│   ├── logger.py
│   ├── rules/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── web_rules.py
│   │   ├── api_rules.py
│   │   └── mobile_rules.py
│   ├── models/
│   │   ├── issue.py
│   │   └── report.py
│   ├── reporters/
│   │   ├── console_reporter.py
│   │   └── json_reporter.py
│   └── suggestions/
│       ├── web.py
│       ├── api.py
│       └── mobile.py
├── examples/
│   ├── bad_web.robot
│   ├── bad_api.robot
│   └── bad_mobile.robot
├── tests/
├── .github/workflows/ci.yml
├── README.md
├── pyproject.toml
└── setup.py
```

---

## 🧠 Modelo de Issue

```python
class Issue:
    def __init__(self, rule_id, category, severity, description,
                 file, line, recommendation, reference):
        self.rule_id = rule_id
        self.category = category
        self.severity = severity
        self.description = description
        self.file = file
        self.line = line
        self.recommendation = recommendation
        self.reference = reference
```

---

## 🔎 Scanner Principal

```python
class QualityScanner:
    def scan(self, path):
        issues = []
        issues += WebRules().analyze(path)
        issues += ApiRules().analyze(path)
        issues += MobileRules().analyze(path)
        return issues
```

---

## ✅ Regras Implementadas (10)

### Web (Selenium)

1. Uso de `Sleep`
2. XPath absoluto
3. Falta de waits explícitos
4. Hardcoded URL

### API

5. Validação apenas de status code
6. Sem validação de schema JSON
7. Headers hardcoded

### Mobile (Appium)

8. Tap por coordenadas
9. Uso de `Sleep` em mobile
10. Ausência de `accessibility_id`

---

## 🕸️ Exemplo de Regra (WEB001)

```python
if 'Sleep' in line:
    issues.append(Issue(
        rule_id='WEB001',
        category='WEB',
        severity='HIGH',
        description='Uso de Sleep detectado.',
        file=file,
        line=line_no,
        recommendation='Use Wait Until Element Is Visible.',
        reference='https://robotframework.org/SeleniumLibrary/'
    ))
```

---

## 🧪 Exemplos Ruins

### bad_web.robot

```robot
*** Test Cases ***
Login
    Open Browser    http://site.com    chrome
    Sleep    5s
    Click Element    /html/body/div[2]/button
```

---

## 📊 Logs no Console

```text
[HIGH] WEB001 - bad_web.robot:5
Uso de Sleep detectado
Sugestão: Use Wait Until Element Is Visible
```

---

## 📄 JSON Report (CI/CD)

```json
{
  "rule_id": "WEB001",
  "severity": "HIGH",
  "file": "bad_web.robot",
  "recommendation": "Use waits explícitos"
}
```

---

## 🤖 Uso no Robot Framework

```robot
*** Settings ***
Library    QualityScanner

*** Test Cases ***
Scan Project
    Scan Project    ./examples
```

---

## 📦 pyproject.toml (PyPI)

```toml
[project]
name = "robotframework-quality-scanner"
version = "0.1.0"
description = "Quality scanner for Robot Framework automation"
```

---

## 🔁 GitHub Actions (.github/workflows/ci.yml)

```yaml
name: CI
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install .
      - run: robot -L TRACE examples/
```

---

## 🚀 Roadmap

### v0.2.0 – Engine & Reports

* Rule Engine configurável via YAML
* HTML Report estilo Allure
* Quality Gate por severidade

### v0.3.0 – CI/CD & Segurança

* Exportação SARIF (GitHub Code Scanning)
* GitHub Action oficial

### v1.0.0 – Educação & Comunidade

* Guia educacional para times QA
* Catálogo de boas práticas
* Regras comunitárias

---

## 🧩 Rule Engine em YAML

As regras são definidas externamente em YAML, permitindo fácil extensão:

```yaml
rules:
  - id: WEB001
    category: WEB
    severity: HIGH
    match: "Sleep"
    description: Uso de Sleep detectado
    recommendation: Utilize waits explícitos
    reference: https://robotframework.org/SeleniumLibrary/
```

O scanner carrega dinamicamente essas regras e aplica regex/keywords nos arquivos `.robot`.

---

## 📊 HTML Report (Estilo Allure)

O relatório HTML apresenta:

* Cards por severidade
* Tabela detalhada de issues
* Resumo executivo (total, críticos, avisos)

Arquivo gerado: `quality-report.html`

---

## 🚦 Quality Gate

É possível configurar falha do build por severidade:

```yaml
quality_gate:
  fail_on:
    - CRITICAL
    - HIGH
```

Se uma issue dessas severidades for encontrada, o scanner retorna exit code ≠ 0.

---

## 🛡️ SARIF (GitHub Code Scanning)

O relatório pode ser exportado em SARIF para integração nativa com GitHub Security:

* Visualização direto no Pull Request
* Histórico de problemas
* Comentários automáticos

---

## 🤖 GitHub Action Oficial

```yaml
name: Robot Framework Quality Scanner
runs:
  using: "docker"
  steps:
    - run: quality-scanner ./tests --rules rules.yaml
```

Permite uso simples em qualquer pipeline GitHub.

---

## 🎓 Ferramenta Educacional para QA

A library pode ser usada como:

* Checklist automatizado de boas práticas
* Ferramenta de onboarding de QAs
* Base para treinamentos internos
* Apoio em code review de testes

Cada issue explica:

* O problema
* O impacto
* A melhor prática
* Referência oficial

---

## 🌍 Visão de Longo Prazo

Este projeto pode evoluir para:

* Padrão de mercado em qualidade de automação
* Plugin educacional para IDEs
* Base de conhecimento comunitária
