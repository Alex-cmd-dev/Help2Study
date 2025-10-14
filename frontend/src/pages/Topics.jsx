import NavBar from "../components/NavBar";
import FlashcardTopics from "../components/ListofTopics";

function Topics() {
  return (
    <div className="min-h-screen bg-background">
      <NavBar />
      <div className="pt-20">
        <FlashcardTopics />
      </div>
    </div>
  );
}

export default Topics;
