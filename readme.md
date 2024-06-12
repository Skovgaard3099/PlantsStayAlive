# Plants Stay Alive Weather Forecast Script

This script checks the weather forecast and sends an email notification if the temperature is expected to drop below a specified threshold.

## Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)

## Setup

1. **Clone the Repository**
    ```sh
    git clone https://github.com/yourusername/plants-stay-alive.git
    cd plants-stay-alive
    ```

2. **Create and Activate a Virtual Environment**
    ```sh
    python -m venv .venv
    .\.venv\Scripts\activate  # On Windows
    source .venv/bin/activate  # On macOS/Linux
    ```

3. **Install Dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure the Script**
    - Create a `config.txt` file in the project directory with the following content:
        ```
        GMAIL_USERNAME=your_email@gmail.com
        GMAIL_APP_PASSWORD=your_app_password
        EMAIL_RECIPIENT=recipient_email@example.com
        ```

5. **Run the Script Manually**
    ```sh
    python main.py
    ```

6. **Set Up Automatic Execution at Startup**

    ### Using a Batch File

    - Create a batch file named `run_PlantStayAlive.bat` with the following content:
        ```bat
        @echo off
        cd C:\path\to\plants-stay-alive
        call .venv\Scripts\activate
        python main.py > C:\path\to\plants-stay-alive\run_log.txt 2>&1
        ```

    - Place a shortcut of this batch file in the Startup folder:
        1. Right-click the batch file and select "Create shortcut".
        2. Press `Win + R`, type `shell:startup`, and press Enter.
        3. Move the shortcut to the Startup folder.

    ### Using Task Scheduler

    1. Open Task Scheduler.
    2. Create a new task:
        - **General Tab**:
            - Name: `PlantsStayAlive`
            - Check "Run with highest privileges"
            - Configure for: `Windows 10` (or the latest version available)
        - **Triggers Tab**:
            - New Trigger: `At log on`
            - Check "Delay task for" and set an appropriate delay (e.g., 5 minutes)
        - **Actions Tab**:
            - New Action: `Start a program`
            - Program/script: `C:\path\to\run_PlantStayAlive.bat`
        - **Conditions Tab**:
            - (Optional) Check "Start only if the following network connection is available" and select your network
        - **Settings Tab**:
            - Ensure "Allow task to be run on demand" is checked

    3. Save the task and restart your computer to test.

## Troubleshooting

- **Check Log File**: If the script does not run as expected, check the `run_log.txt` file in the project directory for any errors or output messages.