import NavBar from "@/components/NavBar";
import DisplayFlascards from "@/components/DisplayFlashcards";


function Flashcards() {
  return (
    <div className="min-h-screen bg-background">
      <NavBar />
      <div className="pt-20">
        <DisplayFlascards />
      </div>
    </div>
  );
}

export default Flashcards;
