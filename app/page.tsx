"use client";

import React, { useState } from "react";
import { Autocomplete } from "./components/Autocomplete";
import dynamic from "next/dynamic";
import axios from "axios";

// Dynamically import LeafletMap to prevent SSR issues
const LeafletMap = dynamic(() => import("./components/LeafletMap"), {
  ssr: false,
});

const HomePage = () => {
  const [startAddress, setStartAddress] = useState("");
  const [endAddress, setEndAddress] = useState("");
  const [path, setPath] = useState<[number, number][] | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchPath = async () => {
    setLoading(true);
    try {
      const response = await axios.post("/api/py/shortest-path", {
        start_address: startAddress,
        end_address: endAddress,
      });
      setPath(response.data.path);
    } catch (error) {
      console.error("Error fetching path:", error);
      alert("Failed to fetch the path. Please check your addresses.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-4">SF Shortest Path Finder</h1>
        <p className="text-center text-gray-700 mb-8">
          This app uses Dijkstra&apos;s algorithm to find the shortest path between two addresses.
          Input two addresses in San Francisco to find the shortest route between them! The source
          code can be found on GitHub{" "}
          <a href="https://github.com/jggreen3/algorithms-project-dijkstra" className="text-blue-600 hover:underline">
            here
          </a>.
        </p>
        <div className="grid gap-4 lg:grid-cols-3 lg:gap-8">
          {/* Address Entry */}
          <div className="space-y-4 flex flex-col justify-center lg:col-span-1">
            <Autocomplete
              label="Start Address"
              value={startAddress}        // Controlled value
              onChange={setStartAddress} // Updates state
              placeholder="Enter start address"
            />
            <Autocomplete
              label="End Address"
              value={endAddress}          // Controlled value
              onChange={setEndAddress}   // Updates state
              placeholder="Enter end address"
            />
            <button
              className={`mt-5 w-full py-2 px-4 rounded-md text-white font-semibold ${
                loading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
              }`}
              onClick={fetchPath}
              disabled={loading}
            >
              {loading ? "Loading..." : "Find Path"}
            </button>
          </div>

          {/* Map */}
          <div className="h-[500px] w-full lg:col-span-2">
            <LeafletMap path={path} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
