
import { useState, useCallback } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, FileText, CheckCircle } from "lucide-react";
import { toast } from "@/hooks/use-toast";

interface UploadSectionProps {
  onTrailAnalysis: (trailData: any) => void;
}

export const UploadSection = ({ onTrailAnalysis }: UploadSectionProps) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [error, setError] = useState<string>(""); // Add error state

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    const gpxFile = files.find(file => file.name.toLowerCase().endsWith('.gpx'));
    
    if (gpxFile) {
      handleFileUpload(gpxFile);
    } else {
      toast({
        title: "Invalid file",
        description: "Please upload a GPX file.",
        variant: "destructive",
      });
    }
  }, []);

  const handleFileUpload = async (file: File) => {
    setIsUploading(true);
    setUploadedFile(file);
    setError("");      // clear any previous error

    // 1️⃣ Build FormData
    const formData = new FormData();
    formData.append("file", file);

    try {
      // 2️⃣ POST to Flask
      const res = await fetch("http://localhost:5000/api/process-gpx", {
        method: "POST",
        body: formData,
      });

      // 3️⃣ Parse JSON
      const data = await res.json();
      console.log("Response data:", data);

      if (!res.ok) {
        // Backend signaled error
        throw new Error(data.error || "Server error");
      }

      // 4️⃣ Pass real data back up
      onTrailAnalysis(data);

      // 5️⃣ Notify success
      toast({
        title: "Upload successful!",
        description: "Trail has been analyzed.",
      });

    } catch (err: any) {
      // 6️⃣ Handle failures
      console.error("Upload failed:", err);
      setError(err.message || "Upload failed");
      toast({
        title: "Upload failed",
        description: err.message || "Please try again.",
        variant: "destructive",
      });
    } finally {
      // 7️⃣ Done uploading
      setIsUploading(false);
    }
  };


  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.name.toLowerCase().endsWith('.gpx')) {
      handleFileUpload(file);
    } else {
      toast({
        title: "Invalid file",
        description: "Please upload a GPX file.",
        variant: "destructive",
      });
    }
  };

  return (
    <Card 
      className={`border-2 border-dashed transition-all duration-300 ${
        isDragOver 
          ? 'border-emerald-400 bg-emerald-50/50' 
          : 'border-muted-foreground/25 hover:border-emerald-300'
      }`}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <CardContent className="p-12 text-center">
        {isUploading ? (
          <div className="space-y-4">
            <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-blue-600 rounded-full flex items-center justify-center mx-auto animate-pulse">
              <FileText className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-lg font-semibold">Processing your trail...</h3>
            <p className="text-muted-foreground">Analyzing elevation data and calculating metrics</p>
          </div>
        ) : uploadedFile ? (
          <div className="space-y-4">
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto">
              <CheckCircle className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-lg font-semibold">File uploaded successfully!</h3>
            <p className="text-muted-foreground">{uploadedFile.name}</p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-blue-600 rounded-full flex items-center justify-center mx-auto">
              <Upload className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-lg font-semibold">Upload your GPX file</h3>
            <p className="text-muted-foreground">
              Drag and drop your GPX file here, or click to browse
            </p>
            <div className="pt-4">
              <input
                type="file"
                accept=".gpx"
                onChange={handleFileInputChange}
                className="hidden"
                id="gpx-upload"
              />
              <Button 
                asChild
                className="bg-gradient-to-r from-emerald-600 to-blue-600 hover:from-emerald-700 hover:to-blue-700"
              >
                <label htmlFor="gpx-upload" className="cursor-pointer">
                  Choose File
                </label>
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
