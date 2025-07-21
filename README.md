# Illumio PCE Support Report Generator

This script connects to an Illumio Policy Compute Engine (PCE) to search for workloads by hostname and request support reports for matching workloads. It reads hostnames from a text file and logs all actions to a file for debugging and auditing purposes.

## Prerequisites

- Python 3.6+
- `illumio` Python library (`pip install illumio`)
- Access to an Illumio PCE instance
- API key and secret for PCE authentication
- A text file containing hostnames (one per line)

## Installation

1. Clone or download this script to your local machine.
2. Install the required Python package:
   ```bash
   pip install illumio
   ```
3. Create a text file (e.g., `hostnames.txt`) with one hostname per line.

## Configuration

Edit the following variables in the script to match your environment:

- `PCE_HOST`: The hostname or IP address of the PCE (e.g., `pce.shocknetwork.com`)
- `PCE_PORT`: The PCE port (default: `8443`)
- `PCE_ORG_ID`: Your Illumio organization ID
- `API_KEY`: Your PCE API key
- `API_SECRET`: Your PCE API secret
- `HOSTNAME_FILE`: Path to the text file containing hostnames (default: `hostnames.txt`)

## Usage

1. Ensure the `hostnames.txt` file exists and contains the hostnames you want to process.
2. Run the script:
   ```bash
   python pce_support_report.py
   ```
3. The script will:
   - Read hostnames from the specified file
   - Connect to the PCE using the provided credentials
   - Search for workloads matching each hostname
   - Request support reports for workloads with a valid VEN (Virtual Enforcement Node)
   - Log all actions to `pce_support_report.log`

## Logging

- Logs are written to `pce_support_report.log` in the same directory as the script.
- Log levels include `INFO`, `WARNING`, `ERROR`, and `DEBUG`.
- Logs include timestamps, log levels, and detailed messages for debugging.

## Functions

- `read_hostnames_from_file(file_path)`: Reads hostnames from the specified file, ignoring empty lines.
- `search_and_request_support_report(pce, hostname_list)`: Queries the PCE for workloads by hostname and requests support reports.
- `request_support_report(pce, workload)`: Requests a support report for a specific workload.
- `main()`: Orchestrates the connection to the PCE and the report generation process.

## Error Handling

- The script handles errors such as:
  - Missing or invalid hostname files
  - PCE connection failures
  - Workloads without a valid VEN
  - API request failures
- Errors are logged to `pce_support_report.log` and printed to the console.

## Output

- Console output includes success and error messages for each hostname processed.
- Log file (`pce_support_report.log`) contains detailed information about the execution, including any errors or warnings.

## Notes

- Ensure the API key and secret are kept secure and not exposed in version control.
- The script assumes exact hostname matches in the PCE. Partial matches are not supported.
- If a workload is found but has no associated VEN, the script logs a warning and skips it.

## License

This script is provided as-is under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For issues or questions, contact your Illumio administrator or support team.
