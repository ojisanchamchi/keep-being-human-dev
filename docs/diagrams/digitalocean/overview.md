---
sidebar_position: 1
---

# DigitalOcean Diagrams

DigitalOcean là một nhà cung cấp dịch vụ đám mây phổ biến, đặc biệt được ưa chuộng bởi các nhà phát triển và doanh nghiệp nhỏ nhờ vào sự đơn giản và chi phí hợp lý. Thư viện Diagrams cung cấp nhiều nodes để biểu diễn các dịch vụ và tài nguyên của DigitalOcean trong các sơ đồ kiến trúc.

## Cách sử dụng

Để sử dụng các nodes DigitalOcean trong diagrams, bạn cần import chúng từ module tương ứng:

```python
from diagrams import Diagram
from diagrams.digitalocean.compute import Droplet
from diagrams.digitalocean.database import DbaasPrimary
from diagrams.digitalocean.network import LoadBalancer
from diagrams.digitalocean.storage import Space
```

## Phân loại Nodes

Các nodes DigitalOcean được phân loại thành các nhóm sau:

1. **Compute (Tính toán)**: Các dịch vụ liên quan đến máy chủ ảo, container và Kubernetes.
2. **Database (Cơ sở dữ liệu)**: Các dịch vụ cơ sở dữ liệu được quản lý.
3. **Network (Mạng)**: Các dịch vụ liên quan đến mạng như load balancer, firewall, VPC.
4. **Storage (Lưu trữ)**: Các dịch vụ lưu trữ như Spaces và Volumes.

## Các Pattern Diagram phổ biến

Khi làm việc với DigitalOcean, có một số pattern diagram phổ biến mà bạn có thể sử dụng:

1. **Web Application Architecture**: Kiến trúc ứng dụng web cơ bản với Droplets, Load Balancer và Database.
2. **Microservices Architecture**: Kiến trúc microservices sử dụng Kubernetes (DOKS).
3. **Highly Available Database Setup**: Thiết lập cơ sở dữ liệu có tính sẵn sàng cao với primary và standby.
4. **Content Delivery Architecture**: Kiến trúc phân phối nội dung sử dụng Spaces và CDN.

Trong các tài liệu tiếp theo, chúng ta sẽ đi sâu vào từng nhóm nodes và cách sử dụng chúng trong các sơ đồ kiến trúc.
