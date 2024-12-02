"use client";

import React, { useState, useRef, useEffect } from "react";

type AutocompleteProps = {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
};

export const Autocomplete: React.FC<AutocompleteProps> = ({
  label,
  value,
  onChange,
  placeholder,
}) => {
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const isClickingSuggestion = useRef(false); // Flag to track clicks on suggestions

  useEffect(() => {
    if (typeof window === "undefined" || !window.google) {
      console.error("Google Places API not loaded.");
      return;
    }

    const autocompleteService = new window.google.maps.places.AutocompleteService();

    const fetchSuggestions = (input: string) => {
      if (!input) {
        setSuggestions([]);
        return;
      }

      autocompleteService.getPlacePredictions({ input }, (predictions, status) => {
        if (status === window.google.maps.places.PlacesServiceStatus.OK && predictions) {
          setSuggestions(predictions.map((prediction) => prediction.description));
        }
      });
    };

    fetchSuggestions(value);
  }, [value]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isClickingSuggestion.current) {
        // Reset the flag and skip clearing suggestions
        isClickingSuggestion.current = false;
        return;
      }

      if (inputRef.current && !inputRef.current.contains(event.target as Node)) {
        setSuggestions([]); // Clear suggestions when clicking outside
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="flex flex-col space-y-2">
      <label className="text-gray-700 font-medium">{label}</label>
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
        {suggestions.length > 0 && (
          <ul className="absolute left-0 right-0 mt-1 bg-white border border-gray-300 rounded-md shadow-lg z-10">
            {suggestions.map((suggestion, index) => (
              <li
                key={index}
                onMouseDown={() => {
                  // Set the flag to indicate a suggestion is being clicked
                  isClickingSuggestion.current = true;
                }}
                onClick={() => {
                  onChange(suggestion); // Update input value with the selected suggestion
                  setSuggestions([]);   // Clear suggestions immediately
                }}
                className="px-3 py-2 cursor-pointer hover:bg-gray-100 text-gray-900 font-medium"
              >
                {suggestion}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};
