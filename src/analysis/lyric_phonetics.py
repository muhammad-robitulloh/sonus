import re

class LyricPhonetics:
    def __init__(self, lyrics_text):
        self.lyrics = lyrics_text

    def analyze_cutting_power(self):
        """Analyze lyrics for plosive and sibilant consonants (Acoustic Cutter)."""
        # Define consonant groups
        plosives = r'[tkpbdg]' # Hard stops
        sibilants = r'[szʃʒfv]' # Hissing sounds (cut through highs)
        vowels = r'[aeiou]' # Soft sounds
        
        words = self.lyrics.lower().split()
        report = []
        
        cutting_score = 0
        soft_score = 0
        
        problematic_words = []
        
        for word in words:
            p_count = len(re.findall(plosives, word))
            s_count = len(re.findall(sibilants, word))
            v_count = len(re.findall(vowels, word))
            
            # Simple scoring: Plosives worth 2, Sibilants 1, Vowels 0
            score = (p_count * 2) + (s_count * 1)
            cutting_score += score
            
            # Check ratio for each word
            if len(word) > 3 and score < 2:
                problematic_words.append(word)
                
        avg_score = cutting_score / (len(words) + 1e-6)
        
        if avg_score < 1.5:
            report.append(f"WEAK PRESENCE: Lirik lo terlalu 'lembut' (Avg Score: {avg_score:.2f}).")
            report.append(f"ADVICE: Ganti kata-kata berikut dengan sinonim yang lebih tajam (banyak T, K, P, S): {', '.join(problematic_words[:5])}...")
        else:
            report.append(f"STRONG CUT: Lirik lo tajam dan bakal nembus mix dengan baik (Avg Score: {avg_score:.2f}).")
            
        return {
            "avg_cutting_score": float(avg_score),
            "problematic_words": problematic_words,
            "findings": report
        }
