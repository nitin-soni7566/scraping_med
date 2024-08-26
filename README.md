# Website Data Scraping Scripts

This repository contains Python scripts for scraping data from various veterinary websites and storing it in Excel files.

## Prerequisites

- **Python 3.12.0**: Make sure you have Python 3.12.0 installed on your machine.

## Setup Instructions

1. **Create a Virtual Environment**:
   - Run the following command to create a virtual environment named `venv`:
     ```bash
     python -m venv venv
     ```

2. **Activate the Virtual Environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS and Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install Required Dependencies**:
   - Install the necessary Python packages using `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

## Running the Scripts

Each script is designed to scrape data from a specific website and save it to an Excel file. Below are the details for each script:

1. **Find A Vet Scraping Script**:
   - **Website**: [Find A Vet](https://findavet.rcvs.org.uk/find-a-vet-practice/?filter-choice=&filter-keyword=&filter-searchtype=practice&filter-pss=true&p=1)
   - **Run the script**:
     ```bash
     python findavet_scraping_script.py
     ```

2. **Medivet Group Scraping Script**:
   - **Website**: [Medivet Group](https://www.medivetgroup.com/vet-practices/?address=Λονδίνο,+Ηνωμένο+Βασίλειο&longitude=-0.1275862&latitude=51.5072178&isEmergency=False&page=1)
   - **Run the script**:
     ```bash
     python medivetgroup_scraping_script.py
     ```

3. **Cat Friendly Clinic Scraping Script**:
   - **Website**: [Cat Friendly Clinic](https://catfriendlyclinic.org/cat-owners/find-a-clinic/)
   - **Run the script**:
     ```bash
     python catfriendlyclinic_scraping_script.py
     ```

Each script will scrape the respective website and store the data in an Excel file for further analysis.
