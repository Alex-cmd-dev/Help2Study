import NavBar from "../components/NavBar";
import FileUploadForm from "../components/FIleUploadForm";

function Home() {
  return (
    <div className="flex justify-center items-center min-h-screen" data-theme="night">
      <NavBar></NavBar>
      <FileUploadForm></FileUploadForm>
      
    </div>
  );
}

export default Home;
