"use client"

import { useParams, Link } from "react-router-dom"
import { useState, useEffect } from "react"
import { ChevronLeft, ChevronRight, RotateCcw, ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import api from "@/api"

function DisplayFlashcards() {
  const { id } = useParams()
  const [flashcards, setFlashcards] = useState([])
  const [currentCardIndex, setCurrentCardIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)

  useEffect(() => {
    getFlashcards()
  }, [id])

  const getFlashcards = () => {
    api
      .get(`/api/flashcards/${id}/`)
      .then((res) => res.data)
      .then((data) => {
        setFlashcards(data)
      })
      .catch((err) => alert(err))
  }

  const handleNextCard = () => {
    if (currentCardIndex < flashcards.length - 1) {
      setCurrentCardIndex(currentCardIndex + 1)
      setIsFlipped(false)
    }
  }

  const handlePrevCard = () => {
    if (currentCardIndex > 0) {
      setCurrentCardIndex(currentCardIndex - 1)
      setIsFlipped(false)
    }
  }

  const handleFlipCard = () => {
    setIsFlipped(!isFlipped)
  }

  // If no flashcards are loaded yet
  if (flashcards.length === 0) {
    return <div className="container py-10">Loading...</div>
  }

  const currentCard = flashcards[currentCardIndex]

  return (
    <div className="container py-10 max-w-4xl mx-auto">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <Link to="/topics" className="flex items-center text-muted-foreground hover:text-foreground mb-2">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Topics
          </Link>
          <h1 className="text-3xl font-bold tracking-tight">{flashcards.topic}</h1>
          <p className="text-muted-foreground mt-1">
            Card {currentCardIndex + 1} of {flashcards.length}
          </p>
        </div>
        <Button variant="outline" size="sm" onClick={() => setIsFlipped(false)}>
          <RotateCcw className="mr-2 h-4 w-4" />
          Reset
        </Button>
      </div>

      {/* Tailwind 4.0 optimized approach */}
      <div className="w-full aspect-[3/2] max-w-2xl mx-auto mb-8 cursor-pointer relative" onClick={handleFlipCard}>
        {/* Using absolute positioning and opacity for a smoother transition */}
        <Card
          className={`absolute inset-0 w-full h-full flex flex-col items-center justify-center p-8 text-center transition-opacity duration-300 ${
            isFlipped ? "opacity-0 pointer-events-none" : "opacity-100"
          }`}
        >
          <div className="text-sm text-muted-foreground mb-2">TERM</div>
          <div className="text-2xl font-semibold">{currentCard.question}</div>
          <div className="mt-6 text-sm text-muted-foreground">Click to flip</div>
        </Card>

        <Card
          className={`absolute inset-0 w-full h-full flex flex-col items-center justify-center p-8 text-center transition-opacity duration-300 bg-muted/20 ${
            isFlipped ? "opacity-100" : "opacity-0 pointer-events-none"
          }`}
        >
          <div className="text-sm text-muted-foreground mb-2">DEFINITION</div>
          <div className="text-xl">{currentCard.answer}</div>
          <div className="mt-6 text-sm text-muted-foreground">Click to flip back</div>
        </Card>
      </div>

      {/* Navigation */}
      <div className="flex justify-center gap-4">
        <Button variant="outline" size="lg" onClick={handlePrevCard} disabled={currentCardIndex === 0}>
          <ChevronLeft className="mr-2 h-5 w-5" />
          Previous
        </Button>
        <Button
          variant="default"
          size="lg"
          onClick={handleNextCard}
          disabled={currentCardIndex === flashcards.length - 1}
        >
          Next
          <ChevronRight className="ml-2 h-5 w-5" />
        </Button>
      </div>
    </div>
  )
}

export default DisplayFlashcards

