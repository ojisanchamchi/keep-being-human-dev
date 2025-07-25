# AWS Glue Crawlers

## Tổng quan

AWS Glue Crawlers là node đại diện cho thành phần tự động khám phá và phân loại dữ liệu trong AWS Glue ecosystem. Crawlers tự động quét các data stores, xác định định dạng dữ liệu, schema, và tạo metadata tables trong AWS Glue Data Catalog. Đây là công cụ quan trọng để tự động hóa việc quản lý metadata và chuẩn bị dữ liệu cho analytics.

## Chức năng chính

### 1. Automatic Schema Discovery
- **Schema Inference**: Tự động phát hiện schema từ dữ liệu
- **Data Type Detection**: Xác định data types chính xác
- **Partition Discovery**: Phát hiện partition structure
- **Format Recognition**: Nhận diện file formats (JSON, Parquet, CSV, etc.)

### 2. Data Store Integration
- **S3 Support**: Crawl dữ liệu trong Amazon S3
- **Database Connectivity**: JDBC connections đến databases
- **DynamoDB Integration**: Crawl DynamoDB tables
- **Custom Classifiers**: Tạo custom classifiers cho formats đặc biệt

### 3. Metadata Management
- **Table Creation**: Tự động tạo tables trong Data Catalog
- **Schema Evolution**: Theo dõi và cập nhật schema changes
- **Partition Management**: Quản lý partitions tự động
- **Data Classification**: Phân loại dữ liệu theo sensitivity

### 4. Scheduling và Automation
- **Scheduled Runs**: Chạy crawlers theo lịch định sẵn
- **Event-driven**: Trigger bởi S3 events hoặc CloudWatch
- **Incremental Crawling**: Chỉ crawl dữ liệu mới hoặc thay đổi
- **Parallel Processing**: Crawl multiple data stores đồng thời

## Use Cases phổ biến

1. **Data Lake Discovery**: Tự động khám phá dữ liệu trong data lake
2. **Schema Management**: Quản lý schema evolution
3. **Data Cataloging**: Tạo comprehensive data catalog
4. **ETL Preparation**: Chuẩn bị metadata cho ETL jobs
5. **Compliance Scanning**: Phát hiện sensitive data cho compliance

## Diagram Architecture

Kiến trúc AWS Glue Crawlers với data discovery workflow:

![AWS Glue Crawlers Architecture](/img/aws-analytics/glue-crawlers.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import GlueCrawlers, GlueDataCatalog, Athena
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch, CloudwatchEventTimeBased
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.database import MySQL

with Diagram("AWS Glue Crawlers Architecture", show=False, direction="TB"):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Sources"):
        s3_raw = S3("Raw Data Lake")
        s3_processed = S3("Processed Data")
        rds_db = RDS("RDS Database")
        mysql_db = MySQL("On-premises DB")
        dynamodb_table = Dynamodb("DynamoDB Tables")
    
    with Cluster("Glue Crawlers"):
        crawlers = GlueCrawlers("Glue Crawlers")
        
        with Cluster("Crawler Types"):
            s3_crawler = GlueCrawlers("S3 Crawler")
            jdbc_crawler = GlueCrawlers("JDBC Crawler")
            dynamodb_crawler = GlueCrawlers("DynamoDB Crawler")
    
    with Cluster("Data Catalog"):
        data_catalog = GlueDataCatalog("Glue Data Catalog")
        
        with Cluster("Catalog Components"):
            databases = GlueDataCatalog("Databases")
            tables = GlueDataCatalog("Tables")
            partitions = GlueDataCatalog("Partitions")
    
    with Cluster("Scheduling & Triggers"):
        cloudwatch_events = CloudwatchEventTimeBased("CloudWatch Events")
        s3_events = S3("S3 Events")
        lambda_trigger = Lambda("Trigger Function")
        scheduler = SQS("Scheduler Queue")
    
    with Cluster("Analytics Integration"):
        athena = Athena("Athena Queries")
        etl_jobs = Lambda("ETL Jobs")
        ml_pipeline = Lambda("ML Pipeline")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        notifications = SNS("Notifications")
        security = IAM("IAM Roles")
    
    # Data source connections
    s3_raw >> Edge(label="Crawl") >> s3_crawler
    s3_processed >> Edge(label="Crawl") >> s3_crawler
    rds_db >> Edge(label="JDBC") >> jdbc_crawler
    mysql_db >> Edge(label="JDBC") >> jdbc_crawler
    dynamodb_table >> Edge(label="Scan") >> dynamodb_crawler
    
    # Crawler orchestration
    crawlers >> s3_crawler
    crawlers >> jdbc_crawler
    crawlers >> dynamodb_crawler
    
    # Metadata creation
    s3_crawler >> Edge(label="Create Tables") >> data_catalog
    jdbc_crawler >> Edge(label="Create Tables") >> data_catalog
    dynamodb_crawler >> Edge(label="Create Tables") >> data_catalog
    
    # Catalog structure
    data_catalog >> databases
    data_catalog >> tables
    data_catalog >> partitions
    
    # Scheduling and triggers
    cloudwatch_events >> Edge(label="Schedule") >> crawlers
    s3_events >> lambda_trigger >> crawlers
    scheduler >> Edge(label="Queue Jobs") >> crawlers
    
    # Analytics consumption
    data_catalog >> athena
    data_catalog >> etl_jobs
    data_catalog >> ml_pipeline
    
    # User interaction
    users >> Edge(label="Configure") >> crawlers
    users >> Edge(label="Query Catalog") >> data_catalog
    users >> Edge(label="Run Analytics") >> athena
    
    # Monitoring and notifications
    crawlers >> Edge(label="Metrics") >> monitoring
    crawlers >> Edge(label="Alerts") >> notifications
    security >> Edge(label="Access Control") >> crawlers
```

## Crawler Configuration

### 1. S3 Crawler Setup
```python
import boto3

glue = boto3.client('glue')

# Create S3 crawler
s3_crawler_config = {
    'Name': 'data-lake-crawler',
    'Role': 'arn:aws:iam::account:role/GlueCrawlerRole',
    'DatabaseName': 'data_lake_db',
    'Description': 'Crawls data lake for schema discovery',
    'Targets': {
        'S3Targets': [
            {
                'Path': 's3://data-lake/raw/',
                'Exclusions': ['*.tmp', '*.log']
            },
            {
                'Path': 's3://data-lake/processed/',
                'SampleSize': 100
            }
        ]
    },
    'Schedule': 'cron(0 2 * * ? *)',  # Daily at 2 AM
    'SchemaChangePolicy': {
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'LOG'
    },
    'RecrawlPolicy': {
        'RecrawlBehavior': 'CRAWL_EVERYTHING'
    },
    'LineageConfiguration': {
        'CrawlerLineageSettings': 'ENABLE'
    },
    'Configuration': json.dumps({
        'Version': 1.0,
        'CrawlerOutput': {
            'Partitions': {'AddOrUpdateBehavior': 'InheritFromTable'},
            'Tables': {'AddOrUpdateBehavior': 'MergeNewColumns'}
        }
    })
}

response = glue.create_crawler(**s3_crawler_config)
```

### 2. JDBC Crawler Configuration
```python
# JDBC crawler for relational databases
jdbc_crawler_config = {
    'Name': 'rds-crawler',
    'Role': 'arn:aws:iam::account:role/GlueCrawlerRole',
    'DatabaseName': 'operational_db',
    'Targets': {
        'JdbcTargets': [
            {
                'ConnectionName': 'rds-connection',
                'Path': 'production/public/%',
                'Exclusions': ['temp_%', 'log_%']
            }
        ]
    },
    'Schedule': 'cron(0 6 ? * SUN *)',  # Weekly on Sunday
    'Classifiers': ['custom-csv-classifier'],
    'TablePrefix': 'prod_',
    'SchemaChangePolicy': {
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'DEPRECATE_IN_DATABASE'
    }
}

# Create JDBC connection first
connection_config = {
    'ConnectionInput': {
        'Name': 'rds-connection',
        'ConnectionType': 'JDBC',
        'ConnectionProperties': {
            'JDBC_CONNECTION_URL': 'jdbc:postgresql://rds-endpoint:5432/production',
            'USERNAME': 'crawler_user',
            'PASSWORD': 'secure_password'
        },
        'PhysicalConnectionRequirements': {
            'SubnetId': 'subnet-12345',
            'SecurityGroupIdList': ['sg-67890'],
            'AvailabilityZone': 'us-west-2a'
        }
    }
}

glue.create_connection(**connection_config)
glue.create_crawler(**jdbc_crawler_config)
```

### 3. Custom Classifier
```python
# Create custom classifier for special formats
classifier_config = {
    'CsvClassifier': {
        'Name': 'custom-csv-classifier',
        'Delimiter': '|',
        'QuoteSymbol': '"',
        'ContainsHeader': 'PRESENT',
        'Header': ['id', 'name', 'email', 'created_date'],
        'DisableValueTrimming': False,
        'AllowSingleColumn': False
    }
}

glue.create_classifier(**classifier_config)

# JSON classifier
json_classifier_config = {
    'JsonClassifier': {
        'Name': 'nested-json-classifier',
        'JsonPath': '$.data[*]'
    }
}

glue.create_classifier(**json_classifier_config)
```

## Advanced Crawler Features

### 1. Schema Evolution Handling
```python
class SchemaEvolutionHandler:
    def __init__(self, glue_client):
        self.glue = glue_client
    
    def handle_schema_changes(self, crawler_name, table_name):
        """Handle schema evolution events"""
        try:
            # Get table versions
            response = self.glue.get_table_versions(
                DatabaseName='data_lake_db',
                TableName=table_name,
                MaxResults=10
            )
            
            versions = response['TableVersions']
            if len(versions) > 1:
                current_schema = versions[0]['Table']['StorageDescriptor']['Columns']
                previous_schema = versions[1]['Table']['StorageDescriptor']['Columns']
                
                # Detect changes
                changes = self.detect_schema_changes(current_schema, previous_schema)
                
                if changes:
                    self.notify_schema_changes(table_name, changes)
                    self.update_downstream_jobs(table_name, changes)
            
        except Exception as e:
            print(f"Error handling schema evolution: {str(e)}")
    
    def detect_schema_changes(self, current, previous):
        """Detect schema changes between versions"""
        changes = {
            'added_columns': [],
            'removed_columns': [],
            'type_changes': []
        }
        
        current_cols = {col['Name']: col['Type'] for col in current}
        previous_cols = {col['Name']: col['Type'] for col in previous}
        
        # Added columns
        for col_name in current_cols:
            if col_name not in previous_cols:
                changes['added_columns'].append(col_name)
        
        # Removed columns
        for col_name in previous_cols:
            if col_name not in current_cols:
                changes['removed_columns'].append(col_name)
        
        # Type changes
        for col_name in current_cols:
            if col_name in previous_cols and current_cols[col_name] != previous_cols[col_name]:
                changes['type_changes'].append({
                    'column': col_name,
                    'old_type': previous_cols[col_name],
                    'new_type': current_cols[col_name]
                })
        
        return changes
```

### 2. Incremental Crawling
```python
class IncrementalCrawler:
    def __init__(self, glue_client, s3_client):
        self.glue = glue_client
        self.s3 = s3_client
    
    def setup_incremental_crawling(self, crawler_name, s3_path):
        """Setup incremental crawling based on S3 events"""
        
        # Create Lambda function for S3 event processing
        lambda_function = self.create_crawler_trigger_function(crawler_name)
        
        # Setup S3 event notification
        bucket_name = s3_path.split('/')[2]
        prefix = '/'.join(s3_path.split('/')[3:])
        
        notification_config = {
            'LambdaConfigurations': [
                {
                    'Id': f'{crawler_name}-trigger',
                    'LambdaFunctionArn': lambda_function['FunctionArn'],
                    'Events': ['s3:ObjectCreated:*'],
                    'Filter': {
                        'Key': {
                            'FilterRules': [
                                {
                                    'Name': 'prefix',
                                    'Value': prefix
                                }
                            ]
                        }
                    }
                }
            ]
        }
        
        self.s3.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration=notification_config
        )
    
    def create_crawler_trigger_function(self, crawler_name):
        """Create Lambda function to trigger crawler"""
        lambda_code = f'''
import boto3
import json

def lambda_handler(event, context):
    glue = boto3.client('glue')
    
    # Check if crawler is already running
    try:
        response = glue.get_crawler(Name='{crawler_name}')
        if response['Crawler']['State'] == 'RUNNING':
            return {{'statusCode': 200, 'body': 'Crawler already running'}}
    except:
        pass
    
    # Start crawler
    try:
        glue.start_crawler(Name='{crawler_name}')
        return {{'statusCode': 200, 'body': 'Crawler started successfully'}}
    except Exception as e:
        return {{'statusCode': 500, 'body': f'Error: {{str(e)}}'}}
'''
        
        # This would create the actual Lambda function
        # Implementation depends on your deployment method
        return {'FunctionArn': f'arn:aws:lambda:region:account:function:{crawler_name}-trigger'}
```

### 3. Data Quality Validation
```python
class CrawlerDataQuality:
    def __init__(self, glue_client):
        self.glue = glue_client
    
    def validate_crawled_data(self, database_name, table_name):
        """Validate data quality after crawling"""
        
        # Get table metadata
        table = self.glue.get_table(
            DatabaseName=database_name,
            Name=table_name
        )
        
        validation_results = {
            'table_name': table_name,
            'validation_time': datetime.utcnow().isoformat(),
            'checks': []
        }
        
        # Check 1: Schema consistency
        schema_check = self.validate_schema_consistency(table)
        validation_results['checks'].append(schema_check)
        
        # Check 2: Data freshness
        freshness_check = self.validate_data_freshness(table)
        validation_results['checks'].append(freshness_check)
        
        # Check 3: Partition completeness
        partition_check = self.validate_partition_completeness(table)
        validation_results['checks'].append(partition_check)
        
        return validation_results
    
    def validate_schema_consistency(self, table):
        """Validate schema consistency"""
        columns = table['Table']['StorageDescriptor']['Columns']
        
        # Check for required columns
        required_columns = ['id', 'created_date']  # Example
        missing_columns = [col for col in required_columns 
                          if col not in [c['Name'] for c in columns]]
        
        return {
            'check_name': 'schema_consistency',
            'status': 'PASS' if not missing_columns else 'FAIL',
            'details': {
                'missing_columns': missing_columns,
                'total_columns': len(columns)
            }
        }
    
    def validate_data_freshness(self, table):
        """Validate data freshness"""
        # Get last update time from table metadata
        last_updated = table['Table'].get('UpdateTime')
        
        if last_updated:
            age_hours = (datetime.utcnow() - last_updated).total_seconds() / 3600
            is_fresh = age_hours <= 24  # Data should be less than 24 hours old
            
            return {
                'check_name': 'data_freshness',
                'status': 'PASS' if is_fresh else 'FAIL',
                'details': {
                    'last_updated': last_updated.isoformat(),
                    'age_hours': age_hours
                }
            }
        
        return {
            'check_name': 'data_freshness',
            'status': 'UNKNOWN',
            'details': {'message': 'No update time available'}
        }
```

## Performance Optimization

### 1. Crawler Performance Tuning
```python
# Optimize crawler performance
optimized_crawler_config = {
    'Name': 'optimized-crawler',
    'Role': 'arn:aws:iam::account:role/GlueCrawlerRole',
    'DatabaseName': 'optimized_db',
    'Targets': {
        'S3Targets': [
            {
                'Path': 's3://large-dataset/',
                'SampleSize': 1000,  # Sample size for large datasets
                'ConnectionName': 's3-vpc-endpoint'  # Use VPC endpoint
            }
        ]
    },
    'Configuration': json.dumps({
        'Version': 1.0,
        'Grouping': {
            'TableGroupingPolicy': 'CombineCompatibleSchemas'
        },
        'CrawlerOutput': {
            'Partitions': {'AddOrUpdateBehavior': 'InheritFromTable'},
            'Tables': {'AddOrUpdateBehavior': 'MergeNewColumns'}
        }
    }),
    'RecrawlPolicy': {
        'RecrawlBehavior': 'CRAWL_NEW_FOLDERS_ONLY'
    }
}
```

### 2. Parallel Crawling Strategy
```python
class ParallelCrawlerManager:
    def __init__(self, glue_client):
        self.glue = glue_client
    
    def create_parallel_crawlers(self, s3_paths, base_crawler_config):
        """Create multiple crawlers for parallel processing"""
        crawlers = []
        
        for i, path in enumerate(s3_paths):
            crawler_config = base_crawler_config.copy()
            crawler_config['Name'] = f"{base_crawler_config['Name']}-{i}"
            crawler_config['Targets'] = {
                'S3Targets': [{'Path': path}]
            }
            
            self.glue.create_crawler(**crawler_config)
            crawlers.append(crawler_config['Name'])
        
        return crawlers
    
    def run_crawlers_parallel(self, crawler_names):
        """Run multiple crawlers in parallel"""
        for crawler_name in crawler_names:
            try:
                self.glue.start_crawler(Name=crawler_name)
                print(f"Started crawler: {crawler_name}")
            except Exception as e:
                print(f"Failed to start crawler {crawler_name}: {str(e)}")
    
    def monitor_crawler_progress(self, crawler_names):
        """Monitor progress of parallel crawlers"""
        while True:
            running_crawlers = []
            
            for crawler_name in crawler_names:
                response = self.glue.get_crawler(Name=crawler_name)
                state = response['Crawler']['State']
                
                if state == 'RUNNING':
                    running_crawlers.append(crawler_name)
                elif state == 'STOPPING':
                    running_crawlers.append(crawler_name)
            
            if not running_crawlers:
                break
            
            print(f"Still running: {running_crawlers}")
            time.sleep(30)
        
        print("All crawlers completed")
```

## Monitoring và Troubleshooting

### 1. Crawler Metrics
```python
class CrawlerMonitoring:
    def __init__(self, cloudwatch_client):
        self.cloudwatch = cloudwatch_client
    
    def get_crawler_metrics(self, crawler_name, start_time, end_time):
        """Get CloudWatch metrics for crawler"""
        
        metrics = [
            'glue.driver.aggregate.numCompletedTasks',
            'glue.driver.aggregate.numFailedTasks',
            'glue.driver.BlockManager.disk.diskSpaceUsed_MB',
            'glue.driver.jvm.heap.usage'
        ]
        
        results = {}
        
        for metric in metrics:
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Glue',
                MetricName=metric,
                Dimensions=[
                    {
                        'Name': 'JobName',
                        'Value': crawler_name
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum']
            )
            
            results[metric] = response['Datapoints']
        
        return results
    
    def create_crawler_alarms(self, crawler_name):
        """Create CloudWatch alarms for crawler"""
        
        # Alarm for failed crawls
        self.cloudwatch.put_metric_alarm(
            AlarmName=f'{crawler_name}-failures',
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=1,
            MetricName='glue.driver.aggregate.numFailedTasks',
            Namespace='AWS/Glue',
            Period=300,
            Statistic='Sum',
            Threshold=0,
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:region:account:crawler-alerts'
            ],
            AlarmDescription=f'Alarm for {crawler_name} failures',
            Dimensions=[
                {
                    'Name': 'JobName',
                    'Value': crawler_name
                }
            ]
        )
```

## Best Practices

1. **Crawler Design**: Tạo separate crawlers cho different data sources
2. **Scheduling**: Sử dụng appropriate schedules để avoid conflicts
3. **Schema Evolution**: Configure proper schema change policies
4. **Performance**: Optimize sample sizes và exclusion patterns
5. **Security**: Use least privilege IAM roles
6. **Monitoring**: Set up comprehensive monitoring và alerting
7. **Cost Management**: Use incremental crawling để reduce costs
8. **Data Quality**: Implement validation checks post-crawling

## Tích hợp với các dịch vụ AWS khác

- **Amazon S3**: Primary data source cho crawling
- **AWS Glue Data Catalog**: Metadata repository
- **Amazon Athena**: Query cataloged data
- **AWS Glue ETL**: Use discovered schemas
- **Amazon EMR**: Access cataloged metadata
- **AWS Lambda**: Event-driven crawler triggers
- **Amazon CloudWatch**: Monitoring và alerting
- **AWS IAM**: Access control và security
- **Amazon SNS**: Notifications và alerts
- **AWS Step Functions**: Orchestrate crawler workflows
