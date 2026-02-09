def print_issues(issues):
    for iss in issues:
        d = iss.to_dict()
        print(f"[{d['severity']}] {d['rule_id']} - {d['file']}:{d['line']}")
        print(d['description'])
        print("Recommendation:", d['recommendation'])
        print()
