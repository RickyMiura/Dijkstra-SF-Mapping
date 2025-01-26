## Introduction

This project is a demonstration of Dijkstra's algorithm for real-life pathfinding. Given two addresses in San Francisco, it computes
the shortest path between them using Dijkstra's algorithm.

## How It Works

Under the hood, the process for computing a path is:
1. Geocode the addresses into coordinates with the Google Maps API
2. Given a set of coordinates, use a KD tree to find the closest nodes in the graph to use as the starting and ending points.
3. Use Dijkstra's algorithm to find the shortest path between the two nodes. 

The app is built with Nextjs for the frontent and fastapi for the backend. 

## Demo

You can check out the app on Vercel [here](https://algorithms-project-dijkstra.vercel.app/)


## Running Locally

First, create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Then, install the dependencies:

```bash
npm install
# or
yarn
# or
pnpm install
```

Then, run the development server(python dependencies will be installed automatically here):

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

The FastApi server will be running on [http://127.0.0.1:8000](http://127.0.0.1:8000)

# Contributors
1) Ricky Miura
2) John Green
3) Eli Mecinas Cruz
