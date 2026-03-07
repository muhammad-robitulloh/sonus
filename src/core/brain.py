import os
import time
import json
from analysis.micro_analyzer import MicroAnalyzer
from analysis.advanced_dsp import AdvancedDSPEngine
from analysis.sidechain_logic import SidechainLogic
from analysis.psycho_masking import PsychoMaskingEngine
from analysis.harmonic_analyzer import HarmonicAnalyzer
from analysis.reference_matcher import ReferenceMatcher
from analysis.lyric_phonetics import LyricPhonetics
from bridge.creative_context import CreativeContextBridge
from generation.synth_engine import PyoSynthEngine
from interface.live_monitor import LiveMonitor

class SonusBrain:
    def __init__(self, project_path=None):
        self.project_path = project_path or os.getcwd()
        self.state = {
            "current_track": None,
            "bpm": None,
            "key": None,
            "genre": "Melodic Dubstep",
            "lyrics": []
        }
        self.synth = None 
        self.monitor = None
        self.knowledge = self._load_knowledge()
        print(f"🧠 Sonus initialized at: {self.project_path}")

    def _load_knowledge(self):
        """Loads label standards and VST recipes."""
        base_path = os.path.dirname(os.path.dirname(__file__))
        standards_path = os.path.join(base_path, 'knowledge', 'label_standards.json')
        vst_path = os.path.join(base_path, 'knowledge', 'vst_recipes.json')
        
        try:
            with open(standards_path, 'r') as f:
                standards = json.load(f)
            with open(vst_path, 'r') as f:
                vst = json.load(f)
            return {"standards": standards, "vst": vst}
        except Exception as e:
            print(f"⚠️ Error loading knowledge base: {e}")
            return {"standards": {}, "vst": {}}

    def compare_to_reference(self, reference_path):
        """Compare current track to a professional reference track."""
        if not self.state["current_track"]:
            return {"error": "No track loaded."}
        
        print(f"👻 Ghost Producer: Comparing to {reference_path}...")
        try:
            matcher = ReferenceMatcher(self.state["current_track"], reference_path)
            return matcher.compare_spectrum()
        except Exception as e:
            return {"error": f"Comparison failed: {str(e)}"}

    def analyze_lyric_phonetics(self, text):
        """Analyze lyric text for acoustic presence (Phonetic Power)."""
        print(f"🎙️ Analyzing phonetic cutting power...")
        try:
            analyzer = LyricPhonetics(text)
            return analyzer.analyze_cutting_power()
        except Exception as e:
            return {"error": f"Phonetic analysis failed: {str(e)}"}

    def start_live_monitor(self):
        """Start the live real-time audio monitor."""
        if not self.monitor:
             self.monitor = LiveMonitor()
        self.monitor.start_monitoring()

    def analyze_psycho_masking(self):
        """Analyze audibility using psychoacoustic models."""
        if not self.state["current_track"]:
            return {"error": "No track loaded."}
        
        print(f"🦻 Simulating human hearing on {self.state['current_track']}...")
        try:
            engine = PsychoMaskingEngine(self.state["current_track"])
            return engine.analyze_masking()
        except Exception as e:
            return {"error": f"Psychoacoustic analysis failed: {str(e)}"}

    def analyze_harmonics_and_transients(self):
        """Analyze even/odd harmonics and transient stress."""
        if not self.state["current_track"]:
            return {"error": "No track loaded."}
        
        print(f"🧬 Analyzing harmonic texture and transient peak stress...")
        try:
            analyzer = HarmonicAnalyzer(self.state["current_track"])
            h_report = analyzer.analyze_harmonics()
            t_report = analyzer.transient_check()
            
            return {
                "harmonics": h_report,
                "transients": t_report,
                "findings": h_report['findings'] + t_report['findings']
            }
        except Exception as e:
            return {"error": f"Harmonic analysis failed: {str(e)}"}

    def get_generative_prompt(self):
        """Get a narrative prompt for creative discussion with Gemini."""
        bridge = CreativeContextBridge(self.state)
        # Mock analysis data to include
        extra = {"loudness": "-14.0 LUFS", "vibe": "Cinematic/Heavy"}
        return bridge.generate_prompt_context(extra)

    def critique_production(self, label_key=None):
        """Perform a deep, objective technical critique, optionally targeting a label."""
        if not self.state["current_track"]:
            return {"error": "No track loaded."}

        print(f"🔍 Analyzing for {label_key or 'Standard'} targets...")
        
        try:
            analyzer = MicroAnalyzer(self.state["current_track"])
            sidechain = SidechainLogic(self.state["current_track"])
            
            report = analyzer.get_full_critique()
            sc_report = sidechain.detect_kick_vs_sub()
            
            report['sidechain_report'] = sc_report
            report['findings'] += sc_report['findings']
            
            # Label-Specific Checks
            if label_key and label_key in self.knowledge['standards']:
                std = self.knowledge['standards'][label_key]
                if report['mastering_report']['lufs']['integrated_lufs'] < std['lufs_target']:
                    report['findings'].append(f"LABEL ({label_key}): integrated LUFS still too quiet for their signature sound.")
                
            return report
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def get_vst_recipe(self, plugin="serum", patch="ophelia_bass"):
        """Returns literal parameter recipes for plugins."""
        if plugin in self.knowledge['vst'] and patch in self.knowledge['vst'][plugin]:
            return self.knowledge['vst'][plugin][patch]
        return None
        """Perform a deep, objective technical critique of the loaded track."""
        if not self.state["current_track"]:
            return {"error": "No track loaded. Use load_track() first."}

        print(f"🔍 Performing deep micro-analysis on {self.state['current_track']}...")
        
        try:
            analyzer = MicroAnalyzer(self.state["current_track"])
            report = analyzer.get_full_critique()
            return report
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def analyze_audio(self):
        """
        Analyzes the loaded track for BPM, Key, and Spectral features.
        Uses Librosa (or similar) in the implementation phase.
        """
        if not self.state["current_track"]:
            return "No track loaded. Use load_track() first."
        
        # Simulation of analysis for now
        print(f"🎧 Analyzing {self.state['current_track']}...")
        time.sleep(1) # Simulating processing time
        
        # Mock results
        self.state["bpm"] = 120
        self.state["key"] = "C Major"
        
        return {
            "bpm": self.state["bpm"],
            "key": self.state["key"],
            "spectral_centroid": "Bright", # Mock
            "dynamic_range": "-14 LUFS"   # Mock
        }

    def production_advice(self, context="mixing"):
        """Provides mixing or mastering advice based on analysis."""
        if context == "mixing":
            return [
                "Suggested: Low-cut anything below 100Hz except Kick/Bass.",
                "Check for frequency masking between 200-400Hz (mud)."
            ]
        elif context == "mastering":
            return [
                "Target -14 LUFS for streaming services.",
                "Ensure true peak does not exceed -1.0 dBTP."
            ]
        return []

    def creative_suggest(self, topic="lyrics"):
        """Generates creative ideas."""
        if topic == "lyrics":
            return "Why not try a rhyme scheme of AABB for the chorus to make it catchy?"
        elif topic == "melody":
            return "Try a pentatonic scale run starting on the root note for a stable hook."
        return "Keep experimenting!"
