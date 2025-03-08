import NavBar from "../components/NavBar";
import FlashcardTopics from "../components/ListofTopics";

function Topics() {
  return (
    <div
      className="flex justify-center items-center min-h-screen"
      data-theme="night"
    >
      <NavBar></NavBar>
      <FlashcardTopics></FlashcardTopics>

    </div>
  );
}

export default Topics;
