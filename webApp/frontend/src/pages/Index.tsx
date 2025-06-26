// frontend/src/pages/Index.tsx
import { useState } from "react";
import { Navbar } from "@/components/Navbar";
import { HeroSection } from "@/components/HeroSection";
import { UploadSection } from "@/components/UploadSection";
import { ResultCard } from "@/components/ResultCard";
import { TrailStats } from "../types";

const Index = () => {
  const [view, setView] = useState<"hero" | "dashboard">("hero");
  const [trail, setTrail] = useState<
    (TrailStats & { name: string; location?: string }) | null
  >(null);

  const handleGetStarted = () => setView("dashboard");

  const handleTrailAnalysis = (trailData: TrailStats) => {
    // Attach a dummy image URL to each of the first 3 recommendations
    const nearest_hikes = trailData.nearest_hikes.slice(0, 3).map((hike, i) => ({
      ...hike,
      image: `https://picsum.photos/seed/${i + 1}/300/180`,
    }));

    setTrail({
      name: "Your Hike",         // replace with real GPX name if you have it
      location: "Unknown",       // or from GPX metadata
      ...trailData,
      nearest_hikes,
    });
  };

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {view === "hero" ? (
        <HeroSection onGetStarted={handleGetStarted} />
      ) : (
        <div className="container mx-auto px-4 py-8 max-w-6xl">
          <UploadSection onTrailAnalysis={handleTrailAnalysis} />

          {trail && (
            <div className="mt-8">
              <ResultCard trail={trail} />
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Index;
