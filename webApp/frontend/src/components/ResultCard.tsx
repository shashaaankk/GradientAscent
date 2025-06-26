// frontend/src/components/ResultCard.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Clock, TrendingUp, Mountain, MapPin, Star } from "lucide-react";
import { TrailStats } from "../types";

interface ResultCardProps {
  trail: TrailStats & { name: string; location?: string };
}

export const ResultCard = ({ trail }: ResultCardProps) => {
  // derived values
  const elevationGain = trail.max_elevation_m - trail.min_elevation_m;
  const avgSlope = trail.length_3d_m
    ? ((elevationGain / trail.length_3d_m) * 100).toFixed(1) + "%"
    : "–";

  // difficulty color
  let diffColor = "bg-green-500";
  if (trail.predicted_difficulty === "Moderate") diffColor = "bg-yellow-500";
  if (trail.predicted_difficulty === "Hard") diffColor = "bg-red-500";

  // star‐rating count
  const stars =
    trail.predicted_difficulty === "Easy" ? 2 :
    trail.predicted_difficulty === "Moderate" ? 3 :
    5;

  return (
    <Card className="max-w-4xl mx-auto shadow-lg border-0 bg-gradient-to-br from-background to-muted/20">
      <CardHeader className="pb-4">
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-2xl font-bold mb-2">
              {trail.name}
            </CardTitle>
            {trail.location && (
              <div className="flex items-center text-muted-foreground text-sm">
                <MapPin className="w-4 h-4 mr-1" />
                {trail.location}
              </div>
            )}
          </div>
          <Badge className={`${diffColor} text-white text-lg px-4 py-2`}>
            {trail.predicted_difficulty}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-5 h-5 text-emerald-600" />
              <span className="text-sm font-medium text-emerald-700">
                Distance
              </span>
            </div>
            <div className="text-2xl font-bold text-emerald-800">
              {trail.length_3d_m.toFixed(2)} m
            </div>
          </div>

          <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
            <div className="flex items-center justify-between mb-2">
              <Mountain className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-medium text-blue-700">
                Elevation
              </span>
            </div>
            <div className="text-2xl font-bold text-blue-800">
              {elevationGain.toFixed(0)} m
            </div>
          </div>

          <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
            <div className="flex items-center justify-between mb-2">
              <Clock className="w-5 h-5 text-orange-600" />
              <span className="text-sm font-medium text-orange-700">
                Est. Time
              </span>
            </div>
            <div className="text-2xl font-bold text-orange-800">
              {trail.predicted_duration_hm}
            </div>
          </div>
        </div>

        {/* ▶ Recommended Hikes */}
        <div className="bg-muted/50 rounded-lg p-4">
          <h4 className="font-semibold mb-3">Recommended Hikes</h4>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
            {trail.nearest_hikes.map((hike, idx) => (
              <div
                key={idx}
                className="bg-white rounded-lg overflow-hidden border border-gray-200"
              >

                {/* Metrics */}
                <div className="p-3 space-y-1">
                  <div className="font-medium">
                    {hike.duration_hm} · {hike.length_3d_m.toFixed(0)} m
                  </div>
                  <div className="text-gray-600 text-xs">
                    ↑{hike.uphill_m.toFixed(0)} m · ↓{hike.downhill_m.toFixed(0)} m
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
