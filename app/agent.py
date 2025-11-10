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
from google.genai import types
from google.adk.tools import AgentTool


from google.adk.agents import Agent
from google.adk.apps.app import App

from .tools.tools_native import app_int_cloud_snowflake_connector
from .prompts import root_agent_instructions, cloud_snowflake_agent_instructions

import vertexai
import os

# Helper function to get environment variables
def get_env_var(key):
    value = os.getenv(key)
    if value is None or not value.strip():
        raise ValueError(f"Environment variable '{key}' not found or is empty.")
    return value

# Load required env variables
root_agent_model = get_env_var("ROOT_AGENT_MODEL")
cloud_snowflake_agent_model = get_env_var("SNOWFLAKE_AGENT_MODEL")
project_id = get_env_var("GOOGLE_CLOUD_PROJECT_ID")
region = get_env_var("GOOGLE_CLOUD_LOCATION")

# Initialize Vertex AI
vertexai.init(project=project_id, location=region)

# Define Cloud SQL Posgres Server Agent
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
