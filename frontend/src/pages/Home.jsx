import NavBar from "../components/NavBar";
import FileUploadForm from "../components/FIleUploadForm";

function Home() {
  return (
    <div className="min-h-screen bg-background">
      <NavBar />
      <div className="flex justify-center items-center min-h-[calc(100vh-4rem)] px-4">
        <FileUploadForm />
      </div>
    </div>
  );
}

export default Home;
