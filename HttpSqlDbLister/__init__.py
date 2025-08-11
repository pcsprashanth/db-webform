import logging
import json
import azure.functions as func  # type: ignore
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request to list SQL servers and databases for a specific resource group.')

    try:
        # Get resource group name from query parameters
        rg_name = req.params.get('resource_group')
        if not rg_name:
            return func.HttpResponse(
                json.dumps({"error": "Missing resource_group query parameter."}),
                status_code=400,
                mimetype="application/json"
            )

        credential = DefaultAzureCredential()
        subscription_id = "25229114-2ec3-4b44-bb5b-649a554894bc"
        sql_client = SqlManagementClient(credential, subscription_id)

        result = {}

        servers = sql_client.servers.list_by_resource_group(rg_name)
        for server in servers:
            server_name = server.name
            databases = sql_client.databases.list_by_server(rg_name, server_name)
            db_names = [db.name for db in databases]
            result[server_name] = db_names

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )