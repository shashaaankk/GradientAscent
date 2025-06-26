
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Clock, TrendingUp, Mountain, MapPin, Star } from "lucide-react";

interface ResultCardProps {
  trail: {
    name: string;
    distance: string;
    elevationGain: string;
    avgSlope: string;
    difficulty: string;
    estimatedTime: string;
    difficultyColor: string;
    location?: string;
  };
}

export const ResultCard = ({ trail }: ResultCardProps) => {
  return (
    <Card className="max-w-4xl mx-auto shadow-lg border-0 bg-gradient-to-br from-background to-muted/20">
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-2xl font-bold mb-2">{trail.name}</CardTitle>
            {trail.location && (
              <div className="flex items-center text-muted-foreground">
                <MapPin className="w-4 h-4 mr-1" />
                <span className="text-sm">{trail.location}</span>
              </div>
            )}
          </div>
          <Badge className={`${trail.difficultyColor} text-white text-lg px-4 py-2`}>
            {trail.difficulty}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-5 h-5 text-emerald-600" />
              <span className="text-sm font-medium text-emerald-700">Distance</span>
            </div>
            <div className="text-2xl font-bold text-emerald-800">{trail.distance}</div>
          </div>
          
          <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
            <div className="flex items-center justify-between mb-2">
              <Mountain className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-medium text-blue-700">Elevation</span>
            </div>
            <div className="text-2xl font-bold text-blue-800">{trail.elevationGain}</div>
          </div>
          
          <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
            <div className="flex items-center justify-between mb-2">
              <Clock className="w-5 h-5 text-orange-600" />
              <span className="text-sm font-medium text-orange-700">Est. Time</span>
            </div>
            <div className="text-2xl font-bold text-orange-800">{trail.estimatedTime}</div>
          </div>
        </div>

        {/* Additional Info */}
        <div className="bg-muted/50 rounded-lg p-4">
          <h4 className="font-semibold mb-3">Trail Details</h4>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-muted-foreground">Average Slope:</span>
              <span className="ml-2 font-medium">{trail.avgSlope}</span>
            </div>
            <div>
              <span className="text-muted-foreground">Difficulty Rating:</span>
              <div className="flex items-center ml-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <Star 
                    key={star} 
                    className={`w-4 h-4 ${
                      (trail.difficulty === 'Easy' && star <= 2) ||
                      (trail.difficulty === 'Moderate' && star <= 3) ||
                      (trail.difficulty === 'Hard' && star <= 5)
                        ? 'fill-yellow-400 text-yellow-400' 
                        : 'text-gray-300'
                    }`} 
                  />
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 pt-4">
          <Button 
            className="flex-1 bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-700 hover:to-blue-700 text-white"
          >
            <MapPin className="w-4 h-4 mr-2" />
            View on Map
          </Button>
          <Button variant="outline" className="flex-1">
            Export Analysis
          </Button>
          <Button variant="outline" className="flex-1">
            Share Trail
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
