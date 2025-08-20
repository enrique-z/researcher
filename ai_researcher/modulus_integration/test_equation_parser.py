
import unittest
from .equation_parser import EquationParser

class TestEquationParser(unittest.TestCase):

    def test_parse_pde(self):
        latex = "$\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}$"
        parser = EquationParser(latex)
        equations = parser.parse()
        self.assertEqual(len(equations['pdes']), 2)
        self.assertIn("\\frac{\\partial u}{\\partial t}", equations['pdes'])
        self.assertIn("\\frac{\\partial^2 u}{\\partial x^2}", equations['pdes'])

    def test_parse_ode(self):
        latex = "$\frac{dy}{dx} = -ky$"
        parser = EquationParser(latex)
        equations = parser.parse()
        self.assertEqual(len(equations['odes']), 1)
        self.assertEqual(equations['odes'][0], "\\frac{dy}{dx}")

if __name__ == '__main__':
    unittest.main()
