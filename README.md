# Web-Update-Checker

A Python script to automatically check for modifications to websites of interest. The script can notify of changes via the OS alert system (Linux systems only).

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/MattiaFerrarini/Web-Update-Checker.git
    ```

2. Navigate to the project directory:
    ```
    cd Web-Update-Checker
    ```

3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

## Configuration

List the URLs of the websites you'd like to monitor on separate lines in `urls.txt` (located in the project directory).
```
https://example-1.com
https://example-2.edu
```

## Usage

### Manually
To manually run the check:
```
python3 webUpdateChecker.py
```

### Automatically
To automatically run the check repeatedly when the computer is on, you can use `cron` and the provided `checkStarter.sh` script.

1. Add the path to your project folder to `checkStarter.sh` by modifying the line:
    ```
    cd "path/to/your/folder"
    ```

2. Make `checkStarter.sh` executable:
    ```
    chmod +x /path/to/checkStarter.sh
    ```
3. Open the crontab file for editing:
    ```
    crontab -e
    ```
4. Set up a cron job to run the script at your desired interval. For example, to run the script every hour, add the following line to your crontab:
    ```
    0 * * * * /path/to/checkStarter.sh
    ```