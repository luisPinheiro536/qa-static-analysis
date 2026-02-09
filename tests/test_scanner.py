from robotframework_quality_scanner.scanner import QualityScanner


def test_scan_example(tmp_path):
    p = tmp_path / "example.robot"
    p.write_text("""*** Test Cases ***\nTC\n    Sleep    1s\n""")
    scanner = QualityScanner()
    issues = scanner.scan(str(p))
    assert any(i.rule_id == 'WEB001' for i in issues)
