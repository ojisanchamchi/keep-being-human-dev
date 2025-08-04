# Amazon Kinesis Data Analytics

## Tổng quan

Amazon Kinesis Data Analytics là node đại diện cho dịch vụ phân tích dữ liệu streaming real-time của AWS. Dịch vụ này cho phép bạn xử lý và phân tích streaming data bằng SQL hoặc Apache Flink, cung cấp khả năng tạo insights từ dữ liệu đang chuyển động mà không cần quản lý infrastructure phức tạp.

## Chức năng chính

### 1. Real-time Stream Processing
- **SQL Queries**: Xử lý streaming data bằng SQL chuẩn
- **Apache Flink**: Advanced stream processing với Flink applications
- **Windowing Functions**: Time-based và count-based windows
- **Pattern Detection**: Phát hiện patterns trong streaming data

### 2. Multiple Runtime Environments
- **SQL Runtime**: Serverless SQL-based analytics
- **Apache Flink Runtime**: Java/Scala applications với Flink
- **Apache Beam**: Portable data processing pipelines
- **Managed Scaling**: Tự động scale based on throughput

### 3. Data Sources Integration
- **Kinesis Data Streams**: Direct integration với data streams
- **Kinesis Data Firehose**: Processed data delivery
- **Amazon MSK**: Apache Kafka integration
- **Reference Data**: Static data joins từ S3

### 4. Output Destinations
- **Real-time Dashboards**: Live analytics dashboards
- **Data Lakes**: Processed data to S3
- **Databases**: Results to RDS, DynamoDB
- **Alerting Systems**: Notifications via SNS, Lambda

## Use Cases phổ biến

1. **Real-time Fraud Detection**: Phát hiện gian lận tức thời
2. **IoT Analytics**: Phân tích dữ liệu IoT real-time
3. **Clickstream Analysis**: Phân tích hành vi người dùng
4. **Log Analytics**: Xử lý và phân tích logs real-time
5. **Financial Trading**: Real-time market data analysis

## Diagram Architecture

Kiến trúc Amazon Kinesis Data Analytics với real-time processing:

![Amazon Kinesis Data Analytics Architecture](/img/aws-analytics/kinesis-data-analytics.png)

### Code để tạo diagram:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import KinesisDataAnalytics, KinesisDataStreams, KinesisDataFirehose
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.onprem.analytics import Flink

with Diagram("Amazon Kinesis Data Analytics Architecture", show=False, direction="TB"):
    
    users = Users("Business Users")
    
    with Cluster("Data Sources"):
        web_apps = Lambda("Web Applications")
        mobile_apps = Lambda("Mobile Apps")
        iot_devices = Lambda("IoT Devices")
        log_sources = Lambda("Log Sources")
    
    with Cluster("Streaming Ingestion"):
        data_streams = KinesisDataStreams("Kinesis Data Streams")
        firehose = KinesisDataFirehose("Kinesis Data Firehose")
        kafka_source = SQS("Apache Kafka/MSK")
    
    with Cluster("Stream Processing"):
        analytics_app = KinesisDataAnalytics("Kinesis Data Analytics")
        
        with Cluster("Processing Engines"):
            sql_runtime = KinesisDataAnalytics("SQL Runtime")
            flink_runtime = Flink("Flink Runtime")
            beam_runtime = Lambda("Beam Runtime")
    
    with Cluster("Reference Data"):
        s3_reference = S3("Reference Data")
        lookup_tables = Dynamodb("Lookup Tables")
    
    with Cluster("Real-time Outputs"):
        real_time_dashboard = Lambda("Real-time Dashboard")
        alerts = SNS("Real-time Alerts")
        lambda_functions = Lambda("Lambda Functions")
        kinesis_output = KinesisDataStreams("Output Streams")
    
    with Cluster("Batch Outputs"):
        s3_results = S3("Analytics Results")
        data_warehouse = RDS("Data Warehouse")
        firehose_output = KinesisDataFirehose("Delivery Streams")
    
    with Cluster("Monitoring & Management"):
        cloudwatch = Cloudwatch("CloudWatch")
        security = IAM("IAM Roles")
    
    # Data ingestion flow
    web_apps >> Edge(label="Events") >> data_streams
    mobile_apps >> Edge(label="Analytics") >> data_streams
    iot_devices >> Edge(label="Sensor Data") >> data_streams
    log_sources >> Edge(label="Logs") >> firehose
    
    # Stream processing input
    data_streams >> Edge(label="Stream Data") >> analytics_app
    firehose >> Edge(label="Buffered Data") >> analytics_app
    kafka_source >> Edge(label="Kafka Topics") >> analytics_app
    
    # Processing engines
    analytics_app >> sql_runtime
    analytics_app >> flink_runtime
    analytics_app >> beam_runtime
    
    # Reference data joins
    s3_reference >> Edge(label="Static Data") >> analytics_app
    lookup_tables >> Edge(label="Lookups") >> analytics_app
    
    # Real-time outputs
    sql_runtime >> real_time_dashboard
    flink_runtime >> alerts
    beam_runtime >> lambda_functions
    analytics_app >> kinesis_output
    
    # Batch outputs
    analytics_app >> firehose_output >> s3_results
    analytics_app >> Edge(label="Aggregated Results") >> data_warehouse
    
    # User interaction
    users >> Edge(label="View Dashboards") >> real_time_dashboard
    users >> Edge(label="Receive Alerts") >> alerts
    
    # Monitoring and security
    analytics_app >> Edge(label="Metrics") >> cloudwatch
    security >> Edge(label="Access Control") >> analytics_app
```

## SQL-based Analytics

### 1. Stream Processing với SQL
```sql
-- Real-time fraud detection
CREATE STREAM fraud_detection_stream (
    transaction_id VARCHAR(50),
    user_id VARCHAR(50),
    amount DECIMAL(10,2),
    merchant_category VARCHAR(20),
    location VARCHAR(100),
    timestamp TIMESTAMP,
    ROWTIME TIMESTAMP
);

-- Detect suspicious patterns
CREATE STREAM suspicious_transactions AS
SELECT 
    user_id,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    ROWTIME_RANGE_START as window_start,
    ROWTIME_RANGE_END as window_end
FROM SOURCE_SQL_STREAM_001
WHERE amount > 1000
GROUP BY 
    user_id,
    RANGE_INTERVAL '5' MINUTE;

-- Alert on anomalies
CREATE STREAM fraud_alerts AS
SELECT 
    user_id,
    transaction_count,
    total_amount,
    'HIGH_VELOCITY' as alert_type,
    window_start
FROM suspicious_transactions
WHERE transaction_count > 10 
   OR total_amount > 50000;
```

### 2. Windowing Functions
```sql
-- Tumbling window (non-overlapping)
CREATE STREAM hourly_metrics AS
SELECT 
    merchant_category,
    COUNT(*) as transaction_count,
    SUM(amount) as total_revenue,
    AVG(amount) as avg_transaction_size,
    ROWTIME_RANGE_START as hour_start
FROM SOURCE_SQL_STREAM_001
GROUP BY 
    merchant_category,
    RANGE_INTERVAL '1' HOUR;

-- Sliding window (overlapping)
CREATE STREAM sliding_averages AS
SELECT 
    user_id,
    AVG(amount) as moving_avg_5min,
    COUNT(*) as transaction_count_5min,
    ROWTIME as event_time
FROM SOURCE_SQL_STREAM_001
GROUP BY 
    user_id,
    RANGE_INTERVAL '5' MINUTE PRECEDING;

-- Session window (gap-based)
CREATE STREAM user_sessions AS
SELECT 
    user_id,
    COUNT(*) as actions_in_session,
    MIN(ROWTIME) as session_start,
    MAX(ROWTIME) as session_end,
    (MAX(ROWTIME) - MIN(ROWTIME)) MINUTE as session_duration
FROM SOURCE_SQL_STREAM_001
GROUP BY 
    user_id,
    SESSION_INTERVAL '30' MINUTE;
```

### 3. Reference Data Joins
```sql
-- Join streaming data with reference data
CREATE STREAM enriched_transactions AS
SELECT 
    t.transaction_id,
    t.user_id,
    t.amount,
    t.merchant_category,
    u.user_tier,
    u.risk_score,
    u.registration_date,
    CASE 
        WHEN u.user_tier = 'PREMIUM' AND t.amount > u.daily_limit THEN 'REVIEW'
        WHEN u.risk_score > 0.8 THEN 'HIGH_RISK'
        ELSE 'NORMAL'
    END as transaction_status
FROM SOURCE_SQL_STREAM_001 t
LEFT JOIN "USER_REFERENCE_DATA" u
ON t.user_id = u.user_id;
```

## Apache Flink Applications

### 1. Flink DataStream API
```java
// Flink application for complex event processing
public class FraudDetectionApp {
    
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Configure checkpointing
        env.enableCheckpointing(60000);
        env.getCheckpointConfig().setCheckpointingMode(CheckpointingMode.EXACTLY_ONCE);
        
        // Read from Kinesis Data Streams
        Properties kinesisProps = new Properties();
        kinesisProps.setProperty(ConsumerConfigConstants.AWS_REGION, "us-west-2");
        kinesisProps.setProperty(ConsumerConfigConstants.STREAM_INITIAL_POSITION, "LATEST");
        
        DataStream<Transaction> transactions = env
            .addSource(new FlinkKinesisConsumer<>("transaction-stream", 
                                                 new TransactionDeserializer(), 
                                                 kinesisProps))
            .assignTimestampsAndWatermarks(
                WatermarkStrategy.<Transaction>forBoundedOutOfOrderness(Duration.ofSeconds(10))
                    .withTimestampAssigner((transaction, timestamp) -> transaction.getTimestamp())
            );
        
        // Fraud detection logic
        DataStream<FraudAlert> alerts = transactions
            .keyBy(Transaction::getUserId)
            .process(new FraudDetectionFunction())
            .filter(alert -> alert.getRiskScore() > 0.8);
        
        // Output to multiple sinks
        alerts.addSink(new FlinkKinesisProducer<>("fraud-alerts-stream", 
                                                 new AlertSerializer(), 
                                                 kinesisProps));
        
        alerts.addSink(new DynamoDBSink<>("fraud-alerts-table"));
        
        env.execute("Real-time Fraud Detection");
    }
}

// Custom process function for fraud detection
public class FraudDetectionFunction extends KeyedProcessFunction<String, Transaction, FraudAlert> {
    
    private ValueState<TransactionProfile> profileState;
    private MapState<Long, Integer> hourlyCountState;
    
    @Override
    public void open(Configuration parameters) {
        profileState = getRuntimeContext().getState(
            new ValueStateDescriptor<>("profile", TransactionProfile.class)
        );
        
        hourlyCountState = getRuntimeContext().getMapState(
            new MapStateDescriptor<>("hourly-count", Long.class, Integer.class)
        );
    }
    
    @Override
    public void processElement(Transaction transaction, Context ctx, Collector<FraudAlert> out) 
            throws Exception {
        
        TransactionProfile profile = profileState.value();
        if (profile == null) {
            profile = new TransactionProfile();
        }
        
        // Update profile with new transaction
        profile.updateWith(transaction);
        profileState.update(profile);
        
        // Check for velocity-based fraud
        long hourWindow = transaction.getTimestamp() / (60 * 60 * 1000);
        Integer hourlyCount = hourlyCountState.get(hourWindow);
        hourlyCount = (hourlyCount == null) ? 1 : hourlyCount + 1;
        hourlyCountState.put(hourWindow, hourlyCount);
        
        // Generate alert if suspicious
        if (hourlyCount > 50 || transaction.getAmount() > profile.getAverageAmount() * 10) {
            FraudAlert alert = new FraudAlert(
                transaction.getUserId(),
                transaction.getTransactionId(),
                calculateRiskScore(transaction, profile, hourlyCount),
                "VELOCITY_FRAUD",
                System.currentTimeMillis()
            );
            out.collect(alert);
        }
        
        // Clean up old hourly counts
        cleanupOldCounts(ctx.timestamp());
    }
    
    private double calculateRiskScore(Transaction transaction, TransactionProfile profile, int hourlyCount) {
        double velocityScore = Math.min(hourlyCount / 50.0, 1.0);
        double amountScore = Math.min(transaction.getAmount() / profile.getMaxAmount(), 1.0);
        double locationScore = profile.isNewLocation(transaction.getLocation()) ? 0.5 : 0.0;
        
        return (velocityScore * 0.4) + (amountScore * 0.4) + (locationScore * 0.2);
    }
}
```

### 2. Complex Event Processing (CEP)
```java
// Pattern detection with Flink CEP
import org.apache.flink.cep.CEP;
import org.apache.flink.cep.PatternStream;
import org.apache.flink.cep.pattern.Pattern;
import org.apache.flink.cep.pattern.conditions.SimpleCondition;

public class PatternDetectionApp {
    
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        DataStream<LoginEvent> loginEvents = env
            .addSource(new FlinkKinesisConsumer<>("login-events", 
                                                 new LoginEventDeserializer(), 
                                                 kinesisProps));
        
        // Define suspicious login pattern
        Pattern<LoginEvent, ?> suspiciousPattern = Pattern.<LoginEvent>begin("first")
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.getStatus().equals("FAILED");
                }
            })
            .next("second")
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.getStatus().equals("FAILED");
                }
            })
            .next("third")
            .where(new SimpleCondition<LoginEvent>() {
                @Override
                public boolean filter(LoginEvent event) {
                    return event.getStatus().equals("SUCCESS");
                }
            })
            .within(Time.minutes(5));
        
        // Apply pattern to stream
        PatternStream<LoginEvent> patternStream = CEP.pattern(
            loginEvents.keyBy(LoginEvent::getUserId),
            suspiciousPattern
        );
        
        // Extract matches and generate alerts
        DataStream<SecurityAlert> alerts = patternStream.select(
            (Map<String, List<LoginEvent>> pattern) -> {
                List<LoginEvent> firstEvents = pattern.get("first");
                List<LoginEvent> thirdEvents = pattern.get("third");
                
                return new SecurityAlert(
                    firstEvents.get(0).getUserId(),
                    "BRUTE_FORCE_ATTEMPT",
                    "Multiple failed logins followed by success",
                    System.currentTimeMillis()
                );
            }
        );
        
        alerts.addSink(new SecurityAlertSink());
        
        env.execute("Login Pattern Detection");
    }
}
```

## Performance Optimization

### 1. Application Scaling
```java
// Auto-scaling configuration
public class ScalingConfiguration {
    
    public static void configureAutoScaling(StreamExecutionEnvironment env) {
        // Set parallelism based on throughput
        env.setParallelism(4);
        
        // Configure memory
        Configuration config = new Configuration();
        config.setString("taskmanager.memory.process.size", "2g");
        config.setString("taskmanager.memory.flink.size", "1.5g");
        
        // Optimize checkpointing
        env.enableCheckpointing(30000); // 30 seconds
        env.getCheckpointConfig().setMinPauseBetweenCheckpoints(10000);
        env.getCheckpointConfig().setCheckpointTimeout(60000);
        env.getCheckpointConfig().setMaxConcurrentCheckpoints(1);
        
        // Configure state backend
        env.setStateBackend(new RocksDBStateBackend("s3://checkpoints/flink/"));
    }
}
```

### 2. SQL Query Optimization
```sql
-- Optimized aggregation query
CREATE STREAM optimized_metrics AS
SELECT 
    merchant_id,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    -- Use approximate functions for better performance
    APPROX_COUNT_DISTINCT(user_id) as unique_users,
    ROWTIME_RANGE_START as window_start
FROM SOURCE_SQL_STREAM_001
-- Filter early to reduce processing
WHERE amount > 0 AND merchant_id IS NOT NULL
GROUP BY 
    merchant_id,
    -- Use smaller windows for lower latency
    RANGE_INTERVAL '1' MINUTE;

-- Partitioned processing for high throughput
CREATE STREAM partitioned_processing AS
SELECT 
    partition_key,
    event_type,
    COUNT(*) as event_count,
    AVG(processing_time) as avg_processing_time
FROM (
    SELECT 
        MOD(ABS(HASH_CODE(user_id)), 10) as partition_key,
        event_type,
        (ROWTIME - event_timestamp) SECOND as processing_time,
        ROWTIME
    FROM SOURCE_SQL_STREAM_001
)
GROUP BY 
    partition_key,
    event_type,
    RANGE_INTERVAL '30' SECOND;
```

## Monitoring và Troubleshooting

### 1. Application Metrics
```python
import boto3
import json

class KinesisAnalyticsMonitor:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.kinesisanalytics = boto3.client('kinesisanalyticsv2')
    
    def get_application_metrics(self, application_name, start_time, end_time):
        """Get comprehensive application metrics"""
        
        metrics = [
            'inputProcessing.DroppedRecords',
            'inputProcessing.ProcessedRecords',
            'inputProcessing.ProcessedBytes',
            'outputDelivery.DeliveredRecords',
            'outputDelivery.DeliveryDelay',
            'kpu.utilization',
            'downtime',
            'uptime'
        ]
        
        results = {}
        
        for metric in metrics:
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/KinesisAnalytics',
                MetricName=metric,
                Dimensions=[
                    {
                        'Name': 'Application',
                        'Value': application_name
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum', 'Sum']
            )
            
            results[metric] = response['Datapoints']
        
        return results
    
    def check_application_health(self, application_name):
        """Check application health and performance"""
        
        response = self.kinesisanalytics.describe_application(
            ApplicationName=application_name
        )
        
        app_detail = response['ApplicationDetail']
        
        health_check = {
            'application_name': application_name,
            'status': app_detail['ApplicationStatus'],
            'version': app_detail['ApplicationVersionId'],
            'runtime_environment': app_detail['RuntimeEnvironment'],
            'last_update': app_detail['LastUpdateTimestamp'].isoformat(),
            'issues': []
        }
        
        # Check for common issues
        if app_detail['ApplicationStatus'] != 'RUNNING':
            health_check['issues'].append(f"Application not running: {app_detail['ApplicationStatus']}")
        
        # Check KPU utilization
        kpu_metrics = self.get_recent_kpu_utilization(application_name)
        if kpu_metrics and kpu_metrics > 80:
            health_check['issues'].append(f"High KPU utilization: {kpu_metrics}%")
        
        return health_check
    
    def create_custom_alarms(self, application_name):
        """Create CloudWatch alarms for the application"""
        
        alarms = [
            {
                'AlarmName': f'{application_name}-high-error-rate',
                'MetricName': 'inputProcessing.DroppedRecords',
                'Threshold': 100,
                'ComparisonOperator': 'GreaterThanThreshold'
            },
            {
                'AlarmName': f'{application_name}-high-kpu-utilization',
                'MetricName': 'kpu.utilization',
                'Threshold': 80,
                'ComparisonOperator': 'GreaterThanThreshold'
            },
            {
                'AlarmName': f'{application_name}-application-downtime',
                'MetricName': 'downtime',
                'Threshold': 0,
                'ComparisonOperator': 'GreaterThanThreshold'
            }
        ]
        
        for alarm in alarms:
            self.cloudwatch.put_metric_alarm(
                AlarmName=alarm['AlarmName'],
                ComparisonOperator=alarm['ComparisonOperator'],
                EvaluationPeriods=2,
                MetricName=alarm['MetricName'],
                Namespace='AWS/KinesisAnalytics',
                Period=300,
                Statistic='Average',
                Threshold=alarm['Threshold'],
                ActionsEnabled=True,
                AlarmActions=[
                    'arn:aws:sns:region:account:kinesis-analytics-alerts'
                ],
                AlarmDescription=f'Alarm for {application_name}',
                Dimensions=[
                    {
                        'Name': 'Application',
                        'Value': application_name
                    }
                ]
            )
```

## Best Practices

1. **Application Design**: Design cho fault tolerance và scalability
2. **State Management**: Sử dụng appropriate state backends
3. **Checkpointing**: Configure proper checkpointing intervals
4. **Resource Sizing**: Right-size KPUs based on throughput
5. **Error Handling**: Implement comprehensive error handling
6. **Monitoring**: Set up detailed monitoring và alerting
7. **Testing**: Thorough testing với realistic data volumes
8. **Security**: Implement proper IAM roles và VPC configuration

## Tích hợp với các dịch vụ AWS khác

- **Amazon Kinesis Data Streams**: Primary data source
- **Amazon Kinesis Data Firehose**: Data delivery
- **Amazon S3**: Reference data và output storage
- **Amazon DynamoDB**: Real-time lookups và results
- **AWS Lambda**: Event-driven processing
- **Amazon SNS**: Real-time notifications
- **Amazon CloudWatch**: Monitoring và alerting
- **AWS IAM**: Security và access control
- **Amazon VPC**: Network isolation
- **Amazon MSK**: Apache Kafka integration
