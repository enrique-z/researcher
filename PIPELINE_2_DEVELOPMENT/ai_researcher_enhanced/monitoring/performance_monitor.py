"""
Pipeline 2 Performance Monitoring System

This module provides comprehensive performance monitoring for Pipeline 2:
- Real-time system health monitoring
- Usage pattern analysis and optimization detection
- Oxford integration performance tracking
- Sakana compliance monitoring
- Resource utilization tracking
- Automated performance reporting
- Trend analysis and predictions

Key Features:
- Continuous performance metrics collection
- Oxford dual-system performance analysis
- Sakana validation efficiency tracking
- Data requirement detection optimization
- Framework component health monitoring
- Automated alerting for performance issues
- Historical trend analysis
- Performance optimization recommendations

Architecture:
- Metrics Collection: Real-time performance data gathering
- Analysis Engine: Pattern recognition and optimization detection
- Reporting System: Automated performance reports
- Alerting System: Performance issue notifications
- Optimization Engine: Automated performance tuning recommendations
"""

import os
import sys
import json
import logging
import asyncio
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from collections import deque, defaultdict
import statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of performance metrics."""
    SYSTEM_HEALTH = "system_health"
    PROCESSING_TIME = "processing_time"
    VALIDATION_SCORE = "validation_score"
    OXFORD_PERFORMANCE = "oxford_performance"
    SAKANA_PERFORMANCE = "sakana_performance"
    DATA_DETECTION_PERFORMANCE = "data_detection_performance"
    RESOURCE_USAGE = "resource_usage"
    ERROR_RATE = "error_rate"
    THROUGHPUT = "throughput"


class AlertLevel(Enum):
    """Performance alert levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class PerformanceMetric:
    """Individual performance metric data point."""
    metric_type: MetricType
    timestamp: str
    value: float
    unit: str
    component: str
    experiment_id: Optional[str] = None
    domain: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class PerformanceAlert:
    """Performance alert data."""
    alert_id: str
    level: AlertLevel
    metric_type: MetricType
    message: str
    timestamp: str
    component: str
    threshold_value: float
    actual_value: float
    recommendations: List[str]
    resolved: bool = False


@dataclass
class PerformanceReport:
    """Comprehensive performance report."""
    report_id: str
    generation_timestamp: str
    reporting_period: str
    system_health_score: float
    component_performance: Dict[str, Dict[str, Any]]
    oxford_integration_analysis: Dict[str, Any]
    sakana_compliance_analysis: Dict[str, Any]
    optimization_opportunities: List[str]
    performance_trends: Dict[str, Any]
    resource_utilization: Dict[str, Any]
    alerts_summary: Dict[str, Any]
    recommendations: List[str]


class PerformanceMonitor:
    """
    Comprehensive performance monitoring system for Pipeline 2.
    
    Provides real-time monitoring, analysis, and optimization recommendations
    for all Pipeline 2 components including Oxford integration and Sakana compliance.
    """
    
    def __init__(self, 
                 monitoring_interval: int = 60,  # seconds
                 max_history_size: int = 1000,
                 enable_alerting: bool = True,
                 enable_optimization: bool = True):
        """
        Initialize performance monitoring system.
        
        Args:
            monitoring_interval: Interval between metric collections (seconds)
            max_history_size: Maximum number of metrics to keep in memory
            enable_alerting: Enable automated alerting
            enable_optimization: Enable optimization recommendations
        """
        self.monitoring_interval = monitoring_interval
        self.max_history_size = max_history_size
        self.enable_alerting = enable_alerting
        self.enable_optimization = enable_optimization
        
        # Metric storage
        self.metrics_history = deque(maxlen=max_history_size)
        self.component_metrics = defaultdict(lambda: deque(maxlen=100))
        
        # Alert management
        self.active_alerts = []
        self.alert_history = deque(maxlen=500)
        
        # Performance thresholds
        self.performance_thresholds = self._initialize_thresholds()
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread = None
        self.start_time = datetime.now()
        
        # Performance statistics
        self.performance_stats = {
            'total_experiments_monitored': 0,
            'average_processing_time': 0.0,
            'average_validation_score': 0.0,
            'oxford_integration_success_rate': 0.0,
            'sakana_compliance_rate': 0.0,
            'system_uptime_hours': 0.0,
            'alerts_generated': 0,
            'critical_alerts': 0
        }
        
        # Component health tracking
        self.component_health = {
            'oxford_bridge': {'status': 'unknown', 'last_check': None, 'performance_score': 0.0},
            'sakana_bridge': {'status': 'unknown', 'last_check': None, 'performance_score': 0.0},
            'data_detector': {'status': 'unknown', 'last_check': None, 'performance_score': 0.0},
            'unified_framework': {'status': 'unknown', 'last_check': None, 'performance_score': 0.0},
            'validation_engine': {'status': 'unknown', 'last_check': None, 'performance_score': 0.0}
        }
        
        logger.info("📊 Pipeline 2 Performance Monitor initialized")
        logger.info(f"Monitoring interval: {monitoring_interval}s")
        logger.info(f"Alerting: {'ENABLED' if enable_alerting else 'DISABLED'}")
        logger.info(f"Optimization: {'ENABLED' if enable_optimization else 'DISABLED'}")
    
    def _initialize_thresholds(self) -> Dict[MetricType, Dict[str, float]]:
        """Initialize performance thresholds for alerting."""
        return {
            MetricType.PROCESSING_TIME: {
                'warning': 30.0,  # seconds
                'critical': 60.0,
                'emergency': 120.0
            },
            MetricType.VALIDATION_SCORE: {
                'warning': 0.4,   # below this triggers warning
                'critical': 0.3,
                'emergency': 0.2
            },
            MetricType.OXFORD_PERFORMANCE: {
                'warning': 0.6,   # success rate below this
                'critical': 0.4,
                'emergency': 0.2
            },
            MetricType.SAKANA_PERFORMANCE: {
                'warning': 0.7,   # compliance rate below this
                'critical': 0.5,
                'emergency': 0.3
            },
            MetricType.ERROR_RATE: {
                'warning': 0.1,   # 10% error rate
                'critical': 0.2,
                'emergency': 0.3
            },
            MetricType.RESOURCE_USAGE: {
                'warning': 0.7,   # 70% resource usage
                'critical': 0.85,
                'emergency': 0.95
            }
        }
    
    def start_monitoring(self):
        """Start performance monitoring in background thread."""
        if self.monitoring_active:
            logger.warning("Performance monitoring already active")
            return
        
        self.monitoring_active = True
        self.start_time = datetime.now()
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        logger.info("📈 Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring."""
        self.monitoring_active = False
        
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=5.0)
        
        logger.info("📉 Performance monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop running in background thread."""
        while self.monitoring_active:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Update component health
                self._update_component_health()
                
                # Check for alerts
                if self.enable_alerting:
                    self._check_performance_alerts()
                
                # Update statistics
                self._update_performance_statistics()
                
                # Sleep until next monitoring cycle
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval)
    
    def record_experiment_metrics(self, 
                                experiment_session: Any,
                                processing_start_time: datetime,
                                processing_end_time: datetime):
        """
        Record performance metrics from an experiment session.
        
        Args:
            experiment_session: Completed experiment session
            processing_start_time: When processing started
            processing_end_time: When processing completed
        """
        try:
            self.performance_stats['total_experiments_monitored'] += 1
            
            # Processing time metric
            processing_time = (processing_end_time - processing_start_time).total_seconds()
            self._record_metric(
                MetricType.PROCESSING_TIME,
                processing_time,
                "seconds",
                "unified_framework",
                experiment_session.experiment_id,
                experiment_session.domain
            )
            
            # Validation score metric
            if experiment_session.validation_result:
                validation_score = experiment_session.validation_result.overall_score
                self._record_metric(
                    MetricType.VALIDATION_SCORE,
                    validation_score,
                    "score",
                    "validation_engine",
                    experiment_session.experiment_id,
                    experiment_session.domain
                )
            
            # Oxford integration performance
            if experiment_session.oxford_integration_status:
                oxford_success = 1.0 if experiment_session.oxford_integration_status.get('query_successful', False) else 0.0
                self._record_metric(
                    MetricType.OXFORD_PERFORMANCE,
                    oxford_success,
                    "success_rate",
                    "oxford_bridge",
                    experiment_session.experiment_id,
                    experiment_session.domain
                )
            
            # Sakana compliance performance
            if experiment_session.sakana_compliance_status:
                sakana_compliant = 1.0 if experiment_session.sakana_compliance_status.get('compliant', False) else 0.0
                self._record_metric(
                    MetricType.SAKANA_PERFORMANCE,
                    sakana_compliant,
                    "compliance_rate",
                    "sakana_bridge",
                    experiment_session.experiment_id,
                    experiment_session.domain
                )
            
            # Data detection performance
            if experiment_session.data_requirement_analysis:
                data_readiness = experiment_session.data_requirement_analysis.overall_data_readiness
                self._record_metric(
                    MetricType.DATA_DETECTION_PERFORMANCE,
                    data_readiness,
                    "readiness_score",
                    "data_detector",
                    experiment_session.experiment_id,
                    experiment_session.domain
                )
            
            # Error rate
            error_count = len(experiment_session.error_log)
            error_rate = 1.0 if error_count > 0 else 0.0
            self._record_metric(
                MetricType.ERROR_RATE,
                error_rate,
                "error_rate",
                "unified_framework",
                experiment_session.experiment_id,
                experiment_session.domain
            )
            
            logger.info(f"📊 Recorded metrics for experiment {experiment_session.experiment_id}")
            
        except Exception as e:
            logger.error(f"Failed to record experiment metrics: {e}")
    
    def _record_metric(self, 
                      metric_type: MetricType,
                      value: float,
                      unit: str,
                      component: str,
                      experiment_id: Optional[str] = None,
                      domain: Optional[str] = None,
                      metadata: Optional[Dict[str, Any]] = None):
        """Record a performance metric."""
        metric = PerformanceMetric(
            metric_type=metric_type,
            timestamp=datetime.now().isoformat(),
            value=value,
            unit=unit,
            component=component,
            experiment_id=experiment_id,
            domain=domain,
            metadata=metadata or {}
        )
        
        # Add to history
        self.metrics_history.append(metric)
        self.component_metrics[component].append(metric)
        
        # Check for immediate alerts
        if self.enable_alerting:
            self._check_metric_threshold(metric)
    
    def _collect_system_metrics(self):
        """Collect system-level performance metrics."""
        try:
            # System uptime
            uptime_hours = (datetime.now() - self.start_time).total_seconds() / 3600
            self._record_metric(
                MetricType.SYSTEM_HEALTH,
                uptime_hours,
                "hours",
                "system"
            )
            
            # Resource usage (if psutil available)
            try:
                import psutil
                
                # CPU usage
                cpu_percent = psutil.cpu_percent()
                self._record_metric(
                    MetricType.RESOURCE_USAGE,
                    cpu_percent / 100.0,
                    "cpu_utilization",
                    "system"
                )
                
                # Memory usage
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                self._record_metric(
                    MetricType.RESOURCE_USAGE,
                    memory_percent / 100.0,
                    "memory_utilization",
                    "system"
                )
                
            except ImportError:
                # psutil not available - use basic metrics
                self._record_metric(
                    MetricType.RESOURCE_USAGE,
                    0.5,  # Assume moderate usage
                    "estimated_utilization",
                    "system"
                )
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
    
    def _update_component_health(self):
        """Update health status for all components."""
        try:
            current_time = datetime.now().isoformat()
            
            for component in self.component_health.keys():
                # Get recent metrics for this component
                recent_metrics = [m for m in self.component_metrics[component] 
                                if (datetime.now() - datetime.fromisoformat(m.timestamp)).total_seconds() < 300]
                
                if recent_metrics:
                    # Calculate average performance
                    avg_performance = statistics.mean(m.value for m in recent_metrics)
                    
                    # Determine health status
                    if avg_performance >= 0.8:
                        status = "excellent"
                    elif avg_performance >= 0.6:
                        status = "good"
                    elif avg_performance >= 0.4:
                        status = "fair"
                    else:
                        status = "poor"
                    
                    self.component_health[component] = {
                        'status': status,
                        'last_check': current_time,
                        'performance_score': avg_performance
                    }
                else:
                    # No recent metrics - mark as unknown
                    self.component_health[component]['status'] = 'unknown'
                    self.component_health[component]['last_check'] = current_time
            
        except Exception as e:
            logger.error(f"Failed to update component health: {e}")
    
    def _check_performance_alerts(self):
        """Check for performance alerts based on current metrics."""
        try:
            # Check recent metrics for threshold violations
            recent_time = datetime.now() - timedelta(minutes=5)
            recent_metrics = [m for m in self.metrics_history 
                            if datetime.fromisoformat(m.timestamp) > recent_time]
            
            # Group metrics by type
            metrics_by_type = defaultdict(list)
            for metric in recent_metrics:
                metrics_by_type[metric.metric_type].append(metric)
            
            # Check each metric type for alerts
            for metric_type, metrics in metrics_by_type.items():
                if metric_type in self.performance_thresholds:
                    self._check_threshold_alerts(metric_type, metrics)
            
        except Exception as e:
            logger.error(f"Failed to check performance alerts: {e}")
    
    def _check_metric_threshold(self, metric: PerformanceMetric):
        """Check if a single metric violates thresholds."""
        if metric.metric_type not in self.performance_thresholds:
            return
        
        thresholds = self.performance_thresholds[metric.metric_type]
        
        # Determine if this is a "higher is better" or "lower is better" metric
        higher_is_better = metric.metric_type in [
            MetricType.VALIDATION_SCORE, 
            MetricType.OXFORD_PERFORMANCE, 
            MetricType.SAKANA_PERFORMANCE
        ]
        
        alert_level = None
        
        if higher_is_better:
            # For metrics where higher values are better (scores, success rates)
            if metric.value <= thresholds.get('emergency', 0):
                alert_level = AlertLevel.EMERGENCY
            elif metric.value <= thresholds.get('critical', 0):
                alert_level = AlertLevel.CRITICAL
            elif metric.value <= thresholds.get('warning', 0):
                alert_level = AlertLevel.WARNING
        else:
            # For metrics where lower values are better (processing time, error rate)
            if metric.value >= thresholds.get('emergency', float('inf')):
                alert_level = AlertLevel.EMERGENCY
            elif metric.value >= thresholds.get('critical', float('inf')):
                alert_level = AlertLevel.CRITICAL
            elif metric.value >= thresholds.get('warning', float('inf')):
                alert_level = AlertLevel.WARNING
        
        if alert_level:
            self._create_alert(metric, alert_level, thresholds)
    
    def _check_threshold_alerts(self, metric_type: MetricType, metrics: List[PerformanceMetric]):
        """Check for threshold violations in a group of metrics."""
        if not metrics:
            return
        
        # Calculate average value for recent metrics
        avg_value = statistics.mean(m.value for m in metrics)
        
        # Create a representative metric for threshold checking
        representative_metric = PerformanceMetric(
            metric_type=metric_type,
            timestamp=datetime.now().isoformat(),
            value=avg_value,
            unit=metrics[0].unit,
            component=metrics[0].component,
            metadata={'sample_size': len(metrics)}
        )
        
        self._check_metric_threshold(representative_metric)
    
    def _create_alert(self, 
                     metric: PerformanceMetric, 
                     level: AlertLevel, 
                     thresholds: Dict[str, float]):
        """Create a performance alert."""
        alert_id = f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{metric.component}_{metric.metric_type.value}"
        
        # Generate alert message
        message = f"{metric.component} {metric.metric_type.value} {level.value}: {metric.value:.2f} {metric.unit}"
        
        # Generate recommendations based on metric type and level
        recommendations = self._generate_alert_recommendations(metric, level)
        
        alert = PerformanceAlert(
            alert_id=alert_id,
            level=level,
            metric_type=metric.metric_type,
            message=message,
            timestamp=datetime.now().isoformat(),
            component=metric.component,
            threshold_value=thresholds.get(level.value, 0),
            actual_value=metric.value,
            recommendations=recommendations
        )
        
        # Add to active alerts
        self.active_alerts.append(alert)
        self.alert_history.append(alert)
        
        # Update statistics
        self.performance_stats['alerts_generated'] += 1
        if level == AlertLevel.CRITICAL or level == AlertLevel.EMERGENCY:
            self.performance_stats['critical_alerts'] += 1
        
        logger.warning(f"🚨 Performance Alert ({level.value}): {message}")
        
        return alert
    
    def _generate_alert_recommendations(self, 
                                      metric: PerformanceMetric, 
                                      level: AlertLevel) -> List[str]:
        """Generate recommendations for performance alerts."""
        recommendations = []
        
        if metric.metric_type == MetricType.PROCESSING_TIME:
            recommendations.extend([
                "Review experiment complexity and reduce if possible",
                "Check Oxford system response times",
                "Consider parallel processing for validation steps",
                "Monitor system resource availability"
            ])
        
        elif metric.metric_type == MetricType.VALIDATION_SCORE:
            recommendations.extend([
                "Review experiment specifications for completeness",
                "Check data requirement coverage",
                "Verify Oxford integration is providing relevant sources",
                "Consider domain-specific validation enhancements"
            ])
        
        elif metric.metric_type == MetricType.OXFORD_PERFORMANCE:
            recommendations.extend([
                "Check Oxford system connectivity",
                "Verify FAISS database accessibility",
                "Check web search API keys and quotas",
                "Review Solomon orchestration logic"
            ])
        
        elif metric.metric_type == MetricType.SAKANA_PERFORMANCE:
            recommendations.extend([
                "Review real data availability",
                "Check empirical validation criteria",
                "Verify data authenticity requirements",
                "Consider Sakana system integration"
            ])
        
        elif metric.metric_type == MetricType.RESOURCE_USAGE:
            recommendations.extend([
                "Monitor system memory and CPU usage",
                "Consider scaling resources",
                "Review concurrent processing limits",
                "Check for memory leaks in components"
            ])
        
        # Add level-specific recommendations
        if level == AlertLevel.CRITICAL or level == AlertLevel.EMERGENCY:
            recommendations.insert(0, "IMMEDIATE ACTION REQUIRED - Review system status")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _update_performance_statistics(self):
        """Update overall performance statistics."""
        try:
            # Update uptime
            uptime = (datetime.now() - self.start_time).total_seconds() / 3600
            self.performance_stats['system_uptime_hours'] = uptime
            
            # Calculate averages from recent metrics
            recent_time = datetime.now() - timedelta(hours=1)
            recent_metrics = [m for m in self.metrics_history 
                            if datetime.fromisoformat(m.timestamp) > recent_time]
            
            if recent_metrics:
                # Processing time average
                processing_times = [m.value for m in recent_metrics 
                                  if m.metric_type == MetricType.PROCESSING_TIME]
                if processing_times:
                    self.performance_stats['average_processing_time'] = statistics.mean(processing_times)
                
                # Validation score average
                validation_scores = [m.value for m in recent_metrics 
                                   if m.metric_type == MetricType.VALIDATION_SCORE]
                if validation_scores:
                    self.performance_stats['average_validation_score'] = statistics.mean(validation_scores)
                
                # Oxford success rate
                oxford_metrics = [m.value for m in recent_metrics 
                                if m.metric_type == MetricType.OXFORD_PERFORMANCE]
                if oxford_metrics:
                    self.performance_stats['oxford_integration_success_rate'] = statistics.mean(oxford_metrics)
                
                # Sakana compliance rate
                sakana_metrics = [m.value for m in recent_metrics 
                                if m.metric_type == MetricType.SAKANA_PERFORMANCE]
                if sakana_metrics:
                    self.performance_stats['sakana_compliance_rate'] = statistics.mean(sakana_metrics)
            
        except Exception as e:
            logger.error(f"Failed to update performance statistics: {e}")
    
    def generate_performance_report(self, period_hours: int = 24) -> PerformanceReport:
        """
        Generate comprehensive performance report.
        
        Args:
            period_hours: Reporting period in hours
            
        Returns:
            PerformanceReport with comprehensive analysis
        """
        try:
            report_start_time = datetime.now() - timedelta(hours=period_hours)
            period_metrics = [m for m in self.metrics_history 
                            if datetime.fromisoformat(m.timestamp) > report_start_time]
            
            # Generate report
            report = PerformanceReport(
                report_id=f"perf_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                generation_timestamp=datetime.now().isoformat(),
                reporting_period=f"{period_hours} hours",
                system_health_score=self._calculate_system_health_score(period_metrics),
                component_performance=self._analyze_component_performance(period_metrics),
                oxford_integration_analysis=self._analyze_oxford_integration(period_metrics),
                sakana_compliance_analysis=self._analyze_sakana_compliance(period_metrics),
                optimization_opportunities=self._identify_optimization_opportunities(period_metrics),
                performance_trends=self._analyze_performance_trends(period_metrics),
                resource_utilization=self._analyze_resource_utilization(period_metrics),
                alerts_summary=self._generate_alerts_summary(period_hours),
                recommendations=self._generate_performance_recommendations(period_metrics)
            )
            
            logger.info(f"📋 Performance report generated: {report.report_id}")
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate performance report: {e}")
            # Return minimal report
            return PerformanceReport(
                report_id="error_report",
                generation_timestamp=datetime.now().isoformat(),
                reporting_period=f"{period_hours} hours",
                system_health_score=0.0,
                component_performance={},
                oxford_integration_analysis={},
                sakana_compliance_analysis={},
                optimization_opportunities=[],
                performance_trends={},
                resource_utilization={},
                alerts_summary={},
                recommendations=[f"Error generating report: {str(e)}"]
            )
    
    def _calculate_system_health_score(self, metrics: List[PerformanceMetric]) -> float:
        """Calculate overall system health score."""
        if not metrics:
            return 0.0
        
        health_factors = []
        
        # Processing time health (faster is better)
        processing_times = [m.value for m in metrics if m.metric_type == MetricType.PROCESSING_TIME]
        if processing_times:
            avg_time = statistics.mean(processing_times)
            # Score based on processing time (30s = 1.0, 60s = 0.5, 120s+ = 0.0)
            time_score = max(0.0, min(1.0, (120 - avg_time) / 90))
            health_factors.append(time_score)
        
        # Validation score health
        validation_scores = [m.value for m in metrics if m.metric_type == MetricType.VALIDATION_SCORE]
        if validation_scores:
            health_factors.append(statistics.mean(validation_scores))
        
        # Error rate health (lower is better)
        error_rates = [m.value for m in metrics if m.metric_type == MetricType.ERROR_RATE]
        if error_rates:
            avg_error_rate = statistics.mean(error_rates)
            error_score = max(0.0, 1.0 - avg_error_rate)
            health_factors.append(error_score)
        
        # Oxford integration health
        oxford_performance = [m.value for m in metrics if m.metric_type == MetricType.OXFORD_PERFORMANCE]
        if oxford_performance:
            health_factors.append(statistics.mean(oxford_performance))
        
        return statistics.mean(health_factors) if health_factors else 0.5
    
    def _analyze_component_performance(self, metrics: List[PerformanceMetric]) -> Dict[str, Dict[str, Any]]:
        """Analyze performance by component."""
        component_analysis = {}
        
        # Group metrics by component
        component_metrics = defaultdict(list)
        for metric in metrics:
            component_metrics[metric.component].append(metric)
        
        for component, comp_metrics in component_metrics.items():
            if comp_metrics:
                # Calculate component statistics
                values = [m.value for m in comp_metrics]
                component_analysis[component] = {
                    'total_metrics': len(comp_metrics),
                    'average_performance': statistics.mean(values),
                    'best_performance': max(values),
                    'worst_performance': min(values),
                    'performance_std': statistics.stdev(values) if len(values) > 1 else 0.0,
                    'health_status': self.component_health.get(component, {}).get('status', 'unknown')
                }
        
        return component_analysis
    
    def _analyze_oxford_integration(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Analyze Oxford integration performance."""
        oxford_metrics = [m for m in metrics if m.metric_type == MetricType.OXFORD_PERFORMANCE]
        
        if not oxford_metrics:
            return {'status': 'no_data', 'message': 'No Oxford integration metrics available'}
        
        success_rate = statistics.mean(m.value for m in oxford_metrics)
        
        return {
            'success_rate': success_rate,
            'total_queries': len(oxford_metrics),
            'status': 'excellent' if success_rate >= 0.8 else 'good' if success_rate >= 0.6 else 'needs_improvement',
            'faiss_system_performance': 'estimated_good',  # Would need more detailed metrics
            'web_search_performance': 'estimated_good',
            'solomon_orchestration_performance': 'estimated_good'
        }
    
    def _analyze_sakana_compliance(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Analyze Sakana compliance performance."""
        sakana_metrics = [m for m in metrics if m.metric_type == MetricType.SAKANA_PERFORMANCE]
        
        if not sakana_metrics:
            return {'status': 'no_data', 'message': 'No Sakana compliance metrics available'}
        
        compliance_rate = statistics.mean(m.value for m in sakana_metrics)
        
        return {
            'compliance_rate': compliance_rate,
            'total_validations': len(sakana_metrics),
            'status': 'excellent' if compliance_rate >= 0.8 else 'good' if compliance_rate >= 0.6 else 'needs_improvement',
            'real_data_availability': 'estimated_good',  # Would need more detailed metrics
            'empirical_validation_effectiveness': 'estimated_good'
        }
    
    def _identify_optimization_opportunities(self, metrics: List[PerformanceMetric]) -> List[str]:
        """Identify optimization opportunities from metrics."""
        opportunities = []
        
        # Processing time optimization
        processing_times = [m.value for m in metrics if m.metric_type == MetricType.PROCESSING_TIME]
        if processing_times and statistics.mean(processing_times) > 45:
            opportunities.append("Optimize processing time - average exceeds 45 seconds")
        
        # Validation score optimization
        validation_scores = [m.value for m in metrics if m.metric_type == MetricType.VALIDATION_SCORE]
        if validation_scores and statistics.mean(validation_scores) < 0.7:
            opportunities.append("Improve validation accuracy - scores below optimal range")
        
        # Oxford integration optimization
        oxford_performance = [m.value for m in metrics if m.metric_type == MetricType.OXFORD_PERFORMANCE]
        if oxford_performance and statistics.mean(oxford_performance) < 0.8:
            opportunities.append("Optimize Oxford integration - success rate below 80%")
        
        # Error rate optimization
        error_rates = [m.value for m in metrics if m.metric_type == MetricType.ERROR_RATE]
        if error_rates and statistics.mean(error_rates) > 0.05:
            opportunities.append("Reduce error rate - current rate above 5%")
        
        return opportunities
    
    def _analyze_performance_trends(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Analyze performance trends over time."""
        if len(metrics) < 10:
            return {'status': 'insufficient_data'}
        
        trends = {}
        
        # Analyze trends by metric type
        for metric_type in MetricType:
            type_metrics = [m for m in metrics if m.metric_type == metric_type]
            if len(type_metrics) >= 5:
                values = [m.value for m in type_metrics]
                
                # Simple trend calculation (comparing first half to second half)
                mid_point = len(values) // 2
                first_half_avg = statistics.mean(values[:mid_point])
                second_half_avg = statistics.mean(values[mid_point:])
                
                if second_half_avg > first_half_avg * 1.1:
                    trend = 'improving'
                elif second_half_avg < first_half_avg * 0.9:
                    trend = 'declining'
                else:
                    trend = 'stable'
                
                trends[metric_type.value] = {
                    'trend': trend,
                    'change_percentage': ((second_half_avg - first_half_avg) / first_half_avg) * 100
                }
        
        return trends
    
    def _analyze_resource_utilization(self, metrics: List[PerformanceMetric]) -> Dict[str, Any]:
        """Analyze resource utilization patterns."""
        resource_metrics = [m for m in metrics if m.metric_type == MetricType.RESOURCE_USAGE]
        
        if not resource_metrics:
            return {'status': 'no_data'}
        
        utilization_values = [m.value for m in resource_metrics]
        
        return {
            'average_utilization': statistics.mean(utilization_values),
            'peak_utilization': max(utilization_values),
            'utilization_variance': statistics.stdev(utilization_values) if len(utilization_values) > 1 else 0.0,
            'status': 'optimal' if statistics.mean(utilization_values) < 0.7 else 'high' if statistics.mean(utilization_values) < 0.9 else 'critical'
        }
    
    def _generate_alerts_summary(self, period_hours: int) -> Dict[str, Any]:
        """Generate summary of alerts for the reporting period."""
        period_start = datetime.now() - timedelta(hours=period_hours)
        period_alerts = [a for a in self.alert_history 
                        if datetime.fromisoformat(a.timestamp) > period_start]
        
        if not period_alerts:
            return {'total_alerts': 0, 'status': 'no_alerts'}
        
        alert_counts = defaultdict(int)
        for alert in period_alerts:
            alert_counts[alert.level.value] += 1
        
        return {
            'total_alerts': len(period_alerts),
            'alert_breakdown': dict(alert_counts),
            'critical_alerts': alert_counts['critical'] + alert_counts['emergency'],
            'active_alerts': len([a for a in period_alerts if not a.resolved])
        }
    
    def _generate_performance_recommendations(self, metrics: List[PerformanceMetric]) -> List[str]:
        """Generate performance recommendations based on analysis."""
        recommendations = []
        
        # General recommendations based on metrics
        if not metrics:
            recommendations.append("Insufficient performance data - ensure monitoring is active")
            return recommendations
        
        # Processing time recommendations
        processing_times = [m.value for m in metrics if m.metric_type == MetricType.PROCESSING_TIME]
        if processing_times and statistics.mean(processing_times) > 30:
            recommendations.append("Consider optimizing processing pipeline for faster execution")
        
        # Oxford integration recommendations
        oxford_metrics = [m.value for m in metrics if m.metric_type == MetricType.OXFORD_PERFORMANCE]
        if oxford_metrics and statistics.mean(oxford_metrics) < 0.8:
            recommendations.append("Review Oxford system integration and optimize query performance")
        
        # Validation score recommendations
        validation_scores = [m.value for m in metrics if m.metric_type == MetricType.VALIDATION_SCORE]
        if validation_scores and statistics.mean(validation_scores) < 0.6:
            recommendations.append("Enhance validation framework to improve experiment assessment quality")
        
        # Error rate recommendations
        error_rates = [m.value for m in metrics if m.metric_type == MetricType.ERROR_RATE]
        if error_rates and statistics.mean(error_rates) > 0.1:
            recommendations.append("Investigate and resolve sources of errors in the processing pipeline")
        
        # Component health recommendations
        poor_components = [comp for comp, health in self.component_health.items() 
                          if health.get('status') in ['poor', 'unknown']]
        if poor_components:
            recommendations.append(f"Review and optimize components: {', '.join(poor_components)}")
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current performance monitoring status."""
        return {
            'monitoring_active': self.monitoring_active,
            'monitoring_uptime_hours': (datetime.now() - self.start_time).total_seconds() / 3600,
            'total_metrics_collected': len(self.metrics_history),
            'active_alerts': len(self.active_alerts),
            'component_health': self.component_health.copy(),
            'performance_statistics': self.performance_stats.copy(),
            'last_update': datetime.now().isoformat()
        }
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved."""
        for alert in self.active_alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                self.active_alerts.remove(alert)
                logger.info(f"✅ Alert resolved: {alert_id}")
                return True
        return False
    
    def get_active_alerts(self) -> List[PerformanceAlert]:
        """Get list of active alerts."""
        return [alert for alert in self.active_alerts if not alert.resolved]
    
    def cleanup_old_data(self, max_age_hours: int = 168):  # 1 week default
        """Clean up old performance data."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        # Clean metrics history
        self.metrics_history = deque([m for m in self.metrics_history 
                                    if datetime.fromisoformat(m.timestamp) > cutoff_time],
                                   maxlen=self.max_history_size)
        
        # Clean component metrics
        for component in self.component_metrics:
            self.component_metrics[component] = deque([m for m in self.component_metrics[component]
                                                     if datetime.fromisoformat(m.timestamp) > cutoff_time],
                                                    maxlen=100)
        
        # Clean alert history
        self.alert_history = deque([a for a in self.alert_history 
                                  if datetime.fromisoformat(a.timestamp) > cutoff_time],
                                 maxlen=500)
        
        logger.info(f"🧹 Cleaned performance data older than {max_age_hours} hours")


# Convenience functions for Pipeline 2 integration
def create_performance_monitor(monitoring_interval: int = 60) -> PerformanceMonitor:
    """Create performance monitor for Pipeline 2."""
    return PerformanceMonitor(monitoring_interval=monitoring_interval)

def start_pipeline2_monitoring(monitoring_interval: int = 60) -> PerformanceMonitor:
    """
    Start Pipeline 2 performance monitoring.
    
    Usage:
    from .performance_monitor import start_pipeline2_monitoring
    monitor = start_pipeline2_monitoring()
    """
    monitor = create_performance_monitor(monitoring_interval)
    monitor.start_monitoring()
    return monitor

def get_performance_snapshot() -> Dict[str, Any]:
    """
    Get quick performance snapshot.
    
    Usage:
    from .performance_monitor import get_performance_snapshot
    snapshot = get_performance_snapshot()
    """
    monitor = create_performance_monitor()
    return monitor.get_current_status()