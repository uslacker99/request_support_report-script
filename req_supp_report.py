import logging
from illumio import PolicyComputeEngine

# PCE connection details
PCE_HOST = "pce.shocknetwork.com"
PCE_PORT = 8443
PCE_ORG_ID = 1  # Replace with your organization ID
ORG_ID = 1  # Replace with your organization ID
API_KEY = "api_1c9e50161eb"
API_SECRET = "75d188c4efa5d20d6ee0ce453b5b2e543ef7f70b42c0d8075"

# Path to hostname file
HOSTNAME_FILE = "hostnames.txt"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='pce_support_report.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

def read_hostnames_from_file(file_path):
    """
    Read hostnames from a file, one per line, ignoring empty lines.
    
    Args:
        file_path: Path to the hostname file
        
    Returns:
        List of hostnames
    """
    hostnames = []
    try:
        with open(file_path, 'r') as f:
            hostnames = [line.strip() for line in f if line.strip()]
        logger.info(f"Successfully read {len(hostnames)} hostnames from {file_path}")
        return hostnames
    except FileNotFoundError:
        logger.error(f"Hostname file not found: {file_path}")
        print(f"Error: Hostname file not found: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Error reading hostname file {file_path}: {e}", exc_info=True)
        print(f"Error reading hostname file: {e}")
        return []

def search_and_request_support_report(pce, hostname_list):
    """
    Search Illumio PCE for workloads by hostname and request support reports.
    
    Args:
        pce: PolicyComputeEngine instance
        hostname_list: List of hostnames to search for
    """
    logger.info("Starting search and support report request process")
    try:
        for hostname in hostname_list:
            logger.info(f"Searching for workload with hostname: {hostname}")
            # Query PCE for workload with exact hostname match
            workloads = pce.workloads.get(params={'hostname': hostname})
            
            if not workloads:
                logger.warning(f"No workload found for hostname: {hostname}")
                print(f"No workload found for hostname: {hostname}")
                continue
                
            # Process each matching workload
            for workload in workloads:
                logger.debug(f"Found workload: {getattr(workload, 'hostname', 'unknown')}")
                request_support_report(pce, workload)
                
    except Exception as e:
        logger.error(f"Error searching PCE for workloads: {e}", exc_info=True)
        print(f"Error searching PCE for workloads: {e}")

def request_support_report(pce, workload):
    """Request a support report for a given workload."""
    hostname = getattr(workload, 'hostname', 'unknown')
    logger.info(f"Processing support report request for workload: {hostname}")
    
    try:
        # Check if workload has a VEN and href
        if not hasattr(workload, 'ven') or not workload.ven or not workload.ven.href:
            logger.warning(f"No VEN href found for workload {hostname}")
            print(f"No VEN href found for workload {hostname}")
            return False

        logger.info(f"Requesting support report for workload: {hostname}")
        # Use the endpoint and payload from the curl command
        response = pce.post(
            f"/orgs/{ORG_ID}/support_report_requests",
            data={'ven': {'href': workload.ven.href}}
        )
        logger.info(f"Support report requested successfully for {hostname}")
        print(f"Support report requested successfully for {hostname}")
        return True
    except Exception as e:
        logger.error(f"Error requesting support report for {hostname}: {e}", exc_info=True)
        print(f"Error requesting support report: {e}")
        return False

def main():
        
    logger.info("Initializing PCE connection")
    try:
        pce = PolicyComputeEngine(PCE_HOST, port=PCE_PORT, org_id=PCE_ORG_ID)
        pce.set_credentials(API_KEY, API_SECRET)
        logger.info("PCE connection established successfully")
        
        # Read hostnames from file
        hostnames = read_hostnames_from_file(HOSTNAME_FILE)
        if not hostnames:
            logger.error("No hostnames to process. Exiting.")
            print("No hostnames to process. Exiting.")
            return
        
        # Search and request support reports
        search_and_request_support_report(pce, hostnames)
        logger.info("Support report request process completed")
        
    except Exception as e:
        logger.error(f"Error connecting to PCE: {e}", exc_info=True)
        print(f"Error connecting to PCE: {e}")

if __name__ == "__main__":
    main()