from typing import Dict

US_WEST_2: str = 'us-west-2'
US_EAST_1: str = 'us-east-1'
AP_EAST_1: str = 'ap-east-1'
EU_WEST_2: str = 'eu-west-2'

REGION_MAPPING: Dict = {
    "North America": US_EAST_1,
    "West Coast US": US_WEST_2,
    "Europe": EU_WEST_2,
    "Asia": AP_EAST_1
}

DYNAMODB_RESOURCE: str = 'dynamodb'

MAX_RETRIES: int = 10
DELAY: int = 3

LOCATION = "Asia"
RECORD_ID = "1740006219"
