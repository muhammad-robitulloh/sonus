import json
import os
import datetime

class LabelPackager:
    def __init__(self, output_dir="exported_demos"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_dossier(self, track_info, analysis_report):
        """Generate a complete technical dossier for label submission."""
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        track_name = os.path.basename(track_info.get("file_path", "unknown_track"))
        
        dossier = {
            "track_title": track_name,
            "artist": "Vareon (Sonus Project)",
            "submission_date": timestamp,
            "technical_specs": {
                "bpm": track_info.get("bpm"),
                "key": track_info.get("key"),
                "integrated_lufs": analysis_report.get("mastering_report", {}).get("lufs", {}).get("integrated_lufs"),
                "true_peak_db": analysis_report.get("mastering_report", {}).get("true_peak", {}).get("true_peak_db"),
                "stereo_mono_compatibility": analysis_report.get("stereo_report", {}).get("low_side_ratio") < 0.15
            },
            "emotional_profile": {
                "density_contrast": analysis_report.get("density_report", {}).get("contrast_ratio"),
                "vibe_tags": ["Melodic Dubstep", "Cinematic", "High Energy"] # Placeholder logic
            },
            "production_notes": analysis_report.get("findings", [])
        }
        
        # Save as JSON
        json_path = os.path.join(self.output_dir, f"{track_name}_dossier.json")
        with open(json_path, 'w') as f:
            json.dump(dossier, f, indent=4)
            
        # Save as readable TXT report for A&R
        txt_path = os.path.join(self.output_dir, f"{track_name}_tech_sheet.txt")
        with open(txt_path, 'w') as f:
            f.write(f"--- TECHNICAL SUBMISSION SHEET ---\n")
            f.write(f"Track: {dossier['track_title']}\n")
            f.write(f"Artist: {dossier['artist']}\n")
            f.write(f"Date: {dossier['submission_date']}\n\n")
            
            f.write("[TECHNICAL SPECS]\n")
            f.write(f"BPM: {dossier['technical_specs']['bpm']}\n")
            f.write(f"Key: {dossier['technical_specs']['key']}\n")
            f.write(f"Loudness: {dossier['technical_specs']['integrated_lufs']:.1f} LUFS (Target: -14.0)\n")
            f.write(f"True Peak: {dossier['technical_specs']['true_peak_db']:.2f} dBTP\n\n")
            
            f.write("[SONUS ANALYSIS]\n")
            f.write(f"Contrast Ratio (Intro vs Drop): {dossier['emotional_profile']['density_contrast']:.2f}\n")
            f.write("Production Notes:\n")
            for note in dossier['production_notes']:
                f.write(f"- {note}\n")
                
        return json_path
