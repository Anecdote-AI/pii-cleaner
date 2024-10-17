
# PII Removal Tool

## Overview

The **PII Removal Tool** is a web-based application designed to help users efficiently remove Personally Identifiable Information (PII) from their CSV datasets. It leverages Streamlit for the user interface and Microsoft's Presidio services for PII detection and anonymization via REST APIs, ensuring your data remains secure and compliant with privacy regulations.

## Features

- **User-Friendly Interface:** Built with Streamlit, offering an intuitive platform for uploading and processing CSV files.
- **Customizable PII Removal:** Select specific columns in your dataset where PII removal is required.
- **Robust Anonymization:** Utilizes Presidio's Analyzer and Anonymizer services to detect and mask various types of PII, including emails, phone numbers, credit cards, and more.
- **Download Processed Data:** After anonymization, download the cleaned CSV file directly from the application.

## Prerequisites

To run the PII Removal Tool, ensure you have the following installed on your system:

- **Docker:** [Download and install Docker](https://www.docker.com/get-started) for your operating system.
- **Docker Compose:** [Install Docker Compose](https://docs.docker.com/compose/install/) to manage multiple Docker containers.

## Running the Application

Follow these steps to run the PII Removal Tool on your local machine:

### 1. Clone the Repository

Open your terminal and clone the repository:

```bash
git clone https://github.com/your-username/pii-removal-tool.git
cd pii-removal-tool
```

### 2. Ensure Service Endpoints Are Correct

Verify that the service endpoints in `pii_removal.py` match the service names defined in the Docker Compose configuration:

```python:pii_removal.py
self.analyzer_url = "http://presidio-analyzer:5001/analyze"
self.anonymizer_url = "http://presidio-anonymizer:5002/anonymize"
```

### 3. Run the Application Using Docker Compose

Use Docker Compose to build and start all the services:

```bash
docker-compose up --build
```

This command will:

- Build the Docker image for the PII Removal Tool.
- Pull the Presidio Analyzer and Anonymizer images from Microsoft's container registry.
- Start all services defined in the `docker-compose.yaml` file.

### 4. Access the Application

Once the services are up and running, open your web browser and navigate to:

```
http://localhost:8501
```

You should see the PII Removal Tool's interface ready for use.

## Usage

1. **Upload a CSV File**

   - Click on the "Upload a CSV file" button.
   - Select the CSV dataset you wish to process.

2. **Preview the Data**

   - After uploading, the application will display a preview of your CSV data.

3. **Select Columns for PII Removal**

   - Choose the columns from which you want to remove PII.
   - By default, all columns are selected.

4. **Apply PII Removal**

   - Click on the "Apply PII Removal" button.
   - The tool will process the data and remove any detected PII from the selected columns.
   - A progress spinner will indicate that processing is underway.

5. **Download the Anonymized CSV**

   - Once processing is complete, a "Download CSV" button will appear.
   - Click it to download your anonymized CSV file.

## Stopping the Application

To stop the application and shut down all services, go back to your terminal and press `Ctrl + C`. Then, run:

```bash
docker-compose down
```

This command stops and removes the containers, networks, and other resources created by `docker-compose up`.

## Troubleshooting

- **Port Conflicts:**
  - Ensure that ports `8501`, `5001`, and `5002` are not being used by other applications.
  - If they are, you can modify the `ports` section in the `docker-compose.yaml` file to use different ports.

- **Docker Resources:**
  - Make sure Docker has enough memory and CPU resources allocated, especially if working with large datasets.

- **Network Issues:**
  - The application and Presidio services communicate over a Docker network. Ensure that all services are correctly connected.

## Additional Information

- **Project Structure:**

  - `app.py`: Streamlit application script.
  - `pii_removal.py`: Contains the `MaskPII` class for PII detection and anonymization.
  - `requirements.txt`: Python dependencies.
  - `Dockerfile`: Docker image configuration for the application.
  - `docker-compose.yaml`: Configuration to run the application with Presidio services.

- **Technologies Used:**

  - Streamlit
  - Pandas
  - Presidio (via REST APIs)
  - Docker & Docker Compose

## License

This project is licensed under the [MIT License](LICENSE).
