# AWS Analytics

Chào mừng bạn đến với tài liệu chi tiết về các AWS Analytics nodes trong thư viện `diagrams` Python. Đây là phần đầu tiên trong series tổng hợp tất cả các AWS nodes.

## Tổng quan

AWS Analytics cung cấp một bộ dịch vụ mạnh mẽ để xử lý, phân tích và trực quan hóa dữ liệu ở mọi quy mô. Các nodes trong `diagrams.aws.analytics` giúp bạn biểu diễn các dịch vụ này trong kiến trúc hệ thống.

## Danh sách Nodes đã hoàn thành

### Batch 1 (5 nodes đầu tiên)

1. **[Amazon OpenSearch Service](./amazon-opensearch-service.md)**
   - Dịch vụ tìm kiếm và phân tích được quản lý hoàn toàn
   - Hỗ trợ real-time analytics và full-text search
   - Tích hợp với nhiều dịch vụ AWS khác

2. **[Analytics](./analytics.md)**
   - Node tổng quát đại diện cho AWS Analytics ecosystem
   - Biểu thị tầng phân tích tổng thể trong kiến trúc
   - Bao gồm tất cả các dịch vụ analytics của AWS

3. **[Amazon Athena](./athena.md)**
   - Dịch vụ truy vấn serverless cho dữ liệu trong S3
   - Sử dụng SQL chuẩn, pay-per-query
   - Tích hợp với AWS Glue Data Catalog

4. **[CloudSearch Search Documents](./cloudsearch-search-documents.md)**
   - Chức năng tìm kiếm và truy xuất tài liệu
   - Xử lý search queries và trả về kết quả
   - Hỗ trợ full-text search và faceted search

5. **[Amazon CloudSearch](./cloudsearch.md)**
   - Dịch vụ tìm kiếm được quản lý hoàn toàn
   - Hỗ trợ 34 ngôn ngữ và nhiều tính năng advanced
   - Phù hợp cho website và ứng dụng search

### Batch 3 (7 EMR nodes)

9. **[EMR Cluster](./emr-cluster.md)**
   - Amazon EMR cluster với big data processing
   - Master, Core, và Task nodes architecture
   - Auto scaling và Spot instance integration

10. **[EMR Engine MapR M3](./emr-engine-mapr-m3.md)**
    - MapR Data Platform trên EC2 M3 instances
    - Unified data fabric với file, database, streaming
    - Enterprise-grade big data platform

11. **[EMR Engine MapR M5](./emr-engine-mapr-m5.md)**
    - MapR platform trên M5 instances thế hệ mới
    - Enhanced performance với Intel Xeon Platinum
    - Advanced analytics và ML capabilities

12. **[EMR Engine MapR M7](./emr-engine-mapr-m7.md)**
    - Next-generation MapR trên M7i instances
    - Intel Ice Lake processors với AVX-512
    - AI/ML acceleration và quantum computing integration

13. **[EMR Engine](./emr-engine.md)**
    - Tổng quát các processing engines trong EMR
    - Multi-framework support: Spark, Hadoop, Flink, Presto
    - Resource management với YARN và Kubernetes

14. **[EMR HDFS Cluster](./emr-hdfs-cluster.md)**
    - EMR cluster với HDFS làm primary storage
    - Distributed file system với fault tolerance
    - High-throughput data processing

15. **[Amazon EMR](./emr.md)**
    - Tổng quan Amazon EMR ecosystem
    - Multiple deployment options: EC2, EKS, Serverless
    - Comprehensive big data platform

### Batch 4 (3 Glue nodes)

16. **[AWS Glue Crawlers](./glue-crawlers.md)**
    - Automatic data discovery và schema inference
    - S3, JDBC, và DynamoDB crawlers
    - Scheduled crawling và event-driven triggers

17. **[AWS Glue Data Catalog](./glue-data-catalog.md)**
    - Centralized metadata repository
    - Schema evolution và version control
    - Data governance và classification

18. **[AWS Glue](./glue.md)**
    - Serverless ETL service tổng quan
    - Spark, Python Shell, và Streaming jobs
    - Workflow orchestration và monitoring

## Cách sử dụng

Mỗi tài liệu bao gồm:
- **Tổng quan**: Giới thiệu về dịch vụ
- **Chức năng chính**: Các tính năng và khả năng
- **Use Cases**: Các trường hợp sử dụng phổ biến
- **Diagram Architecture**: Kiến trúc mẫu với code Python
- **Best Practices**: Khuyến nghị và thực hành tốt
- **Tích hợp**: Cách tích hợp với các dịch vụ AWS khác

## Code Examples

Tất cả các diagram đều được viết bằng Python sử dụng thư viện `diagrams`:

```python
from diagrams import Diagram
from diagrams.aws.analytics import Athena, Analytics
from diagrams.aws.storage import S3

with Diagram("AWS Analytics Example", show=False):
    s3 = S3("Data Lake")
    athena = Athena("Query Engine")
    analytics = Analytics("Analytics Platform")
    
    s3 >> athena >> analytics
```

## Roadmap

Đã hoàn thành 18/30+ AWS Analytics nodes. Các batch tiếp theo sẽ bao gồm:

### Batch 5 (dự kiến)
- Amazon Kinesis (Data Streams, Data Firehose, Data Analytics, Video Streams)
- Amazon Redshift (các variants)

### Batch 6 (dự kiến)  
- Amazon QuickSight
- AWS Lake Formation
- Managed Streaming for Kafka

### Và nhiều nodes khác...

## Đóng góp

Nếu bạn phát hiện lỗi hoặc muốn cải thiện tài liệu, vui lòng tạo issue hoặc pull request.

## Tài liệu tham khảo

- [AWS Analytics Services](https://aws.amazon.com/big-data/datalakes-and-analytics/)
- [Diagrams Python Library](https://diagrams.mingrammer.com/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
