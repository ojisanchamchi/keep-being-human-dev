# Amazon Redshift

## Overview

Amazon Redshift is a fast, fully managed, petabyte-scale data warehouse service that makes it simple and cost-effective to analyze all your data using your existing business intelligence tools. Redshift delivers fast query performance by using columnar storage technology to improve I/O efficiency and parallelizing queries across multiple nodes. It's designed to handle analytic workloads on big data sets stored by a column-oriented DBMS principle.

## Main Functions

### Data Warehousing
- **Columnar Storage**: Optimized for analytical queries with columnar data storage
- **Massively Parallel Processing (MPP)**: Distributes queries across multiple nodes
- **Automatic Compression**: Reduces storage requirements and improves performance
- **Result Caching**: Caches query results for faster subsequent queries

### Scalability and Performance
- **Elastic Resize**: Scale cluster up or down without downtime
- **Concurrency Scaling**: Automatically adds capacity for concurrent queries
- **Workload Management (WLM)**: Manages query queues and resource allocation
- **Materialized Views**: Pre-computed results for faster query performance

### Data Integration
- **COPY Command**: High-performance data loading from S3, DynamoDB, and other sources
- **Federated Queries**: Query data across Redshift, S3, and RDS without moving data
- **Data Sharing**: Share live data across Redshift clusters
- **Streaming Ingestion**: Real-time data ingestion from Kinesis Data Streams

### Security and Compliance
- **Encryption**: Data encryption at rest and in transit
- **VPC Integration**: Network isolation and security
- **IAM Integration**: Fine-grained access control
- **Audit Logging**: Comprehensive logging and monitoring

## Use Cases

### Enterprise Data Warehouse
```python
import boto3
import psycopg2
from datetime import datetime, timedelta
import pandas as pd

class RedshiftDataWarehouse:
    def __init__(self, cluster_endpoint, database, username, password, port=5439):
        self.cluster_endpoint = cluster_endpoint
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.redshift_client = boto3.client('redshift')
        self.connection = None
    
    def connect(self):
        """Establish connection to Redshift cluster"""
        try:
            self.connection = psycopg2.connect(
                host=self.cluster_endpoint,
                database=self.database,
                user=self.username,
                password=self.password,
                port=self.port
            )
            print("Connected to Redshift cluster")
        except Exception as e:
            print(f"Error connecting to Redshift: {e}")
    
    def create_schema_and_tables(self):
        """Create data warehouse schema and tables"""
        try:
            cursor = self.connection.cursor()
            
            # Create schema
            cursor.execute("CREATE SCHEMA IF NOT EXISTS analytics;")
            
            # Create dimension tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics.dim_customer (
                    customer_id INTEGER PRIMARY KEY,
                    customer_name VARCHAR(255),
                    email VARCHAR(255),
                    registration_date DATE,
                    customer_segment VARCHAR(50),
                    geography_id INTEGER
                ) DISTSTYLE KEY DISTKEY(customer_id);
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics.dim_product (
                    product_id INTEGER PRIMARY KEY,
                    product_name VARCHAR(255),
                    category VARCHAR(100),
                    subcategory VARCHAR(100),
                    brand VARCHAR(100),
                    unit_price DECIMAL(10,2)
                ) DISTSTYLE ALL;
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics.dim_date (
                    date_id INTEGER PRIMARY KEY,
                    full_date DATE,
                    year INTEGER,
                    quarter INTEGER,
                    month INTEGER,
                    day INTEGER,
                    day_of_week INTEGER,
                    is_weekend BOOLEAN
                ) DISTSTYLE ALL;
            """)
            
            # Create fact table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics.fact_sales (
                    sale_id BIGINT IDENTITY(1,1) PRIMARY KEY,
                    customer_id INTEGER,
                    product_id INTEGER,
                    date_id INTEGER,
                    quantity INTEGER,
                    unit_price DECIMAL(10,2),
                    total_amount DECIMAL(12,2),
                    discount_amount DECIMAL(10,2),
                    tax_amount DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT GETDATE()
                ) 
                DISTSTYLE KEY 
                DISTKEY(customer_id)
                SORTKEY(date_id, created_at);
            """)
            
            self.connection.commit()
            print("Schema and tables created successfully")
            
        except Exception as e:
            print(f"Error creating schema and tables: {e}")
            self.connection.rollback()
    
    def load_data_from_s3(self, table_name, s3_path, iam_role_arn):
        """Load data from S3 using COPY command"""
        try:
            cursor = self.connection.cursor()
            
            copy_command = f"""
                COPY {table_name}
                FROM '{s3_path}'
                IAM_ROLE '{iam_role_arn}'
                FORMAT AS PARQUET
                COMPUPDATE ON
                STATUPDATE ON;
            """
            
            cursor.execute(copy_command)
            self.connection.commit()
            
            # Get load statistics
            cursor.execute("""
                SELECT 
                    filename,
                    lines_scanned,
                    lines_skipped,
                    load_time
                FROM stl_load_commits 
                WHERE query = pg_last_copy_id()
                ORDER BY starttime DESC;
            """)
            
            results = cursor.fetchall()
            print(f"Data loaded successfully into {table_name}")
            for row in results:
                print(f"File: {row[0]}, Lines: {row[1]}, Time: {row[3]}s")
                
        except Exception as e:
            print(f"Error loading data from S3: {e}")
            self.connection.rollback()
    
    def create_materialized_view(self):
        """Create materialized view for common aggregations"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                CREATE MATERIALIZED VIEW analytics.mv_monthly_sales AS
                SELECT 
                    dd.year,
                    dd.month,
                    dp.category,
                    dp.brand,
                    COUNT(*) as transaction_count,
                    SUM(fs.quantity) as total_quantity,
                    SUM(fs.total_amount) as total_revenue,
                    AVG(fs.total_amount) as avg_order_value,
                    COUNT(DISTINCT fs.customer_id) as unique_customers
                FROM analytics.fact_sales fs
                JOIN analytics.dim_date dd ON fs.date_id = dd.date_id
                JOIN analytics.dim_product dp ON fs.product_id = dp.product_id
                GROUP BY 1, 2, 3, 4;
            """)
            
            self.connection.commit()
            print("Materialized view created successfully")
            
        except Exception as e:
            print(f"Error creating materialized view: {e}")
            self.connection.rollback()
    
    def analyze_sales_performance(self):
        """Analyze sales performance with complex queries"""
        try:
            cursor = self.connection.cursor()
            
            # Monthly revenue trend
            cursor.execute("""
                SELECT 
                    dd.year,
                    dd.month,
                    SUM(fs.total_amount) as monthly_revenue,
                    LAG(SUM(fs.total_amount)) OVER (ORDER BY dd.year, dd.month) as prev_month_revenue,
                    (SUM(fs.total_amount) - LAG(SUM(fs.total_amount)) OVER (ORDER BY dd.year, dd.month)) / 
                    LAG(SUM(fs.total_amount)) OVER (ORDER BY dd.year, dd.month) * 100 as growth_rate
                FROM analytics.fact_sales fs
                JOIN analytics.dim_date dd ON fs.date_id = dd.date_id
                WHERE dd.full_date >= CURRENT_DATE - INTERVAL '12 months'
                GROUP BY 1, 2
                ORDER BY 1, 2;
            """)
            
            monthly_trends = cursor.fetchall()
            
            # Customer segmentation analysis
            cursor.execute("""
                WITH customer_metrics AS (
                    SELECT 
                        fs.customer_id,
                        COUNT(*) as transaction_count,
                        SUM(fs.total_amount) as total_spent,
                        AVG(fs.total_amount) as avg_order_value,
                        MAX(dd.full_date) as last_purchase_date,
                        DATEDIFF(day, MAX(dd.full_date), CURRENT_DATE) as days_since_last_purchase
                    FROM analytics.fact_sales fs
                    JOIN analytics.dim_date dd ON fs.date_id = dd.date_id
                    GROUP BY 1
                )
                SELECT 
                    CASE 
                        WHEN total_spent >= 1000 AND days_since_last_purchase <= 30 THEN 'High Value Active'
                        WHEN total_spent >= 1000 AND days_since_last_purchase > 30 THEN 'High Value Inactive'
                        WHEN total_spent < 1000 AND days_since_last_purchase <= 30 THEN 'Low Value Active'
                        ELSE 'Low Value Inactive'
                    END as customer_segment,
                    COUNT(*) as customer_count,
                    AVG(total_spent) as avg_customer_value,
                    AVG(transaction_count) as avg_transactions
                FROM customer_metrics
                GROUP BY 1
                ORDER BY 3 DESC;
            """)
            
            segmentation_results = cursor.fetchall()
            
            return {
                'monthly_trends': monthly_trends,
                'customer_segmentation': segmentation_results
            }
            
        except Exception as e:
            print(f"Error analyzing sales performance: {e}")

# Usage example
redshift_dw = RedshiftDataWarehouse(
    cluster_endpoint='my-redshift-cluster.abc123.us-east-1.redshift.amazonaws.com',
    database='analytics_db',
    username='admin',
    password='secure_password'
)

# Connect and setup
redshift_dw.connect()
redshift_dw.create_schema_and_tables()

# Load data from S3
redshift_dw.load_data_from_s3(
    table_name='analytics.fact_sales',
    s3_path='s3://my-data-bucket/sales-data/',
    iam_role_arn='arn:aws:iam::123456789012:role/RedshiftRole'
)

# Create materialized view for performance
redshift_dw.create_materialized_view()

# Analyze performance
results = redshift_dw.analyze_sales_performance()
```

### Real-time Analytics with Streaming
```python
import boto3
import json
from datetime import datetime

class RedshiftStreamingAnalytics:
    def __init__(self):
        self.redshift_data = boto3.client('redshift-data')
        self.kinesis = boto3.client('kinesis')
        self.cluster_identifier = 'my-redshift-cluster'
        self.database = 'analytics_db'
        self.db_user = 'admin'
    
    def setup_streaming_ingestion(self, stream_name, table_name):
        """Setup Kinesis streaming ingestion to Redshift"""
        try:
            # Create external schema for Kinesis
            create_schema_sql = f"""
                CREATE EXTERNAL SCHEMA kinesis_schema
                FROM KINESIS
                IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftKinesisRole';
            """
            
            response = self.redshift_data.execute_statement(
                ClusterIdentifier=self.cluster_identifier,
                Database=self.database,
                DbUser=self.db_user,
                Sql=create_schema_sql
            )
            
            # Create materialized view for streaming data
            create_mv_sql = f"""
                CREATE MATERIALIZED VIEW {table_name}_streaming AS
                SELECT 
                    JSON_EXTRACT_PATH_TEXT(kinesis_data, 'user_id') as user_id,
                    JSON_EXTRACT_PATH_TEXT(kinesis_data, 'event_type') as event_type,
                    JSON_EXTRACT_PATH_TEXT(kinesis_data, 'timestamp') as event_timestamp,
                    JSON_EXTRACT_PATH_TEXT(kinesis_data, 'properties') as properties,
                    approximate_arrival_timestamp
                FROM kinesis_schema."{stream_name}"
                WHERE LENGTH(kinesis_data) > 0;
            """
            
            response = self.redshift_data.execute_statement(
                ClusterIdentifier=self.cluster_identifier,
                Database=self.database,
                DbUser=self.db_user,
                Sql=create_mv_sql
            )
            
            print(f"Streaming ingestion setup completed for {stream_name}")
            return response
            
        except Exception as e:
            print(f"Error setting up streaming ingestion: {e}")
    
    def create_real_time_dashboard_queries(self):
        """Create queries for real-time dashboard"""
        queries = {
            'active_users_last_hour': """
                SELECT COUNT(DISTINCT user_id) as active_users
                FROM events_streaming
                WHERE event_timestamp >= DATEADD(hour, -1, GETDATE());
            """,
            
            'events_per_minute': """
                SELECT 
                    DATE_TRUNC('minute', event_timestamp) as minute,
                    COUNT(*) as event_count
                FROM events_streaming
                WHERE event_timestamp >= DATEADD(hour, -1, GETDATE())
                GROUP BY 1
                ORDER BY 1 DESC
                LIMIT 60;
            """,
            
            'top_events_last_hour': """
                SELECT 
                    event_type,
                    COUNT(*) as event_count,
                    COUNT(DISTINCT user_id) as unique_users
                FROM events_streaming
                WHERE event_timestamp >= DATEADD(hour, -1, GETDATE())
                GROUP BY 1
                ORDER BY 2 DESC
                LIMIT 10;
            """
        }
        
        results = {}
        for query_name, sql in queries.items():
            try:
                response = self.redshift_data.execute_statement(
                    ClusterIdentifier=self.cluster_identifier,
                    Database=self.database,
                    DbUser=self.db_user,
                    Sql=sql
                )
                results[query_name] = response['Id']
            except Exception as e:
                print(f"Error executing {query_name}: {e}")
        
        return results
    
    def refresh_materialized_view(self, view_name):
        """Refresh materialized view for latest data"""
        try:
            refresh_sql = f"REFRESH MATERIALIZED VIEW {view_name};"
            
            response = self.redshift_data.execute_statement(
                ClusterIdentifier=self.cluster_identifier,
                Database=self.database,
                DbUser=self.db_user,
                Sql=refresh_sql
            )
            
            print(f"Materialized view {view_name} refreshed")
            return response
            
        except Exception as e:
            print(f"Error refreshing materialized view: {e}")

# Usage example
streaming_analytics = RedshiftStreamingAnalytics()

# Setup streaming ingestion
streaming_analytics.setup_streaming_ingestion(
    stream_name='user-events-stream',
    table_name='events'
)

# Execute real-time queries
query_results = streaming_analytics.create_real_time_dashboard_queries()

# Refresh materialized view
streaming_analytics.refresh_materialized_view('events_streaming')
```

## Architecture Diagram

![Amazon Redshift Architecture](/img/aws-analytics/redshift.png)

## AWS Service Integrations

### Data Sources and ETL
- **Amazon S3**: Primary data lake storage and staging
- **AWS Glue**: ETL and data cataloging
- **Amazon Kinesis**: Real-time data streaming
- **AWS Data Pipeline**: Data workflow orchestration
- **AWS DMS**: Database migration and replication

### Analytics and BI
- **Amazon QuickSight**: Business intelligence and visualization
- **Amazon Athena**: Serverless query service
- **Amazon EMR**: Big data processing
- **Amazon SageMaker**: Machine learning integration

### Security and Management
- **AWS IAM**: Access control and authentication
- **Amazon VPC**: Network isolation
- **AWS CloudTrail**: Audit logging
- **Amazon CloudWatch**: Monitoring and alerting
- **AWS Config**: Configuration compliance

### Integration Services
- **AWS Lambda**: Serverless compute integration
- **Amazon API Gateway**: REST API integration
- **Amazon EventBridge**: Event-driven architectures
- **AWS Step Functions**: Workflow orchestration

## Best Practices

### Performance Optimization
- Choose appropriate distribution and sort keys
- Use columnar compression effectively
- Implement workload management (WLM)
- Optimize table design and data types
- Regular VACUUM and ANALYZE operations

### Cost Management
- Use Reserved Instances for predictable workloads
- Implement pause/resume for development clusters
- Monitor and optimize storage usage
- Use appropriate node types for workloads
- Implement data lifecycle policies

### Security
- Enable encryption at rest and in transit
- Use VPC for network isolation
- Implement fine-grained access control
- Regular security audits and compliance checks
- Secure credential management

### Data Management
- Implement proper backup and recovery strategies
- Use data sharing for cross-cluster access
- Optimize data loading processes
- Monitor data quality and consistency
- Implement data retention policies

## Monitoring and Troubleshooting

### Key Metrics
- Query performance and execution times
- Cluster CPU and memory utilization
- Storage usage and growth trends
- Concurrent query counts
- Data loading performance

### Common Issues
- Slow query performance
- Storage space issues
- Connection and authentication problems
- Data loading failures
- Workload management bottlenecks

### Troubleshooting Steps
1. Check system tables for query performance
2. Monitor cluster metrics in CloudWatch
3. Review WLM queue configurations
4. Analyze table statistics and distribution
5. Validate data loading processes and formats
