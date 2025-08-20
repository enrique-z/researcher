#!/usr/bin/env python3
"""
Test Cambridge SAI Analysis Execution

This script tests the complete URSA universal experimental framework
by executing the Cambridge professor's SAI pulse vs continuous analysis.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ai_researcher.ursa_integration.cambridge_sai_executor import CambridgeSAIExecutor, execute_cambridge_sai_analysis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Test Cambridge SAI analysis execution."""
    logger.info("🎯 Testing Cambridge SAI Analysis Execution")
    logger.info("=" * 60)
    
    try:
        # Test quick summary first
        from ai_researcher.ursa_integration.cambridge_sai_executor import get_cambridge_quick_summary
        summary = get_cambridge_quick_summary()
        
        logger.info("📋 Cambridge Analysis Capability Summary:")
        for key, value in summary.items():
            logger.info(f"  {key}: {value}")
        
        logger.info("\n🚀 Executing Cambridge SAI Analysis...")
        
        # Execute the complete analysis
        results = execute_cambridge_sai_analysis()
        
        logger.info("\n📊 Execution Results:")
        logger.info(f"  Execution successful: {results.get('execution_successful', False)}")
        logger.info(f"  Cambridge paper ready: {results.get('cambridge_paper_ready', False)}")
        
        if results.get('pulse_analysis'):
            pulse_success = results['pulse_analysis'].get('execution_successful', False)
            logger.info(f"  Pulse analysis: {'✅ SUCCESS' if pulse_success else '❌ FAILED'}")
        
        if results.get('continuous_analysis'):
            continuous_success = results['continuous_analysis'].get('execution_successful', False)
            logger.info(f"  Continuous analysis: {'✅ SUCCESS' if continuous_success else '❌ FAILED'}")
        
        if results.get('comparison_analysis'):
            comparison = results['comparison_analysis']
            logger.info(f"  Comparison generated: {'✅ YES' if comparison else '❌ NO'}")
            if comparison and 'cambridge_conclusions' in comparison:
                logger.info("  Cambridge conclusions:")
                for conclusion in comparison['cambridge_conclusions'][:2]:  # Show first 2
                    logger.info(f"    - {conclusion}")
        
        # Test system status
        logger.info("\n🔧 System Status:")
        executor = CambridgeSAIExecutor()
        status = executor.engine.get_system_status()
        logger.info(f"  Engine active: {status['engine_active']}")
        logger.info(f"  URSA available: {status['ursa_available']}")
        logger.info(f"  Research domain: {status['research_domain']}")
        logger.info(f"  Components status: {status['components_status']}")
        
        logger.info("\n✅ Cambridge SAI Analysis Test Complete!")
        
        if results.get('cambridge_paper_ready'):
            logger.info("🎉 READY FOR PAPER GENERATION!")
            logger.info("Next steps: Generate 128-page academic paper using universal paper generation system")
        else:
            logger.info("⚠️ Some issues detected - review logs above")
            
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)