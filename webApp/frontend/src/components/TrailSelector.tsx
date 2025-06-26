
import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { MapPin, TrendingUp, Clock } from "lucide-react";

interface TrailSelectorProps {
  onTrailAnalysis: (trailData: any) => void;
}

const popularTrails = [
  {
    id: "1",
    name: "Eagle Peak Trail",
    distance: "12.4 km",
    elevationGain: "890 m",
    avgSlope: "14%",
    difficulty: "Hard",
    estimatedTime: "4h 30min",
    difficultyColor: "bg-red-500",
    location: "Rocky Mountain National Park"
  },
  {
    id: "2",
    name: "Sunset Ridge Loop",
    distance: "6.8 km",
    elevationGain: "320 m",
    avgSlope: "8%",
    difficulty: "Easy",
    estimatedTime: "2h 15min",
    difficultyColor: "bg-green-500",
    location: "Blue Ridge Mountains"
  },
  {
    id: "3",
    name: "Valley View Trail",
    distance: "9.6 km",
    elevationGain: "520 m",
    avgSlope: "11%",
    difficulty: "Moderate",
    estimatedTime: "3h 45min",
    difficultyColor: "bg-yellow-500",
    location: "Cascade Range"
  },
  {
    id: "4",
    name: "Alpine Lakes Circuit",
    distance: "15.2 km",
    elevationGain: "1200 m",
    avgSlope: "16%",
    difficulty: "Hard",
    estimatedTime: "6h 15min",
    difficultyColor: "bg-red-500",
    location: "Sierra Nevada"
  }
];

export const TrailSelector = ({ onTrailAnalysis }: TrailSelectorProps) => {
  const [selectedTrail, setSelectedTrail] = useState<string>("");

  const handleTrailSelect = (trailId: string) => {
    setSelectedTrail(trailId);
    const trail = popularTrails.find(t => t.id === trailId);
    if (trail) {
      onTrailAnalysis(trail);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <Select onValueChange={handleTrailSelect}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select a popular trail to analyze..." />
          </SelectTrigger>
          <SelectContent>
            {popularTrails.map((trail) => (
              <SelectItem key={trail.id} value={trail.id}>
                <div className="flex items-center justify-between w-full">
                  <span className="font-medium">{trail.name}</span>
                  <div className="flex items-center space-x-2 ml-4">
                    <Badge 
                      className={`${trail.difficultyColor} text-white text-xs`}
                    >
                      {trail.difficulty}
                    </Badge>
                  </div>
                </div>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {popularTrails.map((trail) => (
          <Card 
            key={trail.id}
            className={`cursor-pointer transition-all duration-300 hover:shadow-lg ${
              selectedTrail === trail.id ? 'ring-2 ring-emerald-500 shadow-lg' : ''
            }`}
            onClick={() => handleTrailSelect(trail.id)}
          >
            <CardContent className="p-6">
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <h3 className="font-semibold text-lg">{trail.name}</h3>
                  <Badge className={`${trail.difficultyColor} text-white`}>
                    {trail.difficulty}
                  </Badge>
                </div>
                
                <div className="flex items-center text-muted-foreground text-sm">
                  <MapPin className="w-4 h-4 mr-1" />
                  {trail.location}
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center">
                    <TrendingUp className="w-4 h-4 mr-2 text-emerald-600" />
                    <span>{trail.distance}</span>
                  </div>
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-2 text-blue-600" />
                    <span>{trail.estimatedTime}</span>
                  </div>
                </div>

                <div className="text-xs text-muted-foreground">
                  Elevation: {trail.elevationGain} • Avg Slope: {trail.avgSlope}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
