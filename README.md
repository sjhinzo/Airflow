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

## 🔧 Installation & Setup  & Demo Projects

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
   ![image](https://github.com/user-attachments/assets/40a80fad-2c8a-442f-a72a-8ce69d9db3a1)
 **UI Docker**:
   ![image](https://github.com/user-attachments/assets/ae431347-3d23-4c9b-871b-aaad0d58f48b)

5. **Access Airflow**:
   - URL: http://localhost:8080
   - Username: airflow
   - Password: airflow
![image](https://github.com/user-attachments/assets/6f442225-dad0-4cac-8cc0-1523726bdfbe)
### **UI Airflow**:
![image](https://github.com/user-attachments/assets/de9cf037-effc-4706-92bb-862e6bf9b024)
## 🚀 Running the Workflow

### Step 1: Enable and Trigger DAG
- In Airflow UI, locate and enable the DAG `ETL_apache_airflow`
- Click "Trigger DAG" to start execution
![image](https://github.com/user-attachments/assets/f7934807-4065-41a4-ac15-d1473c714a33)

### Step 2: Monitor Workflow
- Use Graph View or Tree View to track task progress
# **Task Status Indicators in Airflow**

Apache Airflow uses color-coded status indicators to represent the current state of tasks in a DAG. Below is the meaning of each status:

---

### ✅ **Success (Dark Green)**
- **Meaning**: The task completed successfully without any errors.
- **Next Steps**: No further action is needed. The task has been executed successfully.

---

### 💚 **Running (Light Green)**
- **Meaning**: The task is currently being executed.
- **Next Steps**: Monitor the task in **Graph View** or check **Logs** for progress.

---

### ❌ **Failed (Red)**
- **Meaning**: The task failed during execution.
- **Next Steps**:
  1. Click on the task in the Airflow UI.
  2. Review the **Logs** to identify the error and resolve it.

---

### 🟣 **Deferred (Light Purple)**
- **Meaning**: The task has been deferred and is waiting for specific conditions to be met before execution.
- **Next Steps**:
  - Check the DAG to ensure the trigger conditions or upstream dependencies are satisfied.

---

### ⚪ **Queued (Gray)**
- **Meaning**: The task is queued and waiting to be executed.
- **Next Steps**:
  - Verify that sufficient system resources (CPU, memory) are available.
  - Ensure the Airflow scheduler is running.

---

### ⚪ **Removed (Gray)**
- **Meaning**: The task has been removed from the DAG or is no longer executable.
- **Next Steps**: No action is required if the task was intentionally removed.

---

### 💗 **Restarting (Pink)**
- **Meaning**: The task is being restarted after encountering a failure.
- **Next Steps**:
  - Monitor the task in **Logs** or **Graph View** to ensure proper execution after restarting.

---

### ⚪ **Scheduled (Gray)**
- **Meaning**: The task is scheduled and will run at the specified time.
- **Next Steps**:
  - Check the schedule or review **Logs** to confirm the timing.

---

### 🔵 **Shutdown (Blue)**
- **Meaning**: The task has been manually stopped or halted due to a system shutdown.
- **Next Steps**:
  - Investigate the cause of the shutdown and restart the task if necessary.

---

### 💗 **Skipped (Pink)**
- **Meaning**: The task was skipped, often due to unsatisfied conditions or dependencies.
- **Next Steps**:
  - Verify the DAG logic (e.g., Branch Operator or Trigger Rules) to ensure the conditions are correct.

---

### 🔷 **Up for Reschedule (Turquoise)**
- **Meaning**: The task is waiting to be rescheduled due to unmet conditions during the initial attempt.
- **Next Steps**:
  - Monitor the DAG or check the **Logs** to identify why the task was rescheduled.

---

### 🟡 **Up for Retry (Yellow)**
- **Meaning**: The task failed previously but is now retrying automatically as per the retry policy.
- **Next Steps**:
  - Monitor the task to ensure the issue is resolved or increase the retry attempts if needed.

---

### 🟡 **Upstream Failed (Yellow)**
- **Meaning**: The task could not execute because an upstream task it depends on failed.
- **Next Steps**:
  - Check the status of the upstream task and fix the issue before rerunning the DAG.

---

### ⚪ **No Status (Gray)**
- **Meaning**: The task has not started or no status has been recorded yet.
- **Next Steps**:
  - Ensure that the DAG is enabled and the scheduler is running.

---

## **How to Use Task Status Indicators**

1. **Monitor DAG Status**:
   - Use **Graph View** or **Tree View** in the Airflow UI to visualize task statuses and dependencies.
   
2. **Check Logs**:
   - For statuses such as **❌ Failed**, **💗 Restarting**, or **🟡 Up for Retry**, review the task **Logs** to diagnose and resolve issues.
   
3. **System Management**:
   - States like **🔵 Shutdown** or **🟣 Deferred** may require you to check the DAG configuration or system setup.

---

If you need additional details or further assistance, feel free to reach out! 😊

![image](https://github.com/user-attachments/assets/6cf6fa56-787a-4592-b834-d585fc07170e)
### **GRAPH**:
![image](https://github.com/user-attachments/assets/e2a72e25-817f-4d29-b303-269b983b89ea)

### Step 3: Check Logs
- Click on individual tasks to view detailed execution logs
### **LOGS**:
![image](https://github.com/user-attachments/assets/66907f1e-a078-4878-b4ce-4924c5c0fba1)

### Step 4: Validate Output
Generated files:
- `transformed_data.csv`: Consolidated and normalized CSV file
- `transformed_data.json`: JSON format for API integration
![image](https://github.com/user-attachments/assets/e50f7aa3-dab0-40a4-bdd4-277a9bbe4410)

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
- Linkedin: https://www.linkedin.com/in/sjhinzo/
