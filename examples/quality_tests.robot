*** Settings ***
Documentation    Exemplo de testes usando robotframework-quality-scanner
Library          robotframework_quality_scanner.robot_library.QualityAnalysisLibrary

*** Test Cases ***

Escanear Arquivo e Validar Issues
    [Documentation]    Escaneia um arquivo e valida o número de issues
    ${issues}    Scan Quality    examples/bad_web.robot
    Log    Encontrados ${issues} issues
    Should Be Equal As Numbers    ${issues}    14

Gerar Relatórios Completos
    [Documentation]    Escaneia com geração de relatórios
    ${result}    Scan With Reports    examples/bad_web.robot
    Log    Relatórios gerados com sucesso
    Log    ${result}

Obter Sumário de Issues
    [Documentation]    Obtém sumário estruturado
    Scan Quality    examples/bad_web.robot
    ${summary}    Get Issues Summary
    Log    ${summary}
    Log    CRITICAL: ${summary}[CRITICAL]
    Log    HIGH: ${summary}[HIGH]
    Log    MEDIUM: ${summary}[MEDIUM]
    Log    LOW: ${summary}[LOW]
    Log    TOTAL: ${summary}[total]

Imprimir Issues
    [Documentation]    Imprime todos os issues no formato legível
    Scan Quality    examples/bad_web.robot
    Print Issues

Imprimir Relatório de Qualidade
    [Documentation]    Imprime relatório executivo
    Scan With Reports    examples/bad_web.robot
    Print Quality Report

Contar Total de Issues
    [Documentation]    Conta total de issues
    Scan Quality    examples/bad_web.robot
    ${total}    Get Total Issues
    Log    Total de issues: ${total}
    Should Be Equal As Numbers    ${total}    14
