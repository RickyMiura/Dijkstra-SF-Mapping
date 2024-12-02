from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from fastapi.middleware.cors import CORSMiddleware
import pickle
from geopy.distance import geodesic
import logging
import networkx as nx

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

# Initialize Geopy
geolocator = Nominatim(user_agent="shortest-path-app")

# Define the request schema
class PathRequest(BaseModel):
    start_address: str
    end_address: str

# Geocode address to coordinates
def get_coordinates(address: str):
    location = geolocator.geocode(address)
    if not location:
        raise HTTPException(status_code=400, detail=f"Address '{address}' not found.")
    return location.latitude, location.longitude

# Map coordinates to the nearest graph node using precomputed node data
def map_to_node(coords):
    # Find the closest node based on geodesic distance
    closest_node = min(
        node_coordinates.keys(),
        key=lambda node: geodesic(coords, node_coordinates[node]).meters,
    )
    return closest_node

# Shortest path endpoint
@app.post("/api/py/shortest-path")
async def shortest_path(request: PathRequest):
    try:
        # Log the received request
        logger.info(f"Received request with start: {request.start_address}, end: {request.end_address}")
        
        # Geocode the start and end addresses
        start_coords = get_coordinates(request.start_address)
        end_coords = get_coordinates(request.end_address)
        logger.info(f"Start coordinates: {start_coords}, End coordinates: {end_coords}")
        
        # Map coordinates to graph nodes
        start_node = map_to_node(start_coords)
        end_node = map_to_node(end_coords)
        logger.info(f"Start node: {start_node}, End node: {end_node}")
        
        # Compute the shortest path
        path = nx.shortest_path(G, source=start_node, target=end_node, weight="length")
        path_coords = [(node_coordinates[node][0], node_coordinates[node][1]) for node in path]
        
        # Return the path and directions
        return {"path": path_coords, "directions": [f"Walk from {request.start_address} to {request.end_address}."]}
    except Exception as e:
        logger.error(f"Error in shortest_path: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
