// frontend/src/types.ts

export interface NearestHike {
  duration_hm:     string;
  length_3d_m:     number;
  uphill_m:        number;
  downhill_m:      number;
  break_time_hm:   string;
  image?:         string;   // URL for the thumbnail
}

export interface TrailStats {
  length_3d_m:           number;
  uphill_m:              number;
  downhill_m:            number;
  min_elevation_m:       number;
  max_elevation_m:       number;
  break_time_sec:        number;
  observed_duration_hm:  string;
  predicted_duration_hm: string;
  predicted_difficulty:  string;
  nearest_hikes:         NearestHike[];
}
