
import unittest
import json
from pathlib import Path
from execute_qbo_sai_experiment import UniversalExperimentPipeline
from ai_researcher.modulus_integration.integration_bridge import IntegrationBridge
from ai_researcher.modulus_integration.navier_stokes_solver import NavierStokesSolver

class TestModulusDataFlow(unittest.TestCase):

    def setUp(self):
        self.experiment_name = "test_modulus_flow"
        self.pipeline = UniversalExperimentPipeline(experiment_name=self.experiment_name)
        self.pipeline.execute_phase_1_preparation() # Setup directory

    def test_simulation_data_flow(self):
        # 1. Create dummy paper content
        paper_content = "A paper with a navier-stokes equation: $\\frac{{\\partial u}}{{\\partial t}} + (u \\cdot \\nabla) u = -\\frac{1}{\\rho} \\nabla p + \\nu \\nabla^2 u$"
        
        # 2. Run the modulus simulation phase
        results = self.pipeline.execute_phase_2_8_modulus_simulation(paper_content)

        # 3. Check that the results were generated and saved
        self.assertEqual(results['status'], 'completed')
        self.assertIn('simulation_results', results)
        self.assertEqual(results['simulation_results']['simulation_status'], 'completed')

        # 4. Verify file output
        phase_file = self.pipeline.base_dir / "phase_2_8_modulus_simulation.json"
        self.assertTrue(phase_file.exists())

        with open(phase_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['phase'], 'modulus_simulation')
            self.assertEqual(data['status'], 'completed')
            self.assertEqual(data['simulation_results']['visualization_file'], '/path/to/navier_stokes.vtu')

    def tearDown(self):
        import shutil
        shutil.rmtree(self.pipeline.base_dir)

if __name__ == '__main__':
    unittest.main()
