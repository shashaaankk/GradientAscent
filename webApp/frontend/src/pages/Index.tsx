
import { useState } from "react";
import { Navbar } from "../components/Navbar";
import { HeroSection } from "../components/HeroSection";
import { Dashboard } from "../components/Dashboard";
import { UploadSection } from "../components/UploadSection";
import { ResultCard } from "../components/ResultCard";
import { RecommendedHikes } from "../components/RecommendedHikes";

const Index = () => {
  const [currentView, setCurrentView] = useState<'hero' | 'dashboard'>('hero');
  const [uploadedTrail, setUploadedTrail] = useState<any>(null);

  const handleGetStarted = () => {
    setCurrentView('dashboard');
  };

  const handleTrailAnalysis = (trailData: any) => {
    setUploadedTrail(trailData);
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      {currentView === 'hero' ? (
        <HeroSection onGetStarted={handleGetStarted} />
      ) : (
        <div className="container mx-auto px-4 py-8 max-w-6xl">
          <UploadSection onTrailAnalysis={handleTrailAnalysis} />
          
          {uploadedTrail && (
            <div className="mt-8">
              <ResultCard trail={uploadedTrail} />
            </div>
          )}
          
        </div>
      )}
    </div>
  );
};

export default Index;
