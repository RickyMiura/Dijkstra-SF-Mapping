from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from geopy.geocoders import Nominatim
import osmnx as ox
import networkx as nx
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS Middleware

# Initialize FastAPI and Geopy
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins (or specify your frontend's URL)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

geolocator = Nominatim(user_agent="shortest-path-app")

# Load the graph
G = ox.graph_from_place("San Francisco, California, USA", network_type="walk")

# Define request schema
class PathRequest(BaseModel):
    start_address: str
    end_address: str

# Geocode address to coordinates
def get_coordinates(address: str):
    location = geolocator.geocode(address)
    if not location:
        raise HTTPException(status_code=400, detail=f"Address '{address}' not found.")
    return location.latitude, location.longitude

# Map coordinates to graph nodes
def map_to_node(coords):
    return ox.nearest_nodes(G, X=coords[1], Y=coords[0])

# Shortest path endpoint
@app.post("/api/py/shortest-path")
async def shortest_path(request: PathRequest):
    try:
        # Add detailed logging
        logger.debug(f"Received request with start: {request.start_address}, end: {request.end_address}")
        
        start_coords = get_coordinates(request.start_address)
        logger.debug(f"Start coordinates: {start_coords}")
        
        end_coords = get_coordinates(request.end_address)
        logger.debug(f"End coordinates: {end_coords}")
        
        start_node = map_to_node(start_coords)
        logger.debug(f"Start node: {start_node}")
        
        end_node = map_to_node(end_coords)
        logger.debug(f"End node: {end_node}")
        
        path = nx.shortest_path(G, source=start_node, target=end_node, weight="length")
        logger.debug(f"Found path: {path}")
        
        path_coords = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in path]
        
        return {"path": path_coords, "directions": [f"Walk from {request.start_address} to {request.end_address}."]}
    except Exception as e:
        logger.error(f"Error in shortest_path: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
