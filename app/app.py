import os
import json
from PIL import Image
from openai import AzureOpenAI

from dotenv import load_dotenv 
import gradio as gr  
from azure.cosmos import exceptions, CosmosClient, PartitionKey  

load_dotenv()
env_path = "./.env"
load_dotenv(dotenv_path=env_path, override=True)

OPENAI_DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

openai_client = AzureOpenAI(
    azure_endpoint= os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-02-01",
)

# # CosmosDB configuration
cosmos_client = CosmosClient.from_connection_string(os.getenv("COSMOSDB_CONNECTION_STRING"))  
database_name = os.getenv("COSMOSDB_DB_NAME")
container_name = os.getenv("COSMOSDB_CONTAINER_NAME")  
database = cosmos_client.get_database_client(database_name)  
container = database.get_container_client(container_name)  

def get_member_ids():  
    # Query to get member names  
    query = "SELECT c.memberid FROM c"  
    items = list(container.query_items(  
        query=query,  
        enable_cross_partition_query=True  
    ))  
    return [item['memberid'] for item in items]  

def get_member_profile(memeber_id):  
    # Query to get member profile  
    query = f"SELECT * FROM c WHERE c.memberid = '{memeber_id}'"  
    items = list(container.query_items(  
        query=query,  
        enable_cross_partition_query=True  
    ))

    path = os.path.join(f"C:/Users/hyssh/coach_assistant/images/{memeber_id}.png")
    img = Image.open(path)    

    return items[0] if items else {"memberid":"No profile found."}, img

def update_member_profile_photo():  
    # Placeholder for conversation history  
    return "Conversation history will be displayed here."  

def run(message, history, member_id, member_profile):
    system_message = """You're an assistant for Coach who is a personal health coach for members.
    Use following Memeber Information and help Coach to assist the member.

    ## Member Information
    {{member_information}}
    """
    # get member profile
    member_profile = get_member_profile(member_id)
    system_message = system_message.replace("{{member_information}}",str(member_profile))
        
    history_openai_format = []

    if len(history) == 0:        
        history_openai_format.append({"role": "system", "content": system_message})
    else: 
        history_openai_format.append({"role": "system", "content": system_message})
        for human, assistant in history:
            history_openai_format.append({"role": "user", "content": human })
            history_openai_format.append({"role": "assistant", "content":assistant})

    history_openai_format.append({"role": "user", "content": message})

    # res, history_openai_format = run_chat(history_openai_format, functions, available_functions, ENGINE, verbose=False)
    response = openai_client.chat.completions.create(
        model=OPENAI_DEPLOYMENT_NAME,
        messages=history_openai_format,
        temperature=0.1
    )
    return response.choices[0].message.content



with gr.Blocks() as demo:  
    with gr.Row():  
        with gr.Column():  
            member_id = gr.Dropdown(label="SELECT Member name", choices=get_member_ids())  
            # display image based on the memberid
            member_image = gr.Image( height=500, width=500, label="Patient Profile Image")
            # Display JSON
            member_profile = gr.Textbox(label="Member profile details", interactive=False ) 

            # Handle member selection event
            member_id.change(fn=get_member_profile, inputs=member_id, outputs=[member_profile, member_image])  
        with gr.Column():  
            # Check member data has been selected
            if member_profile != None:
                chat = gr.ChatInterface(fn=run,
                                        additional_inputs=[member_id, member_profile],
                                )
            else:
                gr.Info("Please select a member to start the chat.")


if __name__ == "__main__":  
    demo.launch()  
