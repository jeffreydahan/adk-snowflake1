# Native Tools defintion

import os
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset

def get_env_var(key):
    value = os.getenv(key)
    if value is None or not value.strip():
        raise ValueError(f"Environment variable '{key}' not found or is empty.")
    return value

project_id = get_env_var("GOOGLE_CLOUD_PROJECT_ID")

# Set variables for Integration Connector - Cloud SQL SQL Server
cloud_snowflake_app_int_region = get_env_var("CLOUD_SNOWFLAKE_APP_INT_REGION")
cloud_snowflake_app_int_connection = get_env_var("CLOUD_SNOWFLAKE_APP_INT_CONNECTION")
cloud_snowflake_app_int_tool_name_prefix = os.getenv("CLOUD_SNOWFLAKE_APP_INT_TOOL_NAME_PREFIX") # Optional, can be None
cloud_snowflake_app_int_tool_instructions = os.getenv("CLOUD_SNOWFLAKE_APP_INT_TOOL_INSTRUCTIONS") # Optional, can be None

# Build Integration Connector object - Cloud SQL SQL Server
app_int_cloud_snowflake_connector = ApplicationIntegrationToolset(
    project=project_id,
    location=cloud_snowflake_app_int_region, 
    connection=cloud_snowflake_app_int_connection, 
    actions=["ExecuteCustomQuery"],
    tool_name_prefix=cloud_snowflake_app_int_tool_name_prefix,
    tool_instructions=cloud_snowflake_app_int_tool_instructions
)


