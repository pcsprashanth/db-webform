import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request to list SQL servers and databases.')

    try:
        # Authenticate using DefaultAzureCredential
        credential = DefaultAzureCredential()

        # Replace with your Azure subscription ID
        subscription_id = "<YOUR_SUBSCRIPTION_ID>"

        # Initialize clients
        resource_client = ResourceManagementClient(credential, subscription_id)
        sql_client = SqlManagementClient(credential, subscription_id)

        # Retrieve all resource groups
        resource_groups = resource_client.resource_groups.list()

        result = {}

        # Iterate through each resource group
        for rg in resource_groups:
            rg_name = rg.name
            servers = sql_client.servers.list_by_resource_group(rg_name)
            for server in servers:
                server_name = server.name
                databases = sql_client.databases.list_by_server(rg_name, server_name)
                db_names = [db.name for db in databases]
                result[f"{rg_name}/{server_name}"] = db_names

        return func.HttpResponse(str(result), status_code=200)

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)