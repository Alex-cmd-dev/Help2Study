import NavBar from "../components/NavBar";
import ListofTopics from "../components/ListofTopics";

function Flashcards() {
  return (
    <div
      className="flex justify-center items-center min-h-screen"
      data-theme="night"
    >
      <NavBar></NavBar>
      <ListofTopics></ListofTopics>

    </div>
  );
}

export default Flashcards;
