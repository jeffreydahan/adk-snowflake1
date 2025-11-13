# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import google.auth
from google.genai import types
from google.adk.tools import AgentTool
from google.adk.agents import Agent
from google.adk.apps.app import App
from dotenv import load_dotenv
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset

from .prompts import root_agent_instructions, cloud_snowflake_agent_instructions

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Load required env variables
root_agent_model = os.getenv("ROOT_AGENT_MODEL")
cloud_snowflake_agent_model = os.getenv("SNOWFLAKE_AGENT_MODEL")
region = os.getenv("GOOGLE_CLOUD_LOCATION")

# print loaded env variables for debugging
print(f"Loaded Environment Variables:")
print(f"GOOGLE_CLOUD_PROJECT: {project_id}")
print(f"GOOGLE_CLOUD_LOCATION: {region}")
print(f"ROOT_AGENT_MODEL: {root_agent_model}")
print(f"SNOWFLAKE_AGENT_MODEL: {cloud_snowflake_agent_model}")

# Define Snowflake Agent
cloud_snowflake_app_int_region = os.getenv("CLOUD_SNOWFLAKE_APP_INT_REGION")
cloud_snowflake_app_int_connection = os.getenv("CLOUD_SNOWFLAKE_APP_INT_CONNECTION")
cloud_snowflake_app_int_tool_name_prefix = os.getenv("CLOUD_SNOWFLAKE_APP_INT_TOOL_NAME_PREFIX") # Optional, can be None
cloud_snowflake_app_int_tool_instructions = os.getenv("CLOUD_SNOWFLAKE_APP_INT_TOOL_INSTRUCTIONS") # Optional, can be None

# print loaded env variables for debugging
print(f"CLOUD_SNOWFLAKE_APP_INT_REGION: {cloud_snowflake_app_int_region}")
print(f"CLOUD_SNOWFLAKE_APP_INT_CONNECTION: {cloud_snowflake_app_int_connection}")
print(f"CLOUD_SNOWFLAKE_APP_INT_TOOL_NAME_PREFIX: {cloud_snowflake_app_int_tool_name_prefix}")
print(f"CLOUD_SNOWFLAKE_APP_INT_TOOL_INSTRUCTIONS: {cloud_snowflake_app_int_tool_instructions}")

# Build Integration Connector object - Cloud SQL SQL Server
app_int_cloud_snowflake_connector = ApplicationIntegrationToolset(
    project=project_id,
    location=cloud_snowflake_app_int_region, 
    connection=cloud_snowflake_app_int_connection, 
    actions=["ExecuteCustomQuery"],
    tool_name_prefix=cloud_snowflake_app_int_tool_name_prefix,
    tool_instructions=cloud_snowflake_app_int_tool_instructions
)

# Define the Snowflake Agent with tools and instructions
cloud_snowflake_agent = Agent(
    model=cloud_snowflake_agent_model,
    name="cloud_snowflake_agent",
    instruction=cloud_snowflake_agent_instructions,
    tools=[app_int_cloud_snowflake_connector],
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)

# Define the root agent with tools and instructions
root_agent = Agent(
    model=root_agent_model,
    name="RootAgent",
    instruction=root_agent_instructions,
    tools=[AgentTool(agent=cloud_snowflake_agent)],
    generate_content_config=types.GenerateContentConfig(temperature=0.01),
)
