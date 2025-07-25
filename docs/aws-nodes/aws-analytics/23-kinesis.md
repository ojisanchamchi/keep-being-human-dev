# Amazon Kinesis

## Tổng quan

Amazon Kinesis là node tổng quát đại diện cho family of services của AWS dành cho real-time data streaming và analytics. Kinesis giúp bạn dễ dàng collect, process, và analyze real-time streaming data để có thể react nhanh chóng và make informed decisions từ incoming information. Platform này bao gồm nhiều services khác nhau để handle different aspects của streaming data pipeline.

## Chức năng chính

### 1. Real-time Data Streaming
- **High Throughput**: Xử lý terabytes of data per hour
- **Low Latency**: Sub-second processing latency
- **Scalable**: Auto-scale theo data volume
- **Durable**: Reliable data delivery và storage

### 2. Multiple Service Options
- **Kinesis Data Streams**: Core streaming platform
- **Kinesis Data Firehose**: Managed data delivery
- **Kinesis Data Analytics**: Real-time analytics
- **Kinesis Video Streams**: Video streaming platform

### 3. Processing Flexibility
- **Real-time Processing**: Immediate data processing
- **Batch Processing**: Scheduled data processing
- **Stream Analytics**: SQL-based analytics
- **Custom Applications**: SDK-based development

### 4. Integration Ecosystem
- **AWS Services**: Native integration với AWS services
- **Third-party Tools**: Integration với external tools
- **APIs và SDKs**: Comprehensive development support
- **Monitoring**: Built-in monitoring và alerting

## Use Cases phổ biến

1. **Real-time Analytics**: Live dashboards và metrics
2. **IoT Data Processing**: Sensor data streams
3. **Log Aggregation**: Centralized logging
4. **Fraud Detection**: Real-time fraud prevention
5. **Clickstream Analysis**: User behavior tracking

## Diagram Architecture

Kiến trúc tổng quan Amazon Kinesis ecosystem:

![Amazon Kinesis Architecture](/img/aws-analytics/kinesis.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Kinesis, KinesisDataStreams, KinesisDataFirehose, KinesisDataAnalytics, KinesisVideoStreams
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.database import Dynamodb, RDS, Redshift
from diagrams.aws.ml import Rekognition, SagemakerModel
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.iot import IotSensor

with Diagram("Amazon Kinesis Architecture", show=False, direction="TB"):
    
    users = Users("Applications & Users")
    
    with Cluster("Data Sources"):
        web_apps = Lambda("Web Applications")
        mobile_apps = Lambda("Mobile Apps")
        iot_devices = IotSensor("IoT Devices")
        databases = RDS("Databases")
        video_sources = Lambda("Video Sources")
    
    with Cluster("Amazon Kinesis Platform"):
        kinesis_platform = Kinesis("Amazon Kinesis")
        
        with Cluster("Kinesis Services"):
            data_streams = KinesisDataStreams("Data Streams")
            data_firehose = KinesisDataFirehose("Data Firehose")
            data_analytics = KinesisDataAnalytics("Data Analytics")
            video_streams = KinesisVideoStreams("Video Streams")
    
    with Cluster("Stream Processing"):
        lambda_processor = Lambda("Lambda Functions")
        custom_apps = EC2("Custom Applications")
        analytics_apps = Lambda("Analytics Apps")
        ml_inference = SagemakerModel("ML Inference")
    
    with Cluster("Data Destinations"):
        s3_data_lake = S3("Data Lake")
        redshift_dw = Redshift("Data Warehouse")
        dynamodb_table = Dynamodb("Real-time DB")
        opensearch = Lambda("OpenSearch")
    
    with Cluster("Analytics & Insights"):
        real_time_dashboard = Lambda("Real-time Dashboards")
        bi_tools = Lambda("BI Tools")
        ml_models = SagemakerModel("ML Models")
        alerts = SNS("Alert System")
    
    with Cluster("Video Processing"):
        rekognition = Rekognition("Video Analysis")
        video_archive = S3("Video Archive")
        live_streaming = Lambda("Live Streaming")
    
    with Cluster("Monitoring & Management"):
        cloudwatch = Cloudwatch("CloudWatch")
        security = IAM("IAM & Security")
    
    # Data ingestion
    web_apps >> Edge(label="Events") >> data_streams
    mobile_apps >> Edge(label="Analytics") >> data_streams
    iot_devices >> Edge(label="Sensor Data") >> data_streams
    databases >> Edge(label="CDC") >> data_streams
    video_sources >> Edge(label="Video Feed") >> video_streams
    
    # Kinesis platform
    kinesis_platform >> data_streams
    kinesis_platform >> data_firehose
    kinesis_platform >> data_analytics
    kinesis_platform >> video_streams
    
    # Stream processing
    data_streams >> lambda_processor
    data_streams >> custom_apps
    data_analytics >> analytics_apps
    video_streams >> rekognition
    
    # Data delivery
    data_firehose >> s3_data_lake
    data_firehose >> redshift_dw
    lambda_processor >> dynamodb_table
    analytics_apps >> opensearch
    
    # Analytics and insights
    dynamodb_table >> real_time_dashboard
    s3_data_lake >> bi_tools
    opensearch >> ml_models
    rekognition >> alerts
    
    # Video processing
    video_streams >> video_archive
    video_streams >> live_streaming
    
    # User interaction
    users >> Edge(label="View Analytics") >> real_time_dashboard
    users >> Edge(label="BI Reports") >> bi_tools
    users >> Edge(label="Live Video") >> live_streaming
    
    # Monitoring
    kinesis_platform >> cloudwatch
    security >> kinesis_platform
```

## Kinesis Services Overview

### 1. Kinesis Data Streams
```python
# Core streaming service for real-time data
class KinesisDataStreamsManager:
    def __init__(self):
        self.kinesis = boto3.client('kinesis')
    
    def create_stream_architecture(self, stream_config):
        """Create complete streaming architecture"""
        
        # Create main data stream
        main_stream = self.kinesis.create_stream(
            StreamName=stream_config['name'],
            ShardCount=stream_config['shard_count']
        )
        
        # Create consumer applications
        consumers = []
        for consumer_config in stream_config['consumers']:
            consumer = self.create_consumer_application(
                stream_config['name'],
                consumer_config
            )
            consumers.append(consumer)
        
        return {
            'stream': main_stream,
            'consumers': consumers
        }
    
    def create_consumer_application(self, stream_name, consumer_config):
        """Create consumer application"""
        
        if consumer_config['type'] == 'lambda':
            return self.create_lambda_consumer(stream_name, consumer_config)
        elif consumer_config['type'] == 'kcl':
            return self.create_kcl_consumer(stream_name, consumer_config)
        elif consumer_config['type'] == 'kda':
            return self.create_kda_consumer(stream_name, consumer_config)
```

### 2. Kinesis Data Firehose
```python
# Managed delivery service
class KinesisDataFirehoseManager:
    def __init__(self):
        self.firehose = boto3.client('firehose')
    
    def create_delivery_pipeline(self, pipeline_config):
        """Create complete delivery pipeline"""
        
        pipelines = []
        
        for destination in pipeline_config['destinations']:
            if destination['type'] == 's3':
                pipeline = self.create_s3_delivery_stream(destination)
            elif destination['type'] == 'redshift':
                pipeline = self.create_redshift_delivery_stream(destination)
            elif destination['type'] == 'opensearch':
                pipeline = self.create_opensearch_delivery_stream(destination)
            
            pipelines.append(pipeline)
        
        return pipelines
    
    def create_s3_delivery_stream(self, config):
        """Create S3 delivery stream with transformation"""
        
        return self.firehose.create_delivery_stream(
            DeliveryStreamName=config['name'],
            DeliveryStreamType='DirectPut',
            ExtendedS3DestinationConfiguration={
                'RoleARN': config['role_arn'],
                'BucketARN': config['bucket_arn'],
                'Prefix': config.get('prefix', ''),
                'BufferingHints': {
                    'SizeInMBs': config.get('buffer_size', 5),
                    'IntervalInSeconds': config.get('buffer_interval', 300)
                },
                'CompressionFormat': config.get('compression', 'GZIP'),
                'ProcessingConfiguration': {
                    'Enabled': True,
                    'Processors': [
                        {
                            'Type': 'Lambda',
                            'Parameters': [
                                {
                                    'ParameterName': 'LambdaArn',
                                    'ParameterValue': config['transform_lambda_arn']
                                }
                            ]
                        }
                    ]
                } if config.get('transform_lambda_arn') else {'Enabled': False}
            }
        )
```

### 3. Kinesis Data Analytics
```python
# Real-time analytics service
class KinesisDataAnalyticsManager:
    def __init__(self):
        self.kda = boto3.client('kinesisanalyticsv2')
    
    def create_analytics_application(self, app_config):
        """Create Kinesis Data Analytics application"""
        
        if app_config['runtime'] == 'SQL':
            return self.create_sql_application(app_config)
        elif app_config['runtime'] == 'FLINK':
            return self.create_flink_application(app_config)
    
    def create_sql_application(self, config):
        """Create SQL-based analytics application"""
        
        return self.kda.create_application(
            ApplicationName=config['name'],
            ApplicationDescription=config['description'],
            RuntimeEnvironment='SQL-1_0',
            ServiceExecutionRole=config['service_role'],
            ApplicationConfiguration={
                'SqlApplicationConfiguration': {
                    'Inputs': [
                        {
                            'NamePrefix': 'SOURCE_SQL_STREAM',
                            'KinesisStreamsInput': {
                                'ResourceARN': config['input_stream_arn']
                            },
                            'InputSchema': {
                                'RecordFormat': {
                                    'RecordFormatType': 'JSON',
                                    'MappingParameters': {
                                        'JSONMappingParameters': {
                                            'RecordRowPath': '$'
                                        }
                                    }
                                },
                                'RecordColumns': config['input_schema']
                            }
                        }
                    ],
                    'Outputs': [
                        {
                            'Name': 'DESTINATION_SQL_STREAM',
                            'KinesisStreamsOutput': {
                                'ResourceARN': config['output_stream_arn']
                            },
                            'DestinationSchema': {
                                'RecordFormatType': 'JSON'
                            }
                        }
                    ]
                }
            }
        )
    
    def create_flink_application(self, config):
        """Create Flink-based analytics application"""
        
        return self.kda.create_application(
            ApplicationName=config['name'],
            RuntimeEnvironment='FLINK-1_15',
            ServiceExecutionRole=config['service_role'],
            ApplicationConfiguration={
                'FlinkApplicationConfiguration': {
                    'CheckpointConfiguration': {
                        'ConfigurationType': 'CUSTOM',
                        'CheckpointingEnabled': True,
                        'CheckpointInterval': 60000,
                        'MinPauseBetweenCheckpoints': 5000
                    },
                    'MonitoringConfiguration': {
                        'ConfigurationType': 'CUSTOM',
                        'MetricsLevel': 'APPLICATION',
                        'LogLevel': 'INFO'
                    },
                    'ParallelismConfiguration': {
                        'ConfigurationType': 'CUSTOM',
                        'Parallelism': config.get('parallelism', 1),
                        'ParallelismPerKPU': 1,
                        'AutoScalingEnabled': True
                    }
                },
                'ApplicationCodeConfiguration': {
                    'CodeContent': {
                        'S3ContentLocation': {
                            'BucketARN': config['code_bucket_arn'],
                            'FileKey': config['code_file_key']
                        }
                    },
                    'CodeContentType': 'ZIPFILE'
                }
            }
        )
```

### 4. Kinesis Video Streams
```python
# Video streaming service
class KinesisVideoStreamsManager:
    def __init__(self):
        self.kvs = boto3.client('kinesisvideo')
    
    def create_video_analytics_pipeline(self, pipeline_config):
        """Create complete video analytics pipeline"""
        
        # Create video stream
        stream = self.kvs.create_stream(
            StreamName=pipeline_config['stream_name'],
            DataRetentionInHours=pipeline_config.get('retention_hours', 24),
            MediaType='video/h264'
        )
        
        # Set up video analysis
        if pipeline_config.get('enable_rekognition'):
            self.setup_rekognition_analysis(
                pipeline_config['stream_name'],
                pipeline_config['rekognition_config']
            )
        
        # Set up custom processing
        if pipeline_config.get('custom_processor_lambda'):
            self.setup_custom_processing(
                pipeline_config['stream_name'],
                pipeline_config['custom_processor_lambda']
            )
        
        return stream
    
    def setup_rekognition_analysis(self, stream_name, rekognition_config):
        """Set up Rekognition video analysis"""
        
        rekognition = boto3.client('rekognition')
        
        # Start face detection
        if rekognition_config.get('face_detection'):
            rekognition.start_face_detection(
                Video={
                    'KinesisVideoStream': {
                        'Arn': f'arn:aws:kinesisvideo:region:account:stream/{stream_name}'
                    }
                },
                NotificationChannel={
                    'SNSTopicArn': rekognition_config['sns_topic_arn'],
                    'RoleArn': rekognition_config['service_role_arn']
                }
            )
        
        # Start label detection
        if rekognition_config.get('label_detection'):
            rekognition.start_label_detection(
                Video={
                    'KinesisVideoStream': {
                        'Arn': f'arn:aws:kinesisvideo:region:account:stream/{stream_name}'
                    }
                },
                MinConfidence=rekognition_config.get('min_confidence', 80),
                NotificationChannel={
                    'SNSTopicArn': rekognition_config['sns_topic_arn'],
                    'RoleArn': rekognition_config['service_role_arn']
                }
            )
```

## End-to-End Pipeline Implementation

### 1. Complete Streaming Pipeline
```python
class KinesisStreamingPipeline:
    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.kinesis = boto3.client('kinesis')
        self.firehose = boto3.client('firehose')
        self.kda = boto3.client('kinesisanalyticsv2')
        
    def deploy_complete_pipeline(self, config):
        """Deploy complete streaming pipeline"""
        
        pipeline_resources = {}
        
        # 1. Create data streams
        if config.get('data_streams'):
            pipeline_resources['data_streams'] = self.create_data_streams(
                config['data_streams']
            )
        
        # 2. Create analytics applications
        if config.get('analytics_apps'):
            pipeline_resources['analytics_apps'] = self.create_analytics_apps(
                config['analytics_apps']
            )
        
        # 3. Create delivery streams
        if config.get('delivery_streams'):
            pipeline_resources['delivery_streams'] = self.create_delivery_streams(
                config['delivery_streams']
            )
        
        # 4. Set up monitoring
        pipeline_resources['monitoring'] = self.setup_monitoring(config)
        
        # 5. Configure auto-scaling
        if config.get('auto_scaling'):
            pipeline_resources['auto_scaling'] = self.setup_auto_scaling(
                config['auto_scaling']
            )
        
        return pipeline_resources
    
    def create_data_streams(self, streams_config):
        """Create multiple data streams"""
        
        streams = {}
        
        for stream_config in streams_config:
            stream = self.kinesis.create_stream(
                StreamName=f"{self.pipeline_name}-{stream_config['name']}",
                ShardCount=stream_config['shard_count']
            )
            
            # Configure retention
            if stream_config.get('retention_hours'):
                self.kinesis.increase_stream_retention_period(
                    StreamName=f"{self.pipeline_name}-{stream_config['name']}",
                    RetentionPeriodHours=stream_config['retention_hours']
                )
            
            # Enable encryption
            if stream_config.get('encryption_key'):
                self.kinesis.enable_stream_encryption(
                    StreamName=f"{self.pipeline_name}-{stream_config['name']}",
                    EncryptionType='KMS',
                    KeyId=stream_config['encryption_key']
                )
            
            streams[stream_config['name']] = stream
        
        return streams
    
    def setup_monitoring(self, config):
        """Set up comprehensive monitoring"""
        
        cloudwatch = boto3.client('cloudwatch')
        
        # Create custom dashboard
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/Kinesis", "IncomingRecords", "StreamName", f"{self.pipeline_name}-main"],
                            [".", "IncomingBytes", ".", "."],
                            [".", "OutgoingRecords", ".", "."]
                        ],
                        "period": 300,
                        "stat": "Sum",
                        "region": "us-west-2",
                        "title": "Stream Throughput"
                    }
                },
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/KinesisFirehose", "DeliveryToS3.Success", "DeliveryStreamName", f"{self.pipeline_name}-delivery"],
                            [".", "DeliveryToS3.DataFreshness", ".", "."]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": "us-west-2",
                        "title": "Delivery Performance"
                    }
                }
            ]
        }
        
        cloudwatch.put_dashboard(
            DashboardName=f'{self.pipeline_name}-monitoring',
            DashboardBody=json.dumps(dashboard_body)
        )
        
        # Create alarms
        alarms = [
            {
                'AlarmName': f'{self.pipeline_name}-high-incoming-records',
                'MetricName': 'IncomingRecords',
                'Threshold': 10000,
                'ComparisonOperator': 'GreaterThanThreshold'
            },
            {
                'AlarmName': f'{self.pipeline_name}-delivery-failures',
                'MetricName': 'DeliveryToS3.Success',
                'Threshold': 0.95,
                'ComparisonOperator': 'LessThanThreshold'
            }
        ]
        
        for alarm in alarms:
            cloudwatch.put_metric_alarm(
                AlarmName=alarm['AlarmName'],
                ComparisonOperator=alarm['ComparisonOperator'],
                EvaluationPeriods=2,
                MetricName=alarm['MetricName'],
                Namespace='AWS/Kinesis',
                Period=300,
                Statistic='Average',
                Threshold=alarm['Threshold'],
                ActionsEnabled=True,
                AlarmActions=[
                    config.get('sns_topic_arn', 'arn:aws:sns:region:account:kinesis-alerts')
                ]
            )
        
        return {'dashboard': f'{self.pipeline_name}-monitoring', 'alarms': alarms}
```

## Cost Optimization Strategies

### 1. Multi-Service Cost Analysis
```python
class KinesisCostOptimizer:
    def __init__(self):
        self.ce = boto3.client('ce')
        self.cloudwatch = boto3.client('cloudwatch')
    
    def analyze_kinesis_costs(self, start_date, end_date):
        """Analyze costs across all Kinesis services"""
        
        # Get cost breakdown by service
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
                    'Values': [
                        'Amazon Kinesis',
                        'Amazon Kinesis Analytics',
                        'Amazon Kinesis Firehose',
                        'Amazon Kinesis Video Streams'
                    ]
                }
            }
        )
        
        cost_breakdown = {}
        for result in response['ResultsByTime']:
            date = result['TimePeriod']['Start']
            cost_breakdown[date] = {}
            
            for group in result['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                cost_breakdown[date][service] = cost
        
        return cost_breakdown
    
    def optimize_shard_count(self, stream_name):
        """Optimize shard count based on usage patterns"""
        
        # Get stream metrics
        metrics = self.get_stream_utilization_metrics(stream_name)
        
        # Calculate optimal shard count
        avg_throughput_mb = metrics['avg_incoming_bytes'] / (1024 * 1024)  # Convert to MB
        avg_records_per_sec = metrics['avg_incoming_records'] / 60  # Convert to per second
        
        # Each shard can handle 1MB/sec or 1000 records/sec
        shards_needed_for_bytes = math.ceil(avg_throughput_mb)
        shards_needed_for_records = math.ceil(avg_records_per_sec / 1000)
        
        optimal_shards = max(shards_needed_for_bytes, shards_needed_for_records)
        
        # Add 20% buffer for spikes
        recommended_shards = math.ceil(optimal_shards * 1.2)
        
        return {
            'current_metrics': metrics,
            'optimal_shards': optimal_shards,
            'recommended_shards': recommended_shards,
            'potential_savings': self.calculate_shard_savings(
                metrics['current_shards'], 
                recommended_shards
            )
        }
    
    def recommend_on_demand_vs_provisioned(self, stream_usage_pattern):
        """Recommend between on-demand and provisioned capacity"""
        
        # Calculate costs for both models
        provisioned_cost = self.calculate_provisioned_cost(stream_usage_pattern)
        on_demand_cost = self.calculate_on_demand_cost(stream_usage_pattern)
        
        recommendation = {
            'provisioned_cost': provisioned_cost,
            'on_demand_cost': on_demand_cost,
            'recommended_mode': 'on-demand' if on_demand_cost < provisioned_cost else 'provisioned',
            'potential_savings': abs(provisioned_cost - on_demand_cost),
            'reasoning': self.generate_recommendation_reasoning(
                stream_usage_pattern, provisioned_cost, on_demand_cost
            )
        }
        
        return recommendation
```

## Best Practices

1. **Service Selection**: Chọn Kinesis service phù hợp cho use case
2. **Capacity Planning**: Right-size shards và throughput
3. **Cost Optimization**: Monitor và optimize costs regularly
4. **Security**: Implement encryption và proper IAM roles
5. **Monitoring**: Set up comprehensive monitoring
6. **Error Handling**: Implement robust error handling
7. **Data Retention**: Set appropriate retention periods
8. **Integration**: Leverage AWS ecosystem effectively

## Tích hợp với các dịch vụ AWS khác

- **AWS Lambda**: Serverless processing
- **Amazon S3**: Data storage và archival
- **Amazon DynamoDB**: Real-time data storage
- **Amazon Redshift**: Data warehousing
- **Amazon OpenSearch**: Search và analytics
- **Amazon SageMaker**: Machine learning
- **Amazon Rekognition**: Video analysis
- **Amazon CloudWatch**: Monitoring và alerting
- **AWS IAM**: Security và access control
- **Amazon VPC**: Network isolation
- **AWS Glue**: Data catalog và ETL
- **Amazon SNS**: Notifications
