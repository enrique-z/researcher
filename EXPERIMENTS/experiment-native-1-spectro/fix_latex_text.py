#!/usr/bin/env python3
"""
LaTeX Text Intelligibility Fixer

This script analyzes LaTeX documents and automatically fixes unintelligible text
caused by mathematical symbols that aren't properly formatted in math mode.

The main issue occurs when mathematical symbols like \beta, \Delta, \Omega, etc.
are used in text mode without proper delimiters ($...$), causing text concatenation
during PDF rendering.

Usage:
    python fix_latex_text.py input.tex [output.tex]
    
If no output file is specified, creates input_fixed.tex
"""

import re
import sys
import os
from pathlib import Path
from typing import List, Tuple, Dict


class LatexTextFixer:
    def __init__(self):
        # Common mathematical symbols that need math mode
        self.math_symbols = [
            # Greek letters
            r'\\alpha', r'\\beta', r'\\gamma', r'\\delta', r'\\Delta',
            r'\\epsilon', r'\\varepsilon', r'\\zeta', r'\\eta', r'\\theta',
            r'\\Theta', r'\\iota', r'\\kappa', r'\\lambda', r'\\Lambda',
            r'\\mu', r'\\nu', r'\\xi', r'\\Xi', r'\\pi', r'\\Pi',
            r'\\rho', r'\\varrho', r'\\sigma', r'\\Sigma', r'\\tau',
            r'\\upsilon', r'\\Upsilon', r'\\phi', r'\\Phi', r'\\varphi',
            r'\\chi', r'\\psi', r'\\Psi', r'\\omega', r'\\Omega',
            
            # Mathematical operators and symbols
            r'\\infty', r'\\partial', r'\\nabla', r'\\sum', r'\\prod',
            r'\\int', r'\\oint', r'\\lim', r'\\max', r'\\min', r'\\sup',
            r'\\inf', r'\\arg', r'\\det', r'\\exp', r'\\log', r'\\ln',
            r'\\sin', r'\\cos', r'\\tan', r'\\sec', r'\\csc', r'\\cot',
            r'\\sinh', r'\\cosh', r'\\tanh', r'\\arcsin', r'\\arccos',
            r'\\arctan', r'\\sqrt', r'\\pm', r'\\mp', r'\\times',
            r'\\div', r'\\cdot', r'\\ast', r'\\star', r'\\circ',
            
            # Sets and logic
            r'\\in', r'\\notin', r'\\ni', r'\\subset', r'\\subseteq',
            r'\\supset', r'\\supseteq', r'\\cup', r'\\cap', r'\\setminus',
            r'\\emptyset', r'\\varnothing', r'\\forall', r'\\exists',
            r'\\nexists', r'\\land', r'\\lor', r'\\neg', r'\\implies',
            r'\\iff', r'\\equiv', r'\\approx', r'\\sim', r'\\simeq',
            r'\\cong', r'\\propto', r'\\neq', r'\\leq', r'\\geq',
            r'\\ll', r'\\gg', r'\\prec', r'\\succ', r'\\preceq',
            r'\\succeq',
            
            # Arrows
            r'\\to', r'\\rightarrow', r'\\leftarrow', r'\\leftrightarrow',
            r'\\Rightarrow', r'\\Leftarrow', r'\\Leftrightarrow',
            r'\\mapsto', r'\\longmapsto', r'\\longrightarrow',
            r'\\longleftarrow', r'\\longleftrightarrow',
            
            # Fonts and styles in math
            r'\\mathcal', r'\\mathbb', r'\\mathbf', r'\\mathit',
            r'\\mathsf', r'\\mathtt', r'\\mathrm', r'\\text'
        ]
        
        # Patterns for subscripts and superscripts
        self.subscript_pattern = r'_\{[^}]+\}'
        self.superscript_pattern = r'\^\{[^}]+\}'
        
        # Pattern to match already math-mode content
        self.math_mode_patterns = [
            r'\$[^$]*\$',  # Inline math $...$
            r'\$\$[^$]*\$\$',  # Display math $$...$$
            r'\\begin\{equation\}.*?\\end\{equation\}',  # equation environment
            r'\\begin\{align\}.*?\\end\{align\}',  # align environment
            r'\\begin\{align\*\}.*?\\end\{align\*\}',  # align* environment
            r'\\begin\{eqnarray\}.*?\\end\{eqnarray\}',  # eqnarray environment
            r'\\begin\{gather\}.*?\\end\{gather\}',  # gather environment
            r'\\begin\{multline\}.*?\\end\{multline\}',  # multline environment
            r'\\begin\{split\}.*?\\end\{split\}',  # split environment
            r'\\\[.*?\\\]',  # Display math \[...\]
            r'\\\(.*?\\\)',  # Inline math \(...\)
        ]
        
    def is_in_math_mode(self, text: str, position: int) -> bool:
        """Check if a position in text is already inside math mode"""
        for pattern in self.math_mode_patterns:
            for match in re.finditer(pattern, text, re.DOTALL):
                if match.start() <= position <= match.end():
                    return True
        return False
    
    def is_in_command_definition(self, text: str, position: int) -> bool:
        """Check if position is inside a command definition like \newcommand"""
        # Look backwards for \newcommand, \renewcommand, \def, etc.
        before_text = text[:position]
        command_patterns = [r'\\newcommand', r'\\renewcommand', r'\\def', r'\\providecommand']
        
        for pattern in command_patterns:
            matches = list(re.finditer(pattern, before_text))
            if matches:
                last_match = matches[-1]
                # Simple heuristic: if we're within 100 characters of a command definition
                if position - last_match.end() < 100:
                    return True
        return False
    
    def find_math_symbols_needing_fix(self, text: str) -> List[Tuple[int, int, str]]:
        """Find all mathematical symbols that need to be wrapped in math mode"""
        issues = []
        
        # Focus on the most common problematic patterns first
        priority_patterns = [
            # Greek letters that commonly cause issues
            r'\\beta(?![a-zA-Z])', r'\\alpha(?![a-zA-Z])', r'\\gamma(?![a-zA-Z])', 
            r'\\delta(?![a-zA-Z])', r'\\Delta(?![a-zA-Z])', r'\\omega(?![a-zA-Z])', 
            r'\\Omega(?![a-zA-Z])', r'\\phi(?![a-zA-Z])', r'\\Phi(?![a-zA-Z])',
            
            # Variables with subscripts that commonly cause concatenation
            r'[A-Za-z]_{[^}]+}(?:\^{[^}]+})?',
            r'[A-Za-z]\^{[^}]+}(?:_{[^}]+})?',
            
            # Mathematical operators in text
            r'\\in(?![a-zA-Z])', r'\\subset(?![a-zA-Z])', r'\\mathcal\{[^}]+\}',
            r'\\mathrm\{[^}]+\}', r'\\text\{[^}]+\}',
        ]
        
        # Find all potential mathematical content with priority patterns
        for pattern in priority_patterns:
            for match in re.finditer(pattern, text):
                start, end = match.span()
                matched_text = match.group()
                
                # Skip if already in math mode
                if self.is_in_math_mode(text, start):
                    continue
                
                # Skip if in command definition
                if self.is_in_command_definition(text, start):
                    continue
                
                # Skip if it's just regular text (heuristic checks)
                if self.is_regular_text(matched_text):
                    continue
                
                issues.append((start, end, matched_text))
        
        # Remove overlapping matches (keep the longest ones)
        issues = self.remove_overlapping_matches(issues)
        
        return issues
    
    def is_regular_text(self, text: str) -> bool:
        """Heuristic to determine if text is regular English rather than math"""
        # If it's just a single letter without any LaTeX commands, likely regular text
        if re.match(r'^[a-zA-Z]$', text):
            return True
        
        # If it contains common English words, likely regular text
        english_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        if any(word in text.lower() for word in english_words):
            return True
        
        return False
    
    def remove_overlapping_matches(self, matches: List[Tuple[int, int, str]]) -> List[Tuple[int, int, str]]:
        """Remove overlapping matches, keeping the longest ones"""
        if not matches:
            return matches
        
        # Sort by start position
        matches.sort(key=lambda x: x[0])
        
        result = []
        for start, end, text in matches:
            # Check if this match overlaps with the last one in result
            if result and start < result[-1][1]:
                # Overlapping - keep the longer match
                if end - start > result[-1][1] - result[-1][0]:
                    result[-1] = (start, end, text)
            else:
                result.append((start, end, text))
        
        return result
    
    def fix_latex_text(self, text: str) -> Tuple[str, List[str]]:
        """Fix mathematical symbols in LaTeX text by adding proper math mode delimiters"""
        issues_found = self.find_math_symbols_needing_fix(text)
        
        if not issues_found:
            return text, []
        
        # Sort issues by position (reverse order to maintain positions during replacement)
        issues_found.sort(key=lambda x: x[0], reverse=True)
        
        fixes_applied = []
        fixed_text = text
        
        for start, end, matched_text in issues_found:
            # Extract the mathematical expression
            math_expr = fixed_text[start:end]
            
            # Wrap in math mode delimiters
            fixed_expr = f'${math_expr}$'
            
            # Replace in text
            fixed_text = fixed_text[:start] + fixed_expr + fixed_text[end:]
            
            # Record the fix
            line_num = fixed_text[:start].count('\n') + 1
            fixes_applied.append(f"Line {line_num}: '{math_expr}' → '{fixed_expr}'")
        
        return fixed_text, fixes_applied
    
    def analyze_file(self, input_file: str) -> Dict:
        """Analyze a LaTeX file and return statistics about issues found"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(input_file, 'r', encoding='latin-1') as f:
                content = f.read()
        
        issues = self.find_math_symbols_needing_fix(content)
        
        # Group issues by type
        issue_types = {}
        for start, end, text in issues:
            if text not in issue_types:
                issue_types[text] = 0
            issue_types[text] += 1
        
        return {
            'total_issues': len(issues),
            'unique_issues': len(issue_types),
            'issue_breakdown': issue_types,
            'file_size': len(content),
            'line_count': content.count('\n') + 1
        }
    
    def fix_file(self, input_file: str, output_file: str = None) -> bool:
        """Fix a LaTeX file and save the result"""
        if output_file is None:
            base = os.path.splitext(input_file)[0]
            output_file = f"{base}_fixed.tex"
        
        try:
            # Read input file
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(input_file, 'r', encoding='latin-1') as f:
                    content = f.read()
            
            # Fix the content
            fixed_content, fixes = self.fix_latex_text(content)
            
            # Write output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            # Report results
            print(f"✅ Fixed {len(fixes)} mathematical formatting issues")
            print(f"📁 Input:  {input_file}")
            print(f"📁 Output: {output_file}")
            
            if fixes:
                print("\n🔧 Fixes applied:")
                for fix in fixes[:10]:  # Show first 10 fixes
                    print(f"  {fix}")
                
                if len(fixes) > 10:
                    print(f"  ... and {len(fixes) - 10} more fixes")
            
            return True
            
        except Exception as e:
            print(f"❌ Error processing file: {e}")
            return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_latex_text.py input.tex [output.tex]")
        print("\nThis script fixes unintelligible text in LaTeX documents by properly")
        print("formatting mathematical symbols with math mode delimiters ($...$)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    
    fixer = LatexTextFixer()
    
    # First, analyze the file
    print("🔍 Analyzing LaTeX file...")
    analysis = fixer.analyze_file(input_file)
    
    print(f"\n📊 Analysis Results:")
    print(f"  File size: {analysis['file_size']:,} characters")
    print(f"  Lines: {analysis['line_count']:,}")
    print(f"  Math formatting issues found: {analysis['total_issues']}")
    print(f"  Unique issue types: {analysis['unique_issues']}")
    
    if analysis['total_issues'] == 0:
        print("✅ No mathematical formatting issues found!")
        return
    
    print(f"\n🔍 Most common issues:")
    for issue, count in sorted(analysis['issue_breakdown'].items(), 
                              key=lambda x: x[1], reverse=True)[:5]:
        print(f"  '{issue}' appears {count} times")
    
    # Auto-fix if issues found
    if analysis['total_issues'] > 0:
        print(f"\n🔧 Auto-fixing {analysis['total_issues']} issues...")
    
    # Fix the file
    print("\n🔧 Fixing mathematical formatting...")
    success = fixer.fix_file(input_file, output_file)
    
    if success:
        print("\n✅ LaTeX file successfully fixed!")
        print("💡 You can now compile the fixed file with xelatex or pdflatex")
    else:
        print("\n❌ Failed to fix LaTeX file")
        sys.exit(1)


if __name__ == "__main__":
    main()