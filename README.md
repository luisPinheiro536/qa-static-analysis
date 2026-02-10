# robotframework-quality-scanner

Uma **Robot Framework Library** para escanear projetos de automação **Web, Mobile e API**, identificar **más práticas**, gerar **logs estruturados**, **relatórios** e **sugestões de correção baseadas em boas práticas oficiais**.

**Versão**: 0.3.0  
**Status**: Beta com suporte para caching, histórico, 4 analisadores especializados, API REST e logging estruturado com documentação automática.

---

## 🎯 Objetivo

* Analisar arquivos `.robot` e `.resource`
* Detectar anti-patterns comuns em automação
* Classificar problemas por severidade (CRITICAL, HIGH, MEDIUM, LOW)
* Explicar impacto técnico e sugerir soluções
* **Cache 10x mais rápido** para análises repetidas
* Rastrear **histórico e tendências** de qualidade
* Gerar **múltiplos relatórios** (JSON, HTML, TXT)
* **Capturar logs, erros e traces** estruturados em documentação automática
* Integrar facilmente com **CI/CD e ferramentas externas** via API REST

---

## 📦 Instalação

```bash
pip install robotframework-quality-scanner
```

---


## ✨ Features v0.3.0

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

5. **Relatórios Executivos e de Cobertura** (v0.3.0)
   - Score de qualidade (0-100)
   - Distribuição por severidade e categoria
   - Cobertura de testes
   - Formatos: Text, JSON, HTML

6. **Logging Estruturado com Documentação** (v0.3.0)
   - Captura automática de erros e traces
   - Relatórios em Markdown com formatação
   - Exportação em JSON para análise programática
   - Pasta `.docs/` para armazenar documentação
   - Histórico de todas as execuções

7. **API REST**
   - Endpoints para análise de arquivo/diretório
   - Geração de relatórios (JSON, HTML, TXT)
   - Health check e sumário

6. **Relatórios Múltiplos**
   - Console (estruturado)
   - JSON (programável)
   - HTML (visual)
   - TXT (simples)

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

