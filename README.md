# Wikipedia-football-data-engineering-pipeline
End-to-end data pipeline extracting Wikipedia data with Apache Airflow and Azure services

## System Architecture

## Overview
This document describes the architecture of the Wikipedia data pipeline.

## Components

### Data Sources
- **Wikipedia REST API**: Primary data source for page views and metadata
- **Wikipedia Dumps**: Backup source for historical data

### Data Pipeline
- **Apache Airflow**: Orchestration and workflow management
- **Python**: ETL logic implementation
- **Docker**: Containerization for consistent environments

### Storage & Analytics
- **Azure Data Lake Storage Gen2**: Raw and processed data storage
- **Azure Synapse Analytics**: Data warehouse and big data processing
- **Power BI**: Business intelligence and visualization

### Infrastructure
- **Terraform**: Infrastructure as Code
- **GitHub Actions**: CI/CD pipeline
- **Azure Key Vault**: Secrets management

## Data Flow

1. **Extraction**: Airflow DAG triggers Wikipedia API calls
2. **Transformation**: Raw data cleaned and structured
3. **Loading**: Processed data stored in Azure Data Lake
4. **Processing**: Synapse Analytics processes data for analytics
5. **Visualization**: Power BI connects to Synapse for dashboards
