
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Clock, TrendingUp, Mountain, ArrowRight } from "lucide-react";

const recommendedHikes = [
  {
    id: "1",
    name: "Meadow Creek Trail",
    distance: "7.2 km",
    elevationGain: "380 m",
    difficulty: "Easy",
    estimatedTime: "2h 30min",
    difficultyColor: "bg-green-500",
    image: "photo-1469474968028-56623f02e42e"
  },
  {
    id: "2",
    name: "Summit Ridge Path",
    distance: "11.8 km",
    elevationGain: "720 m",
    difficulty: "Moderate",
    estimatedTime: "4h 15min",
    difficultyColor: "bg-yellow-500",
    image: "photo-1482938289607-e9573fc25ebb"
  },
  {
    id: "3",
    name: "Pine Valley Loop",
    distance: "5.4 km",
    elevationGain: "240 m",
    difficulty: "Easy",
    estimatedTime: "1h 45min",
    difficultyColor: "bg-green-500",
    image: "photo-1509316975850-ff9c5deb0cd9"
  },
  {
    id: "4",
    name: "Highland Peak",
    distance: "14.6 km",
    elevationGain: "980 m",
    difficulty: "Hard",
    estimatedTime: "5h 30min",
    difficultyColor: "bg-red-500",
    image: "photo-1470071459604-3b5ec3a7fe05"
  }
];

export const RecommendedHikes = () => {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-3xl font-bold mb-4">
          <span className="bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">
            Recommended Hikes
          </span>
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {recommendedHikes.map((hike) => (
          <Card key={hike.id} className="group hover:shadow-lg transition-all duration-300 cursor-pointer">
            <div className="relative h-48 overflow-hidden rounded-t-lg">
              <img
                src={`https://images.unsplash.com/${hike.image}?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80`}
                alt={hike.name}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              />
              <div className="absolute top-3 right-3">
                <Badge className={`${hike.difficultyColor} text-white`}>
                  {hike.difficulty}
                </Badge>
              </div>
            </div>
            
            <CardContent className="p-4 space-y-3">
              <h3 className="font-semibold text-lg group-hover:text-emerald-600 transition-colors">
                {hike.name}
              </h3>
              
              <div className="space-y-2 text-sm text-muted-foreground">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <TrendingUp className="w-4 h-4 mr-1 text-emerald-600" />
                    <span>{hike.distance}</span>
                  </div>
                  <div className="flex items-center">
                    <Mountain className="w-4 h-4 mr-1 text-blue-600" />
                    <span>{hike.elevationGain}</span>
                  </div>
                </div>
                
                <div className="flex items-center">
                  <Clock className="w-4 h-4 mr-1 text-orange-600" />
                  <span>{hike.estimatedTime}</span>
                </div>
              </div>
              
              <Button 
                variant="outline" 
                size="sm" 
                className="w-full group-hover:bg-emerald-50 group-hover:border-emerald-300 group-hover:text-emerald-700 transition-colors"
              >
                View Details
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
