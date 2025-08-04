# AWS Data Pipeline

## Tổng quan

AWS Data Pipeline là một dịch vụ web giúp bạn xử lý và di chuyển dữ liệu giữa các dịch vụ compute và storage khác nhau của AWS, cũng như các nguồn dữ liệu on-premises, theo các khoảng thời gian được chỉ định. Data Pipeline cho phép bạn tạo các workflows phức tạp để xử lý dữ liệu một cách đáng tin cậy và có thể mở rộng.

## Chức năng chính

### 1. Workflow Orchestration
- **Pipeline Definition**: Định nghĩa workflows bằng JSON
- **Dependency Management**: Quản lý phụ thuộc giữa các tasks
- **Scheduling**: Lập lịch chạy tự động
- **Retry Logic**: Tự động retry khi có lỗi

### 2. Data Movement
- **Cross-service Transfer**: Di chuyển dữ liệu giữa các dịch vụ AWS
- **On-premises Integration**: Tích hợp với dữ liệu on-premises
- **Batch Processing**: Xử lý dữ liệu theo lô
- **Incremental Loading**: Tải dữ liệu tăng dần

### 3. Data Processing
- **ETL Operations**: Extract, Transform, Load
- **Data Validation**: Kiểm tra chất lượng dữ liệu
- **Format Conversion**: Chuyển đổi định dạng dữ liệu
- **Data Aggregation**: Tổng hợp dữ liệu

### 4. Monitoring & Management
- **Pipeline Monitoring**: Theo dõi trạng thái pipeline
- **Error Handling**: Xử lý lỗi và thông báo
- **Resource Management**: Quản lý compute resources
- **Cost Optimization**: Tối ưu chi phí xử lý

## Use Cases phổ biến

1. **Data Warehouse Loading**: Tải dữ liệu vào data warehouse
2. **Log Processing**: Xử lý và phân tích log files
3. **Database Backup**: Sao lưu database định kỳ
4. **Data Migration**: Di chuyển dữ liệu giữa các hệ thống
5. **Report Generation**: Tạo báo cáo tự động

## Diagram Architecture

Kiến trúc AWS Data Pipeline workflow:

![AWS Data Pipeline Architecture](/img/aws-analytics/data-pipeline.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import DataPipeline, EMR
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS, Redshift
from diagrams.aws.compute import EC2
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.database import MySQL
from diagrams.onprem.client import Users

with Diagram("AWS Data Pipeline Architecture", show=False, direction="TB"):
    
    users = Users("Data Engineers")
    
    with Cluster("Data Sources"):
        on_prem_db = MySQL("On-premises DB")
        rds_source = RDS("RDS Source")
        s3_raw = S3("Raw Data")
    
    with Cluster("Pipeline Orchestration"):
        data_pipeline = DataPipeline("Data Pipeline\nService")
        pipeline_queue = SQS("Pipeline Queue")
        notifications = SNS("Notifications")
    
    with Cluster("Processing Resources"):
        ec2_instances = [EC2("EC2 Worker 1"), EC2("EC2 Worker 2")]
        emr_cluster = EMR("EMR Cluster")
    
    with Cluster("Data Destinations"):
        s3_processed = S3("Processed Data")
        redshift = Redshift("Data Warehouse")
        rds_target = RDS("RDS Target")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # Pipeline definition and scheduling
    users >> Edge(label="Define Pipeline") >> data_pipeline
    data_pipeline >> Edge(label="Schedule Tasks") >> pipeline_queue
    
    # Data extraction
    on_prem_db >> Edge(label="Extract") >> ec2_instances
    rds_source >> Edge(label="Extract") >> ec2_instances
    s3_raw >> Edge(label="Read") >> emr_cluster
    
    # Pipeline execution
    pipeline_queue >> ec2_instances
    pipeline_queue >> emr_cluster
    
    # Data processing and loading
    ec2_instances >> Edge(label="Transform") >> s3_processed
    emr_cluster >> Edge(label="Process") >> s3_processed
    s3_processed >> Edge(label="Load") >> redshift
    s3_processed >> Edge(label="Load") >> rds_target
    
    # Monitoring and notifications
    data_pipeline >> Edge(label="Status") >> monitoring
    data_pipeline >> Edge(label="Alerts") >> notifications
    notifications >> Edge(label="Notifications") >> users
    
    # Security
    security >> Edge(label="Access Control") >> data_pipeline
    security >> Edge(label="Resource Permissions") >> ec2_instances
```

## Pipeline Components

### 1. Data Nodes
- **DynamoDBDataNode**: DynamoDB tables
- **SqlDataNode**: SQL databases (RDS, Redshift)
- **S3DataNode**: S3 objects và prefixes
- **RedshiftDataNode**: Redshift tables

### 2. Activities
- **CopyActivity**: Sao chép dữ liệu giữa data nodes
- **EmrActivity**: Chạy EMR jobs
- **HiveActivity**: Thực thi Hive queries
- **ShellCommandActivity**: Chạy shell commands

### 3. Resources
- **Ec2Resource**: EC2 instances cho processing
- **EmrCluster**: EMR clusters cho big data
- **Schedule**: Định nghĩa lịch chạy
- **Precondition**: Điều kiện tiên quyết

### 4. Actions
- **SnsAlarm**: Gửi thông báo qua SNS
- **Terminate**: Kết thúc pipeline khi có lỗi

## Pipeline Definition Example

```json
{
  "objects": [
    {
      "id": "Default",
      "name": "Default",
      "scheduleType": "cron",
      "schedule": {
        "ref": "DefaultSchedule"
      },
      "failureAndRerunMode": "CASCADE",
      "role": "DataPipelineDefaultRole",
      "resourceRole": "DataPipelineDefaultResourceRole"
    },
    {
      "id": "DefaultSchedule",
      "name": "RunOnce",
      "type": "Schedule",
      "period": "1 Day",
      "startDateTime": "2023-01-01T00:00:00",
      "endDateTime": "2023-12-31T00:00:00"
    },
    {
      "id": "CopyData",
      "name": "CopyData",
      "type": "CopyActivity",
      "input": {
        "ref": "InputData"
      },
      "output": {
        "ref": "OutputData"
      },
      "runsOn": {
        "ref": "Ec2Instance"
      }
    }
  ]
}
```

## Best Practices

### 1. Pipeline Design
- **Modular Design**: Chia pipeline thành các modules nhỏ
- **Error Handling**: Implement comprehensive error handling
- **Idempotency**: Đảm bảo pipeline có thể chạy lại an toàn
- **Testing**: Test pipeline trước khi deploy production

### 2. Performance Optimization
- **Parallel Processing**: Chạy các tasks song song khi có thể
- **Resource Sizing**: Chọn instance types phù hợp
- **Data Partitioning**: Phân vùng dữ liệu để xử lý hiệu quả
- **Compression**: Sử dụng compression để giảm I/O

### 3. Security
- **IAM Roles**: Sử dụng IAM roles thay vì access keys
- **Encryption**: Mã hóa dữ liệu in-transit và at-rest
- **VPC**: Deploy trong VPC để bảo mật network
- **Audit Logging**: Enable CloudTrail logging

### 4. Cost Management
- **Spot Instances**: Sử dụng spot instances cho non-critical workloads
- **Auto Scaling**: Tự động scale resources theo nhu cầu
- **Scheduling**: Chạy pipeline vào thời điểm chi phí thấp
- **Resource Cleanup**: Tự động cleanup resources sau khi hoàn thành

## Monitoring và Troubleshooting

### Key Metrics
- **Pipeline Success Rate**: Tỷ lệ thành công của pipeline
- **Execution Duration**: Thời gian thực thi
- **Resource Utilization**: Mức độ sử dụng resources
- **Error Frequency**: Tần suất lỗi

### Common Issues
- **Resource Provisioning**: Lỗi khởi tạo EC2/EMR
- **Data Access**: Lỗi quyền truy cập dữ liệu
- **Network Connectivity**: Lỗi kết nối mạng
- **Data Format**: Lỗi định dạng dữ liệu

### Troubleshooting Steps
1. **Check CloudWatch Logs**: Xem logs chi tiết
2. **Verify IAM Permissions**: Kiểm tra quyền truy cập
3. **Test Data Sources**: Verify data availability
4. **Resource Health**: Kiểm tra trạng thái resources

## Migration và Alternatives

### Migration Strategies
- **Phased Migration**: Di chuyển từng phần một
- **Parallel Running**: Chạy song song với hệ thống cũ
- **Data Validation**: Validate dữ liệu sau migration

### Modern Alternatives
- **AWS Step Functions**: Serverless workflow orchestration
- **AWS Glue**: Managed ETL service
- **Amazon MWAA**: Managed Apache Airflow
- **AWS Batch**: Batch computing service

## Pricing Model

AWS Data Pipeline tính phí theo:
- **Pipeline Frequency**: Số lần chạy pipeline
- **Data Processing**: Lượng dữ liệu được xử lý
- **Resource Usage**: EC2/EMR instances sử dụng
- **Data Transfer**: Lượng dữ liệu transfer

## Tích hợp với các dịch vụ AWS khác

- **Amazon S3**: Primary data storage
- **Amazon RDS**: Relational database source/target
- **Amazon Redshift**: Data warehouse destination
- **Amazon EMR**: Big data processing
- **Amazon DynamoDB**: NoSQL database operations
- **AWS Lambda**: Serverless processing triggers
- **Amazon SNS**: Notifications và alerts
- **Amazon CloudWatch**: Monitoring và logging
