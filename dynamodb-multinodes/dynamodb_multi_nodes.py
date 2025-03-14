"""DynamoDB multi-nodes management
"""
import time
import logging
import random
from typing import Dict
import boto3
from constants import REGION_MAPPING, US_WEST_2, US_EAST_1, \
    AP_EAST_1, EU_WEST_2, DYNAMODB_RESOURCE, MAX_RETRIES, DELAY, \
        LOCATION, RECORD_ID

logger = logging.getLogger(__name__)

class DynamoDBMultiNodes:
    """DynamoDBMultiNodes class
    """
    def __init__(self, table_name: str, main_region: str):
        """Initialize this class and set class member(s)
        """
        self.supported_regions: Dict = {
            US_WEST_2: boto3.resource(DYNAMODB_RESOURCE, region_name=US_WEST_2),
            US_EAST_1: boto3.resource(DYNAMODB_RESOURCE, region_name=US_EAST_1),
            AP_EAST_1: boto3.resource(DYNAMODB_RESOURCE, region_name=AP_EAST_1),
            EU_WEST_2: boto3.resource(DYNAMODB_RESOURCE, region_name=EU_WEST_2)
        }
        self.table_name: str = table_name
        self.main_region: str = main_region
        self.tables: Dict = {region: resource.Table(self.table_name) for region, resource in self.supported_regions.items()}

    def __get_closest_region(self, client_location: str) -> str:
        """Determine the closest AWS region based on the client's location.
        """
        return REGION_MAPPING.get(client_location, US_WEST_2)

    def write_data(self, data: Dict) -> int:
        """Write data into main region
        """
        self.tables[self.main_region].put_item(Item=data)
        return data.id

    def fetch_data(self, item_id: int, client_location: str):
        """Fetch data from the closest available DynamoDB region, with failover.
        """
        closest_region = self.__get_closest_region(client_location=client_location)
        fallback_regions = list(self.supported_regions.keys())

        table_key: Dict = {'id': item_id}
        response = self.tables.get(closest_region).get_item(Key=table_key)
        if 'Item' in response:
            return response['Item']

        fallback_regions.remove(closest_region)
        random.shuffle(fallback_regions)

        for region in fallback_regions:
            response = self.tables[region].get_item(Key=table_key)
            if 'Item' in response:
                return response['Item']

        return None

    def replicate_data(self, item_id: int,  max_retries: int, delay: int) -> bool:
        """Replicate data across supported regions
        """
        for attempt in range(max_retries):
            replicated_regions = []

            for region, table in self.tables.items():
                if region == US_WEST_2:
                    continue

                response = table.get_item(Key={'id': item_id})
                if 'Item' in response:
                    replicated_regions.append(region)

            if len(replicated_regions) == len(self.tables) - 1:
                logger.info("Data replicated in all regions after %s attempts: %s", attempt + 1, replicated_regions)
                return True

            logger.info("Attempt %s: Data not fully replicated, retrying in %s sec...", {attempt + 1}/{max_retries}, delay)
            time.sleep(delay)

        logger.error("Replication check failed: Data was not found in all regions after multiple retries.")
        return False

# use case
if __name__ == "__main__":
    ## initialize dynamodb client
    dynamodb_client = DynamoDBMultiNodes(
        table_name='Users',
        main_region=US_WEST_2
    )

    ## storing and replicating data
    test_data: Dict = {
        'id': str(int(time.time())),
        'location': {
            'lat': '37.4221',
            'lng': '-122.0853'
        },
        'timestamp': int(time.time())
    }
    write_data_result = dynamodb_client.write_data(
        data=test_data
    )
    replication_result = dynamodb_client.replicate_data(
        item_id=write_data_result,
        max_retries=MAX_RETRIES,
        delay=DELAY
    )
    logger.info('write data result id: {write_data_result}')
    logger.info('replication status: {replication_result}')

    ## simulate record fetch from closest client's location
    fetch_data_result = dynamodb_client.fetch_data(item_id=RECORD_ID, client_location=LOCATION)
    logger.info('fetch data result: {fetch_data_result}')
