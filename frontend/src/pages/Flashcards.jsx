import NavBar from "@/components/NavBar";
import DisplayFlascards from "@/components/DisplayFlashcards";


function Flashcards() {

  return (
    <div
      className="flex justify-center items-center min-h-screen"
      data-theme="night"
    >
      <NavBar></NavBar>
      <DisplayFlascards></DisplayFlascards>
    </div>
  );
}

export default Flashcards;
