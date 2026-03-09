import click
import os
import sys
from colorama import init, Fore, Style

# --- TERMUX COMPATIBILITY LAYER ---
# Ensure system libraries (like libpulse.so) are found in Termux environment
if os.path.exists('/data/data/com.termux/files/usr/lib'):
    termux_lib = '/data/data/com.termux/files/usr/lib'
    if termux_lib not in os.environ.get('LD_LIBRARY_PATH', ''):
        os.environ['LD_LIBRARY_PATH'] = f"{os.environ.get('LD_LIBRARY_PATH', '')}:{termux_lib}".strip(':')
        # On some Linux/Android systems, we must re-exec to pick up LD_LIBRARY_PATH changes
        if not os.environ.get('SONUS_REEXEC'):
            os.environ['SONUS_REEXEC'] = '1'
            os.execv(sys.executable, [sys.executable] + sys.argv)
# ----------------------------------

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.brain import SonusBrain

init(autoreset=True)

@click.group()
def cli():
    """Sonus: AI Co-Producer & Creative Partner"""
    pass

@cli.command()
@click.argument('file_path', required=False)
def analyze(file_path):
    """Analyze an audio file for BPM, Key, and Spectral features."""
    brain = SonusBrain()
    
    if not file_path:
        click.echo(Fore.RED + "Error: Please provide a file path.")
        return

    click.echo(Fore.CYAN + f"Loading {file_path}...")
    result = brain.load_track(file_path)
    
    if "error" in result:
        click.echo(Fore.RED + result["error"])
        return

    analysis = brain.analyze_audio()
    
    click.echo(Fore.GREEN + "\n--- Analysis Results ---")
    click.echo(f"BPM: {analysis['bpm']}")
    click.echo(f"Key: {analysis['key']}")
    click.echo(f"Spectral Profile: {analysis['spectral_centroid']}")
    click.echo(f"Dynamic Range: {analysis['dynamic_range']}")

@cli.command()
@click.argument('file_path')
@click.option('--label', default=None, help='Target label: ophelia, monstercat_uncaged')
def critique(file_path, label):
    """Perform a deep, objective technical critique of your production."""
    brain = SonusBrain()
    
    click.echo(Fore.CYAN + f"🔬 Deep analyzing {file_path} for label: {label or 'Standard'}...")
    res = brain.load_track(file_path)
    if "error" in res:
        click.echo(Fore.RED + res["error"])
        return

    report = brain.critique_production(label_key=label)
    
    if "error" in report:
        click.echo(Fore.RED + report["error"])
        return

    click.echo(Fore.WHITE + Style.BRIGHT + "\n--- SONUS OBJECTIVE CRITIQUE REPORT ---")
    
    # Dynamics & Mastering
    click.echo(Fore.YELLOW + f"\n[DYNAMICS & MASTERING]")
    click.echo(f"  Peak (ISP): {report['mastering_report']['true_peak']['true_peak_db']:.2f} dB")
    click.echo(f"  Integrated LUFS: {report['mastering_report']['lufs']['integrated_lufs']:.1f}")
    click.echo(f"  Crest Factor (Punch): {report['dynamic_report']['crest_factor']:.2f}")

    # Sidechain/Masking
    click.echo(Fore.MAGENTA + f"\n[RHYTHMIC INTEGRITY]")
    click.echo(f"  Sidechain Masking Events: {report['sidechain_report']['masking_count']}")
    if report['sidechain_report']['masking_count'] > 0:
        click.echo(Fore.RED + f"  - Collision points: {', '.join(report['sidechain_report']['timestamps'])}")

    # Findings/Advice
    click.echo(Fore.GREEN + f"\n[ACTIONABLE ADVICE]")
    for find in report['findings']:
        click.echo(Fore.RED + f"  - {find}")
    if not report['findings']:
        click.echo(Fore.GREEN + "  - No major technical issues found. Ready for submission.")

    # Final Score
    score = report['overall_score']
    color = Fore.GREEN if score > 7 else (Fore.YELLOW if score > 4 else Fore.RED)
    click.echo(color + Style.BRIGHT + f"\nOVERALL PRODUCTION SCORE: {score:.1f}/10")
    click.echo(Fore.WHITE + "---------------------------------------")

@cli.command()
@click.option('--plugin', default='serum')
@click.option('--patch', default='ophelia_bass')
def recipe(plugin, patch):
    """Get literal parameter settings for VST plugins."""
    brain = SonusBrain()
    recipe_data = brain.get_vst_recipe(plugin, patch)
    
    if not recipe_data:
        click.echo(Fore.RED + f"Recipe not found for {plugin}/{patch}")
        return

    click.echo(Fore.CYAN + Style.BRIGHT + f"\n--- {plugin.upper()} RECIPE: {patch.upper()} ---")
    for key, val in recipe_data.items():
        click.echo(f"{Fore.GREEN}{key.replace('_', ' ').capitalize()}: {Fore.WHITE}{val}")

@cli.command()
@click.argument('file_path')
def vibe(file_path):
    """Deep analysis of vibe, genre, and transients using Essentia/Aubio."""
    brain = SonusBrain()
    click.echo(Fore.CYAN + f"🧬 Extracting deep features from {file_path}...")
    
    res = brain.load_track(file_path)
    if "error" in res:
        click.echo(Fore.RED + res["error"])
        return

    report = brain.deep_vibe_analysis()
    
    if "error" in report:
        click.echo(Fore.RED + report["error"])
        return

    click.echo(Fore.WHITE + Style.BRIGHT + "\n--- SONUS DEEP VIBE REPORT ---")
    
    # Vibe/Mood
    click.echo(Fore.YELLOW + f"\n[MOOD & ENERGY]")
    click.echo(f"  Vibe: {report['vibe']['vibe_estimate']}")
    click.echo(f"  Danceability: {report['vibe']['danceability']:.2f}")
    click.echo(f"  BPM (Aubio): {report['vibe']['tempo']:.1f} (Confidence: {report['vibe']['bpm_confidence']:.2f})")

    # Pitch
    click.echo(Fore.GREEN + f"\n[MELODIC CONTENT]")
    click.echo(f"  Avg Pitch: {report['pitch']['avg_pitch_hz']:.2f} Hz")
    click.echo(f"  Peak Pitch: {report['pitch']['max_pitch_hz']:.2f} Hz")

    # Transient
    click.echo(Fore.MAGENTA + f"\n[RHYTHMIC PRECISION]")
    click.echo(f"  Onset Count: {report['transient']['onset_count']}")
    click.echo(f"  Density: {report['transient']['onset_density']:.2f} (Events per sec)")

    click.echo(Fore.WHITE + "---------------------------------------")

@cli.command()
@click.option('--type', default='fm', help='Synthesis type: fm, sine')
def synth(type):
    """Get AI-powered synthesis suggestions using Pyo."""
    brain = SonusBrain()
    suggestion = brain.suggest_synthesis(type)
    click.echo(Fore.CYAN + "\n--- SONUS SYNTHESIS SUGGESTION ---")
    click.echo(suggestion)

@cli.command()
@click.argument('file_path')
def psycho(file_path):
    """Analyze audibility and masking using psychoacoustic models."""
    brain = SonusBrain()
    click.echo(Fore.CYAN + f"🦻 Analyzing perceived masking in {file_path}...")
    
    res = brain.load_track(file_path)
    if "error" in res:
        click.echo(Fore.RED + res["error"])
        return

    report = brain.analyze_psycho_masking()
    if "error" in report:
        click.echo(Fore.RED + report["error"])
        return

    click.echo(Fore.WHITE + Style.BRIGHT + "\n--- SONUS PSYCHOACOUSTIC REPORT ---")
    click.echo(f"  Detected Masking Points: {report['masking_points_count']}")
    for find in report['findings']:
        click.echo(Fore.RED + f"  - {find}")
    if not report['findings']:
        click.echo(Fore.GREEN + "  - Human audibility is clear. No major masking detected.")
    click.echo(Fore.WHITE + "---------------------------------------")

@cli.command()
@click.argument('file_path')
def harmonic(file_path):
    """Analyze harmonic texture (Odd/Even) and transient stress."""
    brain = SonusBrain()
    click.echo(Fore.CYAN + f"🧬 Analyzing harmonic structure of {file_path}...")
    
    res = brain.load_track(file_path)
    if "error" in res:
        click.echo(Fore.RED + res["error"])
        return

    report = brain.analyze_harmonics_and_transients()
    if "error" in report:
        click.echo(Fore.RED + report["error"])
        return

    click.echo(Fore.WHITE + Style.BRIGHT + "\n--- SONUS HARMONIC & TRANSIENT REPORT ---")
    
    # Harmonics
    click.echo(Fore.YELLOW + f"\n[HARMONIC TEXTURE]")
    click.echo(f"  Fundamental: {report['harmonics']['fundamental_hz']:.1f} Hz")
    click.echo(f"  Even Harmonic Ratio: {report['harmonics']['even_ratio']:.3f} (Warmth)")
    click.echo(f"  Odd Harmonic Ratio: {report['harmonics']['odd_ratio']:.3f} (Grit/Edge)")
    
    # Transients
    click.echo(Fore.MAGENTA + f"\n[TRANSIENT IMPACT]")
    click.echo(f"  Crest Factor: {report['transients']['crest_factor']:.1f} dB")

    # Actionable findings
    click.echo(Fore.GREEN + f"\n[TEXTURE ACTION ADVICE]")
    for find in report['findings']:
        click.echo(Fore.RED + f"  - {find}")
    if not report['findings']:
        click.echo(Fore.GREEN + "  - Sound texture and transients are well-balanced.")
    click.echo(Fore.WHITE + "---------------------------------------")

@cli.command()
@click.argument('file_path')
@click.option('--ref', required=True, help='Path to reference track')
def compare(file_path, ref):
    """Compare your track to a professional reference track."""
    brain = SonusBrain()
    click.echo(Fore.CYAN + f"👻 Ghost Producer: Comparing {file_path} to {ref}...")
    
    res = brain.load_track(file_path)
    if "error" in res:
        click.echo(Fore.RED + res["error"])
        return

    report = brain.compare_to_reference(ref)
    if "error" in report:
        click.echo(Fore.RED + report["error"])
        return

    click.echo(Fore.WHITE + Style.BRIGHT + "\n--- SONUS REFERENCE MATCH REPORT ---")
    
    # Band Comparison
    for band, diff in report['band_comparison'].items():
        color = Fore.GREEN if abs(diff) < 3 else (Fore.YELLOW if abs(diff) < 6 else Fore.RED)
        click.echo(f"  {band}: {color}{diff:+.1f} dB")
    
    # Actionable findings
    click.echo(Fore.GREEN + f"\n[ACTIONABLE ADVICE]")
    for find in report['findings']:
        click.echo(Fore.RED + f"  - {find}")
    if not report['findings']:
        click.echo(Fore.GREEN + "  - Your spectral balance is extremely close to the reference!")
    click.echo(Fore.WHITE + "---------------------------------------")

@cli.command()
@click.option('--text', required=True, help='Lyrics text to analyze')
def phonetics(text):
    """Analyze lyrics for phonetic cutting power (Acoustic Cutter)."""
    brain = SonusBrain()
    report = brain.analyze_lyric_phonetics(text)
    
    click.echo(Fore.WHITE + Style.BRIGHT + "\n--- SONUS PHONETIC ANALYSIS ---")
    click.echo(f"  Avg Cutting Score: {report['avg_cutting_score']:.2f}/5.0")
    
    for find in report['findings']:
        click.echo(Fore.RED + f"  - {find}")
    click.echo(Fore.WHITE + "---------------------------------------")

@cli.command()
def monitor():
    """Start the real-time audio monitor session."""
    brain = SonusBrain()
    brain.start_live_monitor()

@cli.command()
@click.option('--topic', default='lyrics', help='Topic: lyrics, melody, structure, creative')
def creative(topic):
    """Get creative suggestions or a generative narrative prompt."""
    brain = SonusBrain()
    
    if topic == 'creative':
        # Get generative context
        prompt_info = brain.get_generative_prompt()
        click.echo(Fore.BLUE + Style.BRIGHT + "\n--- SONUS GENERATIVE PROMPT (Take this to Gemini) ---")
        click.echo(prompt_info['narrative_prompt'])
        click.echo(Fore.WHITE + "\n--- JSON CONTEXT PAYLOAD ---")
        click.echo(prompt_info['json_payload'])
        return

    suggestion = brain.creative_suggest(topic)
    click.echo(Fore.YELLOW + f"\n--- Creative Suggestion ({topic}) ---")
    click.echo(suggestion)

@cli.command()
@click.option('--context', default='mixing', help='Context: mixing, mastering')
def production(context):
    """Get production advice for mixing or mastering."""
    brain = SonusBrain()
    advice = brain.production_advice(context)
    
    click.echo(Fore.MAGENTA + f"\n--- Production Advice ({context}) ---")
    for tip in advice:
        click.echo(f"- {tip}")

@cli.command()
def interactive():
    """Start an interactive session with Sonus."""
    brain = SonusBrain()
    click.echo(Fore.BLUE + Style.BRIGHT + "\n--- Sonus Interactive Session ---")
    click.echo("Type 'help' for commands, or 'exit' to quit.\n")
    
    while True:
        command = input(Fore.GREEN + "Sonus > " + Style.RESET_ALL).strip().lower()
        
        if command == "exit":
            break
        elif command == "help":
            print("Available commands: analyze, creative, production, help, exit")
        elif command.startswith("analyze"):
            parts = command.split()
            if len(parts) > 1:
                path = parts[1]
                res_load = brain.load_track(path)
                if "error" in res_load:
                    print(res_load["error"])
                else:
                    res = brain.analyze_audio()
                    print(res)
            else:
                print("Usage: analyze <file_path>")
        elif command == "creative":
             print(brain.creative_suggest())
        elif command == "production":
             print(brain.production_advice())
        else:
            print("Unknown command.")

if __name__ == '__main__':
    cli()
