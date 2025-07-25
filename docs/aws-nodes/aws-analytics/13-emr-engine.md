# EMR Engine

## Tổng quan

EMR Engine là node tổng quát đại diện cho các processing engines trong Amazon EMR ecosystem. Node này biểu thị các công cụ xử lý dữ liệu mạnh mẽ như Apache Spark, Apache Hadoop, Apache Flink, Presto, và nhiều framework khác chạy trên EMR cluster. EMR Engine cung cấp khả năng xử lý dữ liệu linh hoạt từ batch processing đến real-time analytics.

## Chức năng chính

### 1. Multi-Engine Support
- **Apache Spark**: In-memory processing cho big data
- **Apache Hadoop**: Distributed computing framework
- **Apache Flink**: Stream processing engine
- **Presto**: Distributed SQL query engine
- **Apache Hive**: Data warehouse software
- **Apache HBase**: NoSQL database

### 2. Processing Modes
- **Batch Processing**: Large-scale data processing
- **Stream Processing**: Real-time data processing
- **Interactive Analytics**: Ad-hoc queries và exploration
- **Machine Learning**: ML model training và inference

### 3. Resource Management
- **YARN**: Resource negotiation và scheduling
- **Kubernetes**: Container orchestration
- **Mesos**: Distributed systems kernel
- **Standalone**: Framework-specific resource management

### 4. Storage Integration
- **HDFS**: Hadoop Distributed File System
- **S3**: Amazon Simple Storage Service
- **EBS**: Elastic Block Store
- **Local Storage**: Instance store volumes

## Use Cases phổ biến

1. **ETL Pipelines**: Data transformation workflows
2. **Data Lake Analytics**: Large-scale data analysis
3. **Real-time Processing**: Streaming data processing
4. **Machine Learning**: ML model development
5. **Business Intelligence**: Interactive analytics

## Diagram Architecture

Kiến trúc EMR Engine với multiple processing frameworks:

![EMR Engine Architecture](/img/aws-analytics/emr-engine.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMREngine, Kinesis, Glue
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Spark

with Diagram("EMR Engine Architecture", show=False, direction="TB"):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Sources"):
        s3_data = S3("Data Lake")
        rds_db = RDS("Transactional DB")
        kinesis_stream = Kinesis("Streaming Data")
        external_data = EC2("External APIs")
    
    with Cluster("EMR Cluster"):
        emr_engine = EMREngine("EMR Processing\nEngines")
        
        with Cluster("Processing Frameworks"):
            spark_engine = Spark("Apache Spark")
            hadoop_engine = EC2("Hadoop MapReduce")
            flink_engine = EC2("Apache Flink")
            presto_engine = EC2("Presto")
            hive_engine = EC2("Apache Hive")
    
    with Cluster("Resource Management"):
        yarn_rm = EC2("YARN ResourceManager")
        yarn_nm = [EC2("NodeManager 1"), EC2("NodeManager 2")]
        k8s_master = EC2("Kubernetes Master")
    
    with Cluster("Storage Layer"):
        hdfs_storage = S3("HDFS Storage")
        s3_storage = S3("S3 Storage")
        local_storage = EC2("Local Storage")
    
    with Cluster("Output & Analytics"):
        processed_data = S3("Processed Data")
        ml_models = SagemakerModel("ML Models")
        data_catalog = Glue("Data Catalog")
        analytics_api = EC2("Analytics API")
    
    with Cluster("Monitoring & Management"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("Security")
    
    # Data ingestion
    s3_data >> Edge(label="Batch Data") >> emr_engine
    rds_db >> Edge(label="CDC") >> emr_engine
    kinesis_stream >> Edge(label="Streaming") >> emr_engine
    external_data >> Edge(label="API Data") >> emr_engine
    
    # Processing engines
    emr_engine >> spark_engine
    emr_engine >> hadoop_engine
    emr_engine >> flink_engine
    emr_engine >> presto_engine
    emr_engine >> hive_engine
    
    # Resource management
    emr_engine >> yarn_rm
    yarn_rm >> yarn_nm
    emr_engine >> k8s_master
    
    # Storage integration
    spark_engine >> hdfs_storage
    hadoop_engine >> s3_storage
    flink_engine >> local_storage
    
    # Output generation
    spark_engine >> processed_data
    flink_engine >> analytics_api
    hive_engine >> data_catalog
    spark_engine >> ml_models
    
    # User interaction
    users >> Edge(label="Submit Jobs") >> emr_engine
    users >> Edge(label="Query Data") >> presto_engine
    users >> Edge(label="Stream Processing") >> flink_engine
    
    # Monitoring
    emr_engine >> monitoring
    security >> emr_engine
```

## Processing Engines

### 1. Apache Spark
```python
# Spark application example
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("EMR-Spark-Processing") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

# Read data from S3
df = spark.read.parquet("s3://data-lake/raw/events/")

# Data transformation
processed_df = df \
    .filter(col("event_type") == "purchase") \
    .groupBy("user_id", "product_category") \
    .agg(
        sum("amount").alias("total_spent"),
        count("*").alias("purchase_count")
    ) \
    .orderBy(desc("total_spent"))

# Write results back to S3
processed_df.write \
    .mode("overwrite") \
    .parquet("s3://data-lake/processed/user_purchases/")
```

### 2. Apache Flink
```java
// Flink streaming application
StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

// Configure checkpointing
env.enableCheckpointing(60000);
env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);

// Data source
DataStream<Event> events = env
    .addSource(new KinesisSource<>(kinesisConfig))
    .map(new EventDeserializer());

// Stream processing
DataStream<ProcessedEvent> processed = events
    .keyBy(Event::getUserId)
    .window(TumblingProcessingTimeWindows.of(Time.minutes(5)))
    .aggregate(new EventAggregator());

// Sink to S3
processed.addSink(new S3Sink<>(s3Config));

env.execute("Real-time Event Processing");
```

### 3. Presto
```sql
-- Presto query example
WITH user_metrics AS (
  SELECT 
    user_id,
    COUNT(*) as total_events,
    SUM(CASE WHEN event_type = 'purchase' THEN amount ELSE 0 END) as total_spent,
    AVG(session_duration) as avg_session_duration
  FROM events 
  WHERE date_partition >= '2023-01-01'
  GROUP BY user_id
),
user_segments AS (
  SELECT 
    user_id,
    total_spent,
    CASE 
      WHEN total_spent > 1000 THEN 'high_value'
      WHEN total_spent > 100 THEN 'medium_value'
      ELSE 'low_value'
    END as user_segment
  FROM user_metrics
)
SELECT 
  user_segment,
  COUNT(*) as user_count,
  AVG(total_spent) as avg_spent_per_user
FROM user_segments
GROUP BY user_segment
ORDER BY avg_spent_per_user DESC;
```

### 4. Apache Hive
```sql
-- Hive data processing
CREATE EXTERNAL TABLE IF NOT EXISTS raw_events (
  event_id STRING,
  user_id STRING,
  event_type STRING,
  timestamp BIGINT,
  properties MAP<STRING, STRING>
)
PARTITIONED BY (date_partition STRING)
STORED AS PARQUET
LOCATION 's3://data-lake/raw/events/';

-- Add partitions
MSCK REPAIR TABLE raw_events;

-- Create processed table
CREATE TABLE user_daily_summary
STORED AS PARQUET
AS
SELECT 
  user_id,
  date_partition,
  COUNT(*) as event_count,
  COUNT(DISTINCT event_type) as unique_event_types,
  SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) as purchase_count
FROM raw_events
WHERE date_partition >= '2023-01-01'
GROUP BY user_id, date_partition;
```

## Resource Management

### 1. YARN Configuration
```xml
<!-- yarn-site.xml -->
<configuration>
  <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>master-node</value>
  </property>
  
  <property>
    <name>yarn.scheduler.maximum-allocation-mb</name>
    <value>14336</value>
  </property>
  
  <property>
    <name>yarn.scheduler.maximum-allocation-vcores</name>
    <value>8</value>
  </property>
  
  <property>
    <name>yarn.nodemanager.resource.memory-mb</name>
    <value>14336</value>
  </property>
  
  <property>
    <name>yarn.nodemanager.resource.cpu-vcores</name>
    <value>8</value>
  </property>
</configuration>
```

### 2. Kubernetes Integration
```yaml
# Spark on Kubernetes
apiVersion: v1
kind: ConfigMap
metadata:
  name: spark-config
data:
  spark-defaults.conf: |
    spark.kubernetes.container.image=spark:3.3.0
    spark.kubernetes.authenticate.driver.serviceAccountName=spark
    spark.kubernetes.executor.instances=10
    spark.kubernetes.executor.request.cores=2
    spark.kubernetes.executor.limit.cores=4
    spark.kubernetes.executor.request.memory=4g
    spark.kubernetes.executor.limit.memory=8g

---
apiVersion: batch/v1
kind: Job
metadata:
  name: spark-job
spec:
  template:
    spec:
      containers:
      - name: spark-driver
        image: spark:3.3.0
        command: ["/opt/spark/bin/spark-submit"]
        args:
        - "--master"
        - "k8s://https://kubernetes.default.svc:443"
        - "--deploy-mode"
        - "client"
        - "s3://spark-jobs/data-processing.py"
```

## Performance Optimization

### 1. Spark Tuning
```python
# Spark configuration for performance
spark_config = {
    # Memory management
    "spark.executor.memory": "8g",
    "spark.executor.memoryFraction": "0.8",
    "spark.executor.memoryStorageFraction": "0.2",
    
    # CPU optimization
    "spark.executor.cores": "4",
    "spark.executor.instances": "20",
    "spark.default.parallelism": "160",
    
    # Shuffle optimization
    "spark.sql.shuffle.partitions": "400",
    "spark.shuffle.compress": "true",
    "spark.shuffle.spill.compress": "true",
    
    # Serialization
    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
    "spark.kryo.registrationRequired": "false",
    
    # Adaptive query execution
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true"
}

spark = SparkSession.builder \
    .appName("Optimized-Spark-Job") \
    .config(conf=SparkConf().setAll(spark_config.items())) \
    .getOrCreate()
```

### 2. Flink Tuning
```java
// Flink performance configuration
Configuration config = new Configuration();

// Memory configuration
config.setString("taskmanager.memory.process.size", "8g");
config.setString("taskmanager.memory.flink.size", "6g");
config.setString("taskmanager.memory.managed.fraction", "0.4");

// Parallelism
config.setInteger("parallelism.default", 16);
config.setInteger("taskmanager.numberOfTaskSlots", 4);

// Checkpointing
config.setLong("execution.checkpointing.interval", 60000);
config.setString("execution.checkpointing.mode", "EXACTLY_ONCE");
config.setLong("execution.checkpointing.timeout", 600000);

// Network
config.setString("taskmanager.network.memory.fraction", "0.1");
config.setInteger("taskmanager.network.numberOfBuffers", 8192);

StreamExecutionEnvironment env = StreamExecutionEnvironment.createLocalEnvironmentWithWebUI(config);
```

## Monitoring và Debugging

### 1. Spark Monitoring
```python
# Custom Spark metrics
from pyspark.util import AccumulatorParam

class ListAccumulatorParam(AccumulatorParam):
    def zero(self, value):
        return []
    
    def addInPlace(self, list1, list2):
        return list1 + list2

# Create custom accumulator
error_accumulator = spark.sparkContext.accumulator([], ListAccumulatorParam())

def process_record(record):
    try:
        # Process record
        return transform_record(record)
    except Exception as e:
        error_accumulator.add([str(e)])
        return None

# Use in RDD operations
processed_rdd = input_rdd.map(process_record).filter(lambda x: x is not None)

# Check errors after action
processed_rdd.count()
print(f"Errors encountered: {error_accumulator.value}")
```

### 2. Application Logging
```python
# Structured logging for EMR applications
import logging
import json
from datetime import datetime

class EMRLogger:
    def __init__(self, app_name):
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_job_start(self, job_id, job_type, input_path):
        self.logger.info(json.dumps({
            "event": "job_start",
            "job_id": job_id,
            "job_type": job_type,
            "input_path": input_path,
            "timestamp": datetime.utcnow().isoformat()
        }))
    
    def log_job_complete(self, job_id, records_processed, duration):
        self.logger.info(json.dumps({
            "event": "job_complete",
            "job_id": job_id,
            "records_processed": records_processed,
            "duration_seconds": duration,
            "timestamp": datetime.utcnow().isoformat()
        }))

# Usage
logger = EMRLogger("data-processing-job")
logger.log_job_start("job-123", "etl", "s3://data/input/")
```

## Security Best Practices

### 1. Data Encryption
```python
# Spark with encryption
spark = SparkSession.builder \
    .appName("Secure-Spark-Job") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.hadoop.fs.s3a.server-side-encryption-algorithm", "AES256") \
    .config("spark.hadoop.fs.s3a.server-side-encryption.key", "arn:aws:kms:region:account:key/key-id") \
    .config("spark.authenticate", "true") \
    .config("spark.network.crypto.enabled", "true") \
    .config("spark.io.encryption.enabled", "true") \
    .getOrCreate()
```

### 2. Access Control
```bash
# Kerberos authentication
kinit -kt /etc/security/keytabs/spark.keytab spark/hostname@REALM

# HDFS permissions
hdfs dfsadmin -setDefaultAcl /data/sensitive user:analyst:r--,group:analytics:r--,other::---

# Hive authorization
SET hive.security.authorization.enabled=true;
SET hive.security.authorization.manager=org.apache.hadoop.hive.ql.security.authorization.plugin.sqlstd.SQLStdHiveAuthorizerFactory;
```

## Cost Optimization

### 1. Spot Instance Strategy
```python
# EMR cluster with Spot instances
import boto3

emr = boto3.client('emr')

cluster_config = {
    'Name': 'cost-optimized-cluster',
    'ReleaseLabel': 'emr-6.9.0',
    'Instances': {
        'MasterInstanceType': 'm5.xlarge',
        'SlaveInstanceType': 'm5.xlarge',
        'InstanceCount': 10,
        'Ec2KeyName': 'my-key',
        'InstanceFleets': [
            {
                'Name': 'Master',
                'InstanceFleetType': 'MASTER',
                'TargetOnDemandCapacity': 1,
                'InstanceTypeConfigs': [
                    {
                        'InstanceType': 'm5.xlarge',
                        'WeightedCapacity': 1
                    }
                ]
            },
            {
                'Name': 'Core',
                'InstanceFleetType': 'CORE',
                'TargetOnDemandCapacity': 2,
                'TargetSpotCapacity': 8,
                'InstanceTypeConfigs': [
                    {
                        'InstanceType': 'm5.xlarge',
                        'WeightedCapacity': 1,
                        'BidPrice': '0.10'
                    },
                    {
                        'InstanceType': 'm5.2xlarge',
                        'WeightedCapacity': 2,
                        'BidPrice': '0.20'
                    }
                ]
            }
        ]
    }
}

response = emr.run_job_flow(**cluster_config)
```

### 2. Auto Termination
```python
# Auto-termination configuration
auto_termination_config = {
    'IdleTimeout': 3600,  # 1 hour
    'MaxIdleTimeBeforeTermination': 7200  # 2 hours
}

# Step configuration with auto-termination
step_config = {
    'Name': 'Data Processing Step',
    'ActionOnFailure': 'TERMINATE_CLUSTER',
    'HadoopJarStep': {
        'Jar': 'command-runner.jar',
        'Args': [
            'spark-submit',
            '--deploy-mode', 'cluster',
            's3://my-bucket/spark-job.py'
        ]
    }
}
```

## Best Practices

1. **Engine Selection**: Chọn engine phù hợp cho workload
2. **Resource Tuning**: Optimize memory và CPU allocation
3. **Data Partitioning**: Partition data hiệu quả
4. **Caching Strategy**: Cache intermediate results
5. **Error Handling**: Implement robust error handling
6. **Monitoring**: Comprehensive monitoring setup
7. **Security**: Enable encryption và access controls
8. **Cost Management**: Use Spot instances và auto-termination

## Tích hợp với các dịch vụ AWS khác

- **Amazon S3**: Primary data storage
- **AWS Glue**: Data catalog và ETL
- **Amazon Kinesis**: Real-time data streaming
- **Amazon Redshift**: Data warehouse integration
- **Amazon SageMaker**: Machine learning workflows
- **AWS Lambda**: Event-driven processing
- **Amazon CloudWatch**: Monitoring và alerting
- **AWS IAM**: Identity và access management
- **Amazon VPC**: Network security
- **AWS KMS**: Encryption key management
