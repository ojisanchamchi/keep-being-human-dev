#!/usr/bin/env python3

import subprocess
import sys
import os

def run_script(script_name):
    """Run a Python script and handle errors"""
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {script_name}: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name}: Error - {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ {script_name}: Unexpected error - {str(e)}")
        return False

def main():
    """Generate all AWS Analytics diagrams"""
    print("🚀 Generating AWS Analytics Diagrams...")
    print("=" * 50)
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # List of diagram scripts to run
    scripts = [
        "opensearch_diagram.py",
        "analytics_diagram.py", 
        "athena_diagram.py",
        "cloudsearch_search_documents_diagram.py",
        "cloudsearch_diagram.py",
        "data_lake_resource_diagram.py",
        "data_pipeline_diagram.py",
        "elasticsearch_service_diagram.py",
        "emr_cluster_diagram.py",
        "emr_engine_mapr_m3_diagram.py",
        "emr_engine_mapr_m5_diagram.py",
        "emr_engine_mapr_m7_diagram.py",
        "emr_engine_diagram.py",
        "emr_hdfs_cluster_diagram.py",
        "emr_diagram.py",
        "glue_crawlers_diagram.py",
        "glue_data_catalog_diagram.py",
        "glue_diagram.py"
    ]
    
    success_count = 0
    total_count = len(scripts)
    
    # Run each script
    for script in scripts:
        script_path = os.path.join(current_dir, script)
        if os.path.exists(script_path):
            if run_script(script_path):
                success_count += 1
        else:
            print(f"❌ {script}: File not found")
    
    print("=" * 50)
    print(f"📊 Summary: {success_count}/{total_count} diagrams generated successfully")
    
    if success_count == total_count:
        print("🎉 All diagrams generated successfully!")
        print("📁 Check the static/img/aws-analytics/ directory for the generated images")
    else:
        print("⚠️  Some diagrams failed to generate. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
