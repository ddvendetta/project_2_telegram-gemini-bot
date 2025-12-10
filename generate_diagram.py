# Import necessary classes from the diagrams library to create architecture diagrams.
from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.compute import Server
from diagrams.gcp.compute import Functions
from diagrams.onprem.client import User
from diagrams.saas.chat import Telegram
# Using AIPlatform as a stand-in for the Gemini API, as it's a suitable representation.
from diagrams.gcp.ml import AIPlatform

# Define global graph attributes for a consistent and dark-themed look.
# These attributes control the appearance of the entire diagram.
graph_attr = {
    "bgcolor": "#0D1117",    # Background color of the diagram
    "fontcolor": "white",       # Default font color for all text
    "splines": "ortho",       # Use orthogonal lines for edges, giving a clean, grid-like look
    "nodesep": "1.0",         # Separation between nodes
    "ranksep": "1.0",         # Separation between ranks (levels) of nodes
    "pad": "0.5"              # Padding around the diagram
}

# Define global edge attributes for styling the connections between nodes.
edge_attr = {
    "color": "white"          # Edge color
}

# --- Default Top-to-Bottom Diagram ---
# This section generates the primary architecture diagram with a standard top-to-bottom flow.
with Diagram("Telegram Bot Architecture", show=False, filename="telegram_bot_architecture", graph_attr=graph_attr, edge_attr=edge_attr):
    # Define the end-user of the system.
    user = User("User", fontcolor="white")
    
    # Cluster for components hosted on Google Cloud Platform.
    with Cluster("Google Cloud Platform", graph_attr={"bgcolor": "#161b22", "pencolor": "white", "fontcolor": "white"}):
        # The Cloud Function that acts as a webhook for Telegram.
        webhook = Functions("Telegram Webhook", fontcolor="white")
        
    # Cluster for services external to our direct control.
    with Cluster("External Services", graph_attr={"bgcolor": "#161b22", "pencolor": "white", "fontcolor": "white"}):
        # Telegram's API which sends updates to our webhook.
        tg_api = Telegram("Telegram API", fontcolor="white")
        # The Gemini API for processing messages.
        gemini_api = AIPlatform("Gemini API", fontcolor="white")

    # Define the flow of data: User -> Telegram -> Webhook -> Gemini API and back.
    user >> tg_api >> webhook >> gemini_api
    gemini_api >> webhook >> tg_api >> user

# --- Left-to-Right (LR) Version ---
# This section generates the same architecture but with a horizontal, left-to-right layout.
graph_attr_lr = graph_attr.copy()
graph_attr_lr["rankdir"] = "LR"  # Set the rank direction to Left to Right.

with Diagram("Telegram Bot Architecture (LR)", show=False, filename="telegram_bot_architecture_lr", graph_attr=graph_attr_lr, edge_attr=edge_attr):
    user = User("User", fontcolor="white")
    
    with Cluster("Google Cloud Platform", graph_attr={"bgcolor": "#161b22", "pencolor": "white", "fontcolor": "white"}):
        webhook = Functions("Telegram Webhook", fontcolor="white")
        
    with Cluster("External Services", graph_attr={"bgcolor": "#161b22", "pencolor": "white", "fontcolor": "white"}):
        tg_api = Telegram("Telegram API", fontcolor="white")
        gemini_api = AIPlatform("Gemini API", fontcolor="white")

    # The data flow remains the same, but the visual layout is horizontal.
    user >> tg_api >> webhook >> gemini_api
    gemini_api >> webhook >> tg_api >> user

# --- Strict Linear Version (One Line) ---
# This version simplifies the diagram to a single, straight-line flow for clarity.
# It removes the clusters and the return path to focus on the primary request path.
graph_attr_linear = graph_attr.copy()
graph_attr_linear["rankdir"] = "LR"
graph_attr_linear["nodesep"] = "2.0" # Increase node separation for a more spaced-out line.

with Diagram("Telegram Bot Linear Flow", show=False, filename="telegram_bot_linear", graph_attr=graph_attr_linear, edge_attr=edge_attr):
    # Define the nodes in the linear sequence.
    user = User("User", fontcolor="white")
    tg_api = Telegram("Telegram API", fontcolor="white")
    webhook = Functions("Telegram Webhook", fontcolor="white")
    gemini_api = AIPlatform("Gemini API", fontcolor="white")

    # Define the simple, unidirectional flow.
    user >> tg_api >> webhook >> gemini_api
