import { useNavigate } from "react-router-dom";
import api from "../api";
import { useState, useEffect } from "react";

function ListofTopics() {
  const [topics, setTopics] = useState([]);

  const items = [
    { id: 1, title: "Dashboard", url: "/dashboard" },
    { id: 2, title: "Profile", url: "/profile" },
    { id: 3, title: "Settings", url: "/settings" },
    { id: 4, title: "Messages", url: "/messages" },
    { id: 5, title: "Analytics", url: "/analytics" },
  ];

  // Function to handle redirection
  const getTopics = () => {
    api
      .get("/api/topics/")
      .then((res) => res.data)
      .then((data) => {
        setNotes(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  return (
    <div className="w-full max-w-md mx-auto mt-8">
      <h2 className="text-xl font-semibold mb-4">Flashcard Topics</h2>
      <div className="space-y-3">
        {items.map((item) => (
          <div
            key={item.id}
            onClick={() => handleRedirect(item.url)}
            className="bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-lg shadow cursor-pointer transition-all duration-200 transform hover:scale-102"
          >
            <div className="flex justify-between items-center">
              <span className="font-medium">{item.title}</span>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
export default ListofTopics;
