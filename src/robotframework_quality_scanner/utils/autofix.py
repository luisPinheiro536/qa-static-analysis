class AutoFixer:
    """Auto-corrigi problemas comuns em arquivos Robot."""

    @staticmethod
    def fix_file(filepath):
        """Aplica todas as correções disponíveis."""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        fixes_applied = []

        # Fix 1: Remove trailing whitespace
        lines = content.split('\n')
        lines = [l.rstrip() for l in lines]
        content = '\n'.join(lines)
        if content != original:
            fixes_applied.append("trailing_whitespace_removed")
            original = content

        # Fix 2: Normaliza indentação (tabs → 4 spaces)
        content = content.replace('\t', '    ')
        if content != original:
            fixes_applied.append("indentation_normalized")
            original = content

        # Fix 3: Adiciona [Documentation] vazio em keywords sem doc
        if '*** Keywords ***' in content:
            kw_section = content.split('*** Keywords ***')[1]
            if 'Log' in kw_section and '[Documentation]' not in kw_section:
                content = content.replace('Log', '[Documentation]\nLog', 1)
                fixes_applied.append("documentation_added")

        # Fix 4: Capitaliza keywords comuns
        keywords_to_capitalize = [
            'log', 'sleep', 'open browser', 'close browser',
            'click element', 'input text', 'wait until'
        ]
        for kw in keywords_to_capitalize:
            if kw.lower() in content.lower():
                import re
                pattern = re.compile(re.escape(kw), re.IGNORECASE)
                content = pattern.sub(kw.title(), content)
                fixes_applied.append(f"capitalized_{kw}")

        # Salva mudanças
        if fixes_applied:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

        return fixes_applied
