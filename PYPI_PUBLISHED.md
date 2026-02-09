# 🎉 Publicado no PyPI!

## `robotframework-quality-scanner` v0.3.0

Seu pacote foi publicado com sucesso no PyPI e está disponível para instalação mundial!

### 📦 Instalação Rápida

```bash
pip install robotframework-quality-scanner
```

### 🚀 Uso Imediato

```python
from robotframework_quality_scanner import QualityScanner

scanner = QualityScanner()
issues, reports = scanner.scan("./tests/")

# Exibir relatório
print(reports['executive'].to_text())

# Salvar relatórios
scanner.save_reports("./quality-reports")
```

### 📊 Links Importantes

- **PyPI Package**: https://pypi.org/project/robotframework-quality-scanner/0.3.0/
- **GitHub Repository**: https://github.com/luisPinheiro536/qa-static-analysis
- **GitHub Releases**: https://github.com/luisPinheiro536/qa-static-analysis/releases/tag/v0.3.0

### 📋 Versões Suportadas

- Python 3.8+
- Robot Framework 6.0+

### ✨ Principais Features

✅ Análise estática de qualidade  
✅ 4 analisadores especializados (Performance, Duplication, Dependency, TestData)  
✅ Cache de análises (10x mais rápido)  
✅ Histórico com detecção de tendências  
✅ Auto-fix automático  
✅ API REST  
✅ **Relatórios executivos e de cobertura (v0.3.0)**  

### 🔧 Instalação com Features Adicionais

```bash
# Com suporte a API REST
pip install robotframework-quality-scanner[api]

# Desenvolvimento completo
pip install robotframework-quality-scanner[all]
```

### 📝 Documentação

Veja o [README.md](https://github.com/luisPinheiro536/qa-static-analysis/blob/main/README.md) completo para:
- Exemplos de uso
- Documentação dos analisadores
- Integração com CI/CD
- Contribuição

### 🐛 Issues e Feedback

Encontrou um problema? Abra uma issue em:
https://github.com/luisPinheiro536/qa-static-analysis/issues

---

**Lançado em:** 9 de fevereiro de 2026  
**Versão:** 0.3.0  
**Status:** ✅ Publicado e disponível mundialmente
