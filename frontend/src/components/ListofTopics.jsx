import { Link } from "react-router-dom";
import { CalendarIcon } from "lucide-react";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import api from "@/api";
import { useState, useEffect } from "react";

function FlashcardTopics() {
  const [topics, setTopics] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getTopics();
  }, []);

  const getTopics = () => {
    setIsLoading(true);
    api
      .get("/api/topics/")
      .then((res) => res.data)
      .then((data) => {
        setTopics(data);
        setIsLoading(false);
      })
      .catch((err) => {
        setError("Failed to load topics");
        setIsLoading(false);
        console.error(err);
      });
  };

  // Sort topics by creation date (newest first)
  const sortedTopics = [...topics].sort(
    (a, b) =>
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  );

  if (isLoading) {
    return <div className="container py-10">Loading topics...</div>;
  }

  if (error) {
    return <div className="container py-10 text-red-500">{error}</div>;
  }

  return (
    <div className="container py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Flashcard Topics</h1>
        <p className="text-muted-foreground mt-2">
          Select a topic to view its flashcards
        </p>
      </div>

      {sortedTopics.length === 0 ? (
        <p className="text-muted-foreground">
          No topics available. Create new Flashcard to get started.
        </p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {sortedTopics.map((topic) => (
            <Link to={`/topics/flashcards/${topic.id}`} key={topic.id}>
              <Card className="h-full transition-all hover:shadow-md">
                <CardHeader>
                  <CardTitle>{topic.name}</CardTitle>
                  <CardDescription className="flex items-center gap-1 mt-2">
                    <CalendarIcon className="h-4 w-4" />
                    <span>
                      {new Date(topic.created_at).toLocaleDateString("en-US", {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                      })}
                    </span>
                  </CardDescription>
                </CardHeader>
                <CardFooter>
                  <div className="text-sm text-muted-foreground">
                    Click to view cards
                  </div>
                </CardFooter>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default FlashcardTopics;
