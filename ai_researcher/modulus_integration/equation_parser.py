
import re
from typing import List, Dict, Any

class EquationParser:
    """
    Parses LaTeX strings to find and extract differential equations.
    """

    def __init__(self, latex_content: str):
        self.latex_content = latex_content
        self.patterns = {
            'pde': r"\\frac{{\\partial(.+?)}}{{.+?}}",
            'ode': r"\\frac{{d(.+?)}}{{d(.+?)}}",
        }

    def parse(self) -> Dict[str, List[str]]:
        """
        Parses the LaTeX content and extracts all found equations.
        """
        found_equations = {'pdes': [], 'odes': []}

        # Find PDEs
        pde_matches = re.findall(self.patterns['pde'], self.latex_content)
        for match in pde_matches:
            found_equations['pdes'].append(f"\\frac{{\\partial{match[0]}}}{{\\partial{match[1]}}}")

        # Find ODES
        ode_matches = re.findall(self.patterns['ode'], self.latex_content)
        for match in ode_matches:
            found_equations['odes'].append(f"\\frac{{d{match[0]}}}{{d{match[1]}}}")
            
        return found_equations

if __name__ == '__main__':
    # Example Usage
    sample_latex = """
    The core of the model is the following partial differential equation:
    $\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$

    We also have an ordinary differential equation:
    $\frac{dy}{dx} = -ky$
    """
    parser = EquationParser(sample_latex)
    equations = parser.parse()
    print(f"Found PDEs: {equations['pdes']}")
    print(f"Found ODEs: {equations['odes']}")
