# Amazon QuickSight

## Overview

Amazon QuickSight is a fast, cloud-powered business intelligence (BI) service that makes it easy to deliver insights to everyone in your organization. QuickSight lets you create and publish interactive dashboards that can be accessed from any device, and embedded into your applications, portals, and websites. With QuickSight, you can scale to hundreds of thousands of users, and achieve performance at a fraction of the cost of traditional BI solutions.

## Main Functions

### Data Visualization and Dashboards
- **Interactive Dashboards**: Create rich, interactive visualizations and dashboards
- **Auto-Generated Insights**: ML-powered insights and anomaly detection
- **Mobile Responsive**: Dashboards that work on any device
- **Real-time Data**: Connect to live data sources for real-time analytics

### Data Connectivity
- **Multiple Data Sources**: Connect to AWS services, databases, files, and SaaS applications
- **Data Preparation**: Built-in data preparation and transformation capabilities
- **SPICE Engine**: In-memory calculation engine for fast query performance
- **Direct Query**: Query data directly from sources without importing

### Collaboration and Sharing
- **Secure Sharing**: Share dashboards and analyses with users and groups
- **Embedded Analytics**: Embed dashboards in applications and websites
- **Commenting**: Collaborate with comments and annotations
- **Scheduled Reports**: Automated report generation and distribution

### Advanced Analytics
- **Machine Learning Insights**: Automated insights using ML algorithms
- **Forecasting**: Built-in forecasting capabilities
- **What-if Analysis**: Scenario planning and analysis
- **Custom Calculations**: Advanced calculated fields and functions

## Use Cases

### Executive Dashboard
```python
import boto3
import json
from datetime import datetime, timedelta

class QuickSightDashboardManager:
    def __init__(self):
        self.quicksight = boto3.client('quicksight')
        self.account_id = boto3.client('sts').get_caller_identity()['Account']
    
    def create_data_source(self, data_source_id, name, connection_params):
        """Create QuickSight data source"""
        try:
            response = self.quicksight.create_data_source(
                AwsAccountId=self.account_id,
                DataSourceId=data_source_id,
                Name=name,
                Type='REDSHIFT',
                DataSourceParameters={
                    'RedshiftParameters': {
                        'Host': connection_params['host'],
                        'Port': connection_params['port'],
                        'Database': connection_params['database']
                    }
                },
                Credentials={
                    'CredentialPair': {
                        'Username': connection_params['username'],
                        'Password': connection_params['password']
                    }
                },
                VpcConnectionProperties={
                    'VpcConnectionArn': connection_params.get('vpc_connection_arn')
                },
                SslProperties={
                    'DisableSsl': False
                }
            )
            print(f"Data source created: {data_source_id}")
            return response
        except Exception as e:
            print(f"Error creating data source: {e}")
    
    def create_dataset(self, dataset_id, name, data_source_id, sql_query):
        """Create QuickSight dataset"""
        try:
            response = self.quicksight.create_data_set(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id,
                Name=name,
                PhysicalTableMap={
                    'sales_data': {
                        'CustomSql': {
                            'DataSourceArn': f"arn:aws:quicksight:us-east-1:{self.account_id}:datasource/{data_source_id}",
                            'Name': 'sales_query',
                            'SqlQuery': sql_query,
                            'Columns': [
                                {
                                    'Name': 'date',
                                    'Type': 'DATETIME'
                                },
                                {
                                    'Name': 'revenue',
                                    'Type': 'DECIMAL'
                                },
                                {
                                    'Name': 'region',
                                    'Type': 'STRING'
                                },
                                {
                                    'Name': 'product_category',
                                    'Type': 'STRING'
                                }
                            ]
                        }
                    }
                },
                ImportMode='SPICE'
            )
            print(f"Dataset created: {dataset_id}")
            return response
        except Exception as e:
            print(f"Error creating dataset: {e}")
    
    def create_analysis(self, analysis_id, name, dataset_id):
        """Create QuickSight analysis"""
        try:
            response = self.quicksight.create_analysis(
                AwsAccountId=self.account_id,
                AnalysisId=analysis_id,
                Name=name,
                Definition={
                    'DataSetIdentifierDeclarations': [
                        {
                            'DataSetArn': f"arn:aws:quicksight:us-east-1:{self.account_id}:dataset/{dataset_id}",
                            'Identifier': 'sales_dataset'
                        }
                    ],
                    'Sheets': [
                        {
                            'SheetId': 'executive_overview',
                            'Name': 'Executive Overview',
                            'Visuals': [
                                {
                                    'LineChartVisual': {
                                        'VisualId': 'revenue_trend',
                                        'Title': {
                                            'Visibility': 'VISIBLE',
                                            'FormatText': {
                                                'PlainText': 'Revenue Trend'
                                            }
                                        },
                                        'FieldWells': {
                                            'LineChartAggregatedFieldWells': {
                                                'Category': [
                                                    {
                                                        'DateDimensionField': {
                                                            'FieldId': 'date_field',
                                                            'Column': {
                                                                'DataSetIdentifier': 'sales_dataset',
                                                                'ColumnName': 'date'
                                                            }
                                                        }
                                                    }
                                                ],
                                                'Values': [
                                                    {
                                                        'NumericalMeasureField': {
                                                            'FieldId': 'revenue_field',
                                                            'Column': {
                                                                'DataSetIdentifier': 'sales_dataset',
                                                                'ColumnName': 'revenue'
                                                            },
                                                            'AggregationFunction': {
                                                                'SimpleNumericalAggregation': 'SUM'
                                                            }
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    ]
                }
            )
            print(f"Analysis created: {analysis_id}")
            return response
        except Exception as e:
            print(f"Error creating analysis: {e}")

# Usage example
dashboard_manager = QuickSightDashboardManager()

# Create data source
connection_params = {
    'host': 'my-redshift-cluster.abc123.us-east-1.redshift.amazonaws.com',
    'port': 5439,
    'database': 'analytics',
    'username': 'quicksight_user',
    'password': 'secure_password'
}

dashboard_manager.create_data_source(
    data_source_id='sales-redshift-source',
    name='Sales Data Warehouse',
    connection_params=connection_params
)

# Create dataset
sql_query = """
SELECT 
    DATE_TRUNC('day', order_date) as date,
    SUM(total_amount) as revenue,
    region,
    product_category
FROM sales_fact sf
JOIN dim_product dp ON sf.product_id = dp.product_id
JOIN dim_geography dg ON sf.geography_id = dg.geography_id
WHERE order_date >= CURRENT_DATE - INTERVAL '365 days'
GROUP BY 1, 3, 4
ORDER BY 1
"""

dashboard_manager.create_dataset(
    dataset_id='executive-sales-dataset',
    name='Executive Sales Data',
    data_source_id='sales-redshift-source',
    sql_query=sql_query
)
```

### Self-Service Analytics
```python
class QuickSightSelfServiceAnalytics:
    def __init__(self):
        self.quicksight = boto3.client('quicksight')
        self.account_id = boto3.client('sts').get_caller_identity()['Account']
    
    def create_s3_data_source(self, data_source_id, name, s3_manifest_url):
        """Create S3 data source for self-service analytics"""
        try:
            response = self.quicksight.create_data_source(
                AwsAccountId=self.account_id,
                DataSourceId=data_source_id,
                Name=name,
                Type='S3',
                DataSourceParameters={
                    'S3Parameters': {
                        'ManifestFileLocation': {
                            'Bucket': s3_manifest_url.split('/')[2],
                            'Key': '/'.join(s3_manifest_url.split('/')[3:])
                        }
                    }
                }
            )
            print(f"S3 data source created: {data_source_id}")
            return response
        except Exception as e:
            print(f"Error creating S3 data source: {e}")
    
    def create_calculated_field(self, dataset_id, field_name, expression):
        """Add calculated field to dataset"""
        try:
            response = self.quicksight.update_data_set(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id,
                LogicalTableMap={
                    'calculated_table': {
                        'Alias': 'Enhanced Data',
                        'Source': {
                            'PhysicalTableId': 'base_table'
                        },
                        'DataTransforms': [
                            {
                                'CreateColumnsOperation': {
                                    'Columns': [
                                        {
                                            'ColumnName': field_name,
                                            'ColumnId': field_name.lower().replace(' ', '_'),
                                            'Expression': expression
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                }
            )
            print(f"Calculated field added: {field_name}")
            return response
        except Exception as e:
            print(f"Error adding calculated field: {e}")
    
    def create_parameter(self, analysis_id, parameter_name, parameter_type, default_values):
        """Create parameter for interactive filtering"""
        try:
            response = self.quicksight.update_analysis(
                AwsAccountId=self.account_id,
                AnalysisId=analysis_id,
                Definition={
                    'ParameterDeclarations': [
                        {
                            'StringParameterDeclaration': {
                                'ParameterName': parameter_name,
                                'Name': parameter_name,
                                'DefaultValues': {
                                    'StaticValues': default_values
                                },
                                'ValueWhenUnset': {
                                    'ValueWhenUnsetOption': 'RECOMMENDED_VALUE'
                                }
                            }
                        }
                    ]
                }
            )
            print(f"Parameter created: {parameter_name}")
            return response
        except Exception as e:
            print(f"Error creating parameter: {e}")

# Usage example
self_service = QuickSightSelfServiceAnalytics()

# Create S3 data source
self_service.create_s3_data_source(
    data_source_id='customer-data-s3',
    name='Customer Analytics Data',
    s3_manifest_url='s3://my-analytics-bucket/manifests/customer_data.json'
)

# Add calculated fields
self_service.create_calculated_field(
    dataset_id='customer-analytics-dataset',
    field_name='Customer Lifetime Value',
    expression='sum({total_purchases}) / count({customer_id})'
)

self_service.create_calculated_field(
    dataset_id='customer-analytics-dataset',
    field_name='Days Since Last Purchase',
    expression='dateDiff(max({last_purchase_date}), now(), "DD")'
)
```

## Architecture Diagram

![Amazon QuickSight Architecture](/img/aws-analytics/quicksight.png)

## AWS Service Integrations

### Data Sources
- **Amazon Redshift**: Data warehouse integration
- **Amazon RDS**: Relational database connectivity
- **Amazon S3**: File-based data sources
- **Amazon Athena**: Serverless query service
- **Amazon DynamoDB**: NoSQL database integration

### Analytics Services
- **AWS Glue**: Data cataloging and ETL
- **Amazon EMR**: Big data processing
- **Amazon Kinesis**: Real-time data streaming
- **AWS Lake Formation**: Data lake governance

### Security and Management
- **AWS IAM**: User authentication and authorization
- **Amazon VPC**: Network isolation
- **AWS CloudTrail**: API audit logging
- **Amazon CloudWatch**: Monitoring and alerting

### Integration Services
- **Amazon API Gateway**: REST API integration
- **AWS Lambda**: Serverless compute integration
- **Amazon EventBridge**: Event-driven architectures
- **AWS Step Functions**: Workflow orchestration

## Best Practices

### Performance Optimization
- Use SPICE for frequently accessed data
- Optimize dataset refresh schedules
- Implement proper data modeling
- Use appropriate visualization types
- Monitor query performance

### Security
- Implement row-level security (RLS)
- Use IAM for access control
- Enable VPC connectivity for sensitive data
- Regular security audits
- Secure embedding practices

### Cost Management
- Monitor SPICE capacity usage
- Optimize data refresh frequency
- Use appropriate user licensing
- Implement data lifecycle policies
- Regular cost analysis

### User Experience
- Design mobile-responsive dashboards
- Implement intuitive navigation
- Use consistent color schemes
- Provide clear data context
- Enable self-service capabilities
