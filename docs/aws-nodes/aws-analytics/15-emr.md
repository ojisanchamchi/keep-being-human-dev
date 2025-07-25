# Amazon EMR

## Tổng quan

Amazon EMR (Elastic MapReduce) là node tổng quát đại diện cho dịch vụ big data platform được quản lý hoàn toàn của AWS. EMR giúp bạn dễ dàng chạy và mở rộng các framework big data như Apache Spark, Apache Hadoop, Apache HBase, Apache Flink, Apache Hudi, và Presto trên AWS. Node này biểu thị toàn bộ EMR ecosystem với khả năng xử lý petabyte-scale data một cách cost-effective.

## Chức năng chính

### 1. Managed Big Data Platform
- **Framework Support**: Spark, Hadoop, Flink, Presto, HBase, Hive
- **Auto Scaling**: Tự động điều chỉnh cluster size
- **Spot Integration**: Sử dụng EC2 Spot Instances
- **Serverless Options**: EMR Serverless cho serverless analytics

### 2. Flexible Deployment Options
- **EC2 Clusters**: Traditional cluster deployment
- **EKS Integration**: Run on Amazon EKS
- **Outposts**: On-premises deployment
- **Serverless**: Pay-per-use serverless execution

### 3. Storage Integration
- **Amazon S3**: Primary data lake storage
- **HDFS**: Local distributed storage
- **EBS**: High-performance block storage
- **EFS**: Shared file system

### 4. Enterprise Features
- **Security**: Encryption, Kerberos, IAM integration
- **Monitoring**: CloudWatch integration
- **Notebooks**: EMR Notebooks cho interactive development
- **Studio**: EMR Studio cho collaborative analytics

## Use Cases phổ biến

1. **Data Processing**: Large-scale ETL operations
2. **Machine Learning**: ML model training và inference
3. **Interactive Analytics**: Ad-hoc data exploration
4. **Streaming Analytics**: Real-time data processing
5. **Data Science**: Research và experimentation

## Diagram Architecture

Kiến trúc tổng quan Amazon EMR ecosystem:

![Amazon EMR Architecture](/img/aws-analytics/emr.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMR, Kinesis, Glue, Athena
from diagrams.aws.storage import S3, EBS
from diagrams.aws.compute import EC2, EKS, Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.ml import SagemakerModel, SagemakerNotebook
from diagrams.aws.network import ELB, VPC
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users

with Diagram("Amazon EMR Architecture", show=False, direction="TB"):
    
    users = Users("Data Teams")
    
    with Cluster("Data Sources"):
        s3_data_lake = S3("Data Lake")
        rds_oltp = RDS("OLTP Systems")
        kinesis_streams = Kinesis("Streaming Data")
        external_apis = Lambda("External APIs")
    
    with Cluster("EMR Ecosystem"):
        emr_service = EMR("Amazon EMR")
        
        with Cluster("Deployment Options"):
            emr_ec2 = EC2("EMR on EC2")
            emr_eks = EKS("EMR on EKS")
            emr_serverless = Lambda("EMR Serverless")
        
        with Cluster("Processing Frameworks"):
            spark = EC2("Apache Spark")
            hadoop = EC2("Apache Hadoop")
            flink = EC2("Apache Flink")
            presto = EC2("Presto")
            hbase = EC2("Apache HBase")
    
    with Cluster("Development Environment"):
        emr_studio = SagemakerNotebook("EMR Studio")
        emr_notebooks = SagemakerNotebook("EMR Notebooks")
        jupyter = EC2("Jupyter Hub")
    
    with Cluster("Storage Layer"):
        s3_storage = S3("S3 Storage")
        hdfs_storage = EBS("HDFS Storage")
        efs_storage = EBS("EFS Storage")
    
    with Cluster("Analytics & ML"):
        athena = Athena("Athena")
        sagemaker = SagemakerModel("SageMaker")
        glue_catalog = Glue("Data Catalog")
        quicksight = EC2("QuickSight")
    
    with Cluster("Infrastructure"):
        vpc = VPC("VPC")
        load_balancer = ELB("Load Balancer")
        monitoring = Cloudwatch("Monitoring")
        security = IAM("Security")
    
    # Data ingestion
    s3_data_lake >> Edge(label="Batch Data") >> emr_service
    rds_oltp >> Edge(label="CDC") >> emr_service
    kinesis_streams >> Edge(label="Streaming") >> emr_service
    external_apis >> Edge(label="API Data") >> emr_service
    
    # EMR deployment options
    emr_service >> emr_ec2
    emr_service >> emr_eks
    emr_service >> emr_serverless
    
    # Processing frameworks
    emr_ec2 >> spark
    emr_ec2 >> hadoop
    emr_eks >> flink
    emr_serverless >> spark
    
    # Development environment
    users >> emr_studio
    users >> emr_notebooks
    emr_studio >> emr_service
    emr_notebooks >> jupyter
    
    # Storage integration
    spark >> s3_storage
    hadoop >> hdfs_storage
    flink >> efs_storage
    
    # Analytics integration
    spark >> athena
    emr_service >> sagemaker
    hadoop >> glue_catalog
    emr_service >> quicksight
    
    # Infrastructure
    emr_service >> vpc
    emr_service >> load_balancer
    emr_service >> monitoring
    security >> emr_service
    
    # User interaction
    users >> Edge(label="Submit Jobs") >> emr_service
    users >> Edge(label="Monitor") >> monitoring
```

## EMR Deployment Options

### 1. EMR on EC2
```python
# EMR cluster configuration
import boto3

emr = boto3.client('emr')

cluster_config = {
    'Name': 'production-analytics-cluster',
    'ReleaseLabel': 'emr-6.9.0',
    'Applications': [
        {'Name': 'Spark'},
        {'Name': 'Hadoop'},
        {'Name': 'Hive'},
        {'Name': 'Presto'},
        {'Name': 'JupyterHub'}
    ],
    'Instances': {
        'InstanceGroups': [
            {
                'Name': 'Master',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 1
            },
            {
                'Name': 'Core',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'CORE',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 2
            },
            {
                'Name': 'Task',
                'Market': 'SPOT',
                'InstanceRole': 'TASK',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 4,
                'BidPrice': '0.10'
            }
        ],
        'Ec2KeyName': 'my-key-pair',
        'KeepJobFlowAliveWhenNoSteps': True,
        'TerminationProtected': False
    },
    'ServiceRole': 'EMR_DefaultRole',
    'JobFlowRole': 'EMR_EC2_DefaultRole',
    'LogUri': 's3://my-emr-logs/',
    'BootstrapActions': [
        {
            'Name': 'Install Additional Packages',
            'ScriptBootstrapAction': {
                'Path': 's3://my-bootstrap-scripts/install-packages.sh'
            }
        }
    ]
}

response = emr.run_job_flow(**cluster_config)
cluster_id = response['JobFlowId']
```

### 2. EMR on EKS
```yaml
# EMR on EKS configuration
apiVersion: emrcontainers.aws.crossplane.io/v1alpha1
kind: VirtualCluster
metadata:
  name: emr-eks-cluster
spec:
  forProvider:
    name: analytics-virtual-cluster
    containerProvider:
      - id: my-eks-cluster
        type: EKS
        info:
          eksInfo:
            - namespace: emr
    region: us-west-2
  providerConfigRef:
    name: aws-provider-config

---
apiVersion: batch/v1
kind: Job
metadata:
  name: spark-job-emr-eks
spec:
  template:
    spec:
      containers:
      - name: spark-submit
        image: amazon/aws-cli
        command: ["aws", "emr-containers", "start-job-run"]
        args:
        - "--virtual-cluster-id"
        - "$(VIRTUAL_CLUSTER_ID)"
        - "--name"
        - "spark-analytics-job"
        - "--execution-role-arn"
        - "$(EXECUTION_ROLE_ARN)"
        - "--release-label"
        - "emr-6.9.0-latest"
        - "--job-driver"
        - |
          {
            "sparkSubmitJobDriver": {
              "entryPoint": "s3://my-bucket/spark-job.py",
              "sparkSubmitParameters": "--conf spark.executor.instances=10"
            }
          }
```

### 3. EMR Serverless
```python
# EMR Serverless application
import boto3

emr_serverless = boto3.client('emr-serverless')

# Create application
app_response = emr_serverless.create_application(
    name='analytics-serverless-app',
    releaseLabel='emr-6.9.0',
    type='Spark',
    initialCapacity={
        'Driver': {
            'workerCount': 1,
            'workerConfiguration': {
                'cpu': '2 vCPU',
                'memory': '4 GB'
            }
        },
        'Executor': {
            'workerCount': 10,
            'workerConfiguration': {
                'cpu': '4 vCPU',
                'memory': '8 GB'
            }
        }
    },
    maximumCapacity={
        'cpu': '400 vCPU',
        'memory': '1000 GB'
    },
    autoStartConfiguration={
        'enabled': True
    },
    autoStopConfiguration={
        'enabled': True,
        'idleTimeoutMinutes': 15
    }
)

application_id = app_response['applicationId']

# Submit job
job_response = emr_serverless.start_job_run(
    applicationId=application_id,
    executionRoleArn='arn:aws:iam::account:role/EMRServerlessRole',
    jobDriver={
        'sparkSubmit': {
            'entryPoint': 's3://my-bucket/analytics-job.py',
            'entryPointArguments': ['--input', 's3://data/input/', '--output', 's3://data/output/'],
            'sparkSubmitParameters': '--conf spark.sql.adaptive.enabled=true'
        }
    },
    configurationOverrides={
        'monitoringConfiguration': {
            's3MonitoringConfiguration': {
                'logUri': 's3://my-logs/emr-serverless/'
            }
        }
    }
)
```

## Framework Integration

### 1. Apache Spark on EMR
```python
# Optimized Spark configuration for EMR
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf

# EMR-optimized Spark configuration
conf = SparkConf() \
    .setAppName("EMR-Optimized-Analytics") \
    .set("spark.sql.adaptive.enabled", "true") \
    .set("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .set("spark.sql.adaptive.skewJoin.enabled", "true") \
    .set("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .set("spark.hadoop.fs.s3a.fast.upload", "true") \
    .set("spark.hadoop.fs.s3a.block.size", "134217728") \
    .set("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2") \
    .set("spark.speculation", "true") \
    .set("spark.sql.execution.arrow.pyspark.enabled", "true")

spark = SparkSession.builder.config(conf=conf).getOrCreate()

# Read from S3 with optimizations
df = spark.read \
    .option("multiline", "true") \
    .option("inferSchema", "true") \
    .parquet("s3://data-lake/events/")

# Optimized transformations
result = df \
    .repartition(200) \
    .cache() \
    .groupBy("user_id", "event_date") \
    .agg(
        count("*").alias("event_count"),
        sum("revenue").alias("total_revenue")
    ) \
    .coalesce(50)

# Write with optimizations
result.write \
    .mode("overwrite") \
    .option("compression", "snappy") \
    .partitionBy("event_date") \
    .parquet("s3://data-lake/user-metrics/")
```

### 2. Apache Flink on EMR
```java
// Flink streaming job on EMR
public class EMRFlinkStreamingJob {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // EMR-specific configuration
        env.setParallelism(16);
        env.enableCheckpointing(60000, CheckpointingMode.EXACTLY_ONCE);
        env.getCheckpointConfig().setCheckpointStorage("s3://checkpoints/flink/");
        
        // Kinesis source
        Properties kinesisProps = new Properties();
        kinesisProps.setProperty(ConsumerConfigConstants.AWS_REGION, "us-west-2");
        kinesisProps.setProperty(ConsumerConfigConstants.STREAM_INITIAL_POSITION, "LATEST");
        
        DataStream<Event> events = env
            .addSource(new FlinkKinesisConsumer<>("analytics-stream", 
                                                 new EventDeserializer(), 
                                                 kinesisProps))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<Event>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                    .withTimestampAssigner((event, timestamp) -> event.getTimestamp())
            );
        
        // Stream processing
        DataStream<UserMetrics> metrics = events
            .keyBy(Event::getUserId)
            .window(TumblingEventTimeWindows.of(Time.minutes(5)))
            .aggregate(new UserMetricsAggregator());
        
        // S3 sink
        StreamingFileSink<UserMetrics> s3Sink = StreamingFileSink
            .forRowFormat(new Path("s3://analytics-output/user-metrics/"), 
                         new SimpleStringEncoder<UserMetrics>("UTF-8"))
            .withRollingPolicy(DefaultRollingPolicy.builder()
                .withRolloverInterval(TimeUnit.MINUTES.toMillis(15))
                .withInactivityInterval(TimeUnit.MINUTES.toMillis(5))
                .build())
            .build();
        
        metrics.addSink(s3Sink);
        
        env.execute("EMR Flink Streaming Analytics");
    }
}
```

### 3. Presto on EMR
```sql
-- Presto queries optimized for EMR
-- Create external table pointing to S3
CREATE TABLE events (
  event_id VARCHAR,
  user_id VARCHAR,
  event_type VARCHAR,
  timestamp BIGINT,
  properties MAP(VARCHAR, VARCHAR)
)
WITH (
  format = 'PARQUET',
  external_location = 's3://data-lake/events/',
  partitioned_by = ARRAY['date_partition']
);

-- Optimized analytical query
WITH user_sessions AS (
  SELECT 
    user_id,
    date_partition,
    COUNT(*) as event_count,
    MIN(timestamp) as session_start,
    MAX(timestamp) as session_end,
    MAX(timestamp) - MIN(timestamp) as session_duration
  FROM events
  WHERE date_partition >= '2023-01-01'
    AND event_type IN ('page_view', 'click', 'purchase')
  GROUP BY user_id, date_partition
),
user_metrics AS (
  SELECT 
    user_id,
    AVG(session_duration) as avg_session_duration,
    SUM(event_count) as total_events,
    COUNT(DISTINCT date_partition) as active_days
  FROM user_sessions
  GROUP BY user_id
)
SELECT 
  CASE 
    WHEN avg_session_duration > 300 THEN 'engaged'
    WHEN avg_session_duration > 60 THEN 'moderate'
    ELSE 'casual'
  END as user_segment,
  COUNT(*) as user_count,
  AVG(total_events) as avg_events_per_user,
  AVG(active_days) as avg_active_days
FROM user_metrics
GROUP BY 1
ORDER BY user_count DESC;
```

## Cost Optimization Strategies

### 1. Spot Instance Strategy
```python
# Advanced Spot instance configuration
spot_fleet_config = {
    'Name': 'cost-optimized-emr-cluster',
    'ReleaseLabel': 'emr-6.9.0',
    'Instances': {
        'InstanceFleets': [
            {
                'Name': 'MasterFleet',
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
                'Name': 'CoreFleet',
                'InstanceFleetType': 'CORE',
                'TargetOnDemandCapacity': 2,
                'TargetSpotCapacity': 8,
                'InstanceTypeConfigs': [
                    {
                        'InstanceType': 'm5.xlarge',
                        'WeightedCapacity': 1,
                        'BidPrice': '0.08',
                        'EbsConfiguration': {
                            'EbsBlockDeviceConfigs': [
                                {
                                    'VolumeSpecification': {
                                        'VolumeType': 'gp3',
                                        'SizeInGB': 100
                                    },
                                    'VolumesPerInstance': 1
                                }
                            ]
                        }
                    },
                    {
                        'InstanceType': 'm5.2xlarge',
                        'WeightedCapacity': 2,
                        'BidPrice': '0.16'
                    },
                    {
                        'InstanceType': 'c5.2xlarge',
                        'WeightedCapacity': 2,
                        'BidPrice': '0.15'
                    }
                ]
            }
        ]
    },
    'AutoTerminationPolicy': {
        'IdleTimeout': 3600  # 1 hour
    }
}
```

### 2. EMR Managed Scaling
```python
# Configure managed scaling
managed_scaling_config = {
    'ComputeLimits': {
        'UnitType': 'Instances',
        'MinimumCapacityUnits': 2,
        'MaximumCapacityUnits': 20,
        'MaximumOnDemandCapacityUnits': 5,
        'MaximumCoreCapacityUnits': 10
    }
}

# Apply to cluster
emr.put_managed_scaling_policy(
    ClusterId=cluster_id,
    ManagedScalingPolicy=managed_scaling_config
)
```

### 3. Cost Monitoring
```python
# EMR cost monitoring
class EMRCostMonitor:
    def __init__(self, cluster_id):
        self.cluster_id = cluster_id
        self.emr = boto3.client('emr')
        self.ce = boto3.client('ce')
    
    def get_cluster_cost(self, start_date, end_date):
        """Get cluster cost for date range"""
        response = self.ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ],
            Filter={
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': ['Amazon Elastic MapReduce']
                }
            }
        )
        
        return response['ResultsByTime']
    
    def optimize_cluster_config(self, workload_pattern):
        """Suggest optimizations based on workload"""
        recommendations = []
        
        if workload_pattern['avg_cpu_utilization'] < 50:
            recommendations.append("Consider using smaller instance types")
        
        if workload_pattern['peak_hours']:
            recommendations.append("Use scheduled scaling for predictable peaks")
        
        if workload_pattern['batch_jobs']:
            recommendations.append("Consider EMR Serverless for batch workloads")
        
        return recommendations
```

## Security Best Practices

### 1. Encryption Configuration
```python
# EMR security configuration
security_config = {
    'Name': 'emr-security-config',
    'EncryptionConfiguration': {
        'AtRestEncryptionConfiguration': {
            'S3EncryptionConfiguration': {
                'EncryptionMode': 'SSE-S3'
            },
            'LocalDiskEncryptionConfiguration': {
                'EncryptionKeyProviderType': 'AwsKms',
                'AwsKmsKey': 'arn:aws:kms:region:account:key/key-id'
            }
        },
        'InTransitEncryptionConfiguration': {
            'TLSCertificateConfiguration': {
                'CertificateProviderType': 'PEM',
                'S3Object': 's3://my-certs/certificate.pem'
            }
        }
    },
    'AuthenticationConfiguration': {
        'KerberosConfiguration': {
            'Provider': 'ClusterDedicatedKdc',
            'ClusterDedicatedKdcConfiguration': {
                'TicketLifetimeInHours': 24,
                'CrossRealmTrustConfiguration': {
                    'Realm': 'AD.DOMAIN.COM',
                    'Domain': 'ad.domain.com',
                    'AdminServer': 'ad.domain.com',
                    'KdcServer': 'ad.domain.com'
                }
            }
        }
    }
}

# Create security configuration
emr.create_security_configuration(**security_config)
```

### 2. IAM Roles và Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": [
        "arn:aws:s3:::data-lake/*",
        "arn:aws:s3:::analytics-output/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::data-lake",
        "arn:aws:s3:::analytics-output"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:GenerateDataKey"
      ],
      "Resource": "arn:aws:kms:region:account:key/key-id"
    }
  ]
}
```

## Monitoring và Troubleshooting

### 1. CloudWatch Integration
```python
# EMR CloudWatch monitoring
class EMRMonitor:
    def __init__(self, cluster_id):
        self.cluster_id = cluster_id
        self.cloudwatch = boto3.client('cloudwatch')
    
    def create_custom_metrics(self):
        """Create custom CloudWatch metrics"""
        # CPU utilization alarm
        self.cloudwatch.put_metric_alarm(
            AlarmName=f'EMR-{self.cluster_id}-HighCPU',
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=2,
            MetricName='CPUUtilization',
            Namespace='AWS/EMR',
            Period=300,
            Statistic='Average',
            Threshold=80.0,
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:region:account:emr-alerts'
            ],
            AlarmDescription='EMR cluster high CPU utilization',
            Dimensions=[
                {
                    'Name': 'JobFlowId',
                    'Value': self.cluster_id
                }
            ]
        )
        
        # Memory utilization alarm
        self.cloudwatch.put_metric_alarm(
            AlarmName=f'EMR-{self.cluster_id}-HighMemory',
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=2,
            MetricName='MemoryPercentage',
            Namespace='AWS/EMR',
            Period=300,
            Statistic='Average',
            Threshold=85.0,
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:region:account:emr-alerts'
            ]
        )
    
    def get_cluster_metrics(self, start_time, end_time):
        """Get cluster performance metrics"""
        metrics = {}
        
        # Get CPU utilization
        cpu_response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/EMR',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                    'Name': 'JobFlowId',
                    'Value': self.cluster_id
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Average', 'Maximum']
        )
        
        metrics['cpu'] = cpu_response['Datapoints']
        
        return metrics
```

## Best Practices

1. **Right-sizing**: Chọn instance types phù hợp với workload
2. **Cost Optimization**: Sử dụng Spot instances và auto-termination
3. **Security**: Enable encryption và proper IAM roles
4. **Monitoring**: Set up comprehensive monitoring
5. **Data Partitioning**: Optimize data layout trong S3
6. **Framework Selection**: Chọn framework phù hợp cho use case
7. **Performance Tuning**: Optimize framework configurations
8. **Backup Strategy**: Implement data backup và recovery

## Tích hợp với các dịch vụ AWS khác

- **Amazon S3**: Primary data storage
- **AWS Glue**: Data catalog và ETL
- **Amazon Athena**: Serverless queries
- **Amazon Kinesis**: Real-time data streaming
- **Amazon SageMaker**: Machine learning workflows
- **Amazon Redshift**: Data warehouse integration
- **AWS Lambda**: Event-driven processing
- **Amazon CloudWatch**: Monitoring và alerting
- **AWS IAM**: Identity và access management
- **Amazon VPC**: Network security
- **AWS KMS**: Encryption key management
- **Amazon EKS**: Container orchestration
