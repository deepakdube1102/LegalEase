import re
import os
from dotenv import load_dotenv

load_dotenv()

class LegalSimplifier:
    def __init__(self):
        self.nlp = "not_loaded"
        self.client = "not_loaded"
        self.gemini_key = os.getenv("GEMINI_API_KEY")

    def _get_nlp(self):
        if self.nlp == "not_loaded":
            try:
                import spacy
                self.nlp = spacy.load("en_core_web_sm")
            except Exception as e:
                print(f"Lazy NLP Load Error: {e}")
                self.nlp = None
        return self.nlp

    def _get_client(self):
        if self.client == "not_loaded":
            try:
                if self.gemini_key:
                    from google import genai
                    self.client = genai.Client(api_key=self.gemini_key)
                else:
                    self.client = None
            except Exception as e:
                print(f"Lazy Client Load Error: {e}")
                self.client = None
        return self.client

    def dictionary_simplify(self, text):
        """Replaces complex legal terms using the dictionary."""
        legal_dict = {
            r"\bhereinafter\b": "later in this document",
            r"\bpursuant to\b": "according to",
            r"\baforementioned\b": "previously mentioned",
            r"\bnotwithstanding\b": "despite",
            r"\bheretofore\b": "before now",
            r"\btherein\b": "in that",
            r"\bwhereby\b": "by which",
            r"\bin witness whereof\b": "to confirm this",
            r"\bmutatis mutandis\b": "with the necessary changes",
            r"\bpro rata\b": "proportionally",
            r"\binter alia\b": "among other things",
            r"\bforce majeure\b": "unforeseeable circumstances",
            r"\bcaveat emptor\b": "buyer beware",
            r"\bde facto\b": "in reality",
            r"\bona fide\b": "genuine",
            r"\bprima facie\b": "at first sight",
            r"\bquid pro quo\b": "an exchange for something",
            r"\bvidelicet\b": "namely",
            r"\bscilicet\b": "that is to say",
            r"\bviz\.\b": "namely",
            r"\bi\.e\.\b": "that is",
            r"\be\.g\.\b": "for example",
            r"\bab initio\b": "from the beginning",
            r"\bad hoc\b": "for this specific purpose",
            r"\bamicus curiae\b": "friend of the court",
            r"\bbona fides\b": "good faith",
            r"\bcorpus delicti\b": "evidence of the crime",
            r"\bde jure\b": "by law",
            r"\bex parte\b": "from one party",
            r"\bin personam\b": "against a person",
            r"\bin rem\b": "against property",
            r"\bmandamus\b": "court order to perform",
            r"\bmens rea\b": "criminal intent",
            r"\bper diem\b": "per day",
            r"\bpro bono\b": "for free",
            r"\bpro se\b": "representing oneself",
            r"\bvoir dire\b": "jury selection",
            r"\bherein\b": "in this document",
            r"\bthereto\b": "to that",
            r"\bthereof\b": "of that",
            r"\bthereupon\b": "immediately after that",
            r"\bhereunder\b": "under this document",
            r"\bwhereas\b": "because",
            r"\bin the event that\b": "if",
            r"\bprior to\b": "before",
            r"\bsubsequent to\b": "after",
            r"\bfor the purpose of\b": "to",
            r"\bwith regard to\b": "about",
            r"\bin accordance with\b": "under",
            r"\bis applicable to\b": "applies to",
            r"\bshall be\b": "must be",
            r"\bshall have\b": "must have",
            r"\bshall\b": "must",
            r"\bprovided that\b": "if",
            r"\bsuch\b": "this",
            r"\bsaid\b": "the",
            r"\bnull and void\b": "invalid",
            r"\bterms and conditions\b": "rules",
            r"\bby and between\b": "between",
            r"\bin lieu of\b": "instead of",
            r"\bto the extent that\b": "if",
            r"\bwithout prejudice to\b": "without affecting",
            r"\bunder the provisions of\b": "under",
            r"\buntil such time as\b": "until",
            r"\bcommencing on\b": "starting on",
            r"\bterminate\b": "end",
            r"\bindemnify\b": "compensate for harm",
            r"\bindemnification\b": "compensation for harm",
            r"\bseverability\b": "separation of invalid parts",
            r"\bwaiver\b": "giving up a right",
            r"\bin consideration of\b": "in return for",
            r"\bit is agreed\b": "we agree",
            r"\bparty of the first part\b": "first party",
            r"\bparty of the second part\b": "second party",
            r"\bupon receipt of\b": "when receiving",
        }
        simplified_text = text
        for pattern, replacement in legal_dict.items():
            # Use a function to preserve the original casing (capitalization)
            def replace_match(match):
                word = match.group(0)
                if word.istitle():
                    return replacement.capitalize()
                elif word.isupper():
                    return replacement.upper()
                return replacement
            simplified_text = re.sub(pattern, replace_match, simplified_text, flags=re.IGNORECASE)
        return simplified_text

    def spacy_simplify(self, text):
        """Uses spaCy to segment and slightly simplify sentence structure."""
        nlp = self._get_nlp()
        if not nlp:
            return text
            
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        return " ".join(sentences)

    def gemini_simplify(self, text):
        """Uses Google Gemini API to completely rewrite the text in plain English."""
        client = self._get_client()
        if not client:
            return None # Signal to use fallback
            
        prompt = (
            "You are an expert legal simplifier. Your task is to rewrite the following complex "
            "legal text into plain, easy-to-understand English. "
            "CRITICAL RULES:\n"
            "1. Preserve ALL original meaning, conditions, obligations, and rights.\n"
            "2. Completely eliminate legal jargon, archaic phrasing (like hereinafter, inter alia), and redundant doublets/triplets.\n"
            "3. Use modern, conversational English while remaining professional.\n"
            "4. Do NOT add any conversational filler, introductory text, or concluding remarks. Just output the simplified text.\n\n"
            f"TEXT TO SIMPLIFY:\n{text}"
        )
        
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            if response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini API Error: {e}")
            
        return None

    def simplify(self, text):
        """Main pipeline for simplification."""
        # Stage 1: Try Gemini API for superior full-text rewriting
        gemini_result = self.gemini_simplify(text)
        if gemini_result:
            return gemini_result
            
        # Stage 2: Fallback to robust dictionary replacement
        text = self.dictionary_simplify(text)
        
        # Stage 3: Sentence Segmentation & run-on cleanup
        nlp = self._get_nlp()
        if nlp:
            doc = nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents]
            final_text = " ".join(sentences)
        else:
            final_text = text
            
        final_text = re.sub(r";\s*and\b", ".\nFurthermore,", final_text, flags=re.IGNORECASE)
        final_text = re.sub(r";\s*or\b", ".\nAlternatively,", final_text, flags=re.IGNORECASE)
        final_text = re.sub(r";\s*", ".\n", final_text)
        
        return final_text
