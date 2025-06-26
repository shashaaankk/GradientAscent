# backend/gpx_pipeline.py
import gpxpy

def analyze_gpx_stream(stream):
    """
    Read a GPX file-like stream, parse it, compute stats, and return a dict.
    """
    # 1. Parse the GPX
    gpx = gpxpy.parse(stream)


    # 2. Flatten all track points
    points = [
        pt
        for track in gpx.tracks
        for seg in track.segments
        for pt in seg.points
    ]
    if len(points) < 2:
        raise ValueError("Not enough data points")
    
    # DUMMY LOGIC: TO BE REPLACED WITH REAL ANALYSIS

    # 3. Compute core stats
    length_3d = gpx.length_3d()
    duration = gpx.get_duration() or 0
    uphill, downhill = gpx.get_uphill_downhill()
    elevations = [pt.elevation for pt in points]
    min_elev, max_elev = min(elevations), max(elevations)

    # 4. Time, speed, break
    start, end = points[0].time, points[-1].time
    total_time = (end - start).total_seconds()
    speed = length_3d / duration if duration else 0
    break_time = total_time - duration

    # 5. Difficulty heuristic
    difficulty = "Easy"
    if uphill > 300 or length_3d > 10_000:
        difficulty = "Moderate"
    if uphill > 600 or length_3d > 20_000:
        difficulty = "Hard"

    # 6. Return everything in one dict
    stats = {
        "duration_sec":       round(duration, 2),
        "length_3d_m":        round(length_3d, 2),
        "min_elevation_m":    round(min_elev, 2),
        "max_elevation_m":    round(max_elev, 2),
        "break_time_sec":     round(break_time, 2),
        "uphill_m":           round(uphill, 2),
        "downhill_m":         round(downhill, 2),
        "speed_mps":          round(speed, 2),
        "difficulty":         difficulty,
    }

    return stats