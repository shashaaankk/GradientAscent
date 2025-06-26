
import { Button } from "@/components/ui/button";
import { Upload, ArrowRight } from "lucide-react";

interface HeroSectionProps {
  onGetStarted: () => void;
}

export const HeroSection = ({ onGetStarted }: HeroSectionProps) => {
  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-blue-50 to-orange-50" />
      
      {/* Mountain silhouette decoration */}
      <div className="absolute bottom-0 left-0 right-0 h-64 bg-gradient-to-t from-emerald-100/30 to-transparent">
        <svg viewBox="0 0 1200 320" className="absolute bottom-0 w-full h-full">
          <path
            d="M0,320L80,290L160,250L240,200L320,170L400,140L480,120L560,100L640,130L720,160L800,180L880,200L960,220L1040,250L1120,280L1200,310L1200,320L0,320Z"
            fill="url(#mountainGradient)"
            opacity="0.3"
          />
          <defs>
            <linearGradient id="mountainGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="50%" stopColor="#3b82f6" />
              <stop offset="100%" stopColor="#f97316" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      <div className="relative z-10 text-center px-4 max-w-4xl mx-auto">
        <h1 className="text-5xl md:text-7xl font-bold mb-6">
          <span className="bg-gradient-to-r from-emerald-600 via-blue-600 to-orange-500 bg-clip-text text-transparent">
            Gradient Ascent
          </span>
        </h1>
        
        <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Smarter, Safer, Smoother Hiking
        </p>
        
        <p className="text-lg text-muted-foreground mb-12 max-w-xl mx-auto">
          Understand trail difficulty, get accurate time estimates, and discover similar hiking routes tailored to you.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button 
            onClick={onGetStarted}
            size="lg" 
            className="bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-700 hover:to-blue-700 text-white px-8 py-3 rounded-full text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
          >
            Get Started
            <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
          
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto">
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🎯</span>
            </div>
            <h3 className="font-semibold text-lg mb-2">Smart Analysis</h3>
            <p className="text-muted-foreground">AI-powered trail difficulty assessment</p>
          </div>
          
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">⏱️</span>
            </div>
            <h3 className="font-semibold text-lg mb-2">Time Estimates</h3>
            <p className="text-muted-foreground">Accurate completion time predictions</p>
          </div>
          
          <div className="text-center">
            <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl">🏔️</span>
            </div>
            <h3 className="font-semibold text-lg mb-2">Trail Discovery</h3>
            <p className="text-muted-foreground">Find similar routes you'll love</p>
          </div>
        </div>
      </div>
    </div>
  );
};
