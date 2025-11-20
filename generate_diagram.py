from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.compute import Server
from diagrams.gcp.compute import Functions
from diagrams.onprem.client import User
from diagrams.saas.chat import Telegram

# Since we don't have a specific Gemini icon in the standard library yet, 
# we can use a generic AI/ML icon or just a custom node if we had an image.
# For now, we'll use a generic Server node labeled "Gemini API" or similar.
# Or better, let's check if there's something in diagrams.gcp.ml
from diagrams.gcp.ml import AIPlatform

graph_attr = {
    "bgcolor": "#0D1117",
    "fontcolor": "white",
    "splines": "ortho",
    "nodesep": "1.0",
    "ranksep": "1.0",
    "pad": "0.5"
}

edge_attr = {
    "color": "white"
}

with Diagram("Telegram Bot Architecture", show=False, filename="telegram_bot_architecture", graph_attr=graph_attr, edge_attr=edge_attr):
    user = User("User", fontcolor="white")
    
    with Cluster("Google Cloud Platform", graph_attr={"bgcolor": "#161b22", "pencolor": "white", "fontcolor": "white"}):
        webhook = Functions("Telegram Webhook", fontcolor="white")
        
    with Cluster("External Services", graph_attr={"bgcolor": "#161b22", "pencolor": "white", "fontcolor": "white"}):
        tg_api = Telegram("Telegram API", fontcolor="white")
        gemini_api = AIPlatform("Gemini API", fontcolor="white")

    user >> tg_api >> webhook >> gemini_api
    gemini_api >> webhook >> tg_api >> user

# Left-to-Right Version
graph_attr_lr = graph_attr.copy()
graph_attr_lr["rankdir"] = "LR"

with Diagram("Telegram Bot Architecture (LR)", show=False, filename="telegram_bot_architecture_lr", graph_attr=graph_attr_lr, edge_attr=edge_attr):
    user = User("User", fontcolor="white")
    
    with Cluster("Google Cloud Platform", graph_attr={"bgcolor": "#161b22", "pencolor": "white", "fontcolor": "white"}):
        webhook = Functions("Telegram Webhook", fontcolor="white")
        
    with Cluster("External Services", graph_attr={"bgcolor": "#161b22", "pencolor": "white", "fontcolor": "white"}):
        tg_api = Telegram("Telegram API", fontcolor="white")
        gemini_api = AIPlatform("Gemini API", fontcolor="white")

    user >> tg_api >> webhook >> gemini_api
    gemini_api >> webhook >> tg_api >> user

# Strict Linear Version (One Line)
graph_attr_linear = graph_attr.copy()
graph_attr_linear["rankdir"] = "LR"
graph_attr_linear["nodesep"] = "2.0"

with Diagram("Telegram Bot Linear Flow", show=False, filename="telegram_bot_linear", graph_attr=graph_attr_linear, edge_attr=edge_attr):
    user = User("User", fontcolor="white")
    tg_api = Telegram("Telegram API", fontcolor="white")
    webhook = Functions("Telegram Webhook", fontcolor="white")
    gemini_api = AIPlatform("Gemini API", fontcolor="white")

    user >> tg_api >> webhook >> gemini_api
