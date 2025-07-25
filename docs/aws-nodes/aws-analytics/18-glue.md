# AWS Glue

## Tổng quan

AWS Glue là node tổng quát đại diện cho fully managed ETL (Extract, Transform, Load) service của AWS. Glue giúp bạn dễ dàng chuẩn bị và load dữ liệu cho analytics bằng cách tự động hóa việc khám phá dữ liệu, schema inference, và code generation. Đây là serverless service cho phép bạn focus vào data transformation logic thay vì quản lý infrastructure.

## Chức năng chính

### 1. ETL Processing
- **Serverless ETL**: Không cần quản lý servers hoặc clusters
- **Auto Scaling**: Tự động scale based on workload
- **Code Generation**: Tự động generate ETL code
- **Multiple Languages**: Hỗ trợ Python và Scala

### 2. Data Catalog
- **Centralized Metadata**: Single source of truth cho metadata
- **Schema Discovery**: Tự động discover và infer schemas
- **Data Classification**: Classify sensitive data
- **Version Control**: Track schema evolution

### 3. Data Crawlers
- **Automatic Discovery**: Tự động discover data sources
- **Schema Inference**: Infer schemas từ data
- **Partition Detection**: Detect partition structures
- **Scheduled Crawling**: Schedule regular crawls

### 4. Job Orchestration
- **Workflow Management**: Orchestrate complex ETL workflows
- **Dependency Management**: Handle job dependencies
- **Error Handling**: Built-in error handling và retry logic
- **Monitoring**: Comprehensive job monitoring

## Use Cases phổ biến

1. **Data Lake ETL**: Transform data trong data lakes
2. **Data Warehouse Loading**: Load data vào data warehouses
3. **Data Migration**: Migrate data giữa systems
4. **Real-time Processing**: Stream processing với Glue Streaming
5. **Data Quality**: Implement data quality checks

## Diagram Architecture

Kiến trúc tổng quan AWS Glue ecosystem:

![AWS Glue Architecture](/img/aws-analytics/glue.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Glue, GlueCrawlers, GlueDataCatalog, Athena
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Redshift, Dynamodb
from diagrams.aws.integration import SQS, SNS, StepFunctions
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.database import MySQL

with Diagram("AWS Glue Architecture", show=False, direction="TB"):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Sources"):
        s3_raw = S3("Raw Data")
        rds_db = RDS("RDS Database")
        mysql_db = MySQL("On-premises DB")
        dynamodb_table = Dynamodb("DynamoDB")
        streaming_data = SQS("Streaming Data")
    
    with Cluster("AWS Glue Services"):
        glue_service = Glue("AWS Glue")
        
        with Cluster("Core Components"):
            crawlers = GlueCrawlers("Glue Crawlers")
            data_catalog = GlueDataCatalog("Data Catalog")
            etl_jobs = Glue("ETL Jobs")
            workflows = StepFunctions("Glue Workflows")
    
    with Cluster("Job Execution"):
        spark_jobs = Glue("Spark ETL Jobs")
        python_shell = Lambda("Python Shell Jobs")
        streaming_jobs = Glue("Streaming Jobs")
        ray_jobs = Glue("Ray Jobs")
    
    with Cluster("Data Targets"):
        s3_processed = S3("Processed Data")
        redshift_dw = Redshift("Data Warehouse")
        analytics_db = RDS("Analytics DB")
        data_lake = S3("Data Lake")
    
    with Cluster("Analytics Integration"):
        athena = Athena("Athena")
        quicksight = Glue("QuickSight")
        sagemaker = Lambda("SageMaker")
    
    with Cluster("Orchestration & Monitoring"):
        step_functions = StepFunctions("Step Functions")
        cloudwatch = Cloudwatch("CloudWatch")
        notifications = SNS("Notifications")
        security = IAM("IAM Roles")
    
    # Data discovery flow
    s3_raw >> crawlers
    rds_db >> crawlers
    mysql_db >> crawlers
    dynamodb_table >> crawlers
    
    crawlers >> data_catalog
    
    # ETL processing
    glue_service >> etl_jobs
    etl_jobs >> spark_jobs
    etl_jobs >> python_shell
    etl_jobs >> streaming_jobs
    etl_jobs >> ray_jobs
    
    # Data consumption from catalog
    data_catalog >> etl_jobs
    data_catalog >> athena
    
    # Data transformation flow
    s3_raw >> spark_jobs >> s3_processed
    rds_db >> python_shell >> redshift_dw
    streaming_data >> streaming_jobs >> data_lake
    
    # Workflow orchestration
    workflows >> etl_jobs
    step_functions >> workflows
    
    # Analytics integration
    s3_processed >> athena
    redshift_dw >> quicksight
    data_lake >> sagemaker
    
    # User interaction
    users >> Edge(label="Develop Jobs") >> glue_service
    users >> Edge(label="Monitor") >> cloudwatch
    users >> Edge(label="Query Data") >> athena
    
    # Monitoring and security
    etl_jobs >> cloudwatch
    cloudwatch >> notifications
    security >> glue_service
```

## ETL Job Development

### 1. Spark ETL Job
```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as F

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read data from Data Catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="raw_data_db",
    table_name="customer_events",
    transformation_ctx="datasource"
)

# Data transformations
# 1. Filter out invalid records
filtered_data = Filter.apply(
    frame=datasource,
    f=lambda x: x["customer_id"] is not None and x["event_type"] is not None,
    transformation_ctx="filtered_data"
)

# 2. Convert to DataFrame for complex transformations
df = filtered_data.toDF()

# 3. Add derived columns
df_transformed = df.withColumn(
    "event_date", 
    F.to_date(F.col("timestamp"))
).withColumn(
    "event_hour",
    F.hour(F.col("timestamp"))
).withColumn(
    "is_weekend",
    F.when(F.dayofweek(F.col("timestamp")).isin([1, 7]), True).otherwise(False)
)

# 4. Aggregate data
df_aggregated = df_transformed.groupBy(
    "customer_id", "event_date", "event_type"
).agg(
    F.count("*").alias("event_count"),
    F.sum("amount").alias("total_amount"),
    F.avg("amount").alias("avg_amount"),
    F.max("timestamp").alias("last_event_time")
)

# Convert back to DynamicFrame
dynamic_frame_aggregated = DynamicFrame.fromDF(
    df_aggregated, 
    glueContext, 
    "dynamic_frame_aggregated"
)

# Write to S3 in Parquet format with partitioning
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_aggregated,
    connection_type="s3",
    connection_options={
        "path": "s3://processed-data/customer-daily-metrics/",
        "partitionKeys": ["event_date"]
    },
    format="parquet",
    transformation_ctx="write_to_s3"
)

# Update Data Catalog
glueContext.write_dynamic_frame.from_catalog(
    frame=dynamic_frame_aggregated,
    database="processed_data_db",
    table_name="customer_daily_metrics",
    transformation_ctx="write_to_catalog"
)

job.commit()
```

### 2. Python Shell Job
```python
import boto3
import pandas as pd
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize AWS clients
    glue = boto3.client('glue')
    s3 = boto3.client('s3')
    
    try:
        # Read configuration from Glue job parameters
        job_name = sys.argv[1] if len(sys.argv) > 1 else 'data-quality-check'
        
        # Get job parameters
        response = glue.get_job(JobName=job_name)
        job_params = response['Job']['DefaultArguments']
        
        source_bucket = job_params.get('--source-bucket')
        source_prefix = job_params.get('--source-prefix')
        target_bucket = job_params.get('--target-bucket')
        
        # Data quality checks
        quality_results = perform_data_quality_checks(
            s3, source_bucket, source_prefix
        )
        
        # Generate quality report
        report = generate_quality_report(quality_results)
        
        # Save report to S3
        save_report_to_s3(s3, target_bucket, report)
        
        # Send notifications if issues found
        if quality_results['has_issues']:
            send_quality_alert(quality_results)
        
        logger.info("Data quality check completed successfully")
        
    except Exception as e:
        logger.error(f"Job failed: {str(e)}")
        raise

def perform_data_quality_checks(s3_client, bucket, prefix):
    """Perform comprehensive data quality checks"""
    
    quality_results = {
        'timestamp': datetime.utcnow().isoformat(),
        'checks': [],
        'has_issues': False
    }
    
    # List files in S3 prefix
    response = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )
    
    for obj in response.get('Contents', []):
        file_key = obj['Key']
        
        if file_key.endswith('.parquet'):
            # Read parquet file
            df = pd.read_parquet(f's3://{bucket}/{file_key}')
            
            # Perform checks
            file_checks = {
                'file': file_key,
                'row_count': len(df),
                'null_checks': check_null_values(df),
                'duplicate_checks': check_duplicates(df),
                'data_type_checks': check_data_types(df),
                'range_checks': check_value_ranges(df)
            }
            
            # Check if any issues found
            if any([
                file_checks['null_checks']['has_issues'],
                file_checks['duplicate_checks']['has_issues'],
                file_checks['data_type_checks']['has_issues'],
                file_checks['range_checks']['has_issues']
            ]):
                quality_results['has_issues'] = True
            
            quality_results['checks'].append(file_checks)
    
    return quality_results

def check_null_values(df):
    """Check for null values in critical columns"""
    
    critical_columns = ['customer_id', 'event_type', 'timestamp']
    null_counts = {}
    has_issues = False
    
    for col in critical_columns:
        if col in df.columns:
            null_count = df[col].isnull().sum()
            null_counts[col] = null_count
            
            if null_count > 0:
                has_issues = True
    
    return {
        'has_issues': has_issues,
        'null_counts': null_counts
    }

def check_duplicates(df):
    """Check for duplicate records"""
    
    if 'event_id' in df.columns:
        duplicate_count = df['event_id'].duplicated().sum()
        return {
            'has_issues': duplicate_count > 0,
            'duplicate_count': duplicate_count
        }
    
    return {'has_issues': False, 'duplicate_count': 0}

if __name__ == "__main__":
    main()
```

### 3. Streaming ETL Job
```python
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import DataFrame, functions as F
from pyspark.sql.types import *
import sys

# Initialize
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Define schema for incoming data
schema = StructType([
    StructField("event_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("amount", DoubleType(), True),
    StructField("properties", MapType(StringType(), StringType()), True)
])

# Read from Kinesis stream
kinesis_options = {
    "streamName": "customer-events-stream",
    "startingPosition": "TRIM_HORIZON",
    "inferSchema": "false"
}

streaming_df = glueContext.create_data_frame.from_options(
    connection_type="kinesis",
    connection_options=kinesis_options,
    transformation_ctx="streaming_df"
)

# Parse JSON data
parsed_df = streaming_df.select(
    F.from_json(F.col("data"), schema).alias("parsed_data")
).select("parsed_data.*")

# Real-time transformations
def process_batch(df, epoch_id):
    """Process each micro-batch"""
    
    if df.count() > 0:
        # Add processing timestamp
        processed_df = df.withColumn(
            "processing_time", 
            F.current_timestamp()
        ).withColumn(
            "event_date",
            F.to_date(F.col("timestamp"))
        )
        
        # Filter and validate
        valid_df = processed_df.filter(
            (F.col("customer_id").isNotNull()) &
            (F.col("event_type").isNotNull()) &
            (F.col("amount") >= 0)
        )
        
        # Write to S3 (append mode for streaming)
        valid_df.write \
            .mode("append") \
            .partitionBy("event_date") \
            .parquet("s3://streaming-output/processed-events/")
        
        # Write to DynamoDB for real-time lookups
        write_to_dynamodb(valid_df)
        
        print(f"Processed {valid_df.count()} records in batch {epoch_id}")

def write_to_dynamodb(df):
    """Write aggregated data to DynamoDB"""
    
    # Aggregate by customer and event type
    aggregated = df.groupBy("customer_id", "event_type") \
        .agg(
            F.count("*").alias("event_count"),
            F.sum("amount").alias("total_amount"),
            F.max("timestamp").alias("last_event_time")
        )
    
    # Convert to format suitable for DynamoDB
    dynamodb_df = aggregated.select(
        F.col("customer_id").alias("pk"),
        F.concat(F.lit("EVENT#"), F.col("event_type")).alias("sk"),
        F.col("event_count"),
        F.col("total_amount"),
        F.col("last_event_time")
    )
    
    # Write to DynamoDB using Glue DynamoDB connector
    glueContext.write_dynamic_frame.from_options(
        frame=DynamicFrame.fromDF(dynamodb_df, glueContext, "dynamodb_df"),
        connection_type="dynamodb",
        connection_options={
            "dynamodb.output.tableName": "customer-event-aggregates",
            "dynamodb.throughput.write.percent": "0.5"
        }
    )

# Start streaming query
query = parsed_df.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .option("checkpointLocation", "s3://glue-checkpoints/streaming-job/") \
    .trigger(processingTime='30 seconds') \
    .start()

query.awaitTermination()
job.commit()
```

## Workflow Orchestration

### 1. Glue Workflow Definition
```python
import boto3

glue = boto3.client('glue')

# Create workflow
workflow_config = {
    'Name': 'data-processing-workflow',
    'Description': 'End-to-end data processing workflow',
    'DefaultRunProperties': {
        'glue:version': '3.0'
    },
    'MaxConcurrentRuns': 1
}

glue.create_workflow(**workflow_config)

# Create triggers
triggers = [
    {
        'Name': 'start-crawlers-trigger',
        'Type': 'ON_DEMAND',
        'Actions': [
            {
                'CrawlerName': 'raw-data-crawler'
            },
            {
                'CrawlerName': 'reference-data-crawler'
            }
        ],
        'WorkflowName': 'data-processing-workflow'
    },
    {
        'Name': 'etl-jobs-trigger',
        'Type': 'CONDITIONAL',
        'Predicate': {
            'Conditions': [
                {
                    'LogicalOperator': 'EQUALS',
                    'CrawlerName': 'raw-data-crawler',
                    'CrawlState': 'SUCCEEDED'
                },
                {
                    'LogicalOperator': 'EQUALS',
                    'CrawlerName': 'reference-data-crawler',
                    'CrawlState': 'SUCCEEDED'
                }
            ],
            'Logical': 'AND'
        },
        'Actions': [
            {
                'JobName': 'data-cleaning-job'
            }
        ],
        'WorkflowName': 'data-processing-workflow'
    },
    {
        'Name': 'aggregation-trigger',
        'Type': 'CONDITIONAL',
        'Predicate': {
            'Conditions': [
                {
                    'LogicalOperator': 'EQUALS',
                    'JobName': 'data-cleaning-job',
                    'State': 'SUCCEEDED'
                }
            ]
        },
        'Actions': [
            {
                'JobName': 'data-aggregation-job'
            },
            {
                'JobName': 'data-quality-job'
            }
        ],
        'WorkflowName': 'data-processing-workflow'
    }
]

for trigger in triggers:
    glue.create_trigger(**trigger)
```

### 2. Advanced Workflow Management
```python
class GlueWorkflowManager:
    def __init__(self, glue_client):
        self.glue = glue_client
    
    def create_complex_workflow(self, workflow_config):
        """Create complex workflow with error handling"""
        
        # Create main workflow
        self.glue.create_workflow(
            Name=workflow_config['name'],
            Description=workflow_config['description'],
            DefaultRunProperties=workflow_config.get('properties', {})
        )
        
        # Create jobs with error handling
        for job_config in workflow_config['jobs']:
            self.create_job_with_error_handling(job_config)
        
        # Create triggers with dependencies
        for trigger_config in workflow_config['triggers']:
            self.create_conditional_trigger(trigger_config)
    
    def create_job_with_error_handling(self, job_config):
        """Create job with comprehensive error handling"""
        
        # Main job
        main_job = {
            'Name': job_config['name'],
            'Role': job_config['role'],
            'Command': {
                'Name': 'glueetl',
                'ScriptLocation': job_config['script_location'],
                'PythonVersion': '3'
            },
            'DefaultArguments': job_config.get('arguments', {}),
            'MaxRetries': job_config.get('max_retries', 2),
            'Timeout': job_config.get('timeout', 2880),
            'NotificationProperty': {
                'NotifyDelayAfter': 60
            }
        }
        
        self.glue.create_job(**main_job)
        
        # Error handling job
        if job_config.get('error_handler'):
            error_job = {
                'Name': f"{job_config['name']}-error-handler",
                'Role': job_config['role'],
                'Command': {
                    'Name': 'pythonshell',
                    'ScriptLocation': job_config['error_handler']['script'],
                    'PythonVersion': '3'
                },
                'DefaultArguments': {
                    '--failed-job-name': job_config['name'],
                    '--notification-topic': job_config['error_handler']['sns_topic']
                }
            }
            
            self.glue.create_job(**error_job)
    
    def monitor_workflow_execution(self, workflow_name, run_id):
        """Monitor workflow execution with detailed logging"""
        
        import time
        
        while True:
            # Get workflow run status
            response = self.glue.get_workflow_run(
                Name=workflow_name,
                RunId=run_id
            )
            
            run_status = response['Run']['Status']
            
            if run_status in ['COMPLETED', 'STOPPED', 'ERROR']:
                break
            
            # Get detailed status of jobs and crawlers
            self.log_workflow_progress(workflow_name, run_id)
            
            time.sleep(30)
        
        return run_status
    
    def log_workflow_progress(self, workflow_name, run_id):
        """Log detailed workflow progress"""
        
        # Get workflow run details
        response = self.glue.get_workflow_run(
            Name=workflow_name,
            RunId=run_id,
            IncludeGraph=True
        )
        
        graph = response['Run']['Graph']
        
        # Log job statuses
        for node in graph.get('Nodes', []):
            if node['Type'] == 'JOB':
                job_runs = node.get('JobDetails', {}).get('JobRuns', [])
                for job_run in job_runs:
                    print(f"Job {node['Name']}: {job_run['JobRunState']}")
            
            elif node['Type'] == 'CRAWLER':
                crawler_details = node.get('CrawlerDetails', {})
                if crawler_details:
                    print(f"Crawler {node['Name']}: {crawler_details.get('LastCrawl', {}).get('Status', 'UNKNOWN')}")
```

## Performance Optimization

### 1. Job Performance Tuning
```python
# Optimized Glue job configuration
optimized_job_config = {
    'Name': 'optimized-etl-job',
    'Role': 'GlueServiceRole',
    'Command': {
        'Name': 'glueetl',
        'ScriptLocation': 's3://glue-scripts/optimized-etl.py',
        'PythonVersion': '3'
    },
    'DefaultArguments': {
        '--job-language': 'python',
        '--job-bookmark-option': 'job-bookmark-enable',
        '--enable-metrics': 'true',
        '--enable-continuous-cloudwatch-log': 'true',
        '--enable-spark-ui': 'true',
        '--spark-event-logs-path': 's3://glue-logs/spark-events/',
        
        # Performance optimizations
        '--conf': 'spark.sql.adaptive.enabled=true',
        '--conf': 'spark.sql.adaptive.coalescePartitions.enabled=true',
        '--conf': 'spark.sql.adaptive.skewJoin.enabled=true',
        '--conf': 'spark.serializer=org.apache.spark.serializer.KryoSerializer',
        
        # Memory optimizations
        '--conf': 'spark.sql.execution.arrow.pyspark.enabled=true',
        '--conf': 'spark.sql.execution.arrow.maxRecordsPerBatch=10000'
    },
    'MaxCapacity': 10,  # Use appropriate DPU count
    'WorkerType': 'G.1X',
    'NumberOfWorkers': 10,
    'Timeout': 2880,
    'MaxRetries': 1
}
```

### 2. Cost Optimization
```python
class GlueCostOptimizer:
    def __init__(self, glue_client, cloudwatch_client):
        self.glue = glue_client
        self.cloudwatch = cloudwatch_client
    
    def analyze_job_costs(self, job_name, days=30):
        """Analyze job costs over time"""
        
        from datetime import datetime, timedelta
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)
        
        # Get job runs
        job_runs = self.glue.get_job_runs(
            JobName=job_name,
            MaxResults=100
        )
        
        cost_analysis = {
            'total_dpu_hours': 0,
            'total_runs': len(job_runs['JobRuns']),
            'avg_duration_minutes': 0,
            'cost_breakdown': []
        }
        
        total_duration = 0
        
        for run in job_runs['JobRuns']:
            if run['JobRunState'] == 'SUCCEEDED':
                start = run['StartedOn']
                end = run.get('CompletedOn', datetime.utcnow())
                duration_hours = (end - start).total_seconds() / 3600
                
                dpu_count = run.get('MaxCapacity', 2)
                dpu_hours = duration_hours * dpu_count
                
                cost_analysis['total_dpu_hours'] += dpu_hours
                total_duration += duration_hours * 60  # Convert to minutes
                
                cost_analysis['cost_breakdown'].append({
                    'run_id': run['Id'],
                    'duration_hours': duration_hours,
                    'dpu_count': dpu_count,
                    'dpu_hours': dpu_hours,
                    'estimated_cost': dpu_hours * 0.44  # $0.44 per DPU-hour
                })
        
        if cost_analysis['total_runs'] > 0:
            cost_analysis['avg_duration_minutes'] = total_duration / cost_analysis['total_runs']
        
        return cost_analysis
    
    def recommend_optimizations(self, cost_analysis):
        """Recommend cost optimizations"""
        
        recommendations = []
        
        # Check for over-provisioning
        if cost_analysis['avg_duration_minutes'] < 10:
            recommendations.append({
                'type': 'REDUCE_DPU',
                'description': 'Job completes quickly, consider reducing DPU count',
                'potential_savings': '20-40%'
            })
        
        # Check for long-running jobs
        if cost_analysis['avg_duration_minutes'] > 120:
            recommendations.append({
                'type': 'OPTIMIZE_CODE',
                'description': 'Long-running job, optimize ETL logic and use job bookmarks',
                'potential_savings': '30-50%'
            })
        
        # Check frequency
        if cost_analysis['total_runs'] > days * 24:  # More than hourly
            recommendations.append({
                'type': 'BATCH_PROCESSING',
                'description': 'High frequency job, consider batching data',
                'potential_savings': '25-35%'
            })
        
        return recommendations
```

## Best Practices

1. **Job Design**: Design modular và reusable ETL jobs
2. **Performance**: Optimize Spark configurations
3. **Cost Management**: Use appropriate DPU counts và job bookmarks
4. **Error Handling**: Implement comprehensive error handling
5. **Monitoring**: Set up detailed monitoring và alerting
6. **Security**: Use IAM roles và encrypt data
7. **Testing**: Test jobs thoroughly before production
8. **Documentation**: Document job logic và dependencies

## Tích hợp với các dịch vụ AWS khác

- **Amazon S3**: Primary data storage
- **AWS Glue Data Catalog**: Metadata management
- **Amazon Athena**: Query processed data
- **Amazon EMR**: Big data processing
- **Amazon Redshift**: Data warehouse loading
- **AWS Lambda**: Event-driven processing
- **Amazon Kinesis**: Real-time data streaming
- **AWS Step Functions**: Workflow orchestration
- **Amazon CloudWatch**: Monitoring và logging
- **AWS IAM**: Security và access control
- **Amazon SNS**: Notifications và alerts
- **AWS Lake Formation**: Data lake governance
