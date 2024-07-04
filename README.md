# Coach Assistant Application

## Overview

The Coach Assistant Application is designed to assist a personal health coach by providing information about members and enabling chat interactions. It leverages Azure OpenAI for chat capabilities and Azure CosmosDB for storing and retrieving member data. The application interface is built using Gradio for easy interaction.
Features

- Member Selection: Allows the coach to select a member from a dropdown list.
- Profile Display: Displays the selected member's profile details and profile image.
- Chat Interface: Provides a chat interface for the coach to interact with the assistant, which uses member information to assist in the conversation.

## Prerequisites

- Python 3.7 or higher
- Azure OpenAI and CosmosDB accounts
- .env file with the following environment variables:
    - DEPLOYMENT_NAME
    - OPENAI_API_BASE
    - OPENAI_API_KEY
    - COSMOSDB_CONNECTION_STRING
    - COSMOSDB_DB_NAME
    - COSMOSDB_CONTAINER_NAME

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repository/coach-assistant.git  
cd coach-assistant  
```

2. Install dependencies:

```bash
pip install -r requirements.txt  
```

3. Set up environment variables:

Create a .env file in the root directory.
Add the required environment variables as mentioned in the Prerequisites section.

##  Usage 

1. Run the application:

```bash
python app.py  
```

2. Interact with the interface:

Select a member from the dropdown list to view their profile details and image.
Use the chat interface to interact with the assistant.

## Code Explanation

### Imports and Configuration

Libraries: The code imports necessary libraries such as os, json, PIL, openai, dotenv, gradio, and azure.cosmos.
Environment Variables: Loads environment variables from a .env file.

### Azure OpenAI and CosmosDB Clients

AzureOpenAI: Initializes the Azure OpenAI client using environment variables.
CosmosDB: Configures the CosmosDB client and retrieves the database and container clients.

### Functions

get_member_ids: Retrieves a list of member IDs from CosmosDB.
get_member_profile: Retrieves the profile details and image of a specific member.
update_member_profile_photo: Placeholder function for updating the member profile photo.
run: Handles the chat interaction by formatting the message history and calling the Azure OpenAI API for responses.

### Gradio Interface

Gradio Blocks: Sets up the Gradio interface with rows and columns for member selection, profile display, and chat interaction.
Event Handling: Updates the profile details and image based on the selected member.

### Main Execution

Launch Gradio App: Launches the Gradio application when the script is run.
