# Amazon Kinesis Data Firehose

## Tổng quan

Amazon Kinesis Data Firehose là node đại diện cho dịch vụ delivery streaming data được quản lý hoàn toàn của AWS. Firehose tự động capture, transform, và load streaming data vào các data stores như Amazon S3, Amazon Redshift, Amazon OpenSearch Service, và third-party services. Đây là cách đơn giản nhất để load streaming data vào data lakes và analytics services.

## Chức năng chính

### 1. Managed Data Delivery
- **Serverless**: Không cần quản lý infrastructure
- **Auto Scaling**: Tự động scale theo throughput
- **Reliable Delivery**: Guaranteed delivery với retry logic
- **Buffering**: Intelligent buffering based on size và time

### 2. Data Transformation
- **Built-in Transformations**: Format conversion (JSON to Parquet/ORC)
- **AWS Lambda Integration**: Custom data transformation
- **Data Compression**: GZIP, Snappy, ZIP compression
- **Error Record Handling**: Separate error records processing

### 3. Multiple Destinations
- **Amazon S3**: Data lake storage
- **Amazon Redshift**: Data warehouse loading
- **Amazon OpenSearch**: Search và analytics
- **Third-party**: Splunk, Datadog, New Relic, MongoDB

### 4. Monitoring và Management
- **CloudWatch Integration**: Comprehensive metrics
- **Error Logging**: Detailed error tracking
- **Data Lineage**: Track data flow
- **Cost Optimization**: Pay only for data processed

## Use Cases phổ biến

1. **Data Lake Ingestion**: Load streaming data vào S3 data lakes
2. **Log Aggregation**: Centralize logs từ multiple sources
3. **Real-time ETL**: Transform và load data for analytics
4. **Backup và Archival**: Backup streaming data
5. **Multi-destination Delivery**: Deliver data đến multiple targets

## Diagram Architecture

Kiến trúc Amazon Kinesis Data Firehose với data delivery pipeline:

![Amazon Kinesis Data Firehose Architecture](/img/aws-analytics/kinesis-data-firehose.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisDataFirehose, KinesisDataStreams, Athena
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Redshift, Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Splunk

with Diagram("Amazon Kinesis Data Firehose Architecture", show=False, direction="TB"):
    
    users = Users("Applications")
    
    with Cluster("Data Sources"):
        web_logs = Lambda("Web Server Logs")
        app_events = Lambda("Application Events")
        iot_sensors = Lambda("IoT Sensors")
        clickstream = Lambda("Clickstream Data")
        kinesis_streams = KinesisDataStreams("Kinesis Data Streams")
    
    with Cluster("Firehose Delivery Streams"):
        firehose_s3 = KinesisDataFirehose("S3 Delivery Stream")
        firehose_redshift = KinesisDataFirehose("Redshift Delivery Stream")
        firehose_opensearch = KinesisDataFirehose("OpenSearch Delivery Stream")
        firehose_splunk = KinesisDataFirehose("Splunk Delivery Stream")
    
    with Cluster("Data Transformation"):
        lambda_transform = Lambda("Data Transformation")
        format_converter = Lambda("Format Converter")
        data_enrichment = Lambda("Data Enrichment")
    
    with Cluster("Destinations"):
        s3_data_lake = S3("S3 Data Lake")
        redshift_dw = Redshift("Redshift DW")
        opensearch = Lambda("OpenSearch Service")
        splunk_cloud = Splunk("Splunk Cloud")
    
    with Cluster("Error Handling"):
        error_bucket = S3("Error Records")
        processing_errors = S3("Processing Errors")
        dlq = SQS("Dead Letter Queue")
    
    with Cluster("Analytics & Monitoring"):
        athena = Athena("Athena Queries")
        cloudwatch = Cloudwatch("CloudWatch")
        notifications = SNS("Notifications")
        security = IAM("IAM Roles")
    
    # Data ingestion flow
    web_logs >> Edge(label="Direct PUT") >> firehose_s3
    app_events >> Edge(label="SDK/API") >> firehose_redshift
    iot_sensors >> Edge(label="IoT Core") >> firehose_opensearch
    clickstream >> Edge(label="Analytics") >> firehose_splunk
    kinesis_streams >> Edge(label="Stream Consumer") >> firehose_s3
    
    # Data transformation
    firehose_s3 >> lambda_transform
    firehose_redshift >> format_converter
    firehose_opensearch >> data_enrichment
    
    lambda_transform >> firehose_s3
    format_converter >> firehose_redshift
    data_enrichment >> firehose_opensearch
    
    # Data delivery
    firehose_s3 >> Edge(label="Parquet/ORC") >> s3_data_lake
    firehose_redshift >> Edge(label="COPY Command") >> redshift_dw
    firehose_opensearch >> Edge(label="Bulk API") >> opensearch
    firehose_splunk >> Edge(label="HEC Protocol") >> splunk_cloud
    
    # Error handling
    firehose_s3 >> Edge(label="Failed Records") >> error_bucket
    lambda_transform >> Edge(label="Processing Errors") >> processing_errors
    firehose_redshift >> Edge(label="Failed Loads") >> dlq
    
    # Analytics integration
    s3_data_lake >> athena
    users >> Edge(label="Query Data") >> athena
    
    # Monitoring
    firehose_s3 >> Edge(label="Metrics") >> cloudwatch
    cloudwatch >> notifications
    security >> Edge(label="Access Control") >> firehose_s3
```

## Delivery Stream Configuration

### 1. S3 Delivery Stream
```python
import boto3
import json

firehose = boto3.client('firehose')

# S3 delivery stream with transformation
s3_delivery_config = {
    'DeliveryStreamName': 'web-logs-to-s3',
    'DeliveryStreamType': 'DirectPut',
    'ExtendedS3DestinationConfiguration': {
        'RoleARN': 'arn:aws:iam::account:role/firehose-delivery-role',
        'BucketARN': 'arn:aws:s3:::data-lake-bucket',
        'Prefix': 'web-logs/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/',
        'ErrorOutputPrefix': 'errors/web-logs/',
        'BufferingHints': {
            'SizeInMBs': 128,
            'IntervalInSeconds': 60
        },
        'CompressionFormat': 'GZIP',
        'DataFormatConversionConfiguration': {
            'Enabled': True,
            'OutputFormatConfiguration': {
                'Serializer': {
                    'ParquetSerDe': {}
                }
            },
            'SchemaConfiguration': {
                'DatabaseName': 'web_logs_db',
                'TableName': 'access_logs',
                'RoleARN': 'arn:aws:iam::account:role/glue-catalog-role'
            }
        },
        'ProcessingConfiguration': {
            'Enabled': True,
            'Processors': [
                {
                    'Type': 'Lambda',
                    'Parameters': [
                        {
                            'ParameterName': 'LambdaArn',
                            'ParameterValue': 'arn:aws:lambda:region:account:function:log-transformer'
                        }
                    ]
                }
            ]
        },
        'CloudWatchLoggingOptions': {
            'Enabled': True,
            'LogGroupName': '/aws/kinesisfirehose/web-logs-to-s3'
        }
    }
}

response = firehose.create_delivery_stream(**s3_delivery_config)
```

### 2. Redshift Delivery Stream
```python
# Redshift delivery stream configuration
redshift_delivery_config = {
    'DeliveryStreamName': 'events-to-redshift',
    'DeliveryStreamType': 'DirectPut',
    'RedshiftDestinationConfiguration': {
        'RoleARN': 'arn:aws:iam::account:role/firehose-redshift-role',
        'ClusterJDBCURL': 'jdbc:redshift://redshift-cluster.region.redshift.amazonaws.com:5439/analytics',
        'CopyCommand': {
            'DataTableName': 'user_events',
            'DataTableColumns': 'event_id,user_id,event_type,timestamp,properties',
            'CopyOptions': "JSON 'auto' GZIP TRUNCATECOLUMNS"
        },
        'Username': 'firehose_user',
        'Password': 'secure_password',
        'S3Configuration': {
            'RoleARN': 'arn:aws:iam::account:role/firehose-s3-role',
            'BucketARN': 'arn:aws:s3:::redshift-staging-bucket',
            'Prefix': 'staging/events/',
            'BufferingHints': {
                'SizeInMBs': 5,
                'IntervalInSeconds': 300
            },
            'CompressionFormat': 'GZIP'
        },
        'ProcessingConfiguration': {
            'Enabled': True,
            'Processors': [
                {
                    'Type': 'Lambda',
                    'Parameters': [
                        {
                            'ParameterName': 'LambdaArn',
                            'ParameterValue': 'arn:aws:lambda:region:account:function:redshift-transformer'
                        }
                    ]
                }
            ]
        },
        'RetryDuration': 3600,
        'CloudWatchLoggingOptions': {
            'Enabled': True,
            'LogGroupName': '/aws/kinesisfirehose/events-to-redshift'
        }
    }
}

response = firehose.create_delivery_stream(**redshift_delivery_config)
```

## Data Transformation

### 1. Lambda Transformation Function
```python
import json
import base64
import gzip
from datetime import datetime

def lambda_handler(event, context):
    """
    Transform Kinesis Data Firehose records
    """
    
    output = []
    
    for record in event['records']:
        # Decode the data
        compressed_payload = base64.b64decode(record['data'])
        uncompressed_payload = gzip.decompress(compressed_payload)
        data = json.loads(uncompressed_payload)
        
        # Transform the data
        transformed_data = transform_log_record(data)
        
        # Encode the transformed data
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(
                json.dumps(transformed_data).encode('utf-8') + b'\n'
            ).decode('utf-8')
        }
        
        output.append(output_record)
    
    return {'records': output}

def transform_log_record(data):
    """Transform individual log record"""
    
    transformed = {
        'timestamp': datetime.utcnow().isoformat(),
        'source_ip': data.get('ip', ''),
        'user_agent': data.get('user_agent', ''),
        'request_method': data.get('method', ''),
        'request_uri': data.get('uri', ''),
        'response_code': int(data.get('status', 0)),
        'response_size': int(data.get('size', 0)),
        'processing_time': float(data.get('response_time', 0.0))
    }
    
    # Add derived fields
    transformed['is_error'] = transformed['response_code'] >= 400
    transformed['is_bot'] = is_bot_request(transformed['user_agent'])
    transformed['country'] = get_country_from_ip(transformed['source_ip'])
    
    # Data quality checks
    if not validate_record(transformed):
        raise ValueError("Invalid record format")
    
    return transformed

def is_bot_request(user_agent):
    """Detect bot requests"""
    bot_indicators = ['bot', 'crawler', 'spider', 'scraper']
    return any(indicator in user_agent.lower() for indicator in bot_indicators)

def get_country_from_ip(ip_address):
    """Get country from IP address (simplified)"""
    # In production, use a proper GeoIP service
    if ip_address.startswith('192.168.'):
        return 'US'  # Private IP
    return 'UNKNOWN'

def validate_record(record):
    """Validate transformed record"""
    required_fields = ['timestamp', 'source_ip', 'request_method']
    return all(field in record and record[field] for field in required_fields)
```

### 2. Advanced Transformation Pipeline
```python
class FirehoseTransformationPipeline:
    def __init__(self):
        self.transformers = [
            self.parse_log_format,
            self.enrich_with_geolocation,
            self.detect_anomalies,
            self.add_metadata
        ]
    
    def process_records(self, records):
        """Process batch of records through transformation pipeline"""
        
        processed_records = []
        
        for record in records:
            try:
                # Decode record
                data = self.decode_record(record)
                
                # Apply transformation pipeline
                for transformer in self.transformers:
                    data = transformer(data)
                
                # Encode transformed record
                processed_record = self.encode_record(record['recordId'], data)
                processed_records.append(processed_record)
                
            except Exception as e:
                # Handle transformation errors
                error_record = {
                    'recordId': record['recordId'],
                    'result': 'ProcessingFailed',
                    'data': record['data']  # Return original data
                }
                processed_records.append(error_record)
                
                # Log error for monitoring
                print(f"Transformation error: {str(e)}")
        
        return processed_records
    
    def parse_log_format(self, data):
        """Parse common log formats"""
        
        if 'message' in data:
            # Parse Apache/Nginx log format
            log_pattern = r'(\S+) \S+ \S+ \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+)'
            match = re.match(log_pattern, data['message'])
            
            if match:
                data.update({
                    'ip': match.group(1),
                    'timestamp': match.group(2),
                    'method': match.group(3),
                    'uri': match.group(4),
                    'protocol': match.group(5),
                    'status': int(match.group(6)),
                    'size': int(match.group(7))
                })
        
        return data
    
    def enrich_with_geolocation(self, data):
        """Enrich with geolocation data"""
        
        if 'ip' in data:
            # In production, use MaxMind GeoIP or similar service
            geo_data = self.lookup_geolocation(data['ip'])
            data.update({
                'country': geo_data.get('country', 'UNKNOWN'),
                'city': geo_data.get('city', 'UNKNOWN'),
                'latitude': geo_data.get('latitude'),
                'longitude': geo_data.get('longitude')
            })
        
        return data
    
    def detect_anomalies(self, data):
        """Detect anomalous patterns"""
        
        anomaly_score = 0.0
        
        # Check for suspicious patterns
        if data.get('status', 0) >= 400:
            anomaly_score += 0.3
        
        if data.get('size', 0) > 10000000:  # Large response
            anomaly_score += 0.2
        
        if self.is_suspicious_uri(data.get('uri', '')):
            anomaly_score += 0.5
        
        data['anomaly_score'] = anomaly_score
        data['is_anomalous'] = anomaly_score > 0.7
        
        return data
    
    def add_metadata(self, data):
        """Add processing metadata"""
        
        data['processed_at'] = datetime.utcnow().isoformat()
        data['processor_version'] = '1.0.0'
        data['partition_key'] = self.generate_partition_key(data)
        
        return data
```

## Performance Optimization

### 1. Buffering Configuration
```python
class FirehoseOptimizer:
    def __init__(self):
        self.firehose = boto3.client('firehose')
    
    def optimize_buffering(self, delivery_stream_name, throughput_mbps):
        """Optimize buffering based on throughput"""
        
        if throughput_mbps < 1:
            # Low throughput - optimize for latency
            buffer_config = {
                'SizeInMBs': 1,
                'IntervalInSeconds': 60
            }
        elif throughput_mbps < 10:
            # Medium throughput - balanced approach
            buffer_config = {
                'SizeInMBs': 5,
                'IntervalInSeconds': 300
            }
        else:
            # High throughput - optimize for efficiency
            buffer_config = {
                'SizeInMBs': 128,
                'IntervalInSeconds': 900
            }
        
        return buffer_config
    
    def configure_compression(self, data_type):
        """Choose optimal compression based on data type"""
        
        compression_map = {
            'logs': 'GZIP',        # Good compression ratio
            'json': 'GZIP',        # Good for structured data
            'csv': 'GZIP',         # Good for tabular data
            'binary': 'UNCOMPRESSED',  # Already compressed
            'images': 'UNCOMPRESSED'   # Already compressed
        }
        
        return compression_map.get(data_type, 'GZIP')
    
    def estimate_costs(self, records_per_second, avg_record_size_kb, hours_per_month):
        """Estimate Firehose costs"""
        
        # Calculate monthly data volume
        monthly_records = records_per_second * 3600 * hours_per_month
        monthly_gb = (monthly_records * avg_record_size_kb) / (1024 * 1024)
        
        # Firehose pricing (example rates)
        cost_per_gb = 0.029  # $0.029 per GB
        
        estimated_cost = monthly_gb * cost_per_gb
        
        return {
            'monthly_records': monthly_records,
            'monthly_gb': monthly_gb,
            'estimated_cost_usd': estimated_cost,
            'cost_per_million_records': (estimated_cost / monthly_records) * 1000000
        }
```

## Error Handling và Monitoring

### 1. Comprehensive Error Handling
```python
class FirehoseErrorHandler:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
    
    def handle_delivery_errors(self, delivery_stream_name):
        """Monitor and handle delivery errors"""
        
        # Get error metrics
        error_metrics = self.get_error_metrics(delivery_stream_name)
        
        if error_metrics['error_rate'] > 0.05:  # 5% error rate threshold
            self.send_alert(
                f"High error rate detected for {delivery_stream_name}",
                error_metrics
            )
        
        # Check for specific error patterns
        self.analyze_error_patterns(delivery_stream_name)
    
    def get_error_metrics(self, delivery_stream_name):
        """Get delivery error metrics"""
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)
        
        # Get delivery success/failure metrics
        success_response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/KinesisFirehose',
            MetricName='DeliveryToS3.Success',
            Dimensions=[
                {
                    'Name': 'DeliveryStreamName',
                    'Value': delivery_stream_name
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Sum']
        )
        
        failure_response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/KinesisFirehose',
            MetricName='DeliveryToS3.DataFreshness',
            Dimensions=[
                {
                    'Name': 'DeliveryStreamName',
                    'Value': delivery_stream_name
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Maximum']
        )
        
        total_success = sum([dp['Sum'] for dp in success_response['Datapoints']])
        max_freshness = max([dp['Maximum'] for dp in failure_response['Datapoints']] or [0])
        
        return {
            'total_deliveries': total_success,
            'max_data_freshness': max_freshness,
            'error_rate': 0 if total_success == 0 else (1 - total_success / (total_success + 1))
        }
    
    def create_monitoring_dashboard(self, delivery_stream_names):
        """Create CloudWatch dashboard for monitoring"""
        
        dashboard_body = {
            "widgets": []
        }
        
        for i, stream_name in enumerate(delivery_stream_names):
            # Delivery metrics widget
            widget = {
                "type": "metric",
                "properties": {
                    "metrics": [
                        ["AWS/KinesisFirehose", "DeliveryToS3.Records", "DeliveryStreamName", stream_name],
                        [".", "DeliveryToS3.Bytes", ".", "."],
                        [".", "DeliveryToS3.Success", ".", "."]
                    ],
                    "period": 300,
                    "stat": "Sum",
                    "region": "us-west-2",
                    "title": f"Delivery Metrics - {stream_name}"
                }
            }
            dashboard_body["widgets"].append(widget)
        
        self.cloudwatch.put_dashboard(
            DashboardName='KinesisFirehose-Monitoring',
            DashboardBody=json.dumps(dashboard_body)
        )
```

## Best Practices

1. **Buffer Sizing**: Optimize buffer size và interval cho throughput
2. **Compression**: Sử dụng appropriate compression formats
3. **Partitioning**: Design effective S3 partitioning strategy
4. **Error Handling**: Implement comprehensive error handling
5. **Monitoring**: Set up detailed monitoring và alerting
6. **Cost Optimization**: Monitor và optimize costs regularly
7. **Security**: Use IAM roles và encrypt data in transit
8. **Testing**: Test với realistic data volumes

## Tích hợp với các dịch vụ AWS khác

- **Amazon Kinesis Data Streams**: Source for streaming data
- **AWS Lambda**: Data transformation functions
- **Amazon S3**: Primary destination for data lakes
- **Amazon Redshift**: Data warehouse loading
- **Amazon OpenSearch Service**: Search và analytics
- **AWS Glue**: Data catalog integration
- **Amazon Athena**: Query delivered data
- **Amazon CloudWatch**: Monitoring và alerting
- **AWS IAM**: Security và access control
- **Amazon VPC**: Network isolation
