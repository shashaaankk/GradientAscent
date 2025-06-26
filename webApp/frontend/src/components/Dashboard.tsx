
import { UploadSection } from "./UploadSection";
import { TrailSelector } from "./TrailSelector";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface DashboardProps {
  onTrailAnalysis: (trailData: any) => void;
}

export const Dashboard = ({ onTrailAnalysis }: DashboardProps) => {
  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">
          <span className="bg-gradient-to-r from-emerald-600 to-blue-600 bg-clip-text text-transparent">
            Trail Analysis Dashboard
          </span>
        </h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Upload your GPX file or select from our curated collection of popular trails to get detailed insights and recommendations.
        </p>
      </div>

      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle>Analyze Your Trail</CardTitle>
          <CardDescription>
            Choose how you'd like to get started with your trail analysis
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="upload" className="space-y-6">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="upload">Upload GPX File</TabsTrigger>
              <TabsTrigger value="select">Trail Recommendations</TabsTrigger>
            </TabsList>
            
            <TabsContent value="upload" className="space-y-4">
              <UploadSection onTrailAnalysis={onTrailAnalysis} />
            </TabsContent>
            
            <TabsContent value="select" className="space-y-4">
              <TrailSelector onTrailAnalysis={onTrailAnalysis} />
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};
