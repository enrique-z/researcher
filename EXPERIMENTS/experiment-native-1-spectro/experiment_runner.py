#!/usr/bin/env python3
"""
Long-Duration AI Research Paper Generation Experiment Runner
experiment-native-1-spectro: SAI Active Spectroscopy Framework

This script runs a comprehensive 4-5 hour experiment to generate high-quality
research papers on Stratospheric Aerosol Injection using active spectroscopy.
"""

import json
import time
import logging
import psutil
import os
import gc
from datetime import datetime, timedelta
from typing import List, Dict, Any
import traceback

# Import AI Researcher components
from ai_researcher import CycleResearcher, CycleReviewer, DeepReviewer, AIDetector
from ai_researcher.utils import print_paper_summary

class ExperimentRunner:
    """Manages long-duration AI research paper generation experiment"""
    
    def __init__(self, experiment_dir: str = "."):
        self.experiment_dir = experiment_dir
        self.start_time = datetime.now()
        self.experiment_id = f"native-1-spectro-{self.start_time.strftime('%Y%m%d_%H%M%S')}"
        
        # Load experiment configuration
        with open(os.path.join(experiment_dir, 'input/experiment_config.json'), 'r') as f:
            self.config = json.load(f)
            
        # Load research data
        with open(os.path.join(experiment_dir, 'input/research_topic_formatted.txt'), 'r') as f:
            self.research_topic = f.read().strip()
            
        with open(os.path.join(experiment_dir, 'input/references.bib'), 'r') as f:
            self.bibtex_references = f.read().strip()
        
        # Initialize tracking
        self.checkpoints = []
        self.generated_papers = []
        self.review_results = []
        self.performance_metrics = []
        
        # Setup logging
        self.setup_logging()
        
        # Initialize models (will be loaded lazily)
        self.researcher = None
        self.reviewer = None
        self.deep_reviewer = None
        self.detector = None
        
    def setup_logging(self):
        """Configure comprehensive logging"""
        log_filename = f"logs/experiment_{self.experiment_id}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("ExperimentRunner")
        self.logger.info(f"🚀 Starting experiment: {self.experiment_id}")
        self.logger.info(f"📊 Target: {self.config['target_papers']} papers in {self.config['expected_duration_hours']} hours")
    
    def save_checkpoint(self, stage: str, data: Dict[str, Any]):
        """Save experiment checkpoint"""
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'elapsed_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
            'stage': stage,
            'data': data,
            'memory_usage_mb': psutil.Process().memory_info().rss / 1024 / 1024,
            'papers_generated': len(self.generated_papers),
            'reviews_completed': len(self.review_results)
        }
        
        self.checkpoints.append(checkpoint)
        
        # Save to file
        checkpoint_file = f"checkpoints/checkpoint_{len(self.checkpoints):03d}_{stage}.json"
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)
            
        self.logger.info(f"📁 Checkpoint saved: {stage} - {checkpoint['elapsed_hours']:.2f}h elapsed")
        
    def load_models_lazy(self):
        """Load AI models lazily to optimize memory"""
        if self.researcher is None:
            self.logger.info("🔄 Loading CycleResearcher (12B model)...")
            self.researcher = CycleResearcher(
                custom_model_name="/Users/apple/code/Researcher/westlake-12b",
                model_size="12B",
                device="cpu",
                max_model_len=8192,
                gpu_memory_utilization=0.95
            )
            self.logger.info("✅ CycleResearcher loaded successfully")
            
    def stage1_initial_generation(self) -> List[Dict[str, Any]]:
        """Stage 1: Initial Paper Generation (60 minutes)"""
        self.logger.info("🎯 Starting Stage 1: Initial Paper Generation")
        stage_start = datetime.now()
        
        # Load researcher model
        self.load_models_lazy()
        
        # Generate initial batch of papers
        self.logger.info("📝 Generating initial paper batch...")
        papers = self.researcher.generate_paper(
            topic=self.research_topic,
            references=self.bibtex_references,
            n=self.config['target_papers']
        )
        
        # Process and save papers
        for i, paper in enumerate(papers):
            paper['stage'] = 'initial_generation'
            paper['paper_id'] = f"{self.experiment_id}_initial_{i+1}"
            paper['generation_timestamp'] = datetime.now().isoformat()
            
            # Save individual paper
            paper_file = f"output/{paper['paper_id']}.json"
            with open(paper_file, 'w') as f:
                json.dump(paper, f, indent=2)
        
        self.generated_papers.extend(papers)
        
        stage_duration = (datetime.now() - stage_start).total_seconds() / 60
        self.logger.info(f"✅ Stage 1 completed in {stage_duration:.1f} minutes")
        
        # Save checkpoint
        self.save_checkpoint("stage1_complete", {
            'papers_generated': len(papers),
            'stage_duration_minutes': stage_duration,
            'average_paper_length': sum(len(p.get('generated_text', '')) for p in papers) / len(papers)
        })
        
        return papers
    
    def stage2_iterative_refinement(self, initial_papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Stage 2: Iterative Refinement with CycleReviewer (90 minutes)"""
        self.logger.info("🔄 Starting Stage 2: Iterative Refinement")
        stage_start = datetime.now()
        
        # Load reviewer if not already loaded
        if self.reviewer is None:
            self.logger.info("🔄 Loading CycleReviewer...")
            self.reviewer = CycleReviewer(model_size="8B")
            self.logger.info("✅ CycleReviewer loaded successfully")
        
        reviewed_papers = []
        
        for i, paper in enumerate(initial_papers):
            self.logger.info(f"📊 Reviewing paper {i+1}/{len(initial_papers)}")
            
            # Get paper text for review
            paper_text = paper.get('generated_text', paper.get('latex', ''))
            
            if paper_text:
                try:
                    # Review the paper
                    review_result = self.reviewer.evaluate(paper_text)
                    
                    # Store review results
                    paper['review_results'] = review_result
                    paper['avg_rating'] = review_result[0].get('avg_rating', 0) if review_result else 0
                    
                    # Log review score
                    self.logger.info(f"📈 Paper {i+1} score: {paper['avg_rating']:.2f}")
                    
                    reviewed_papers.append(paper)
                    self.review_results.extend(review_result)
                    
                except Exception as e:
                    self.logger.error(f"❌ Error reviewing paper {i+1}: {str(e)}")
                    paper['review_error'] = str(e)
                    reviewed_papers.append(paper)
            
            # Memory cleanup every few papers
            if i % 2 == 0:
                gc.collect()
        
        # Identify best papers for refinement
        best_papers = sorted(reviewed_papers, key=lambda x: x.get('avg_rating', 0), reverse=True)[:3]
        
        # Generate refined versions of top papers
        refined_papers = []
        for i, paper in enumerate(best_papers):
            try:
                self.logger.info(f"🔧 Refining paper {i+1} (score: {paper.get('avg_rating', 0):.2f})")
                
                # Create enhanced prompt with review feedback
                enhanced_topic = f"{self.research_topic}\n\nINCORPORATE THESE IMPROVEMENTS:\n"
                if paper.get('review_results'):
                    for result in paper['review_results']:
                        if 'summary' in result:
                            enhanced_topic += f"- {result['summary'][:200]}...\n"
                
                # Generate refined paper
                refined = self.researcher.generate_paper(
                    topic=enhanced_topic,
                    references=self.bibtex_references,
                    n=1
                )
                
                if refined:
                    refined_paper = refined[0]
                    refined_paper['stage'] = 'refined'
                    refined_paper['paper_id'] = f"{self.experiment_id}_refined_{i+1}"
                    refined_paper['original_paper_id'] = paper['paper_id']
                    refined_paper['generation_timestamp'] = datetime.now().isoformat()
                    
                    refined_papers.append(refined_paper)
                    
                    # Save refined paper
                    paper_file = f"output/{refined_paper['paper_id']}.json"
                    with open(paper_file, 'w') as f:
                        json.dump(refined_paper, f, indent=2)
                        
                    self.logger.info(f"✅ Refined paper {i+1} generated successfully")
                
            except Exception as e:
                self.logger.error(f"❌ Error refining paper {i+1}: {str(e)}")
        
        self.generated_papers.extend(refined_papers)
        
        stage_duration = (datetime.now() - stage_start).total_seconds() / 60
        self.logger.info(f"✅ Stage 2 completed in {stage_duration:.1f} minutes")
        
        # Save checkpoint
        self.save_checkpoint("stage2_complete", {
            'papers_reviewed': len(reviewed_papers),
            'papers_refined': len(refined_papers),
            'average_score': sum(p.get('avg_rating', 0) for p in reviewed_papers) / len(reviewed_papers) if reviewed_papers else 0,
            'best_score': max(p.get('avg_rating', 0) for p in reviewed_papers) if reviewed_papers else 0,
            'stage_duration_minutes': stage_duration
        })
        
        return reviewed_papers + refined_papers
    
    def stage3_deep_review(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Stage 3: Deep Review and Enhancement (60 minutes)"""
        self.logger.info("🔍 Starting Stage 3: Deep Review and Enhancement")
        stage_start = datetime.now()
        
        # Load deep reviewer
        if self.deep_reviewer is None:
            self.logger.info("🔄 Loading DeepReviewer...")
            self.deep_reviewer = DeepReviewer(model_size="14B")
            self.logger.info("✅ DeepReviewer loaded successfully")
        
        # Select top papers for deep review
        top_papers = sorted(papers, key=lambda x: x.get('avg_rating', 0), reverse=True)[:3]
        
        deep_reviewed_papers = []
        
        for i, paper in enumerate(top_papers):
            try:
                self.logger.info(f"🔬 Deep reviewing paper {i+1}/{len(top_papers)}")
                
                paper_text = paper.get('generated_text', paper.get('latex', ''))
                
                if paper_text:
                    # Perform deep review with multiple reviewers
                    deep_review = self.deep_reviewer.evaluate(
                        paper_text,
                        mode="Standard Mode",
                        reviewer_num=4
                    )
                    
                    paper['deep_review_results'] = deep_review
                    paper['deep_review_timestamp'] = datetime.now().isoformat()
                    
                    # Calculate enhanced metrics
                    if deep_review and deep_review[0].get('reviews'):
                        reviews = deep_review[0]['reviews']
                        paper['multi_reviewer_scores'] = [r.get('rating', 0) for r in reviews]
                        paper['multi_reviewer_average'] = sum(paper['multi_reviewer_scores']) / len(paper['multi_reviewer_scores'])
                        
                        self.logger.info(f"📊 Deep review scores: {paper['multi_reviewer_scores']}")
                        self.logger.info(f"📈 Average: {paper['multi_reviewer_average']:.2f}")
                    
                    deep_reviewed_papers.append(paper)
                    
                    # Save updated paper
                    paper_file = f"output/{paper['paper_id']}_deep_reviewed.json"
                    with open(paper_file, 'w') as f:
                        json.dump(paper, f, indent=2)
                
            except Exception as e:
                self.logger.error(f"❌ Error in deep review {i+1}: {str(e)}")
                paper['deep_review_error'] = str(e)
                deep_reviewed_papers.append(paper)
        
        stage_duration = (datetime.now() - stage_start).total_seconds() / 60
        self.logger.info(f"✅ Stage 3 completed in {stage_duration:.1f} minutes")
        
        # Save checkpoint
        self.save_checkpoint("stage3_complete", {
            'papers_deep_reviewed': len(deep_reviewed_papers),
            'multi_reviewer_scores': [p.get('multi_reviewer_average', 0) for p in deep_reviewed_papers],
            'stage_duration_minutes': stage_duration
        })
        
        return deep_reviewed_papers
    
    def stage4_final_validation(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Stage 4: Final Generation and Validation (30 minutes)"""
        self.logger.info("🏁 Starting Stage 4: Final Generation and Validation")
        stage_start = datetime.now()
        
        # Select the best paper for final enhancement
        best_paper = max(papers, key=lambda x: x.get('multi_reviewer_average', x.get('avg_rating', 0)))
        
        self.logger.info(f"🥇 Best paper selected: {best_paper['paper_id']}")
        self.logger.info(f"📊 Score: {best_paper.get('multi_reviewer_average', best_paper.get('avg_rating', 0)):.2f}")
        
        # Load AI detector
        if self.detector is None:
            self.logger.info("🔄 Loading AI Detector...")
            self.detector = AIDetector(device='cpu')
            self.logger.info("✅ AI Detector loaded successfully")
        
        # Run AI detection on best paper
        try:
            paper_text = best_paper.get('generated_text', best_paper.get('latex', ''))
            if paper_text:
                detection_result = self.detector.analyze_paper(best_paper)
                best_paper['ai_detection'] = detection_result
                
                self.logger.info(f"🔍 AI Detection: {detection_result.get('probability', 0)*100:.1f}% AI-generated")
                self.logger.info(f"🎯 Confidence: {detection_result.get('confidence_level', 'Unknown')}")
            
        except Exception as e:
            self.logger.error(f"❌ AI Detection error: {str(e)}")
            best_paper['ai_detection_error'] = str(e)
        
        # Compile final experiment results
        final_results = {
            'experiment_id': self.experiment_id,
            'completion_timestamp': datetime.now().isoformat(),
            'total_duration_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
            'papers_generated': len(self.generated_papers),
            'best_paper': best_paper,
            'all_papers': papers,
            'performance_summary': {
                'highest_score': max(p.get('multi_reviewer_average', p.get('avg_rating', 0)) for p in papers),
                'average_score': sum(p.get('multi_reviewer_average', p.get('avg_rating', 0)) for p in papers) / len(papers),
                'target_achieved': max(p.get('multi_reviewer_average', p.get('avg_rating', 0)) for p in papers) >= self.config.get('quality_target', 5.0),
                'checkpoints': len(self.checkpoints)
            }
        }
        
        # Save final results
        with open('output/final_experiment_results.json', 'w') as f:
            json.dump(final_results, f, indent=2)
        
        # Save best paper separately
        with open('output/best_paper_final.json', 'w') as f:
            json.dump(best_paper, f, indent=2)
        
        stage_duration = (datetime.now() - stage_start).total_seconds() / 60
        self.logger.info(f"✅ Stage 4 completed in {stage_duration:.1f} minutes")
        
        # Final checkpoint
        self.save_checkpoint("experiment_complete", final_results['performance_summary'])
        
        return final_results
    
    def run_experiment(self) -> Dict[str, Any]:
        """Execute the complete 4-5 hour experiment"""
        try:
            self.logger.info("🚀 Starting complete experiment run")
            
            # Stage 1: Initial Generation
            initial_papers = self.stage1_initial_generation()
            
            # Stage 2: Iterative Refinement  
            refined_papers = self.stage2_iterative_refinement(initial_papers)
            
            # Stage 3: Deep Review
            deep_reviewed_papers = self.stage3_deep_review(refined_papers)
            
            # Stage 4: Final Validation
            final_results = self.stage4_final_validation(deep_reviewed_papers)
            
            total_duration = (datetime.now() - self.start_time).total_seconds() / 3600
            
            self.logger.info("🎉 EXPERIMENT COMPLETED SUCCESSFULLY!")
            self.logger.info(f"⏱️  Total Duration: {total_duration:.2f} hours")
            self.logger.info(f"📄 Papers Generated: {len(self.generated_papers)}")
            self.logger.info(f"🏆 Best Score: {final_results['performance_summary']['highest_score']:.2f}")
            self.logger.info(f"📊 Average Score: {final_results['performance_summary']['average_score']:.2f}")
            self.logger.info(f"🎯 Target Achieved: {final_results['performance_summary']['target_achieved']}")
            
            return final_results
            
        except Exception as e:
            self.logger.error(f"💥 CRITICAL ERROR: {str(e)}")
            self.logger.error(f"Stack trace: {traceback.format_exc()}")
            
            # Save error checkpoint
            error_data = {
                'error': str(e),
                'traceback': traceback.format_exc(),
                'papers_generated_before_error': len(self.generated_papers)
            }
            self.save_checkpoint("error", error_data)
            
            raise


def main():
    """Main execution function"""
    print("🌟 Starting Long-Duration AI Research Experiment")
    print("📊 experiment-native-1-spectro: SAI Active Spectroscopy Framework")
    print("⏱️  Expected Duration: 4-5 hours")
    print("")
    
    # Change to experiment directory
    os.chdir('/Users/apple/code/Researcher/EXPERIMENTS/experiment-native-1-spectro')
    
    # Initialize and run experiment
    runner = ExperimentRunner()
    
    try:
        results = runner.run_experiment()
        
        print("\n" + "="*60)
        print("🎊 EXPERIMENT COMPLETED SUCCESSFULLY! 🎊")
        print("="*60)
        print(f"📄 Papers Generated: {results['papers_generated']}")
        print(f"🏆 Best Score: {results['performance_summary']['highest_score']:.2f}/10")
        print(f"📊 Average Score: {results['performance_summary']['average_score']:.2f}/10") 
        print(f"⏱️  Duration: {results['total_duration_hours']:.2f} hours")
        print(f"🎯 Quality Target Achieved: {'✅' if results['performance_summary']['target_achieved'] else '❌'}")
        print("\n📁 Results saved in output/ directory")
        print("📋 Full logs available in logs/ directory")
        print("💾 Checkpoints saved in checkpoints/ directory")
        
    except KeyboardInterrupt:
        print("\n⚠️  Experiment interrupted by user")
        print("💾 Checkpoints and partial results preserved")
        
    except Exception as e:
        print(f"\n💥 Experiment failed: {str(e)}")
        print("💾 Error logs and checkpoints saved for analysis")


if __name__ == "__main__":
    main()