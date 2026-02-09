# 🤖 Robot Framework CLI - Guia Completo

## Instalação Rápida

```bash
# Instalar a biblioteca
pip install -e .

# Ou via PyPI
pip install robotframework-quality-scanner
```

## Executar via CLI Robot Framework

### **Opção 1: Executar teste simples**

```bash
robot examples/quality_tests.robot
```

**Output esperado:**
```
==============================================================================
Example :: Exemplo de testes usando robotframework-quality-scanner
==============================================================================
Escanear Arquivo e Validar Issues                                  | PASS |
Gerar Relatórios Completos                                         | PASS |
Obter Sumário de Issues                                            | PASS |
Imprimir Issues                                                    | PASS |
Imprimir Relatório de Qualidade                                    | PASS |
Contar Total de Issues                                             | PASS |
==============================================================================
6 tests, 6 passed, 0 failed in 0.42s
```

---

### **Opção 2: Com diretório de output customizado**

```bash
robot --outputdir ./results examples/quality_tests.robot
```

**Gera:**
- `results/output.xml` - Dados brutos
- `results/log.html` - Log detalhado
- `results/report.html` - Relatório visual

---

### **Opção 3: Modo verbose (mais detalhes)**

```bash
robot -v PYTHONPATH:src examples/quality_tests.robot
```

---

### **Opção 4: Executar teste específico**

```bash
# Apenas um teste
robot --test "Imprimir Relatório de Qualidade" examples/quality_tests.robot

# Múltiplos testes
robot --test "Imprimir*" examples/quality_tests.robot
```

---

### **Opção 5: Gerar relatórios em formato diferente**

```bash
# Com screenshots e detalhes
robot --outputdir ./results --log log.html --report report.html examples/quality_tests.robot

# Apenas output.xml (mais rápido)
robot --outputdir ./results --log NONE --report NONE examples/quality_tests.robot
```

---

## Criar seu próprio teste RF

Crie um arquivo `meus_testes.robot`:

```robot
*** Settings ***
Documentation    Meus testes de qualidade
Library          robotframework_quality_scanner.robot_library.QualityAnalysisLibrary

*** Test Cases ***

Validar Qualidade do Projeto
    [Documentation]    Verifica qualidade geral
    Scan Quality    ./tests/
    ${score}    Get Quality Score
    Log    Pontuação: ${score}/100
    Should Be Equal As Numbers    ${score}    80    delta=20

Não Deve Ter Issues Críticos
    [Documentation]    Garante que não há issues críticos
    Scan Quality    ./tests/
    Assert No Critical Issues

Analisar por Severidade
    [Documentation]    Filtra issues por severidade
    Scan Quality    ./tests/
    ${summary}    Get Issues Summary
    Log    HIGH severity: ${summary}[HIGH]
    Should Be Equal As Numbers    ${summary}[HIGH]    0

Analisar por Regra
    [Documentation]    Filtra por tipo de regra
    Scan Quality    ./tests/
    ${issues}    Get Issues By Rule    KEYWORD_NAMING_CONVENTION
    Log    Issues de naming: ${issues}
```

Execute com:
```bash
robot meus_testes.robot
```

---

## Opções Avançadas

### **Executar com tag específica**

```robot
*** Test Cases ***

Teste de Produção
    [Tags]    production
    Scan Quality    ./tests/

Teste de Desenvolvimento
    [Tags]    dev
    Scan Quality    ./tests/
```

Execute:
```bash
robot --include production examples/quality_tests.robot
robot --include dev examples/quality_tests.robot
robot --exclude dev examples/quality_tests.robot
```

---

### **Executar múltiplos arquivos**

```bash
robot tests/  # Executa todos os .robot em tests/
robot *.robot  # Executa todos os .robot no diretório
```

---

### **Modo paralelo (com PABOT)**

```bash
# Instalar
pip install robotframework-pabot

# Executar em paralelo
pabot --processes 4 examples/quality_tests.robot
```

---

## Keyword Reference Rápido

| Keyword | Descrição | Retorno |
|---------|-----------|---------|
| `Scan Quality` | Escaneia caminho | Número de issues |
| `Scan With Reports` | Escaneia + gera relatórios | [issues, reports_dict] |
| `Get Quality Score` | Pontuação 0-100 | Float |
| `Get Issues Summary` | Sumário por severidade | Dict |
| `Get Total Issues` | Total de issues | Int |
| `Get Issues By Severity` | Filtra por severidade | List |
| `Get Issues By Rule` | Filtra por regra | List |
| `Assert No Critical Issues` | Falha se houver crítico | - |
| `Assert No High Issues` | Falha se houver alto | - |
| `Assert Quality Score Above` | Valida pontuação mínima | - |
| `Print Issues` | Imprime tabela formatada | - |
| `Print Quality Report` | Imprime relatório completo | - |

---

## Exemplos Práticos

### **CI/CD Pipeline (GitHub Actions)**

```yaml
# .github/workflows/quality.yml
name: Quality Scan

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -e .
      - run: robot --outputdir ./results examples/quality_tests.robot
      - uses: actions/upload-artifact@v2
        if: always()
        with:
          name: Robot Results
          path: results/
```

---

### **Validação em Pre-commit**

```bash
# Criar arquivo .robot com validação
#!/bin/bash
robot --outputdir /tmp --log NONE --report NONE tests/quality_validation.robot
exit $?
```

---

## Troubleshooting

### **Erro: "Library not found"**
```bash
# Solução 1: Instalar em desenvolvimento
pip install -e .

# Solução 2: Adicionar ao PYTHONPATH
PYTHONPATH=src robot examples/quality_tests.robot
```

### **Erro: "Keyword not found"**
```bash
# Verificar se a biblioteca está instalada
python -c "from robotframework_quality_scanner.robot_library import QualityAnalysisLibrary; print('OK')"

# Reinstalar se necessário
pip install --force-reinstall -e .
```

### **Output lento**
```bash
# Desabilitar log HTML (mais rápido)
robot --log NONE examples/quality_tests.robot
```

---

## Comandos Úteis

```bash
# Ver ajuda do robot
robot --help

# Listar testes sem executar
robot --dryrun examples/quality_tests.robot

# Executar com timeout
robot --timeout 30 examples/quality_tests.robot

# Ver logs em tempo real
robot --loglevel DEBUG examples/quality_tests.robot

# Apenas sumário final
robot --log NONE --report NONE examples/quality_tests.robot
```

---

## Integração com Scripts

```python
# run_tests.py
import subprocess
import sys

result = subprocess.run(
    ["robot", "--outputdir", "./results", "examples/quality_tests.robot"],
    capture_output=True,
    text=True
)

print(result.stdout)
if result.returncode != 0:
    print("❌ Testes falharam!")
    sys.exit(1)
else:
    print("✅ Todos os testes passaram!")
```

Execute com:
```bash
python run_tests.py
```

---

## Próximos Passos

1. **Customizar tests para seu projeto**
2. **Integrar em CI/CD**
3. **Criar templates reutilizáveis**
4. **Configurar alertas de qualidade**

Para mais informações: https://robotframework.org/
