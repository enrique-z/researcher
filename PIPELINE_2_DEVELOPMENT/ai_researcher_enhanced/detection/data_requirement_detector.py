"""
Data Requirement Detection System with Dual Oxford Integration

This module automatically detects data requirements for Pipeline 2 experiments
and uses Oxford's dual-system framework to identify available data sources
from both historical literature (FAISS) and current research (web search).

Key Features:
- Automatic data requirement detection from experiment specifications
- Oxford dual-system integration for data source identification
- Sakana compliance for real data requirement validation
- Domain-specific data requirement patterns
- Gap analysis and recommendation generation
- Real-time and historical data source mapping

Architecture:
- Requirement Detection: Analyzes experiments to identify data needs
- Oxford Integration: Uses FAISS + Web Search to find data sources
- Gap Analysis: Identifies missing data requirements
- Recommendation Engine: Suggests data acquisition strategies
"""

import os
import sys
import json
import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple, Set
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Pipeline 2 imports
from ..integration.oxford_dual_system_bridge import OxfordDualSystemBridge
from ..integration.sakana_bridge import SakanaBridge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataRequirementType(Enum):
    """Types of data requirements for experiments."""
    EXPERIMENTAL_DATA = "experimental_data"       # Direct experimental measurements
    VALIDATION_DATA = "validation_data"           # Data for validation/comparison
    PARAMETER_DATA = "parameter_data"             # Input parameters and constants
    ENVIRONMENTAL_DATA = "environmental_data"     # Environmental conditions
    HISTORICAL_DATA = "historical_data"           # Historical context/trends
    REFERENCE_DATA = "reference_data"             # Literature reference data
    REAL_TIME_DATA = "real_time_data"            # Current/live data feeds


class DataSource(Enum):
    """Available data sources through Oxford integration."""
    FAISS_LITERATURE = "faiss_literature"        # 1100+ PDFs in FAISS
    WEB_RESEARCH = "web_research"                 # Real-time web search
    SAKANA_EMPIRICAL = "sakana_empirical"         # Sakana real data systems
    DOMAIN_DATABASES = "domain_databases"         # Domain-specific databases
    EXPERIMENTAL_LOGS = "experimental_logs"       # Direct experiment data


@dataclass
class DataRequirement:
    """Represents a detected data requirement."""
    requirement_id: str
    requirement_type: DataRequirementType
    description: str
    domain: str
    priority: float  # 0.0-1.0
    required_for_validation: bool
    sakana_compliant: bool
    estimated_availability: float  # 0.0-1.0
    potential_sources: List[DataSource]
    search_queries: List[str]
    metadata: Dict[str, Any]


@dataclass
class DataSourceResult:
    """Result from data source search."""
    source: DataSource
    query: str
    found_data: List[Dict[str, Any]]
    availability_score: float
    quality_score: float
    relevance_score: float
    access_information: Dict[str, Any]


@dataclass
class DataRequirementAnalysis:
    """Complete analysis of data requirements for an experiment."""
    experiment_id: str
    analysis_timestamp: str
    detected_requirements: List[DataRequirement]
    source_results: List[DataSourceResult]
    coverage_analysis: Dict[str, Any]
    gap_analysis: Dict[str, Any]
    recommendations: List[str]
    oxford_integration_status: Dict[str, Any]
    sakana_compliance_status: Dict[str, Any]
    overall_data_readiness: float


class DataRequirementDetector:
    """
    Data requirement detection system with Oxford dual-system integration.
    
    Automatically detects what data is needed for Pipeline 2 experiments
    and uses Oxford's FAISS + Web Search to identify available sources.
    """
    
    def __init__(self, 
                 oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun",
                 enable_oxford: bool = True,
                 enable_sakana: bool = True):
        """
        Initialize data requirement detector.
        
        Args:
            oxford_path: Path to Oxford framework
            enable_oxford: Enable Oxford dual-system integration
            enable_sakana: Enable Sakana integration
        """
        self.oxford_path = Path(oxford_path)
        self.enable_oxford = enable_oxford
        self.enable_sakana = enable_sakana
        
        # Initialize Oxford integration
        self.oxford_bridge = None
        if self.enable_oxford:
            try:
                self.oxford_bridge = OxfordDualSystemBridge(oxford_path)
                logger.info("✅ Oxford dual-system connected for data detection")
            except Exception as e:
                logger.error(f"❌ Oxford integration failed: {e}")
                self.enable_oxford = False
        
        # Initialize Sakana integration
        self.sakana_bridge = None
        if self.enable_sakana:
            try:
                self.sakana_bridge = SakanaBridge()
                logger.info("✅ Sakana bridge connected for data validation")
            except Exception as e:
                logger.error(f"❌ Sakana integration failed: {e}")
                self.enable_sakana = False
        
        # Detection patterns for different domains
        self.detection_patterns = self._initialize_detection_patterns()
        
        # Data source capabilities
        self.source_capabilities = self._initialize_source_capabilities()
        
        # Detection statistics
        self.detection_stats = {
            'total_analyses': 0,
            'successful_detections': 0,
            'oxford_assisted_detections': 0,
            'sakana_compliant_detections': 0,
            'average_data_readiness': 0.0
        }
        
        # Analysis history
        self.analysis_history = []
        
        logger.info("🔍 Data Requirement Detector initialized")
        logger.info(f"Oxford integration: {'ENABLED' if self.enable_oxford else 'DISABLED'}")
        logger.info(f"Sakana integration: {'ENABLED' if self.enable_sakana else 'DISABLED'}")
    
    def _initialize_detection_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize data requirement detection patterns for different domains."""
        return {
            'climate': {
                'experimental_data': [
                    r'temperature\s+measurements?',
                    r'atmospheric\s+composition',
                    r'aerosol\s+optical\s+depth',
                    r'radiation\s+balance',
                    r'cloud\s+properties',
                    r'precipitation\s+data'
                ],
                'validation_data': [
                    r'climate\s+model\s+output',
                    r'satellite\s+observations',
                    r'ground\s+station\s+data',
                    r'historical\s+climate\s+records'
                ],
                'parameter_data': [
                    r'injection\s+rate',
                    r'particle\s+size\s+distribution',
                    r'stratospheric\s+conditions',
                    r'chemical\s+composition'
                ]
            },
            'chemical': {
                'experimental_data': [
                    r'reaction\s+rates?',
                    r'concentration\s+measurements?',
                    r'spectroscopic\s+data',
                    r'thermodynamic\s+properties'
                ],
                'validation_data': [
                    r'literature\s+values?',
                    r'reference\s+standards?',
                    r'calibration\s+data'
                ],
                'parameter_data': [
                    r'molecular\s+properties',
                    r'chemical\s+constants',
                    r'equilibrium\s+conditions'
                ]
            },
            'general': {
                'experimental_data': [
                    r'measurement\s+data',
                    r'experimental\s+results?',
                    r'observational\s+data',
                    r'sensor\s+readings?'
                ],
                'validation_data': [
                    r'validation\s+dataset',
                    r'reference\s+data',
                    r'benchmark\s+results?'
                ],
                'parameter_data': [
                    r'input\s+parameters?',
                    r'configuration\s+settings?',
                    r'experimental\s+conditions?'
                ]
            }
        }
    
    def _initialize_source_capabilities(self) -> Dict[DataSource, Dict[str, Any]]:
        """Initialize capabilities of different data sources."""
        return {
            DataSource.FAISS_LITERATURE: {
                'data_types': [DataRequirementType.REFERENCE_DATA, DataRequirementType.HISTORICAL_DATA],
                'domains': ['climate', 'chemical', 'general'],
                'access_method': 'faiss_search',
                'real_time': False,
                'quality_score': 0.9,
                'description': '1100+ climate science PDFs with historical research data'
            },
            DataSource.WEB_RESEARCH: {
                'data_types': [DataRequirementType.REAL_TIME_DATA, DataRequirementType.VALIDATION_DATA],
                'domains': ['climate', 'chemical', 'general'],
                'access_method': 'web_search',
                'real_time': True,
                'quality_score': 0.7,
                'description': 'Current research and real-time data from web sources'
            },
            DataSource.SAKANA_EMPIRICAL: {
                'data_types': [DataRequirementType.EXPERIMENTAL_DATA, DataRequirementType.VALIDATION_DATA],
                'domains': ['climate', 'chemical'],
                'access_method': 'sakana_bridge',
                'real_time': True,
                'quality_score': 0.95,
                'description': 'Real empirical data from Sakana systems'
            }
        }
    
    async def analyze_data_requirements(self, 
                                      experiment: Dict[str, Any],
                                      domain: str = "general") -> DataRequirementAnalysis:
        """
        Analyze data requirements for an experiment using Oxford dual-system.
        
        Args:
            experiment: Experiment specification
            domain: Experimental domain
            
        Returns:
            DataRequirementAnalysis with comprehensive data requirement assessment
        """
        analysis_start = datetime.now()
        self.detection_stats['total_analyses'] += 1
        
        experiment_id = experiment.get('id', 'unknown')
        
        # Initialize analysis result
        analysis = DataRequirementAnalysis(
            experiment_id=experiment_id,
            analysis_timestamp=analysis_start.isoformat(),
            detected_requirements=[],
            source_results=[],
            coverage_analysis={},
            gap_analysis={},
            recommendations=[],
            oxford_integration_status={},
            sakana_compliance_status={},
            overall_data_readiness=0.0
        )
        
        try:
            # Step 1: Detect data requirements from experiment specification
            detected_requirements = await self._detect_requirements_from_experiment(experiment, domain)
            analysis.detected_requirements = detected_requirements
            
            # Step 2: Search for data sources using Oxford dual-system
            if self.enable_oxford and self.oxford_bridge:
                source_results = await self._search_data_sources_with_oxford(detected_requirements, domain)
                analysis.source_results = source_results
                self.detection_stats['oxford_assisted_detections'] += 1
            
            # Step 3: Validate Sakana compliance
            if self.enable_sakana and self.sakana_bridge:
                sakana_status = await self._validate_sakana_compliance(detected_requirements, analysis.source_results)
                analysis.sakana_compliance_status = sakana_status
                
                if sakana_status.get('compliant', False):
                    self.detection_stats['sakana_compliant_detections'] += 1
            
            # Step 4: Perform coverage and gap analysis
            coverage_analysis = await self._analyze_data_coverage(detected_requirements, analysis.source_results)
            analysis.coverage_analysis = coverage_analysis
            
            gap_analysis = await self._analyze_data_gaps(detected_requirements, analysis.source_results, domain)
            analysis.gap_analysis = gap_analysis
            
            # Step 5: Generate recommendations
            recommendations = await self._generate_data_recommendations(
                detected_requirements, analysis.source_results, gap_analysis
            )
            analysis.recommendations = recommendations
            
            # Step 6: Calculate overall data readiness
            overall_readiness = self._calculate_data_readiness(coverage_analysis, gap_analysis)
            analysis.overall_data_readiness = overall_readiness
            
            # Update statistics
            self.detection_stats['successful_detections'] += 1
            total_readiness = (self.detection_stats['average_data_readiness'] * 
                             (self.detection_stats['successful_detections'] - 1) + 
                             overall_readiness)
            self.detection_stats['average_data_readiness'] = total_readiness / self.detection_stats['successful_detections']
            
            # Set Oxford integration status
            analysis.oxford_integration_status = {
                'faiss_system_used': self.enable_oxford and self.oxford_bridge is not None,
                'web_search_used': self.enable_oxford and self.oxford_bridge is not None,
                'solomon_orchestration_used': self.enable_oxford and self.oxford_bridge is not None,
                'total_sources_found': len(analysis.source_results)
            }
            
            logger.info(f"✅ Data requirement analysis completed: readiness {overall_readiness:.2f}")
            
        except Exception as e:
            logger.error(f"❌ Data requirement analysis failed: {e}")
            analysis.recommendations.append(f"Analysis failed: {str(e)}")
        
        # Record analysis history
        analysis_duration = (datetime.now() - analysis_start).total_seconds()
        self.analysis_history.append({
            'experiment_id': experiment_id,
            'analysis_timestamp': analysis_start.isoformat(),
            'duration_seconds': analysis_duration,
            'data_readiness': analysis.overall_data_readiness,
            'requirements_detected': len(analysis.detected_requirements),
            'sources_found': len(analysis.source_results)
        })
        
        return analysis
    
    async def _detect_requirements_from_experiment(self, 
                                                 experiment: Dict[str, Any], 
                                                 domain: str) -> List[DataRequirement]:
        """Detect data requirements from experiment specification."""
        requirements = []
        
        # Get experiment text for analysis
        experiment_text = self._extract_experiment_text(experiment)
        
        # Get domain-specific patterns
        domain_patterns = self.detection_patterns.get(domain, self.detection_patterns['general'])
        
        # Detect requirements for each category
        for req_type_name, patterns in domain_patterns.items():
            req_type = DataRequirementType(req_type_name)
            
            for pattern in patterns:
                matches = re.findall(pattern, experiment_text, re.IGNORECASE)
                
                if matches:
                    # Create requirement for this pattern
                    requirement = DataRequirement(
                        requirement_id=f"{experiment.get('id', 'unknown')}_{req_type.value}_{len(requirements)}",
                        requirement_type=req_type,
                        description=f"Data requirement detected: {pattern}",
                        domain=domain,
                        priority=self._calculate_requirement_priority(req_type, matches),
                        required_for_validation=req_type in [DataRequirementType.VALIDATION_DATA, DataRequirementType.EXPERIMENTAL_DATA],
                        sakana_compliant=req_type in [DataRequirementType.EXPERIMENTAL_DATA, DataRequirementType.REAL_TIME_DATA],
                        estimated_availability=0.5,  # Will be updated by source search
                        potential_sources=self._identify_potential_sources(req_type),
                        search_queries=self._generate_search_queries(pattern, matches, domain),
                        metadata={
                            'pattern': pattern,
                            'matches': matches,
                            'detection_method': 'pattern_matching'
                        }
                    )
                    
                    requirements.append(requirement)
        
        # Add explicit requirements from experiment parameters
        explicit_requirements = self._detect_explicit_requirements(experiment, domain)
        requirements.extend(explicit_requirements)
        
        logger.info(f"🔍 Detected {len(requirements)} data requirements for {domain} experiment")
        
        return requirements
    
    async def _search_data_sources_with_oxford(self, 
                                             requirements: List[DataRequirement], 
                                             domain: str) -> List[DataSourceResult]:
        """Search for data sources using Oxford dual-system."""
        source_results = []
        
        for requirement in requirements:
            # Search FAISS literature database
            if DataSource.FAISS_LITERATURE in requirement.potential_sources:
                faiss_result = await self._search_faiss_for_requirement(requirement)
                if faiss_result:
                    source_results.append(faiss_result)
            
            # Search web for current data
            if DataSource.WEB_RESEARCH in requirement.potential_sources:
                web_result = await self._search_web_for_requirement(requirement)
                if web_result:
                    source_results.append(web_result)
        
        return source_results
    
    async def _search_faiss_for_requirement(self, requirement: DataRequirement) -> Optional[DataSourceResult]:
        """Search FAISS literature for data requirement."""
        try:
            # Use Oxford bridge to search FAISS
            for query in requirement.search_queries:
                faiss_result = self.oxford_bridge._query_faiss_system(query, max_results=3)
                
                if faiss_result.get('results'):
                    # Convert FAISS results to data source format
                    found_data = []
                    for result in faiss_result['results']:
                        found_data.append({
                            'source_document': result.get('source', 'Unknown'),
                            'content': result.get('content', ''),
                            'similarity_score': result.get('similarity_score', 0.0),
                            'page': result.get('page', 'Unknown'),
                            'data_type': 'literature_reference'
                        })
                    
                    return DataSourceResult(
                        source=DataSource.FAISS_LITERATURE,
                        query=query,
                        found_data=found_data,
                        availability_score=len(found_data) / 3.0,  # Normalize by max results
                        quality_score=0.9,  # High quality for literature
                        relevance_score=sum(d.get('similarity_score', 0) for d in found_data) / len(found_data),
                        access_information={
                            'access_method': 'faiss_search',
                            'database_size': '1100+ PDFs',
                            'search_timestamp': datetime.now().isoformat()
                        }
                    )
            
        except Exception as e:
            logger.error(f"FAISS search failed for requirement {requirement.requirement_id}: {e}")
        
        return None
    
    async def _search_web_for_requirement(self, requirement: DataRequirement) -> Optional[DataSourceResult]:
        """Search web for data requirement."""
        try:
            # Use Oxford bridge to search web
            for query in requirement.search_queries:
                web_result = self.oxford_bridge._query_web_search_system(query, max_results=3)
                
                if web_result.get('results'):
                    # Convert web results to data source format
                    found_data = []
                    for result in web_result['results']:
                        found_data.append({
                            'title': result.get('title', 'Unknown'),
                            'url': result.get('url', ''),
                            'snippet': result.get('snippet', ''),
                            'date': result.get('date', 'Recent'),
                            'source_domain': result.get('source_domain', 'Unknown'),
                            'data_type': 'web_research'
                        })
                    
                    return DataSourceResult(
                        source=DataSource.WEB_RESEARCH,
                        query=query,
                        found_data=found_data,
                        availability_score=len(found_data) / 3.0,  # Normalize by max results
                        quality_score=0.7,  # Medium quality for web
                        relevance_score=sum(d.get('relevance_score', 0.7) for d in found_data) / len(found_data),
                        access_information={
                            'access_method': 'web_search',
                            'real_time': True,
                            'search_timestamp': datetime.now().isoformat()
                        }
                    )
            
        except Exception as e:
            logger.error(f"Web search failed for requirement {requirement.requirement_id}: {e}")
        
        return None
    
    def _extract_experiment_text(self, experiment: Dict[str, Any]) -> str:
        """Extract text from experiment for requirement detection."""
        text_parts = []
        
        # Extract from common fields
        for field in ['title', 'description', 'methodology', 'objectives', 'parameters']:
            if field in experiment:
                value = experiment[field]
                if isinstance(value, str):
                    text_parts.append(value)
                elif isinstance(value, dict):
                    text_parts.append(json.dumps(value, indent=2))
        
        return ' '.join(text_parts)
    
    def _calculate_requirement_priority(self, req_type: DataRequirementType, matches: List[str]) -> float:
        """Calculate priority score for a data requirement."""
        base_priorities = {
            DataRequirementType.EXPERIMENTAL_DATA: 0.9,
            DataRequirementType.VALIDATION_DATA: 0.8,
            DataRequirementType.PARAMETER_DATA: 0.7,
            DataRequirementType.ENVIRONMENTAL_DATA: 0.6,
            DataRequirementType.HISTORICAL_DATA: 0.5,
            DataRequirementType.REFERENCE_DATA: 0.4,
            DataRequirementType.REAL_TIME_DATA: 0.8
        }
        
        base_priority = base_priorities.get(req_type, 0.5)
        
        # Boost priority based on number of matches
        match_boost = min(len(matches) * 0.1, 0.3)
        
        return min(base_priority + match_boost, 1.0)
    
    def _identify_potential_sources(self, req_type: DataRequirementType) -> List[DataSource]:
        """Identify potential data sources for a requirement type."""
        potential_sources = []
        
        for source, capabilities in self.source_capabilities.items():
            if req_type in capabilities['data_types']:
                potential_sources.append(source)
        
        return potential_sources
    
    def _generate_search_queries(self, pattern: str, matches: List[str], domain: str) -> List[str]:
        """Generate search queries for data requirement."""
        queries = []
        
        # Create query from pattern
        base_query = pattern.replace(r'\s+', ' ').replace('?', '').replace(r'\\', '')
        queries.append(f"{domain} {base_query} data")
        
        # Create queries from specific matches
        for match in matches[:2]:  # Limit to first 2 matches
            queries.append(f"{domain} {match} measurement data")
        
        return queries
    
    def _detect_explicit_requirements(self, experiment: Dict[str, Any], domain: str) -> List[DataRequirement]:
        """Detect explicit data requirements from experiment parameters."""
        requirements = []
        
        # Check if experiment has explicit data requirements
        if 'data_requirements' in experiment:
            for i, req_text in enumerate(experiment['data_requirements']):
                requirement = DataRequirement(
                    requirement_id=f"{experiment.get('id', 'unknown')}_explicit_{i}",
                    requirement_type=DataRequirementType.EXPERIMENTAL_DATA,
                    description=f"Explicit requirement: {req_text}",
                    domain=domain,
                    priority=0.8,
                    required_for_validation=True,
                    sakana_compliant=True,
                    estimated_availability=0.3,
                    potential_sources=[DataSource.SAKANA_EMPIRICAL, DataSource.WEB_RESEARCH],
                    search_queries=[f"{domain} {req_text}", f"{req_text} data"],
                    metadata={'source': 'explicit_requirement', 'original_text': req_text}
                )
                requirements.append(requirement)
        
        return requirements
    
    async def _validate_sakana_compliance(self, 
                                        requirements: List[DataRequirement], 
                                        source_results: List[DataSourceResult]) -> Dict[str, Any]:
        """Validate Sakana compliance for data requirements."""
        sakana_status = {
            'compliant': False,
            'real_data_requirements': 0,
            'real_data_sources_found': 0,
            'compliance_score': 0.0,
            'non_compliant_requirements': [],
            'recommendations': []
        }
        
        # Count requirements that need real data
        real_data_requirements = [req for req in requirements if req.sakana_compliant]
        sakana_status['real_data_requirements'] = len(real_data_requirements)
        
        # Count sources that provide real data
        real_data_sources = [result for result in source_results 
                            if result.source in [DataSource.SAKANA_EMPIRICAL, DataSource.WEB_RESEARCH]]
        sakana_status['real_data_sources_found'] = len(real_data_sources)
        
        # Calculate compliance score
        if sakana_status['real_data_requirements'] > 0:
            sakana_status['compliance_score'] = (sakana_status['real_data_sources_found'] / 
                                               sakana_status['real_data_requirements'])
        
        # Determine overall compliance
        sakana_status['compliant'] = sakana_status['compliance_score'] >= 0.7
        
        # Identify non-compliant requirements
        for requirement in real_data_requirements:
            has_real_data_source = any(
                result.source in [DataSource.SAKANA_EMPIRICAL, DataSource.WEB_RESEARCH]
                for result in source_results
                if any(query in result.query for query in requirement.search_queries)
            )
            
            if not has_real_data_source:
                sakana_status['non_compliant_requirements'].append(requirement.requirement_id)
        
        # Generate recommendations
        if not sakana_status['compliant']:
            sakana_status['recommendations'].extend([
                "Increase real data sources for Sakana compliance",
                "Consider integrating with empirical data systems",
                "Validate data authenticity for non-compliant requirements"
            ])
        
        return sakana_status
    
    async def _analyze_data_coverage(self, 
                                   requirements: List[DataRequirement], 
                                   source_results: List[DataSourceResult]) -> Dict[str, Any]:
        """Analyze data coverage for requirements."""
        coverage = {
            'total_requirements': len(requirements),
            'covered_requirements': 0,
            'coverage_percentage': 0.0,
            'coverage_by_type': {},
            'coverage_by_source': {},
            'high_priority_coverage': 0.0
        }
        
        # Calculate coverage by requirement type
        for req_type in DataRequirementType:
            type_requirements = [req for req in requirements if req.requirement_type == req_type]
            type_covered = sum(1 for req in type_requirements if self._is_requirement_covered(req, source_results))
            
            coverage['coverage_by_type'][req_type.value] = {
                'total': len(type_requirements),
                'covered': type_covered,
                'percentage': type_covered / max(len(type_requirements), 1)
            }
        
        # Calculate coverage by source
        for source in DataSource:
            source_results_count = len([result for result in source_results if result.source == source])
            coverage['coverage_by_source'][source.value] = source_results_count
        
        # Calculate overall coverage
        covered_requirements = sum(1 for req in requirements if self._is_requirement_covered(req, source_results))
        coverage['covered_requirements'] = covered_requirements
        coverage['coverage_percentage'] = covered_requirements / max(len(requirements), 1)
        
        # Calculate high-priority requirement coverage
        high_priority_reqs = [req for req in requirements if req.priority >= 0.7]
        high_priority_covered = sum(1 for req in high_priority_reqs if self._is_requirement_covered(req, source_results))
        coverage['high_priority_coverage'] = high_priority_covered / max(len(high_priority_reqs), 1)
        
        return coverage
    
    def _is_requirement_covered(self, requirement: DataRequirement, source_results: List[DataSourceResult]) -> bool:
        """Check if a requirement is covered by available sources."""
        for result in source_results:
            # Check if any of the requirement's search queries match this result
            if any(query in result.query for query in requirement.search_queries):
                # Check if the result has sufficient quality and availability
                if result.availability_score >= 0.3 and result.quality_score >= 0.5:
                    return True
        return False
    
    async def _analyze_data_gaps(self, 
                               requirements: List[DataRequirement], 
                               source_results: List[DataSourceResult], 
                               domain: str) -> Dict[str, Any]:
        """Analyze data gaps and missing requirements."""
        gaps = {
            'uncovered_requirements': [],
            'low_quality_sources': [],
            'missing_source_types': [],
            'critical_gaps': [],
            'gap_severity': 0.0,
            'recommendations': []
        }
        
        # Identify uncovered requirements
        for requirement in requirements:
            if not self._is_requirement_covered(requirement, source_results):
                gaps['uncovered_requirements'].append({
                    'requirement_id': requirement.requirement_id,
                    'description': requirement.description,
                    'priority': requirement.priority,
                    'type': requirement.requirement_type.value
                })
        
        # Identify low-quality sources
        for result in source_results:
            if result.quality_score < 0.6:
                gaps['low_quality_sources'].append({
                    'source': result.source.value,
                    'query': result.query,
                    'quality_score': result.quality_score
                })
        
        # Identify missing source types
        available_sources = set(result.source for result in source_results)
        all_potential_sources = set()
        for req in requirements:
            all_potential_sources.update(req.potential_sources)
        
        missing_sources = all_potential_sources - available_sources
        gaps['missing_source_types'] = [source.value for source in missing_sources]
        
        # Identify critical gaps (high-priority uncovered requirements)
        critical_gaps = [gap for gap in gaps['uncovered_requirements'] if gap['priority'] >= 0.7]
        gaps['critical_gaps'] = critical_gaps
        
        # Calculate gap severity
        total_priority = sum(req.priority for req in requirements)
        uncovered_priority = sum(gap['priority'] for gap in gaps['uncovered_requirements'])
        gaps['gap_severity'] = uncovered_priority / max(total_priority, 1)
        
        return gaps
    
    async def _generate_data_recommendations(self, 
                                           requirements: List[DataRequirement], 
                                           source_results: List[DataSourceResult], 
                                           gap_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for data acquisition and improvement."""
        recommendations = []
        
        # Recommendations based on gaps
        if gap_analysis['critical_gaps']:
            recommendations.append(
                f"CRITICAL: Address {len(gap_analysis['critical_gaps'])} high-priority data gaps"
            )
        
        if gap_analysis['missing_source_types']:
            missing_sources = gap_analysis['missing_source_types']
            recommendations.append(
                f"Consider integrating missing data sources: {', '.join(missing_sources)}"
            )
        
        if gap_analysis['low_quality_sources']:
            recommendations.append(
                f"Improve quality of {len(gap_analysis['low_quality_sources'])} data sources"
            )
        
        # Recommendations based on source availability
        faiss_results = [r for r in source_results if r.source == DataSource.FAISS_LITERATURE]
        web_results = [r for r in source_results if r.source == DataSource.WEB_RESEARCH]
        
        if faiss_results and not web_results:
            recommendations.append("Consider adding real-time web search for current data")
        elif web_results and not faiss_results:
            recommendations.append("Consider accessing historical literature for context")
        elif faiss_results and web_results:
            recommendations.append("Excellent: Both historical and current data sources available")
        
        # Sakana compliance recommendations
        sakana_requirements = [req for req in requirements if req.sakana_compliant]
        if sakana_requirements:
            recommendations.append("Ensure Sakana compliance with real empirical data")
        
        # Oxford integration recommendations
        if self.enable_oxford:
            recommendations.append("Leveraging Oxford dual-system for comprehensive data coverage")
        
        return recommendations
    
    def _calculate_data_readiness(self, coverage_analysis: Dict[str, Any], gap_analysis: Dict[str, Any]) -> float:
        """Calculate overall data readiness score."""
        coverage_score = coverage_analysis.get('coverage_percentage', 0.0)
        gap_penalty = gap_analysis.get('gap_severity', 0.0)
        
        # Weight high-priority coverage more heavily
        high_priority_score = coverage_analysis.get('high_priority_coverage', 0.0)
        
        # Calculate weighted readiness score
        readiness = (coverage_score * 0.5 + high_priority_score * 0.3 + (1.0 - gap_penalty) * 0.2)
        
        return min(readiness, 1.0)
    
    def get_detection_statistics(self) -> Dict[str, Any]:
        """Get data detection system statistics."""
        return {
            'detector_name': 'Oxford-Enhanced Data Requirement Detector',
            'total_analyses': self.detection_stats['total_analyses'],
            'successful_detections': self.detection_stats['successful_detections'],
            'oxford_assisted_detections': self.detection_stats['oxford_assisted_detections'],
            'sakana_compliant_detections': self.detection_stats['sakana_compliant_detections'],
            'average_data_readiness': self.detection_stats['average_data_readiness'],
            'success_rate': (self.detection_stats['successful_detections'] / 
                           max(self.detection_stats['total_analyses'], 1)),
            'oxford_integration': {
                'faiss_system_available': self.enable_oxford and self.oxford_bridge is not None,
                'web_search_available': self.enable_oxford and self.oxford_bridge is not None,
                'dual_system_active': self.enable_oxford
            },
            'sakana_integration': {
                'empirical_validation_available': self.enable_sakana and self.sakana_bridge is not None,
                'real_data_enforcement': self.enable_sakana
            },
            'analysis_history_count': len(self.analysis_history)
        }


# Convenience functions for Pipeline 2 integration
def create_data_detector(oxford_path: str = "/Users/apple/code/scientificoxford-try-shaun") -> DataRequirementDetector:
    """Create data requirement detector for Pipeline 2."""
    return DataRequirementDetector(oxford_path)

async def detect_experiment_data_requirements(experiment: Dict[str, Any], 
                                            domain: str = "general") -> DataRequirementAnalysis:
    """
    One-line function to detect data requirements with Oxford integration.
    
    Usage in Pipeline 2:
    from .data_requirement_detector import detect_experiment_data_requirements
    analysis = await detect_experiment_data_requirements(experiment, "climate")
    """
    detector = create_data_detector()
    return await detector.analyze_data_requirements(experiment, domain)