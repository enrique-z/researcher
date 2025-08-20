
from abc import ABC, abstractmethod
from typing import Dict, Any

class ModulusSolverTemplate(ABC):
    """
    Abstract base class for Modulus solver templates.
    """

    @abstractmethod
    def define_physical_constraints(self) -> Dict[str, Any]:
        """
        Define the physical constraints for the simulation.
        This can include boundary conditions, material properties, noise models, etc.

        Returns:
            Dict[str, Any]: A dictionary of physical constraints.
        """
        pass

    @abstractmethod
    def solve(self, equations: Dict[str, Any], constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve the given equations using a specific Modulus configuration.

        Args:
            equations (Dict[str, Any]): A dictionary of equations parsed from the paper.
            constraints (Dict[str, Any]): A dictionary of physical constraints for the simulation.

        Returns:
            Dict[str, Any]: A dictionary containing the simulation results.
        """
        pass
