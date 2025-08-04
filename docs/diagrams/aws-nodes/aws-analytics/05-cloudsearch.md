# Amazon CloudSearch

## Tổng quan

Amazon CloudSearch là một dịch vụ tìm kiếm được quản lý hoàn toàn trong AWS Cloud, giúp bạn dễ dàng thiết lập, quản lý và mở rộng giải pháp tìm kiếm cho website hoặc ứng dụng. CloudSearch hỗ trợ 34 ngôn ngữ và cung cấp các tính năng tìm kiếm như highlighting, autocomplete, và faceted search.

## Chức năng chính

### 1. Search Domain Management
- **Domain Creation**: Tạo và cấu hình search domains
- **Field Configuration**: Định nghĩa các fields có thể tìm kiếm
- **Index Management**: Quản lý việc indexing documents
- **Multi-AZ Deployment**: Triển khai trên nhiều Availability Zones

### 2. Document Processing
- **Document Upload**: Upload documents để index
- **Batch Processing**: Xử lý hàng loạt documents
- **Real-time Updates**: Cập nhật documents real-time
- **Document Deletion**: Xóa documents khỏi index

### 3. Search Capabilities
- **Full-text Search**: Tìm kiếm toàn văn
- **Structured Search**: Tìm kiếm có cấu trúc
- **Faceted Search**: Tìm kiếm theo categories
- **Geospatial Search**: Tìm kiếm theo vị trí địa lý

### 4. Advanced Features
- **Auto-complete**: Gợi ý tự động
- **Highlighting**: Highlight từ khóa trong kết quả
- **Stemming**: Hỗ trợ từ gốc cho nhiều ngôn ngữ
- **Synonyms**: Hỗ trợ từ đồng nghĩa

## Use Cases phổ biến

1. **E-commerce Websites**: Tìm kiếm sản phẩm
2. **Content Management Systems**: Tìm kiếm nội dung
3. **Document Repositories**: Tìm kiếm tài liệu
4. **News Websites**: Tìm kiếm bài viết
5. **Job Portals**: Tìm kiếm việc làm

## Diagram Architecture

Kiến trúc hoàn chỉnh của Amazon CloudSearch:

![Amazon CloudSearch Complete Architecture](/img/aws-analytics/cloudsearch-architecture.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Cloudsearch, CloudsearchSearchDocuments
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import ELB, CloudFront, Route53
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users

with Diagram("Amazon CloudSearch Complete Architecture", show=False, direction="TB"):
    
    users = Users("Website Visitors")
    
    with Cluster("DNS & CDN Layer"):
        dns = Route53("Route 53")
        cdn = CloudFront("CloudFront")
    
    with Cluster("Application Layer"):
        load_balancer = ELB("Load Balancer")
        web_servers = [EC2("Web Server 1"), EC2("Web Server 2")]
    
    with Cluster("Search Infrastructure"):
        cloudsearch_domain = Cloudsearch("CloudSearch Domain")
        search_api = CloudsearchSearchDocuments("Search API")
    
    with Cluster("Data Sources"):
        primary_db = RDS("Primary Database")
        nosql_db = Dynamodb("Product Catalog")
        content_storage = S3("Content Storage")
    
    with Cluster("Data Processing"):
        index_queue = SQS("Indexing Queue")
        indexer_lambda = Lambda("Document Indexer")
        search_lambda = Lambda("Search Processor")
        notification = SNS("Search Notifications")
    
    with Cluster("Monitoring & Security"):
        monitoring = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # User search flow
    users >> dns >> cdn >> load_balancer
    load_balancer >> web_servers
    web_servers >> Edge(label="Search Query") >> search_lambda
    search_lambda >> search_api
    search_api >> cloudsearch_domain
    cloudsearch_domain >> Edge(label="Results") >> search_api
    search_api >> search_lambda >> web_servers
    
    # Data indexing flow
    primary_db >> Edge(label="Data Changes") >> index_queue
    nosql_db >> Edge(label="Product Updates") >> index_queue
    content_storage >> Edge(label="New Content") >> index_queue
    
    index_queue >> indexer_lambda
    indexer_lambda >> Edge(label="Index Documents") >> cloudsearch_domain
    indexer_lambda >> Edge(label="Status Updates") >> notification
    
    # Monitoring and security
    cloudsearch_domain >> Edge(label="Metrics") >> monitoring
    search_lambda >> Edge(label="Search Analytics") >> monitoring
    security >> Edge(label="Access Control") >> cloudsearch_domain
    security >> Edge(label="API Permissions") >> search_api
```

## Data Types và Field Configuration

### 1. Field Types
- **text**: Văn bản có thể tìm kiếm
- **literal**: Giá trị chính xác (không phân tích)
- **int**: Số nguyên
- **double**: Số thực
- **date**: Ngày tháng
- **latlon**: Tọa độ địa lý

### 2. Field Options
- **search**: Có thể tìm kiếm
- **facet**: Có thể dùng cho faceted search
- **return**: Trả về trong kết quả
- **sort**: Có thể sắp xếp theo field này

### 3. Example Configuration
```json
{
  "fields": {
    "title": {"type": "text", "search": true, "return": true},
    "price": {"type": "double", "facet": true, "sort": true},
    "category": {"type": "literal", "facet": true, "return": true},
    "description": {"type": "text", "search": true},
    "location": {"type": "latlon", "search": true}
  }
}
```

## Scaling và Performance

### 1. Instance Types
- **search.m4.small**: Nhỏ, phù hợp cho development
- **search.m4.large**: Trung bình, cho production nhỏ
- **search.m4.xlarge**: Lớn, cho high-traffic applications
- **search.m4.2xlarge**: Rất lớn, cho enterprise applications

### 2. Scaling Strategies
- **Vertical Scaling**: Tăng instance size
- **Horizontal Scaling**: Tăng số lượng instances
- **Partitioning**: Phân vùng dữ liệu
- **Replication**: Tạo replicas cho high availability

### 3. Performance Optimization
- **Batch Uploads**: Upload documents theo batch
- **Field Optimization**: Chỉ enable các options cần thiết
- **Query Optimization**: Tối ưu search queries
- **Caching**: Cache kết quả tìm kiếm phổ biến

## Pricing Model

Amazon CloudSearch tính phí theo:
- **Search Instance Hours**: Thời gian chạy search instances
- **Data Upload**: Lượng dữ liệu upload để index
- **Search Requests**: Số lượng search requests
- **Data Transfer**: Lượng dữ liệu transfer out

## Best Practices

1. **Field Design**: Thiết kế fields hiệu quả
2. **Batch Processing**: Sử dụng batch uploads
3. **Query Optimization**: Tối ưu search queries
4. **Monitoring**: Theo dõi performance metrics
5. **Security**: Implement proper access controls

## Security Features

- **IAM Integration**: Kiểm soát truy cập bằng IAM policies
- **VPC Support**: Deploy trong Virtual Private Cloud
- **HTTPS Support**: Mã hóa data in transit
- **Access Policies**: Fine-grained access control
- **IP Restrictions**: Giới hạn truy cập theo IP

## Monitoring và Troubleshooting

### Key Metrics
- **Search Latency**: Thời gian response của searches
- **Search Rate**: Số lượng searches per second
- **Index Utilization**: Mức độ sử dụng index
- **Instance Health**: Tình trạng search instances

### Common Issues
- **Slow Searches**: Tối ưu queries và fields
- **Index Errors**: Kiểm tra document format
- **Capacity Issues**: Scale up instances
- **Timeout Errors**: Tăng timeout settings

## Migration và Alternatives

### Migration from Other Search Solutions
- **From Elasticsearch**: Export data và re-index
- **From Solr**: Convert schema và migrate data
- **From Database Search**: Extract data và optimize for search

### Modern Alternatives
- **Amazon OpenSearch**: Successor với nhiều features hơn
- **Amazon Kendra**: AI-powered enterprise search
- **Elasticsearch Service**: Managed Elasticsearch

## Tích hợp với các dịch vụ AWS khác

- **Amazon S3**: Lưu trữ documents và backups
- **AWS Lambda**: Automated indexing và processing
- **Amazon CloudWatch**: Monitoring và alerting
- **Amazon API Gateway**: REST API wrapper
- **AWS IAM**: Access control và security
