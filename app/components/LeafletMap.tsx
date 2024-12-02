"use client";

import React, { useRef, useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

type LeafletMapProps = {
  path: [number, number][] | null;
};

const LeafletMap: React.FC<LeafletMapProps> = ({ path }) => {
  const mapRef = useRef<L.Map | null>(null);

  useEffect(() => {
    // Initialize the map if it hasn't been initialized already
    if (!mapRef.current) {
      mapRef.current = L.map("map", {
        center: [37.7749, -122.4194], // Default center (San Francisco)
        zoom: 13,
      });

      // Add the tile layer
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(mapRef.current);
    }

    // If a path is provided, add it to the map
    if (path && mapRef.current) {
      // Clear existing layers (if any)
      mapRef.current.eachLayer((layer) => {
        if (layer instanceof L.Polyline) {
          mapRef.current?.removeLayer(layer);
        }
      });

      // Add the new path
      const polyline = L.polyline(path, { color: "blue" }).addTo(mapRef.current);

      // Fit the map to the polyline
      mapRef.current.fitBounds(polyline.getBounds());
    }

    // Cleanup function to remove the map instance
    return () => {
      if (mapRef.current) {
        mapRef.current.off();
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, [path]); // Re-run effect whenever `path` changes

  return <div id="map" style={{ height: "100%", width: "100%" }} />;
};

export default LeafletMap;
