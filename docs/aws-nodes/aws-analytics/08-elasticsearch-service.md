# Amazon Elasticsearch Service

## Tổng quan

Amazon Elasticsearch Service (Amazon ES) là phiên bản cũ của Amazon OpenSearch Service. Đây là một dịch vụ được quản lý hoàn toàn giúp bạn triển khai, vận hành và mở rộng các cluster Elasticsearch trong AWS Cloud. Elasticsearch là một công cụ tìm kiếm và phân tích phân tán, mã nguồn mở được xây dựng trên Apache Lucene.

> **Lưu ý quan trọng**: Amazon Elasticsearch Service đã được đổi tên thành Amazon OpenSearch Service vào tháng 9/2021. Tuy nhiên, node này vẫn tồn tại trong thư viện diagrams để tương thích ngược.

## Chức năng chính

### 1. Search và Analytics Engine
- **Full-text Search**: Tìm kiếm toàn văn với scoring algorithms
- **Real-time Analytics**: Phân tích dữ liệu thời gian thực
- **Aggregations**: Tính toán thống kê và metrics
- **Geospatial Search**: Tìm kiếm theo vị trí địa lý

### 2. Cluster Management
- **Managed Service**: AWS quản lý infrastructure
- **Auto Scaling**: Tự động mở rộng cluster
- **Multi-AZ Deployment**: Triển khai trên nhiều AZ
- **Automated Backups**: Sao lưu tự động

### 3. Data Ingestion
- **Bulk API**: Tải dữ liệu hàng loạt
- **Streaming Ingestion**: Nhận dữ liệu real-time
- **Logstash Integration**: Tích hợp với Logstash
- **Beats Support**: Hỗ trợ Elastic Beats

### 4. Visualization
- **Kibana**: Dashboard và visualization
- **Custom Dashboards**: Tạo dashboard tùy chỉnh
- **Alerting**: Cảnh báo dựa trên dữ liệu
- **Reporting**: Tạo báo cáo tự động

## Use Cases phổ biến

1. **Log Analytics**: Phân tích log từ applications và systems
2. **Application Monitoring**: Giám sát hiệu suất ứng dụng
3. **Security Analytics**: Phân tích bảo mật và threat detection
4. **Business Intelligence**: Phân tích dữ liệu kinh doanh
5. **Content Search**: Tìm kiếm nội dung trong websites

## Diagram Architecture

Kiến trúc Elasticsearch Service với ELK Stack:

![Amazon Elasticsearch Service Architecture](/img/aws-analytics/elasticsearch-service.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import ElasticsearchService, Kinesis
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS
from diagrams.aws.network import ELB, CloudFront
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.logging import Fluentbit
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.client import Users

with Diagram("Amazon Elasticsearch Service Architecture", show=False, direction="TB"):
    
    users = Users("Analysts & Developers")
    
    with Cluster("Data Sources"):
        app_servers = [EC2("App Server 1"), EC2("App Server 2")]
        database = RDS("Application DB")
        s3_logs = S3("Log Storage")
        kinesis_stream = Kinesis("Log Stream")
    
    with Cluster("Data Processing"):
        log_processor = Fluentbit("Log Processor")
        lambda_processor = Lambda("Log Processor")
        queue = SQS("Processing Queue")
    
    with Cluster("Elasticsearch Cluster"):
        elasticsearch = ElasticsearchService("Elasticsearch\nService")
        dashboard = Grafana("Analytics\nDashboard")
    
    with Cluster("Load Balancing & CDN"):
        load_balancer = ELB("Load Balancer")
        cdn = CloudFront("CloudFront")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # Data ingestion flow
    app_servers >> Edge(label="Application Logs") >> kinesis_stream
    database >> Edge(label="Query Logs") >> s3_logs
    s3_logs >> lambda_processor >> queue
    
    # Log processing
    kinesis_stream >> log_processor
    queue >> log_processor
    log_processor >> Edge(label="Structured Logs") >> elasticsearch
    
    # User access
    users >> cdn >> load_balancer >> dashboard
    dashboard >> Edge(label="Queries") >> elasticsearch
    elasticsearch >> Edge(label="Results") >> dashboard
    
    # Monitoring and security
    elasticsearch >> Edge(label="Cluster Metrics") >> monitoring
    security >> Edge(label="Access Control") >> elasticsearch
    security >> Edge(label="Dashboard Access") >> dashboard
    
    # Direct search access
    users >> Edge(label="Search API") >> elasticsearch
```

## ELK Stack Components

### 1. Elasticsearch
- **Search Engine**: Core search và analytics engine
- **Document Store**: Lưu trữ documents dạng JSON
- **RESTful API**: API để tương tác với cluster
- **Distributed**: Phân tán trên nhiều nodes

### 2. Logstash
- **Data Pipeline**: Xử lý và transform dữ liệu
- **Input Plugins**: Nhận dữ liệu từ nhiều nguồn
- **Filter Plugins**: Transform và enrich dữ liệu
- **Output Plugins**: Gửi dữ liệu đến destinations

### 3. Kibana
- **Visualization**: Tạo charts và graphs
- **Dashboard**: Tổng hợp nhiều visualizations
- **Discover**: Khám phá dữ liệu interactively
- **Management**: Quản lý Elasticsearch cluster

### 4. Beats
- **Filebeat**: Thu thập log files
- **Metricbeat**: Thu thập system metrics
- **Packetbeat**: Phân tích network traffic
- **Heartbeat**: Monitoring uptime

## Index Management

### 1. Index Structure
```json
{
  "mappings": {
    "properties": {
      "timestamp": {"type": "date"},
      "level": {"type": "keyword"},
      "message": {"type": "text"},
      "source": {"type": "keyword"},
      "tags": {"type": "keyword"}
    }
  }
}
```

### 2. Index Templates
- **Pattern Matching**: Tự động áp dụng cho indices mới
- **Settings**: Cấu hình shards, replicas
- **Mappings**: Định nghĩa field types
- **Aliases**: Tạo aliases cho indices

### 3. Index Lifecycle Management
- **Hot Phase**: Dữ liệu mới, truy cập thường xuyên
- **Warm Phase**: Dữ liệu ít truy cập hơn
- **Cold Phase**: Dữ liệu archive, ít truy cập
- **Delete Phase**: Tự động xóa dữ liệu cũ

## Query DSL Examples

### 1. Basic Search
```json
{
  "query": {
    "match": {
      "message": "error"
    }
  }
}
```

### 2. Range Query
```json
{
  "query": {
    "range": {
      "timestamp": {
        "gte": "2023-01-01",
        "lte": "2023-12-31"
      }
    }
  }
}
```

### 3. Aggregations
```json
{
  "aggs": {
    "error_count": {
      "terms": {
        "field": "level"
      }
    }
  }
}
```

## Performance Tuning

### 1. Cluster Configuration
- **Node Types**: Master, data, ingest nodes
- **Shard Strategy**: Optimal shard size và count
- **Replica Settings**: Balance availability và performance
- **Memory Settings**: JVM heap sizing

### 2. Indexing Optimization
- **Bulk Indexing**: Sử dụng bulk API
- **Refresh Interval**: Tối ưu refresh frequency
- **Mapping Optimization**: Efficient field mappings
- **Document Routing**: Custom routing strategies

### 3. Search Optimization
- **Query Optimization**: Efficient query structures
- **Caching**: Leverage query và filter caches
- **Field Selection**: Chỉ retrieve cần thiết fields
- **Pagination**: Sử dụng scroll API cho large results

## Security Features

### 1. Authentication & Authorization
- **IAM Integration**: AWS IAM-based access control
- **Fine-grained Access**: Resource-level permissions
- **SAML Integration**: Enterprise SSO support
- **API Key Authentication**: Programmatic access

### 2. Network Security
- **VPC Deployment**: Private network isolation
- **Security Groups**: Network-level access control
- **Encryption in Transit**: HTTPS/TLS encryption
- **Encryption at Rest**: Data encryption

### 3. Audit & Compliance
- **Audit Logging**: Comprehensive audit trails
- **CloudTrail Integration**: API call logging
- **Compliance**: SOC, PCI DSS, HIPAA support
- **Data Residency**: Regional data storage

## Migration to OpenSearch

### 1. Migration Path
- **In-place Upgrade**: Upgrade existing clusters
- **Blue-Green Migration**: Zero-downtime migration
- **Data Reindexing**: Reindex data to new cluster
- **Application Updates**: Update client applications

### 2. Compatibility
- **API Compatibility**: Most APIs remain compatible
- **Plugin Support**: Check plugin compatibility
- **Client Libraries**: Update to OpenSearch clients
- **Kibana Alternative**: OpenSearch Dashboards

## Best Practices

1. **Cluster Design**: Proper node sizing và distribution
2. **Index Strategy**: Efficient index patterns
3. **Monitoring**: Comprehensive cluster monitoring
4. **Security**: Implement proper access controls
5. **Backup**: Regular snapshot backups

## Pricing Considerations

- **Instance Hours**: EC2 instance costs
- **Storage**: EBS volume costs
- **Data Transfer**: Network transfer costs
- **Dedicated Master**: Additional master node costs

## Tích hợp với các dịch vụ AWS khác

- **Amazon Kinesis**: Real-time data streaming
- **AWS Lambda**: Serverless data processing
- **Amazon S3**: Data storage và backup
- **Amazon CloudWatch**: Monitoring và alerting
- **AWS IAM**: Access management
- **Amazon VPC**: Network isolation
- **AWS CloudFormation**: Infrastructure as Code
