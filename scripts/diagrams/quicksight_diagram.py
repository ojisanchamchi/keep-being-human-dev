#!/usr/bin/env python3

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import Quicksight, Athena, Redshift, EMR
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.onprem.client import Users
from diagrams.generic.device import Mobile, Tablet

# Set output directory
import os
output_dir = "/Users/dangquangminh/minhpro/keep-being-human-dev/keep-being-human-dev/static/img/aws-analytics"

with Diagram("Amazon QuickSight Architecture", 
             show=False, 
             direction="TB",
             filename=f"{output_dir}/quicksight"):
    
    # Users and devices
    with Cluster("Business Users"):
        executives = Users("Executives")
        analysts = Users("Business Analysts")
        mobile_users = Mobile("Mobile Users")
        tablet_users = Tablet("Tablet Users")
    
    # QuickSight service
    with Cluster("Amazon QuickSight"):
        qs_service = Quicksight("QuickSight Service")
        spice_engine = Lambda("SPICE Engine")
        ml_insights = Lambda("ML Insights")
        dashboards = Lambda("Dashboards")
    
    # Data sources - AWS services
    with Cluster("AWS Data Sources"):
        redshift_dw = Redshift("Redshift DW")
        athena_query = Athena("Athena")
        s3_data = S3("S3 Data Lake")
        rds_db = RDS("RDS Database")
        dynamodb_nosql = Dynamodb("DynamoDB")
    
    # Data sources - External
    with Cluster("External Data Sources"):
        salesforce = Lambda("Salesforce")
        jira = Lambda("Jira")
        servicenow = Lambda("ServiceNow")
        excel_files = Lambda("Excel/CSV Files")
    
    # Data preparation
    with Cluster("Data Preparation"):
        data_prep = Lambda("Data Prep")
        calculated_fields = Lambda("Calculated Fields")
        parameters = Lambda("Parameters")
        filters = Lambda("Filters")
    
    # Analytics and visualization
    with Cluster("Analytics & Visualization"):
        interactive_dashboards = Lambda("Interactive Dashboards")
        paginated_reports = Lambda("Paginated Reports")
        embedded_analytics = Lambda("Embedded Analytics")
        auto_narratives = Lambda("Auto Narratives")
    
    # Sharing and collaboration
    with Cluster("Sharing & Collaboration"):
        email_reports = SNS("Email Reports")
        slack_integration = Lambda("Slack Integration")
        api_embedding = Lambda("API Embedding")
        row_level_security = IAM("Row Level Security")
    
    # Monitoring and administration
    with Cluster("Administration"):
        user_management = IAM("User Management")
        usage_monitoring = Cloudwatch("Usage Monitoring")
        cost_management = Lambda("Cost Management")
    
    # User connections to QuickSight
    executives >> Edge(label="Executive Dashboards") >> qs_service
    analysts >> Edge(label="Self-Service Analytics") >> qs_service
    mobile_users >> Edge(label="Mobile Access") >> qs_service
    tablet_users >> Edge(label="Responsive UI") >> qs_service
    
    # Data source connections
    redshift_dw >> Edge(label="Direct Connect") >> qs_service
    athena_query >> Edge(label="Serverless Queries") >> qs_service
    s3_data >> Edge(label="File Import") >> qs_service
    rds_db >> Edge(label="Live Connection") >> qs_service
    dynamodb_nosql >> Edge(label="NoSQL Data") >> qs_service
    
    # External data sources
    salesforce >> Edge(label="CRM Data") >> qs_service
    jira >> Edge(label="Project Data") >> qs_service
    servicenow >> Edge(label="Service Data") >> qs_service
    excel_files >> Edge(label="File Upload") >> qs_service
    
    # QuickSight internal components
    qs_service >> Edge(label="In-Memory") >> spice_engine
    qs_service >> Edge(label="Auto Insights") >> ml_insights
    qs_service >> Edge(label="Visualizations") >> dashboards
    
    # Data preparation flow
    qs_service >> Edge(label="Transform") >> data_prep
    data_prep >> Edge(label="Enhance") >> calculated_fields
    calculated_fields >> Edge(label="Parameterize") >> parameters
    parameters >> Edge(label="Filter") >> filters
    
    # Analytics outputs
    filters >> Edge(label="Create") >> interactive_dashboards
    interactive_dashboards >> Edge(label="Generate") >> paginated_reports
    dashboards >> Edge(label="Embed") >> embedded_analytics
    ml_insights >> Edge(label="Generate") >> auto_narratives
    
    # Sharing mechanisms
    paginated_reports >> Edge(label="Schedule") >> email_reports
    dashboards >> Edge(label="Notify") >> slack_integration
    embedded_analytics >> Edge(label="API") >> api_embedding
    qs_service >> Edge(label="Secure") >> row_level_security
    
    # Administration
    qs_service >> Edge(label="Manage") >> user_management
    qs_service >> Edge(label="Monitor") >> usage_monitoring
    usage_monitoring >> Edge(label="Optimize") >> cost_management

print("QuickSight diagram generated successfully!")
