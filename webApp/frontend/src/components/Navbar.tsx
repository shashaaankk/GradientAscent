
import { Mountain } from "lucide-react";
import { Button } from "@/components/ui/button";

export const Navbar = () => {
  return (
    <nav className="bg-background/95 backdrop-blur-sm border-b border-border sticky top-0 z-50">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div className="w-10 h-10 bg-white rounded-md flex items-center justify-center">
            <img
                src="/logo_3.png"
                alt="Logo"
                className="w-180 h-180 object-contain rounded"
                />
          </div>
          <span className="text-xl font-bold bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">
            Gradient Ascent
          </span>
        </div>
        
        <Button variant="outline" className="md:hidden">
          Menu
        </Button>
      </div>
    </nav>
  );
};
