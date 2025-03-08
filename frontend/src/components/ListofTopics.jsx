import { Link } from "react-router-dom" // Assuming you're using React Router
import { CalendarIcon } from "lucide-react"

import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

// This would typically come from a database or props
const topics = [
  {
    id: "1",
    title: "JavaScript Fundamentals",
    createdAt: "2023-05-15T10:00:00Z",
  },
  {
    id: "2",
    title: "React Hooks",
    createdAt: "2023-08-22T14:30:00Z",
  },
  {
    id: "3",
    title: "CSS Grid & Flexbox",
    createdAt: "2023-06-10T09:15:00Z",
  },
  {
    id: "4",
    title: "TypeScript Basics",
    createdAt: "2023-09-05T16:45:00Z",
  },
  {
    id: "5",
    title: "Data Structures",
    createdAt: "2023-04-03T11:20:00Z",
  },
]

function FlashcardTopics() {
  // Sort topics by creation date (newest first)
  const sortedTopics = [...topics].sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())

  return (
    <div className="container py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Flashcard Topics</h1>
        <p className="text-muted-foreground mt-2">Select a topic to view its flashcards</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {sortedTopics.map((topic) => (
          <Link to={`/topics/${topic.id}`} key={topic.id}>
            <Card className="h-full transition-all hover:shadow-md">
              <CardHeader>
                <CardTitle>{topic.title}</CardTitle>
                <CardDescription className="flex items-center gap-1 mt-2">
                  <CalendarIcon className="h-4 w-4" />
                  <span>
                    {new Date(topic.createdAt).toLocaleDateString("en-US", {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                    })}
                  </span>
                </CardDescription>
              </CardHeader>
              <CardFooter>
                <div className="text-sm text-muted-foreground">Click to view cards</div>
              </CardFooter>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default FlashcardTopics

