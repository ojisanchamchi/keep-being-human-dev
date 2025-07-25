# Amazon Athena

## Tổng quan

Amazon Athena là một dịch vụ truy vấn tương tác serverless giúp bạn dễ dàng phân tích dữ liệu trong Amazon S3 bằng SQL chuẩn. Athena không cần server, bạn chỉ trả tiền cho các truy vấn mà bạn chạy. Dịch vụ này được xây dựng trên Presto, một công cụ truy vấn phân tán mã nguồn mở.

## Chức năng chính

### 1. Serverless Query Engine
- **Không cần quản lý infrastructure**: Không cần thiết lập hay quản lý server
- **Auto Scaling**: Tự động mở rộng theo nhu cầu truy vấn
- **Pay-per-query**: Chỉ trả tiền cho dữ liệu được scan

### 2. SQL Support
- **ANSI SQL**: Hỗ trợ SQL chuẩn ANSI
- **Complex Queries**: Joins, window functions, arrays
- **User-defined Functions**: Tạo function tùy chỉnh

### 3. Data Format Support
- **Structured Data**: CSV, JSON, ORC, Parquet
- **Semi-structured Data**: Nested JSON, XML
- **Compressed Data**: GZIP, LZO, Snappy

### 4. Integration Capabilities
- **AWS Glue Data Catalog**: Metadata management
- **Amazon QuickSight**: Visualization
- **AWS Lambda**: Automated queries

## Use Cases phổ biến

1. **Ad-hoc Analysis**: Phân tích dữ liệu tức thời
2. **Log Analysis**: Phân tích log files từ S3
3. **Data Lake Queries**: Truy vấn data lake
4. **ETL Validation**: Kiểm tra chất lượng dữ liệu
5. **Business Reporting**: Báo cáo kinh doanh

## Diagram Architecture

Kiến trúc điển hình sử dụng Amazon Athena:

![Amazon Athena Data Analytics](/img/aws-analytics/athena-analytics.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Athena, Glue, Quicksight
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SQS
from diagrams.aws.database import RDS
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import Users

with Diagram("Amazon Athena Data Analytics", show=False, direction="TB"):
    
    users = Users("Data Analysts")
    
    with Cluster("Data Sources"):
        rds = RDS("Operational DB")
        logs = S3("Application Logs")
        raw_data = S3("Raw Data")
    
    with Cluster("Data Lake"):
        s3_bronze = S3("Bronze Layer\n(Raw)")
        s3_silver = S3("Silver Layer\n(Cleaned)")
        s3_gold = S3("Gold Layer\n(Aggregated)")
    
    with Cluster("Analytics Services"):
        glue_catalog = Glue("Glue Data Catalog")
        athena = Athena("Athena Query Engine")
        quicksight = Quicksight("QuickSight BI")
    
    with Cluster("Automation"):
        lambda_etl = Lambda("ETL Lambda")
        queue = SQS("Query Queue")
        monitoring = Cloudwatch("Query Monitoring")
    
    # Data ingestion flow
    rds >> Edge(label="Export") >> s3_bronze
    logs >> s3_bronze
    raw_data >> s3_bronze
    
    # ETL processing
    s3_bronze >> lambda_etl >> s3_silver
    s3_silver >> lambda_etl >> s3_gold
    
    # Catalog and query
    s3_gold >> glue_catalog
    glue_catalog >> athena
    
    # User interaction
    users >> Edge(label="SQL Queries") >> athena
    athena >> Edge(label="Results") >> quicksight
    quicksight >> Edge(label="Dashboards") >> users
    
    # Monitoring
    athena >> Edge(label="Query Metrics") >> monitoring
    queue >> Edge(label="Scheduled Queries") >> athena
```

## Performance Optimization

### 1. Data Format Optimization
- **Columnar Formats**: Sử dụng Parquet hoặc ORC
- **Compression**: Áp dụng compression algorithms
- **Partitioning**: Phân vùng dữ liệu theo thời gian hoặc category

### 2. Query Optimization
- **Projection Pushdown**: Chỉ select các cột cần thiết
- **Predicate Pushdown**: Sử dụng WHERE clause hiệu quả
- **Join Optimization**: Tối ưu thứ tự join

### 3. Cost Optimization
- **Data Compression**: Giảm lượng dữ liệu scan
- **Query Result Caching**: Cache kết quả truy vấn
- **Lifecycle Policies**: Tự động archive dữ liệu cũ

## Pricing Model

Amazon Athena tính phí theo:
- **Data Scanned**: $5.00 per TB dữ liệu được scan
- **DDL Queries**: Miễn phí cho CREATE, ALTER, DROP
- **Failed Queries**: Không tính phí cho queries bị lỗi

## Best Practices

1. **Use Columnar Formats**: Parquet giảm 30-90% chi phí
2. **Partition Your Data**: Giảm lượng dữ liệu scan
3. **Compress Your Data**: Giảm storage cost và query time
4. **Use Appropriate Data Types**: Tối ưu performance
5. **Optimize JOIN Operations**: Đặt bảng nhỏ bên trái

## Security Features

- **IAM Integration**: Kiểm soát truy cập bằng IAM
- **VPC Endpoints**: Truy cập private qua VPC
- **Encryption**: Mã hóa dữ liệu at-rest và in-transit
- **CloudTrail Logging**: Audit trail cho queries

## Limitations

- **Query Timeout**: Maximum 30 phút per query
- **Result Set Size**: Maximum 1GB per query result
- **Concurrent Queries**: Giới hạn số query đồng thời
- **DDL Operations**: Một số operations không được hỗ trợ

## Tích hợp với các dịch vụ AWS khác

- **AWS Glue**: Data catalog và ETL
- **Amazon S3**: Data storage
- **Amazon QuickSight**: Data visualization
- **AWS Lambda**: Query automation
- **Amazon CloudWatch**: Monitoring và alerting
