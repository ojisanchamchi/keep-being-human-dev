# AWS Glue Data Catalog

## Tổng quan

AWS Glue Data Catalog là node đại diện cho metadata repository trung tâm của AWS Glue ecosystem. Data Catalog lưu trữ metadata về data sources, transformations, và targets, cung cấp unified view của dữ liệu across multiple data stores. Đây là thành phần cốt lõi cho data discovery, schema management, và ETL operations trong AWS analytics ecosystem.

## Chức năng chính

### 1. Metadata Management
- **Schema Storage**: Lưu trữ table schemas và column definitions
- **Database Organization**: Tổ chức tables thành logical databases
- **Partition Management**: Quản lý partition metadata
- **Data Location**: Tracking physical location của data

### 2. Schema Evolution
- **Version Control**: Theo dõi schema versions theo thời gian
- **Backward Compatibility**: Maintain compatibility với older schemas
- **Change Detection**: Tự động phát hiện schema changes
- **Impact Analysis**: Phân tích impact của schema changes

### 3. Data Discovery
- **Search Capabilities**: Tìm kiếm tables và columns
- **Data Lineage**: Theo dõi data flow và transformations
- **Classification**: Tự động classify sensitive data
- **Tagging**: Metadata tagging cho organization

### 4. Integration Hub
- **Cross-Service**: Tích hợp với Athena, EMR, Redshift, Spark
- **API Access**: RESTful APIs cho programmatic access
- **Security Integration**: IAM-based access control
- **Event Notifications**: CloudWatch events cho metadata changes

## Use Cases phổ biến

1. **Centralized Metadata**: Single source of truth cho metadata
2. **Data Governance**: Implement data governance policies
3. **Self-Service Analytics**: Enable self-service data discovery
4. **ETL Automation**: Automate ETL job creation
5. **Compliance Management**: Track sensitive data locations

## Diagram Architecture

Kiến trúc AWS Glue Data Catalog ecosystem:

![AWS Glue Data Catalog Architecture](/img/aws-analytics/glue-data-catalog.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import GlueDataCatalog, GlueCrawlers, Athena, EMR
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Redshift, Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Spark

with Diagram("AWS Glue Data Catalog Architecture", show=False, direction="TB"):
    
    users = Users("Data Analysts")
    
    with Cluster("Data Sources"):
        s3_data_lake = S3("Data Lake")
        rds_db = RDS("RDS Database")
        redshift_dw = Redshift("Data Warehouse")
        dynamodb_table = Dynamodb("DynamoDB")
    
    with Cluster("Metadata Discovery"):
        crawlers = GlueCrawlers("Glue Crawlers")
        manual_entry = Lambda("Manual Entry")
        api_import = Lambda("API Import")
    
    with Cluster("Data Catalog Core"):
        data_catalog = GlueDataCatalog("Glue Data Catalog")
        
        with Cluster("Catalog Structure"):
            databases = GlueDataCatalog("Databases")
            tables = GlueDataCatalog("Tables")
            partitions = GlueDataCatalog("Partitions")
            connections = GlueDataCatalog("Connections")
    
    with Cluster("Analytics Services"):
        athena = Athena("Athena")
        emr_cluster = EMR("EMR")
        spark_jobs = Spark("Spark Jobs")
        etl_jobs = Lambda("Glue ETL")
    
    with Cluster("Data Governance"):
        data_lineage = GlueDataCatalog("Data Lineage")
        classification = GlueDataCatalog("Data Classification")
        security_tags = IAM("Security Tags")
    
    with Cluster("Monitoring & Events"):
        cloudwatch = Cloudwatch("CloudWatch")
        notifications = SNS("Notifications")
        event_queue = SQS("Event Queue")
    
    # Metadata discovery flow
    s3_data_lake >> crawlers
    rds_db >> crawlers
    redshift_dw >> crawlers
    dynamodb_table >> crawlers
    
    crawlers >> Edge(label="Discover Schema") >> data_catalog
    manual_entry >> Edge(label="Manual Input") >> data_catalog
    api_import >> Edge(label="API Import") >> data_catalog
    
    # Catalog structure
    data_catalog >> databases
    data_catalog >> tables
    data_catalog >> partitions
    data_catalog >> connections
    
    # Analytics consumption
    data_catalog >> Edge(label="Schema Info") >> athena
    data_catalog >> Edge(label="Metadata") >> emr_cluster
    data_catalog >> Edge(label="Table Definitions") >> spark_jobs
    data_catalog >> Edge(label="ETL Metadata") >> etl_jobs
    
    # Data governance
    data_catalog >> data_lineage
    data_catalog >> classification
    data_catalog >> security_tags
    
    # User interaction
    users >> Edge(label="Search & Browse") >> data_catalog
    users >> Edge(label="Query Data") >> athena
    users >> Edge(label="Run Analytics") >> emr_cluster
    
    # Monitoring and events
    data_catalog >> Edge(label="Metadata Events") >> cloudwatch
    cloudwatch >> notifications
    data_catalog >> event_queue
```

## Data Catalog Structure

### 1. Database Management
```python
import boto3

glue = boto3.client('glue')

# Create database
database_config = {
    'DatabaseInput': {
        'Name': 'analytics_db',
        'Description': 'Analytics database for data lake',
        'LocationUri': 's3://data-lake/analytics/',
        'Parameters': {
            'classification': 'analytics',
            'department': 'data-engineering',
            'cost-center': 'analytics-team'
        }
    }
}

glue.create_database(**database_config)

# Create multiple databases for organization
databases = [
    {
        'Name': 'raw_data_db',
        'Description': 'Raw data from various sources',
        'LocationUri': 's3://data-lake/raw/'
    },
    {
        'Name': 'processed_data_db', 
        'Description': 'Processed and cleaned data',
        'LocationUri': 's3://data-lake/processed/'
    },
    {
        'Name': 'analytics_db',
        'Description': 'Analytics-ready datasets',
        'LocationUri': 's3://data-lake/analytics/'
    }
]

for db in databases:
    glue.create_database(DatabaseInput=db)
```

### 2. Table Definition
```python
# Create table with comprehensive metadata
table_config = {
    'DatabaseName': 'analytics_db',
    'TableInput': {
        'Name': 'customer_events',
        'Description': 'Customer interaction events',
        'Owner': 'data-engineering-team',
        'Parameters': {
            'classification': 'parquet',
            'compressionType': 'snappy',
            'typeOfData': 'file',
            'sizeKey': '1000000',
            'recordCount': '500000',
            'averageRecordSize': '200',
            'has_encrypted_data': 'false'
        },
        'StorageDescriptor': {
            'Columns': [
                {
                    'Name': 'event_id',
                    'Type': 'string',
                    'Comment': 'Unique event identifier'
                },
                {
                    'Name': 'customer_id',
                    'Type': 'string',
                    'Comment': 'Customer identifier'
                },
                {
                    'Name': 'event_type',
                    'Type': 'string',
                    'Comment': 'Type of event (click, view, purchase)'
                },
                {
                    'Name': 'timestamp',
                    'Type': 'timestamp',
                    'Comment': 'Event timestamp'
                },
                {
                    'Name': 'properties',
                    'Type': 'struct<page:string,product_id:string,amount:double>',
                    'Comment': 'Event properties'
                }
            ],
            'Location': 's3://data-lake/analytics/customer_events/',
            'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
            'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
            'SerdeInfo': {
                'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
            },
            'Compressed': True,
            'StoredAsSubDirectories': False
        },
        'PartitionKeys': [
            {
                'Name': 'year',
                'Type': 'string',
                'Comment': 'Year partition'
            },
            {
                'Name': 'month',
                'Type': 'string', 
                'Comment': 'Month partition'
            },
            {
                'Name': 'day',
                'Type': 'string',
                'Comment': 'Day partition'
            }
        ],
        'TableType': 'EXTERNAL_TABLE'
    }
}

glue.create_table(**table_config)
```

### 3. Partition Management
```python
class PartitionManager:
    def __init__(self, glue_client):
        self.glue = glue_client
    
    def add_partitions_batch(self, database_name, table_name, partitions):
        """Add multiple partitions efficiently"""
        
        partition_inputs = []
        for partition in partitions:
            partition_input = {
                'Values': partition['values'],
                'StorageDescriptor': {
                    'Columns': partition.get('columns', []),
                    'Location': partition['location'],
                    'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
                    'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
                    'SerdeInfo': {
                        'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
                    }
                },
                'Parameters': partition.get('parameters', {})
            }
            partition_inputs.append(partition_input)
        
        # Batch create partitions (max 100 per batch)
        batch_size = 100
        for i in range(0, len(partition_inputs), batch_size):
            batch = partition_inputs[i:i + batch_size]
            
            try:
                self.glue.batch_create_partition(
                    DatabaseName=database_name,
                    TableName=table_name,
                    PartitionInputList=batch
                )
                print(f"Created {len(batch)} partitions")
            except Exception as e:
                print(f"Error creating partition batch: {str(e)}")
    
    def auto_discover_partitions(self, database_name, table_name, s3_path):
        """Automatically discover and add new partitions"""
        import boto3
        from datetime import datetime, timedelta
        
        s3 = boto3.client('s3')
        bucket = s3_path.split('/')[2]
        prefix = '/'.join(s3_path.split('/')[3:])
        
        # List S3 objects to find partition structure
        response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            Delimiter='/'
        )
        
        partitions = []
        for obj in response.get('CommonPrefixes', []):
            partition_path = obj['Prefix']
            
            # Extract partition values from path
            # Assuming structure: year=2023/month=01/day=15/
            path_parts = partition_path.strip('/').split('/')
            partition_values = []
            
            for part in path_parts:
                if '=' in part:
                    partition_values.append(part.split('=')[1])
            
            if partition_values:
                partitions.append({
                    'values': partition_values,
                    'location': f's3://{bucket}/{partition_path}'
                })
        
        if partitions:
            self.add_partitions_batch(database_name, table_name, partitions)
```

## Advanced Features

### 1. Data Lineage Tracking
```python
class DataLineageTracker:
    def __init__(self, glue_client):
        self.glue = glue_client
    
    def create_lineage_relationship(self, source_table, target_table, transformation_info):
        """Create data lineage relationship"""
        
        lineage_metadata = {
            'source': {
                'database': source_table['database'],
                'table': source_table['table'],
                'columns': source_table.get('columns', [])
            },
            'target': {
                'database': target_table['database'],
                'table': target_table['table'],
                'columns': target_table.get('columns', [])
            },
            'transformation': {
                'type': transformation_info['type'],
                'job_name': transformation_info.get('job_name'),
                'transformation_logic': transformation_info.get('logic'),
                'created_by': transformation_info.get('created_by'),
                'created_date': datetime.utcnow().isoformat()
            }
        }
        
        # Store lineage in table parameters
        self.glue.update_table(
            DatabaseName=target_table['database'],
            TableInput={
                'Name': target_table['table'],
                'Parameters': {
                    'data_lineage': json.dumps(lineage_metadata)
                }
            }
        )
    
    def get_table_lineage(self, database_name, table_name):
        """Get lineage information for a table"""
        
        try:
            response = self.glue.get_table(
                DatabaseName=database_name,
                Name=table_name
            )
            
            parameters = response['Table'].get('Parameters', {})
            lineage_data = parameters.get('data_lineage')
            
            if lineage_data:
                return json.loads(lineage_data)
            
        except Exception as e:
            print(f"Error getting lineage: {str(e)}")
        
        return None
    
    def trace_data_flow(self, database_name, table_name, direction='downstream'):
        """Trace data flow upstream or downstream"""
        
        visited = set()
        flow_graph = {}
        
        def trace_recursive(db, table, current_direction):
            key = f"{db}.{table}"
            if key in visited:
                return
            
            visited.add(key)
            lineage = self.get_table_lineage(db, table)
            
            if lineage:
                if current_direction == 'downstream':
                    # Find tables that use this table as source
                    flow_graph[key] = lineage.get('targets', [])
                else:
                    # Find source tables for this table
                    flow_graph[key] = lineage.get('sources', [])
                
                # Recursively trace
                for related_table in flow_graph[key]:
                    trace_recursive(
                        related_table['database'],
                        related_table['table'],
                        current_direction
                    )
        
        trace_recursive(database_name, table_name, direction)
        return flow_graph
```

### 2. Data Classification
```python
class DataClassifier:
    def __init__(self, glue_client):
        self.glue = glue_client
        self.sensitive_patterns = {
            'PII': [
                r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
                r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'  # Credit Card
            ],
            'FINANCIAL': [
                r'\$\d+\.\d{2}',  # Currency
                r'\b\d{9}\b',  # Routing number
                r'\bACCT\d+\b'  # Account number
            ]
        }
    
    def classify_table_columns(self, database_name, table_name):
        """Classify columns based on content patterns"""
        
        # Get table metadata
        table = self.glue.get_table(
            DatabaseName=database_name,
            Name=table_name
        )
        
        columns = table['Table']['StorageDescriptor']['Columns']
        classifications = {}
        
        for column in columns:
            column_name = column['Name']
            column_type = column['Type']
            
            # Classify based on name patterns
            classification = self.classify_by_name(column_name)
            
            # Classify based on data type
            if not classification:
                classification = self.classify_by_type(column_type)
            
            if classification:
                classifications[column_name] = classification
        
        # Update table with classification metadata
        self.update_table_classification(database_name, table_name, classifications)
        
        return classifications
    
    def classify_by_name(self, column_name):
        """Classify column based on name patterns"""
        
        name_lower = column_name.lower()
        
        if any(pattern in name_lower for pattern in ['ssn', 'social_security', 'social']):
            return 'PII_SSN'
        elif any(pattern in name_lower for pattern in ['email', 'mail']):
            return 'PII_EMAIL'
        elif any(pattern in name_lower for pattern in ['phone', 'mobile', 'tel']):
            return 'PII_PHONE'
        elif any(pattern in name_lower for pattern in ['address', 'addr', 'street']):
            return 'PII_ADDRESS'
        elif any(pattern in name_lower for pattern in ['salary', 'income', 'wage']):
            return 'FINANCIAL_INCOME'
        elif any(pattern in name_lower for pattern in ['account', 'acct']):
            return 'FINANCIAL_ACCOUNT'
        
        return None
    
    def classify_by_type(self, column_type):
        """Classify column based on data type"""
        
        if 'decimal' in column_type or 'double' in column_type:
            return 'NUMERIC'
        elif 'timestamp' in column_type or 'date' in column_type:
            return 'TEMPORAL'
        elif 'string' in column_type:
            return 'TEXT'
        
        return 'UNKNOWN'
    
    def update_table_classification(self, database_name, table_name, classifications):
        """Update table with classification metadata"""
        
        # Get current table
        table = self.glue.get_table(
            DatabaseName=database_name,
            Name=table_name
        )
        
        # Update parameters with classification
        parameters = table['Table'].get('Parameters', {})
        parameters['data_classification'] = json.dumps(classifications)
        
        # Update table
        table_input = table['Table'].copy()
        table_input['Parameters'] = parameters
        
        # Remove read-only fields
        table_input.pop('DatabaseName', None)
        table_input.pop('CreateTime', None)
        table_input.pop('UpdateTime', None)
        table_input.pop('CreatedBy', None)
        table_input.pop('IsRegisteredWithLakeFormation', None)
        
        self.glue.update_table(
            DatabaseName=database_name,
            TableInput=table_input
        )
```

### 3. Schema Evolution Management
```python
class SchemaEvolutionManager:
    def __init__(self, glue_client):
        self.glue = glue_client
    
    def compare_schemas(self, database_name, table_name, version1, version2):
        """Compare two schema versions"""
        
        # Get table versions
        response = self.glue.get_table_versions(
            DatabaseName=database_name,
            TableName=table_name,
            MaxResults=100
        )
        
        versions = response['TableVersions']
        
        # Find specified versions
        schema1 = None
        schema2 = None
        
        for version in versions:
            if version['VersionId'] == version1:
                schema1 = version['Table']['StorageDescriptor']['Columns']
            elif version['VersionId'] == version2:
                schema2 = version['Table']['StorageDescriptor']['Columns']
        
        if not schema1 or not schema2:
            raise ValueError("One or both schema versions not found")
        
        # Compare schemas
        return self.analyze_schema_differences(schema1, schema2)
    
    def analyze_schema_differences(self, schema1, schema2):
        """Analyze differences between two schemas"""
        
        cols1 = {col['Name']: col for col in schema1}
        cols2 = {col['Name']: col for col in schema2}
        
        differences = {
            'added_columns': [],
            'removed_columns': [],
            'modified_columns': [],
            'reordered_columns': []
        }
        
        # Find added columns
        for col_name in cols2:
            if col_name not in cols1:
                differences['added_columns'].append(cols2[col_name])
        
        # Find removed columns
        for col_name in cols1:
            if col_name not in cols2:
                differences['removed_columns'].append(cols1[col_name])
        
        # Find modified columns
        for col_name in cols1:
            if col_name in cols2:
                if cols1[col_name]['Type'] != cols2[col_name]['Type']:
                    differences['modified_columns'].append({
                        'column_name': col_name,
                        'old_type': cols1[col_name]['Type'],
                        'new_type': cols2[col_name]['Type']
                    })
        
        return differences
    
    def create_schema_migration_plan(self, differences):
        """Create migration plan for schema changes"""
        
        migration_plan = {
            'migration_steps': [],
            'risk_assessment': 'LOW',
            'estimated_downtime': '0 minutes',
            'rollback_plan': []
        }
        
        # Analyze risk
        if differences['removed_columns'] or differences['modified_columns']:
            migration_plan['risk_assessment'] = 'HIGH'
            migration_plan['estimated_downtime'] = '30 minutes'
        elif differences['added_columns']:
            migration_plan['risk_assessment'] = 'MEDIUM'
            migration_plan['estimated_downtime'] = '5 minutes'
        
        # Create migration steps
        for col in differences['added_columns']:
            migration_plan['migration_steps'].append({
                'action': 'ADD_COLUMN',
                'column': col,
                'sql': f"ALTER TABLE ADD COLUMN {col['Name']} {col['Type']}"
            })
        
        for col in differences['removed_columns']:
            migration_plan['migration_steps'].append({
                'action': 'DROP_COLUMN',
                'column': col,
                'sql': f"ALTER TABLE DROP COLUMN {col['Name']}"
            })
        
        return migration_plan
```

## Performance Optimization

### 1. Catalog Query Optimization
```python
class CatalogOptimizer:
    def __init__(self, glue_client):
        self.glue = glue_client
    
    def optimize_table_search(self, search_criteria):
        """Optimize table search with filters"""
        
        # Use pagination for large results
        paginator = self.glue.get_paginator('get_tables')
        
        page_iterator = paginator.paginate(
            DatabaseName=search_criteria.get('database', ''),
            Expression=search_criteria.get('expression', ''),
            MaxItems=search_criteria.get('max_items', 1000),
            PaginationConfig={
                'PageSize': 100
            }
        )
        
        tables = []
        for page in page_iterator:
            tables.extend(page['TableList'])
        
        return tables
    
    def cache_frequently_accessed_metadata(self, database_name):
        """Cache metadata for frequently accessed tables"""
        
        # Get all tables in database
        tables = self.glue.get_tables(DatabaseName=database_name)
        
        metadata_cache = {}
        
        for table in tables['TableList']:
            table_name = table['Name']
            
            # Cache essential metadata
            metadata_cache[table_name] = {
                'columns': table['StorageDescriptor']['Columns'],
                'location': table['StorageDescriptor']['Location'],
                'input_format': table['StorageDescriptor']['InputFormat'],
                'partition_keys': table.get('PartitionKeys', []),
                'parameters': table.get('Parameters', {}),
                'last_updated': table.get('UpdateTime', '').isoformat() if table.get('UpdateTime') else None
            }
        
        # Store cache (implementation depends on your caching strategy)
        return metadata_cache
```

## Security và Access Control

### 1. Fine-grained Access Control
```python
class CatalogSecurity:
    def __init__(self, glue_client, iam_client):
        self.glue = glue_client
        self.iam = iam_client
    
    def create_resource_policy(self, database_name, access_rules):
        """Create resource-based policy for database"""
        
        policy_document = {
            "Version": "2012-10-17",
            "Statement": []
        }
        
        for rule in access_rules:
            statement = {
                "Sid": rule['sid'],
                "Effect": rule['effect'],
                "Principal": rule['principal'],
                "Action": rule['actions'],
                "Resource": f"arn:aws:glue:*:*:database/{database_name}"
            }
            
            if rule.get('condition'):
                statement['Condition'] = rule['condition']
            
            policy_document['Statement'].append(statement)
        
        # Apply resource policy
        self.glue.put_resource_policy(
            PolicyInJson=json.dumps(policy_document)
        )
    
    def setup_column_level_security(self, database_name, table_name, column_permissions):
        """Setup column-level security"""
        
        # This would integrate with AWS Lake Formation
        # for fine-grained access control
        
        for permission in column_permissions:
            # Example: Grant SELECT on specific columns
            lake_formation_client = boto3.client('lakeformation')
            
            lake_formation_client.grant_permissions(
                Principal={'DataLakePrincipalIdentifier': permission['principal']},
                Resource={
                    'Table': {
                        'DatabaseName': database_name,
                        'Name': table_name
                    }
                },
                Permissions=['SELECT'],
                PermissionsWithGrantOption=[],
                CatalogId=permission.get('catalog_id', ''),
                ColumnWildcard={
                    'IncludedColumnNames': permission['columns']
                }
            )
```

## Best Practices

1. **Organization**: Organize tables into logical databases
2. **Naming Conventions**: Use consistent naming conventions
3. **Metadata Quality**: Maintain high-quality metadata với descriptions
4. **Schema Evolution**: Plan for schema changes
5. **Security**: Implement proper access controls
6. **Performance**: Optimize for query performance
7. **Governance**: Establish data governance policies
8. **Monitoring**: Monitor catalog usage và performance

## Tích hợp với các dịch vụ AWS khác

- **AWS Glue Crawlers**: Automatic metadata discovery
- **Amazon Athena**: Query cataloged data
- **Amazon EMR**: Access metadata for big data processing
- **AWS Glue ETL**: Use schemas for ETL jobs
- **Amazon Redshift**: Integrate với Redshift Spectrum
- **AWS Lake Formation**: Fine-grained access control
- **Amazon SageMaker**: ML feature store integration
- **AWS Lambda**: Programmatic catalog access
- **Amazon CloudWatch**: Monitoring và events
- **AWS IAM**: Access control và security
