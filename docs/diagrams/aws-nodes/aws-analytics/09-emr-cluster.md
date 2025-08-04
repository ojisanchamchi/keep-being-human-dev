# EMR Cluster

## Tổng quan

EMR Cluster là node đại diện cho Amazon EMR (Elastic MapReduce) Cluster - một dịch vụ big data platform được quản lý giúp xử lý và phân tích lượng lớn dữ liệu bằng các framework mã nguồn mở như Apache Spark, Apache Hadoop, Apache HBase, Apache Flink, Apache Hudi, và Presto. EMR Cluster cung cấp khả năng mở rộng linh hoạt và tối ưu chi phí cho các workload big data.

## Chức năng chính

### 1. Cluster Management
- **Auto Scaling**: Tự động điều chỉnh số lượng nodes
- **Spot Instance Support**: Sử dụng EC2 Spot Instances để tiết kiệm chi phí
- **Multi-AZ Deployment**: Triển khai trên nhiều Availability Zones
- **Cluster Templates**: Sử dụng templates để tạo cluster nhanh chóng

### 2. Big Data Processing
- **Batch Processing**: Xử lý dữ liệu theo lô với Hadoop MapReduce
- **Stream Processing**: Xử lý dữ liệu real-time với Spark Streaming
- **Interactive Analytics**: Phân tích tương tác với Spark SQL
- **Machine Learning**: ML workflows với Spark MLlib

### 3. Storage Integration
- **HDFS**: Hadoop Distributed File System
- **S3 Integration**: Đọc/ghi trực tiếp từ Amazon S3
- **EBS Volumes**: Elastic Block Store cho local storage
- **EMRFS**: EMR File System cho S3 optimization

### 4. Framework Support
- **Apache Spark**: In-memory processing engine
- **Apache Hadoop**: Distributed computing framework
- **Apache HBase**: NoSQL database
- **Apache Hive**: Data warehouse software
- **Apache Pig**: High-level data flow language
- **Presto**: Distributed SQL query engine

## Use Cases phổ biến

1. **ETL Processing**: Extract, Transform, Load operations
2. **Data Lake Analytics**: Phân tích dữ liệu trong data lake
3. **Machine Learning**: Training và inference ML models
4. **Log Processing**: Xử lý và phân tích log files
5. **Financial Analytics**: Phân tích dữ liệu tài chính quy mô lớn

## Diagram Architecture

Kiến trúc EMR Cluster với big data processing:

![EMR Cluster Architecture](/img/aws-analytics/emr-cluster.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import EMRCluster, Glue, Athena
from diagrams.aws.storage import S3
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import SQS
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users

with Diagram("EMR Cluster Architecture", show=False, direction="TB"):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Sources"):
        rds = RDS("Operational DB")
        dynamodb = Dynamodb("NoSQL DB")
        s3_raw = S3("Raw Data Lake")
        streaming_data = SQS("Streaming Data")
    
    with Cluster("EMR Processing"):
        emr_cluster = EMRCluster("EMR Cluster")
        master_node = EC2("Master Node")
        core_nodes = [EC2("Core Node 1"), EC2("Core Node 2")]
        task_nodes = [EC2("Task Node 1"), EC2("Task Node 2")]
    
    with Cluster("Storage & Output"):
        s3_processed = S3("Processed Data")
        s3_results = S3("Analytics Results")
        glue_catalog = Glue("Data Catalog")
    
    with Cluster("Analytics & ML"):
        athena = Athena("Query Engine")
        ml_model = SagemakerModel("ML Pipeline")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # Data ingestion
    rds >> Edge(label="Extract") >> s3_raw
    dynamodb >> Edge(label="Export") >> s3_raw
    streaming_data >> Edge(label="Stream") >> emr_cluster
    
    # EMR cluster structure
    emr_cluster >> master_node
    master_node >> core_nodes
    master_node >> task_nodes
    
    # Data processing flow
    s3_raw >> Edge(label="Input Data") >> emr_cluster
    emr_cluster >> Edge(label="Processed") >> s3_processed
    emr_cluster >> Edge(label="Results") >> s3_results
    
    # Analytics integration
    s3_processed >> glue_catalog >> athena
    s3_results >> ml_model
    
    # User interaction
    users >> Edge(label="Submit Jobs") >> emr_cluster
    users >> Edge(label="Query Results") >> athena
    
    # Monitoring and security
    emr_cluster >> Edge(label="Metrics") >> monitoring
    security >> Edge(label="Access Control") >> emr_cluster
```

## Cluster Architecture

### 1. Node Types

#### Master Node
- **Cluster Coordination**: Quản lý cluster và phân phối tasks
- **Resource Management**: YARN ResourceManager
- **Job Tracking**: Theo dõi job execution
- **Web Interfaces**: Spark UI, Hadoop UI

#### Core Nodes
- **Data Storage**: HDFS DataNodes
- **Task Execution**: Chạy tasks và lưu trữ dữ liệu
- **Persistent Storage**: EBS volumes cho HDFS
- **Always Running**: Không thể terminate trong quá trình chạy

#### Task Nodes (Optional)
- **Additional Compute**: Thêm compute capacity
- **No Data Storage**: Không lưu trữ HDFS data
- **Spot Instances**: Thích hợp cho Spot Instances
- **Scalable**: Có thể add/remove linh hoạt

### 2. Storage Options

#### HDFS (Hadoop Distributed File System)
- **Local Storage**: Lưu trữ trên EBS volumes
- **High Performance**: Truy cập nhanh cho processing
- **Replication**: Data replication across nodes
- **Temporary**: Mất dữ liệu khi terminate cluster

#### EMRFS (EMR File System)
- **S3 Integration**: Truy cập S3 như local filesystem
- **Persistent**: Dữ liệu tồn tại sau khi terminate cluster
- **Cost Effective**: Sử dụng S3 storage classes
- **Consistent View**: Consistency cho S3 operations

## Framework Configuration

### 1. Apache Spark
```json
{
  "Classification": "spark-defaults",
  "Properties": {
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
    "spark.dynamicAllocation.enabled": "true"
  }
}
```

### 2. Apache Hadoop
```json
{
  "Classification": "hadoop-env",
  "Properties": {},
  "Configurations": [
    {
      "Classification": "export",
      "Properties": {
        "JAVA_HOME": "/usr/lib/jvm/java-1.8.0"
      }
    }
  ]
}
```

### 3. Apache Hive
```json
{
  "Classification": "hive-site",
  "Properties": {
    "javax.jdo.option.ConnectionURL": "jdbc:mysql://hostname:port/hive?createDatabaseIfNotExist=true",
    "javax.jdo.option.ConnectionUserName": "username",
    "javax.jdo.option.ConnectionPassword": "password"
  }
}
```

## Performance Optimization

### 1. Instance Selection
- **Compute Optimized**: C5 instances cho CPU-intensive workloads
- **Memory Optimized**: R5 instances cho in-memory processing
- **Storage Optimized**: I3 instances cho high I/O workloads
- **General Purpose**: M5 instances cho balanced workloads

### 2. Scaling Strategies
- **Cluster Scaling**: Thêm/bớt core và task nodes
- **Automatic Scaling**: EMR Managed Scaling
- **Spot Fleet**: Sử dụng multiple Spot Instance types
- **Custom Scaling**: CloudWatch-based scaling policies

### 3. Data Optimization
- **File Formats**: Sử dụng Parquet, ORC cho columnar data
- **Compression**: GZIP, Snappy, LZO compression
- **Partitioning**: Partition data theo date, region
- **Bucketing**: Bucket data để tối ưu joins

## Cost Optimization

### 1. Instance Pricing
- **On-Demand**: Predictable pricing
- **Reserved Instances**: Discount cho long-term usage
- **Spot Instances**: Lên đến 90% discount
- **Mixed Fleet**: Kết hợp On-Demand và Spot

### 2. Cluster Management
- **Auto Termination**: Tự động terminate khi idle
- **Step Execution**: Chạy jobs theo steps
- **Transient Clusters**: Tạo cluster cho từng job
- **Persistent Clusters**: Giữ cluster cho multiple jobs

### 3. Storage Optimization
- **S3 Storage Classes**: IA, Glacier cho archival
- **Data Lifecycle**: Tự động move data theo lifecycle
- **Compression**: Giảm storage và transfer costs
- **Deduplication**: Loại bỏ duplicate data

## Security Features

### 1. Network Security
- **VPC Deployment**: Private subnets
- **Security Groups**: Network-level access control
- **NACLs**: Additional network layer security
- **VPC Endpoints**: Private connectivity to AWS services

### 2. Data Encryption
- **Encryption at Rest**: EBS, S3 encryption
- **Encryption in Transit**: TLS/SSL
- **Key Management**: AWS KMS integration
- **Client-side Encryption**: Application-level encryption

### 3. Access Control
- **IAM Roles**: Service và user roles
- **Kerberos**: Authentication protocol
- **LDAP Integration**: Enterprise directory integration
- **Apache Ranger**: Fine-grained access control

## Monitoring và Troubleshooting

### Key Metrics
- **Cluster Utilization**: CPU, memory, disk usage
- **Job Performance**: Execution time, throughput
- **Resource Allocation**: YARN resource usage
- **Error Rates**: Failed jobs, task failures

### Logging
- **Application Logs**: Spark, Hadoop application logs
- **System Logs**: EMR system logs
- **CloudWatch Logs**: Centralized log management
- **S3 Log Archive**: Long-term log storage

### Common Issues
- **Out of Memory**: Tune Spark memory settings
- **Slow Performance**: Optimize data formats, partitioning
- **Cluster Failures**: Check instance health, network
- **Permission Errors**: Verify IAM roles, S3 permissions

## Best Practices

1. **Right-sizing**: Chọn instance types phù hợp
2. **Data Locality**: Minimize data movement
3. **Resource Tuning**: Optimize Spark/Hadoop configurations
4. **Monitoring**: Comprehensive monitoring setup
5. **Security**: Implement defense-in-depth
6. **Cost Management**: Regular cost review và optimization

## Tích hợp với các dịch vụ AWS khác

- **Amazon S3**: Primary data storage
- **AWS Glue**: Data catalog và ETL
- **Amazon Athena**: Serverless queries
- **Amazon Redshift**: Data warehouse integration
- **Amazon Kinesis**: Real-time data streaming
- **AWS Lambda**: Event-driven processing
- **Amazon SageMaker**: Machine learning workflows
- **Amazon CloudWatch**: Monitoring và alerting
