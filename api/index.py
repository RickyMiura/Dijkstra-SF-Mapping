from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
from geopy.distance import geodesic
import logging
import networkx as nx
import time
import googlemaps
import dotenv
import os
from pykdtree.kdtree import KDTree
import numpy as np



dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI and add CORS middleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins (or specify your frontend's URL)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load the preprocessed graph and node coordinates
with open("graph_preprocessed.pickle", "rb") as f:
    data = pickle.load(f)
G = data["graph"]
node_coordinates = data["node_coordinates"]

# Build KD-tree for nearest neighbor queries
node_coords = np.array([(lat, lon) for lat, lon in node_coordinates.values()])
node_ids = list(node_coordinates.keys())
kd_tree = KDTree(node_coords)


# Initialize Geopy
gmaps = googlemaps.Client(key=os.getenv('NEXT_PUBLIC_GOOGLE_API_KEY'))

def get_coordinates(address: str):
    try:
        geocode_result = gmaps.geocode(address)
        if not geocode_result:
            raise HTTPException(status_code=400, detail=f"Address '{address}' not found.")
        
        location = geocode_result[0]["geometry"]["location"]
        return location["lat"], location["lng"]
    except Exception as e:
        logger.error(f"Error in geocoding: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to geocode address.")


# Define the request schema
class PathRequest(BaseModel):
    start_address: str
    end_address: str

def map_to_node(coords):
    lat, lon = coords
    distance, index = kd_tree.query(np.array([[lat, lon]]
))
    nearest_node = node_ids[index[0]]
    logger.info(f"KD-tree Closest Node: {nearest_node}, Distance: {distance}")
    return nearest_node


# Shortest path endpoint
@app.post("/api/py/shortest-path")
async def shortest_path(request: PathRequest):
    try:
        # Log the received request
        logger.info(f"Received request with start: {request.start_address}, end: {request.end_address}")

        # Geocode the start and end addresses
        start_coords = get_coordinates(request.start_address)
        end_coords = get_coordinates(request.end_address)
        
        # Map coordinates to graph nodes
        start_node = map_to_node(start_coords)
        end_node = map_to_node(end_coords)
        
        # Compute the shortest path
        path = nx.shortest_path(G, source=start_node, target=end_node, weight="length")
        path_coords = [(node_coordinates[node][0], node_coordinates[node][1]) for node in path]
        logger.info(path_coords)
        
        # Return the path and directions
        return {"path": path_coords, "directions": [f"Walk from {request.start_address} to {request.end_address}."]}
    except Exception as e:
        logger.error(f"Error in shortest_path: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
