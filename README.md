# ETL Apache Airflow - Automatic Workflow for Data Processing

## 📋 Overview
This project demonstrates an automated ETL pipeline built with **Apache Airflow** to process, transform, and store data from multiple sources. The pipeline is containerized using **Docker**, making it easy to deploy and scalable for larger datasets. The workflow is fully managed via **Apache Airflow**, ensuring seamless execution and monitoring of each ETL stage.

## 🌟 Features
- **Automated ETL Workflow**: End-to-end automation from data download to transformation and export
- **Modular Task Design**: Tasks are reusable and easy to scale for larger projects
- **Error Handling**: Comprehensive logging and detailed monitoring for each ETL step
- **Flexible Output**: Data exported in both **CSV** and **JSON** formats for downstream use

## 🏗️ Project Architecture
The ETL pipeline consists of the following stages:

1. **Download Dataset**: Automatically fetches `.tgz` data from a public URL
2. **Extract Data**: Extracts CSV and fixed-width files from the compressed archive
3. **Data Processing**:
   - Filters relevant fields from CSV and fixed-width files
   - Combines extracted data into a consolidated file
4. **Data Transformation**:
   - Standardizes fields (e.g., normalizes `Vehicle Type`)
5. **Export Data**:
   - Outputs to both **CSV** and **JSON** formats
6. **Validation**:
   - Verifies file integrity and checks for valid data rows

## 🖥️ Technologies Used
- **Apache Airflow**: Workflow management and ETL task automation
- **Docker**: Environment containerization and deployment
- **Python**:
  - Libraries: `pandas`, `csv`, `tarfile`, `requests`, `json`
  - Data processing and transformation logic
- **PostgreSQL**: Airflow metadata backend database

## 📊 System Workflow
The DAG (Directed Acyclic Graph) structure in Airflow:

```
download_dataset --> extract_tgz --> [extract_data_from_csv, extract_data_from_fixed_width] 
      --> consolidate_data --> transform_data --> check_data_rows --> [export_to_json, loading_data]
      --> check_data_files
```

## 🔧 Installation & Setup

### Prerequisites
- Docker and Docker Compose installed on your machine

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sjhinzo/Airflow
   cd Airflow
   ```

3. **Start Docker**:
   ```bash
   docker-compose up -d
   ```

4. **Access Airflow**:
   - URL: http://localhost:8080
   - Username: airflow
   - Password: airflow

## 🚀 Running the Workflow

### Step 1: Enable and Trigger DAG
- In Airflow UI, locate and enable the DAG `ETL_apache_airflow`
- Click "Trigger DAG" to start execution

### Step 2: Monitor Workflow
- Use Graph View or Tree View to track task progress
- Task status indicators:
  - ✅ Green: Success
  - 🟡 Yellow: Running
  - ❌ Red: Failed

### Step 3: Check Logs
- Click on individual tasks to view detailed execution logs

### Step 4: Validate Output
Generated files:
- `transformed_data.csv`: Consolidated and normalized CSV file
- `transformed_data.json`: JSON format for API integration

## 📂 Project Structure
```
📂 Project
├── 📂 config                # Configuration files for Airflow
│   └── fernet_key.txt       # Fernet key for secure data encryption
├── 📂 dags                  # Contains all DAG definitions and related files
│   ├── 📂 staging           # Intermediate or staging data for DAGs
│   └── ETL.py               # Main DAG script for the ETL workflow
├── 📂 logs                  # Log files generated by Airflow
│   └── scheduler            # Logs specific to the Airflow scheduler
├── 📂 plugins               # Custom plugins for Airflow (if any)
├── 📄 .env                  # Environment variables for the Docker setup
├── 📄 .gitattributes        # Git configuration for managing files
├── 📄 docker-compose.yaml   # Docker Compose configuration to run Airflow services

```

## 🌟 Key Benefits
- Fully automated data pipeline with minimal manual intervention
- Scalable architecture supporting additional data sources/transformations
- Clean and reusable codebase for future projects

## 📧 Contact
For questions or issues, please:
- Open an issue in this repository
- Contact: buitiensang191@gmail.com
