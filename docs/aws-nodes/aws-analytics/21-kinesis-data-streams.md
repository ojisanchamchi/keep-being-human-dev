# Amazon Kinesis Data Streams

## Tổng quan

Amazon Kinesis Data Streams là node đại diện cho dịch vụ streaming data platform real-time của AWS. Data Streams cho phép bạn build applications có thể process và analyze streaming data trong real-time. Dịch vụ này có thể handle terabytes của data per hour từ hàng trăm nghìn sources như website clickstreams, database event streams, financial transactions, social media feeds, IT logs, và location-tracking events.

## Chức năng chính

### 1. Real-time Data Ingestion
- **High Throughput**: Xử lý millions of records per second
- **Low Latency**: Sub-second processing latency
- **Durable Storage**: Data retention từ 24 hours đến 365 days
- **Ordered Processing**: Maintain order within shards

### 2. Scalable Architecture
- **Shard-based Scaling**: Scale bằng cách thêm/bớt shards
- **Auto Scaling**: Tự động adjust capacity
- **Multiple Consumers**: Multiple applications có thể consume cùng stream
- **Fan-out**: Enhanced fan-out cho multiple consumers

### 3. Data Processing Models
- **Shared Throughput**: Traditional consumer model
- **Enhanced Fan-out**: Dedicated throughput per consumer
- **Kinesis Client Library**: Simplified consumer development
- **Lambda Integration**: Serverless processing

### 4. Monitoring và Management
- **CloudWatch Integration**: Comprehensive metrics
- **Server-side Encryption**: Data encryption at rest
- **VPC Endpoints**: Private connectivity
- **Cross-region Replication**: Disaster recovery

## Use Cases phổ biến

1. **Real-time Analytics**: Live dashboards và metrics
2. **Log Processing**: Centralized log aggregation
3. **IoT Data Processing**: Sensor data streams
4. **Clickstream Analysis**: Website user behavior
5. **Financial Data**: Trading data và fraud detection

## Diagram Architecture

Kiến trúc Amazon Kinesis Data Streams với real-time processing:

![Amazon Kinesis Data Streams Architecture](/img/aws-analytics/kinesis-data-streams.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisDataStreams, KinesisDataAnalytics, KinesisDataFirehose
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.database import Dynamodb, RDS
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users

with Diagram("Amazon Kinesis Data Streams Architecture", show=False, direction="TB"):
    
    users = Users("Data Producers")
    
    with Cluster("Data Producers"):
        web_apps = Lambda("Web Applications")
        mobile_apps = Lambda("Mobile Apps")
        iot_devices = Lambda("IoT Devices")
        log_agents = EC2("Log Agents")
        databases = RDS("Database CDC")
    
    with Cluster("Kinesis Data Streams"):
        stream = KinesisDataStreams("Data Stream")
        
        with Cluster("Shards"):
            shard1 = KinesisDataStreams("Shard 1")
            shard2 = KinesisDataStreams("Shard 2")
            shard3 = KinesisDataStreams("Shard 3")
            shard4 = KinesisDataStreams("Shard 4")
    
    with Cluster("Stream Consumers"):
        lambda_consumer = Lambda("Lambda Consumer")
        kda_app = KinesisDataAnalytics("KDA Application")
        firehose_consumer = KinesisDataFirehose("Firehose Consumer")
        custom_consumer = EC2("Custom Consumer")
    
    with Cluster("Processing & Storage"):
        real_time_db = Dynamodb("Real-time Results")
        s3_storage = S3("Data Lake")
        analytics_db = RDS("Analytics DB")
        search_index = Lambda("Search Index")
    
    with Cluster("Downstream Applications"):
        dashboard = Lambda("Real-time Dashboard")
        alerts = SNS("Alert System")
        ml_pipeline = Lambda("ML Pipeline")
        reporting = Lambda("Reporting System")
    
    with Cluster("Monitoring & Management"):
        cloudwatch = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
        scaling = Lambda("Auto Scaling")
    
    # Data ingestion
    web_apps >> Edge(label="Events") >> stream
    mobile_apps >> Edge(label="Analytics") >> stream
    iot_devices >> Edge(label="Sensor Data") >> stream
    log_agents >> Edge(label="Logs") >> stream
    databases >> Edge(label="Change Events") >> stream
    
    # Shard distribution
    stream >> shard1
    stream >> shard2
    stream >> shard3
    stream >> shard4
    
    # Stream consumption
    shard1 >> lambda_consumer
    shard2 >> kda_app
    shard3 >> firehose_consumer
    shard4 >> custom_consumer
    
    # Data processing and storage
    lambda_consumer >> real_time_db
    kda_app >> analytics_db
    firehose_consumer >> s3_storage
    custom_consumer >> search_index
    
    # Downstream applications
    real_time_db >> dashboard
    analytics_db >> alerts
    s3_storage >> ml_pipeline
    search_index >> reporting
    
    # User interaction
    users >> Edge(label="View Dashboards") >> dashboard
    users >> Edge(label="Receive Alerts") >> alerts
    
    # Monitoring and management
    stream >> Edge(label="Metrics") >> cloudwatch
    cloudwatch >> scaling >> stream
    security >> Edge(label="Access Control") >> stream
```

## Stream Configuration

### 1. Stream Creation và Management
```python
import boto3
import json
from datetime import datetime

kinesis = boto3.client('kinesis')

# Create stream with multiple shards
def create_kinesis_stream(stream_name, shard_count):
    """Create Kinesis Data Stream"""
    
    try:
        response = kinesis.create_stream(
            StreamName=stream_name,
            ShardCount=shard_count,
            StreamModeDetails={
                'StreamMode': 'PROVISIONED'
            }
        )
        
        print(f"Stream {stream_name} created with {shard_count} shards")
        return response
        
    except kinesis.exceptions.ResourceInUseException:
        print(f"Stream {stream_name} already exists")
        return None

# On-demand mode for variable workloads
def create_on_demand_stream(stream_name):
    """Create on-demand Kinesis stream"""
    
    response = kinesis.create_stream(
        StreamName=stream_name,
        StreamModeDetails={
            'StreamMode': 'ON_DEMAND'
        }
    )
    
    return response

# Configure stream retention
def configure_retention(stream_name, retention_hours):
    """Configure data retention period"""
    
    kinesis.increase_stream_retention_period(
        StreamName=stream_name,
        RetentionPeriodHours=retention_hours  # 24-8760 hours
    )
    
    print(f"Retention set to {retention_hours} hours for {stream_name}")

# Enable server-side encryption
def enable_encryption(stream_name, key_id):
    """Enable server-side encryption"""
    
    kinesis.enable_stream_encryption(
        StreamName=stream_name,
        EncryptionType='KMS',
        KeyId=key_id
    )
    
    print(f"Encryption enabled for {stream_name}")
```

### 2. Data Producer Implementation
```python
class KinesisProducer:
    def __init__(self, stream_name, region='us-west-2'):
        self.kinesis = boto3.client('kinesis', region_name=region)
        self.stream_name = stream_name
        
    def put_record(self, data, partition_key):
        """Put single record to stream"""
        
        try:
            response = self.kinesis.put_record(
                StreamName=self.stream_name,
                Data=json.dumps(data),
                PartitionKey=partition_key
            )
            
            return {
                'success': True,
                'shard_id': response['ShardId'],
                'sequence_number': response['SequenceNumber']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def put_records_batch(self, records):
        """Put multiple records in batch"""
        
        # Prepare records for batch put
        kinesis_records = []
        for record in records:
            kinesis_records.append({
                'Data': json.dumps(record['data']),
                'PartitionKey': record['partition_key']
            })
        
        # Batch put with retry logic
        failed_records = []
        batch_size = 500  # Max 500 records per batch
        
        for i in range(0, len(kinesis_records), batch_size):
            batch = kinesis_records[i:i + batch_size]
            
            try:
                response = self.kinesis.put_records(
                    Records=batch,
                    StreamName=self.stream_name
                )
                
                # Handle partial failures
                if response['FailedRecordCount'] > 0:
                    for j, record_result in enumerate(response['Records']):
                        if 'ErrorCode' in record_result:
                            failed_records.append({
                                'record': batch[j],
                                'error': record_result['ErrorMessage']
                            })
                
            except Exception as e:
                # Add entire batch to failed records
                failed_records.extend([{
                    'record': record,
                    'error': str(e)
                } for record in batch])
        
        return {
            'total_records': len(kinesis_records),
            'failed_records': failed_records,
            'success_rate': (len(kinesis_records) - len(failed_records)) / len(kinesis_records)
        }
    
    def put_record_with_retry(self, data, partition_key, max_retries=3):
        """Put record with exponential backoff retry"""
        
        import time
        import random
        
        for attempt in range(max_retries + 1):
            result = self.put_record(data, partition_key)
            
            if result['success']:
                return result
            
            if attempt < max_retries:
                # Exponential backoff with jitter
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
        
        return result
```

### 3. Advanced Producer với KPL
```python
# Kinesis Producer Library (KPL) configuration
class AdvancedKinesisProducer:
    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.producer = self.create_kpl_producer()
    
    def create_kpl_producer(self):
        """Create KPL producer with optimized configuration"""
        
        from amazon_kinesis_producer import KinesisProducer
        
        config = {
            'region': 'us-west-2',
            'aggregation_enabled': True,
            'aggregation_max_count': 4294967295,
            'aggregation_max_size': 51200,
            'collection_max_count': 500,
            'collection_max_size': 5242880,
            'record_max_buffered_time': 100,
            'request_timeout': 6000,
            'record_ttl': 30000,
            'metrics_level': 'detailed',
            'metrics_granularity': 'shard'
        }
        
        return KinesisProducer(config)
    
    def send_async(self, data, partition_key):
        """Send record asynchronously with KPL"""
        
        future = self.producer.add_user_record(
            stream_name=self.stream_name,
            partition_key=partition_key,
            data=json.dumps(data)
        )
        
        return future
    
    def send_batch_async(self, records):
        """Send batch of records asynchronously"""
        
        futures = []
        
        for record in records:
            future = self.send_async(record['data'], record['partition_key'])
            futures.append(future)
        
        return futures
    
    def flush_and_wait(self):
        """Flush all pending records and wait for completion"""
        
        self.producer.flush_sync()
```

## Stream Consumer Implementation

### 1. Lambda Consumer
```python
import json
import base64
from datetime import datetime

def lambda_handler(event, context):
    """Process Kinesis records in Lambda"""
    
    processed_records = []
    failed_records = []
    
    for record in event['Records']:
        try:
            # Decode Kinesis data
            payload = base64.b64decode(record['kinesis']['data'])
            data = json.loads(payload)
            
            # Process the record
            processed_data = process_kinesis_record(data, record)
            processed_records.append(processed_data)
            
        except Exception as e:
            failed_records.append({
                'recordId': record['kinesis']['sequenceNumber'],
                'error': str(e)
            })
    
    # Store processed records
    if processed_records:
        store_processed_records(processed_records)
    
    # Handle failed records
    if failed_records:
        handle_failed_records(failed_records)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'processed': len(processed_records),
            'failed': len(failed_records)
        })
    }

def process_kinesis_record(data, kinesis_record):
    """Process individual Kinesis record"""
    
    processed = {
        'original_data': data,
        'kinesis_metadata': {
            'shard_id': kinesis_record['kinesis']['shardId'],
            'sequence_number': kinesis_record['kinesis']['sequenceNumber'],
            'approximate_arrival_timestamp': kinesis_record['kinesis']['approximateArrivalTimestamp']
        },
        'processed_at': datetime.utcnow().isoformat()
    }
    
    # Add business logic processing
    if data.get('event_type') == 'user_action':
        processed['user_segment'] = determine_user_segment(data)
        processed['action_score'] = calculate_action_score(data)
    
    return processed

def determine_user_segment(data):
    """Determine user segment based on data"""
    
    user_id = data.get('user_id')
    action_type = data.get('action_type')
    
    # Simple segmentation logic
    if action_type in ['purchase', 'premium_feature']:
        return 'high_value'
    elif action_type in ['login', 'page_view']:
        return 'active'
    else:
        return 'standard'

def calculate_action_score(data):
    """Calculate action importance score"""
    
    score_map = {
        'purchase': 10,
        'signup': 8,
        'premium_feature': 7,
        'login': 3,
        'page_view': 1
    }
    
    return score_map.get(data.get('action_type'), 0)
```

### 2. KCL Consumer Application
```python
from amazon_kclpy import kcl
from amazon_kclpy.v3 import processor
import json

class KinesisRecordProcessor(processor.RecordProcessorBase):
    """
    Kinesis Client Library record processor
    """
    
    def __init__(self):
        self.shard_id = None
        self.checkpoint_freq_seconds = 60
        self.last_checkpoint_time = 0
    
    def initialize(self, initialize_input):
        """Initialize the processor"""
        
        self.shard_id = initialize_input.shard_id
        print(f"Initialized processor for shard: {self.shard_id}")
    
    def process_records(self, process_records_input):
        """Process batch of records"""
        
        try:
            records = process_records_input.records
            
            for record in records:
                # Process individual record
                self.process_single_record(record)
            
            # Checkpoint periodically
            current_time = time.time()
            if current_time - self.last_checkpoint_time > self.checkpoint_freq_seconds:
                self.checkpoint(process_records_input.checkpointer)
                self.last_checkpoint_time = current_time
                
        except Exception as e:
            print(f"Error processing records: {str(e)}")
    
    def process_single_record(self, record):
        """Process individual record"""
        
        try:
            # Decode record data
            data = json.loads(record.binary_data.decode('utf-8'))
            
            # Business logic processing
            if data.get('event_type') == 'order':
                self.process_order_event(data)
            elif data.get('event_type') == 'user_activity':
                self.process_user_activity(data)
            
            print(f"Processed record: {record.sequence_number}")
            
        except Exception as e:
            print(f"Error processing record {record.sequence_number}: {str(e)}")
    
    def process_order_event(self, data):
        """Process order-related events"""
        
        # Update real-time metrics
        self.update_order_metrics(data)
        
        # Check for fraud patterns
        if self.detect_fraud_pattern(data):
            self.send_fraud_alert(data)
        
        # Update inventory
        self.update_inventory(data)
    
    def process_user_activity(self, data):
        """Process user activity events"""
        
        # Update user profile
        self.update_user_profile(data)
        
        # Personalization engine
        self.update_recommendations(data)
        
        # Analytics tracking
        self.track_user_journey(data)
    
    def checkpoint(self, checkpointer):
        """Checkpoint progress"""
        
        try:
            checkpointer.checkpoint()
            print(f"Checkpointed shard: {self.shard_id}")
        except Exception as e:
            print(f"Error checkpointing: {str(e)}")
    
    def shutdown(self, shutdown_input):
        """Shutdown processor"""
        
        try:
            if shutdown_input.reason == 'TERMINATE':
                # Final checkpoint
                shutdown_input.checkpointer.checkpoint()
            
            print(f"Shutdown processor for shard: {self.shard_id}")
            
        except Exception as e:
            print(f"Error during shutdown: {str(e)}")

# KCL application configuration
if __name__ == '__main__':
    kcl_process = kcl.KCLProcess(KinesisRecordProcessor())
    kcl_process.run()
```

## Scaling và Performance

### 1. Shard Management
```python
class KinesisShardManager:
    def __init__(self, stream_name):
        self.kinesis = boto3.client('kinesis')
        self.cloudwatch = boto3.client('cloudwatch')
        self.stream_name = stream_name
    
    def get_stream_metrics(self):
        """Get stream performance metrics"""
        
        from datetime import datetime, timedelta
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)
        
        metrics = {}
        
        # Get incoming records metric
        response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/Kinesis',
            MetricName='IncomingRecords',
            Dimensions=[
                {
                    'Name': 'StreamName',
                    'Value': self.stream_name
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Sum', 'Average']
        )
        
        metrics['incoming_records'] = response['Datapoints']
        
        # Get incoming bytes metric
        response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/Kinesis',
            MetricName='IncomingBytes',
            Dimensions=[
                {
                    'Name': 'StreamName',
                    'Value': self.stream_name
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Sum', 'Average']
        )
        
        metrics['incoming_bytes'] = response['Datapoints']
        
        return metrics
    
    def should_scale_out(self):
        """Determine if stream should scale out"""
        
        metrics = self.get_stream_metrics()
        
        # Check if any shard is approaching limits
        stream_description = self.kinesis.describe_stream(StreamName=self.stream_name)
        shard_count = len(stream_description['StreamDescription']['Shards'])
        
        # Calculate average throughput per shard
        if metrics['incoming_records']:
            avg_records_per_minute = sum([dp['Sum'] for dp in metrics['incoming_records']]) / len(metrics['incoming_records'])
            records_per_shard_per_minute = avg_records_per_minute / shard_count
            
            # Scale out if approaching 1000 records/second per shard
            if records_per_shard_per_minute > 50000:  # 1000 * 60 * 0.8 (80% threshold)
                return True
        
        if metrics['incoming_bytes']:
            avg_bytes_per_minute = sum([dp['Sum'] for dp in metrics['incoming_bytes']]) / len(metrics['incoming_bytes'])
            bytes_per_shard_per_minute = avg_bytes_per_minute / shard_count
            
            # Scale out if approaching 1MB/second per shard
            if bytes_per_shard_per_minute > 48000000:  # 1MB * 60 * 0.8 (80% threshold)
                return True
        
        return False
    
    def scale_stream(self, target_shard_count):
        """Scale stream to target shard count"""
        
        current_description = self.kinesis.describe_stream(StreamName=self.stream_name)
        current_shard_count = len(current_description['StreamDescription']['Shards'])
        
        if target_shard_count > current_shard_count:
            # Scale out
            self.kinesis.update_shard_count(
                StreamName=self.stream_name,
                TargetShardCount=target_shard_count,
                ScalingType='UNIFORM_SCALING'
            )
            print(f"Scaling out from {current_shard_count} to {target_shard_count} shards")
            
        elif target_shard_count < current_shard_count:
            # Scale in
            self.kinesis.update_shard_count(
                StreamName=self.stream_name,
                TargetShardCount=target_shard_count,
                ScalingType='UNIFORM_SCALING'
            )
            print(f"Scaling in from {current_shard_count} to {target_shard_count} shards")
    
    def auto_scale_based_on_metrics(self):
        """Automatically scale based on metrics"""
        
        if self.should_scale_out():
            current_description = self.kinesis.describe_stream(StreamName=self.stream_name)
            current_shard_count = len(current_description['StreamDescription']['Shards'])
            
            # Scale out by 50%
            new_shard_count = int(current_shard_count * 1.5)
            self.scale_stream(new_shard_count)
```

## Best Practices

1. **Partition Key Design**: Choose partition keys để distribute data evenly
2. **Shard Management**: Monitor và scale shards appropriately
3. **Consumer Design**: Implement efficient consumer applications
4. **Error Handling**: Handle failures và implement retry logic
5. **Monitoring**: Set up comprehensive monitoring
6. **Security**: Use IAM roles và encrypt sensitive data
7. **Cost Optimization**: Use on-demand mode cho variable workloads
8. **Data Retention**: Set appropriate retention periods

## Tích hợp với các dịch vụ AWS khác

- **AWS Lambda**: Serverless stream processing
- **Amazon Kinesis Data Analytics**: Real-time analytics
- **Amazon Kinesis Data Firehose**: Data delivery
- **Amazon DynamoDB**: Real-time data storage
- **Amazon S3**: Data archival và analytics
- **Amazon CloudWatch**: Monitoring và alerting
- **AWS IAM**: Security và access control
- **Amazon VPC**: Network isolation
- **AWS KMS**: Data encryption
- **Amazon SNS**: Notifications và alerts
