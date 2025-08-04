# Amazon Redshift Dense Compute Node

## Overview

Amazon Redshift Dense Compute (DC) nodes are optimized for performance-intensive workloads with fast CPUs, large amounts of RAM, and solid-state drives (SSDs). DC nodes are ideal for workloads that require high performance and don't need massive amounts of storage. They provide the best price-performance for data warehouses that prioritize query speed over storage capacity.

## Main Functions

### High-Performance Computing
- **Fast SSD Storage**: Local SSD storage for maximum I/O performance
- **High CPU Performance**: Optimized processors for complex analytical queries
- **Large Memory**: Substantial RAM for in-memory processing and caching
- **Low Latency**: Minimal query response times for interactive analytics

### Workload Optimization
- **OLAP Workloads**: Optimized for online analytical processing
- **Complex Queries**: Handles sophisticated analytical queries efficiently
- **Concurrent Users**: Supports multiple concurrent analytical sessions
- **Real-time Analytics**: Fast response times for real-time dashboards

### Scalability Features
- **Elastic Resize**: Scale cluster size without downtime
- **Concurrency Scaling**: Automatic scaling for concurrent queries
- **Performance Monitoring**: Built-in performance metrics and optimization
- **Workload Management**: Advanced query queue management

## Use Cases

### High-Performance Analytics Platform
```python
import boto3
import psycopg2
from datetime import datetime, timedelta
import time

class RedshiftDCClusterManager:
    def __init__(self):
        self.redshift = boto3.client('redshift')
        self.cloudwatch = boto3.client('cloudwatch')
    
    def create_dc_cluster(self, cluster_identifier, node_type='dc2.large', num_nodes=2):
        """Create Dense Compute Redshift cluster"""
        try:
            response = self.redshift.create_cluster(
                ClusterIdentifier=cluster_identifier,
                NodeType=node_type,
                MasterUsername='admin',
                MasterUserPassword='SecurePassword123!',
                DBName='analytics',
                NumberOfNodes=num_nodes,
                ClusterType='multi-node' if num_nodes > 1 else 'single-node',
                VpcSecurityGroupIds=['sg-12345678'],
                ClusterSubnetGroupName='redshift-subnet-group',
                PubliclyAccessible=False,
                Encrypted=True,
                KmsKeyId='arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012',
                EnhancedVpcRouting=True,
                ClusterParameterGroupName='high-performance-params',
                Tags=[
                    {
                        'Key': 'Environment',
                        'Value': 'Production'
                    },
                    {
                        'Key': 'NodeType',
                        'Value': 'DenseCompute'
                    }
                ]
            )
            print(f"DC cluster creation initiated: {cluster_identifier}")
            return response
        except Exception as e:
            print(f"Error creating DC cluster: {e}")
    
    def optimize_for_performance(self, cluster_identifier):
        """Configure cluster for optimal performance"""
        try:
            # Create custom parameter group for performance
            param_group_response = self.redshift.create_cluster_parameter_group(
                ParameterGroupName='dc-performance-optimized',
                ParameterGroupFamily='redshift-1.0',
                Description='Optimized parameters for DC nodes'
            )
            
            # Set performance parameters
            performance_params = [
                {
                    'ParameterName': 'wlm_json_configuration',
                    'ParameterValue': '''[
                        {
                            "query_group": "dashboard",
                            "query_group_wild_card": 0,
                            "query_concurrency": 5,
                            "memory_percent_to_use": 30,
                            "max_execution_time": 300000
                        },
                        {
                            "query_group": "etl",
                            "query_group_wild_card": 0,
                            "query_concurrency": 2,
                            "memory_percent_to_use": 60,
                            "max_execution_time": 1800000
                        },
                        {
                            "query_concurrency": 3,
                            "memory_percent_to_use": 10
                        }
                    ]'''
                },
                {
                    'ParameterName': 'enable_result_cache_for_session',
                    'ParameterValue': 'true'
                },
                {
                    'ParameterName': 'max_cursor_result_set_size',
                    'ParameterValue': '1000'
                }
            ]
            
            for param in performance_params:
                self.redshift.modify_cluster_parameter_group(
                    ParameterGroupName='dc-performance-optimized',
                    Parameters=[param]
                )
            
            # Apply parameter group to cluster
            self.redshift.modify_cluster(
                ClusterIdentifier=cluster_identifier,
                ClusterParameterGroupName='dc-performance-optimized',
                ApplyImmediately=True
            )
            
            print(f"Performance optimization applied to {cluster_identifier}")
            
        except Exception as e:
            print(f"Error optimizing cluster performance: {e}")
    
    def monitor_dc_performance(self, cluster_identifier):
        """Monitor DC cluster performance metrics"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=1)
            
            # Get CPU utilization
            cpu_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Redshift',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'ClusterIdentifier',
                        'Value': cluster_identifier
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum']
            )
            
            # Get query performance metrics
            query_duration_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Redshift',
                MetricName='QueryDuration',
                Dimensions=[
                    {
                        'Name': 'ClusterIdentifier',
                        'Value': cluster_identifier
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum']
            )
            
            # Get concurrent connections
            connections_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Redshift',
                MetricName='DatabaseConnections',
                Dimensions=[
                    {
                        'Name': 'ClusterIdentifier',
                        'Value': cluster_identifier
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum']
            )
            
            performance_metrics = {
                'cpu_utilization': cpu_response['Datapoints'],
                'query_duration': query_duration_response['Datapoints'],
                'database_connections': connections_response['Datapoints']
            }
            
            return performance_metrics
            
        except Exception as e:
            print(f"Error monitoring DC performance: {e}")
    
    def implement_concurrency_scaling(self, cluster_identifier):
        """Enable and configure concurrency scaling"""
        try:
            # Enable concurrency scaling
            response = self.redshift.modify_cluster(
                ClusterIdentifier=cluster_identifier,
                ConcurrencyScalingMode='auto'
            )
            
            # Create usage limit for concurrency scaling
            usage_limit_response = self.redshift.create_usage_limit(
                ClusterIdentifier=cluster_identifier,
                FeatureType='concurrency-scaling',
                LimitType='time',
                Amount=60,  # 60 minutes per day
                Period='daily',
                BreachAction='log'
            )
            
            print(f"Concurrency scaling enabled for {cluster_identifier}")
            return response
            
        except Exception as e:
            print(f"Error implementing concurrency scaling: {e}")

# Usage example
dc_manager = RedshiftDCClusterManager()

# Create DC cluster
dc_manager.create_dc_cluster(
    cluster_identifier='analytics-dc-cluster',
    node_type='dc2.8xlarge',
    num_nodes=4
)

# Optimize for performance
dc_manager.optimize_for_performance('analytics-dc-cluster')

# Enable concurrency scaling
dc_manager.implement_concurrency_scaling('analytics-dc-cluster')

# Monitor performance
performance_data = dc_manager.monitor_dc_performance('analytics-dc-cluster')
print("Performance metrics:", performance_data)
```

### Interactive Analytics Workbench
```python
import psycopg2
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

class DCInteractiveAnalytics:
    def __init__(self, cluster_endpoint, database, username, password):
        self.connection = psycopg2.connect(
            host=cluster_endpoint,
            database=database,
            user=username,
            password=password,
            port=5439
        )
        self.connection.set_session(autocommit=True)
    
    def create_optimized_tables(self):
        """Create tables optimized for DC nodes"""
        cursor = self.connection.cursor()
        
        # Create fact table with optimal distribution
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_fact_dc (
                sale_id BIGINT IDENTITY(1,1),
                customer_id INTEGER,
                product_id INTEGER,
                sale_date DATE,
                quantity INTEGER,
                unit_price DECIMAL(10,2),
                total_amount DECIMAL(12,2),
                region_id INTEGER
            )
            DISTSTYLE KEY
            DISTKEY(customer_id)
            SORTKEY(sale_date, customer_id)
            ENCODE AUTO;
        """)
        
        # Create dimension table for fast joins
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_dim_dc (
                customer_id INTEGER PRIMARY KEY,
                customer_name VARCHAR(255),
                email VARCHAR(255),
                segment VARCHAR(50),
                registration_date DATE
            )
            DISTSTYLE ALL
            SORTKEY(customer_id)
            ENCODE AUTO;
        """)
        
        print("Optimized tables created for DC nodes")
    
    def execute_interactive_query(self, query, params=None):
        """Execute query optimized for interactive performance"""
        start_time = datetime.now()
        
        try:
            df = pd.read_sql_query(query, self.connection, params=params)
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            print(f"Query executed in {execution_time:.2f} seconds")
            print(f"Returned {len(df)} rows")
            
            return df, execution_time
            
        except Exception as e:
            print(f"Error executing query: {e}")
            return None, None
    
    def real_time_dashboard_queries(self):
        """Execute real-time dashboard queries"""
        queries = {
            'daily_sales': """
                SELECT 
                    sale_date,
                    COUNT(*) as transaction_count,
                    SUM(total_amount) as daily_revenue,
                    AVG(total_amount) as avg_order_value
                FROM sales_fact_dc
                WHERE sale_date >= CURRENT_DATE - 30
                GROUP BY 1
                ORDER BY 1;
            """,
            
            'top_customers': """
                SELECT 
                    c.customer_name,
                    COUNT(s.sale_id) as purchase_count,
                    SUM(s.total_amount) as total_spent,
                    MAX(s.sale_date) as last_purchase
                FROM sales_fact_dc s
                JOIN customer_dim_dc c ON s.customer_id = c.customer_id
                WHERE s.sale_date >= CURRENT_DATE - 90
                GROUP BY 1
                ORDER BY 3 DESC
                LIMIT 20;
            """,
            
            'hourly_trends': """
                SELECT 
                    EXTRACT(hour FROM GETDATE()) as current_hour,
                    COUNT(*) as current_hour_sales,
                    SUM(total_amount) as current_hour_revenue
                FROM sales_fact_dc
                WHERE sale_date = CURRENT_DATE
                    AND EXTRACT(hour FROM created_at) = EXTRACT(hour FROM GETDATE())
                GROUP BY 1;
            """
        }
        
        results = {}
        total_time = 0
        
        for query_name, sql in queries.items():
            df, exec_time = self.execute_interactive_query(sql)
            if df is not None:
                results[query_name] = df
                total_time += exec_time
        
        print(f"All dashboard queries completed in {total_time:.2f} seconds")
        return results
    
    def performance_analysis(self):
        """Analyze query performance on DC nodes"""
        cursor = self.connection.cursor()
        
        # Get recent query performance
        cursor.execute("""
            SELECT 
                query,
                starttime,
                endtime,
                DATEDIFF(milliseconds, starttime, endtime) as duration_ms,
                rows,
                bytes,
                cpu_time,
                blocks_read,
                blocks_skipped
            FROM stl_query
            WHERE starttime >= GETDATE() - INTERVAL '1 hour'
                AND userid > 1
            ORDER BY duration_ms DESC
            LIMIT 20;
        """)
        
        performance_data = cursor.fetchall()
        
        # Analyze table statistics
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                size,
                tbl_rows,
                skew_sortkey1,
                skew_rows,
                estimated_visible_rows
            FROM svv_table_info
            WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
            ORDER BY size DESC;
        """)
        
        table_stats = cursor.fetchall()
        
        return {
            'query_performance': performance_data,
            'table_statistics': table_stats
        }

# Usage example
dc_analytics = DCInteractiveAnalytics(
    cluster_endpoint='analytics-dc-cluster.abc123.us-east-1.redshift.amazonaws.com',
    database='analytics',
    username='admin',
    password='SecurePassword123!'
)

# Setup optimized tables
dc_analytics.create_optimized_tables()

# Execute real-time dashboard queries
dashboard_results = dc_analytics.real_time_dashboard_queries()

# Analyze performance
performance_analysis = dc_analytics.performance_analysis()
```

## Architecture Diagram

![Redshift Dense Compute Node Architecture](/img/aws-analytics/redshift-dense-compute-node.png)

## Node Type Specifications

### DC2 Instance Types
- **dc2.large**: 2 vCPUs, 15 GB RAM, 160 GB SSD
- **dc2.8xlarge**: 32 vCPUs, 244 GB RAM, 2,560 GB SSD

### Performance Characteristics
- **Storage**: Local SSD storage for maximum I/O performance
- **Network**: Enhanced networking for low latency
- **Memory**: High memory-to-vCPU ratio for analytical workloads
- **CPU**: Optimized processors for complex calculations

## Best Practices

### Performance Optimization
- Use appropriate distribution keys for even data distribution
- Implement effective sort keys for query performance
- Optimize table design for analytical workloads
- Use result caching for frequently accessed data
- Monitor and tune workload management queues

### Cost Management
- Right-size clusters based on performance requirements
- Use Reserved Instances for predictable workloads
- Implement pause/resume for development environments
- Monitor usage patterns and optimize accordingly
- Consider migration to RA3 nodes for growing datasets

### Workload Management
- Configure WLM queues for different user groups
- Set appropriate memory allocation per queue
- Implement query monitoring rules
- Use concurrency scaling for peak loads
- Monitor queue wait times and adjust as needed

## When to Choose DC Nodes

### Ideal Scenarios
- Performance-critical analytical workloads
- Interactive dashboards and real-time analytics
- Workloads with high query concurrency
- Applications requiring sub-second response times
- Datasets that fit within local SSD storage limits

### Migration Considerations
- Evaluate storage requirements vs. performance needs
- Consider RA3 nodes for larger datasets
- Plan for data growth and future scalability
- Assess cost implications of different node types
- Test performance with representative workloads
