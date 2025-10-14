import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { BookOpen, LogOut, Upload } from "lucide-react";

function NavBar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <Link to="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <BookOpen className="h-6 w-6" />
            <span className="text-xl font-bold">Help2Study</span>
          </Link>

          <div className="flex items-center gap-2">
            <Link to="/">
              <Button variant="ghost" size="sm">
                <Upload className="h-4 w-4 mr-2" />
                Upload
              </Button>
            </Link>
            <Link to="/topics">
              <Button variant="ghost" size="sm">
                <BookOpen className="h-4 w-4 mr-2" />
                Flashcards
              </Button>
            </Link>
            <Link to="/logout">
              <Button variant="ghost" size="sm">
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
