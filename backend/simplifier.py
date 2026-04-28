import spacy
import re
import requests
import os

class LegalSimplifier:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            self.nlp = None
        
        self.api_url = "https://api-inference.huggingface.co/models/t5-small"
        self.api_token = os.getenv("HF_TOKEN")

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
        }
        simplified_text = text
        for pattern, replacement in legal_dict.items():
            simplified_text = re.sub(pattern, replacement, simplified_text, flags=re.IGNORECASE)
        return simplified_text

    def spacy_simplify(self, text):
        """Uses spaCy to segment and slightly simplify sentence structure."""
        if not self.nlp:
            return text
            
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        return " ".join(sentences)

    def ai_simplify(self, text):
        """Uses Hugging Face Inference API to rewrite the text in simpler terms."""
        if not self.nlp:
            sentences = [text]
        else:
            doc = self.nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents]

        headers = {"Authorization": f"Bearer {self.api_token}"} if self.api_token else {}
        simplified_sentences = []
        
        for sent in sentences:
            if len(sent.split()) < 3:
                simplified_sentences.append(sent)
                continue
                
            try:
                payload = {"inputs": f"summarize: {sent}"}
                response = requests.post(self.api_url, headers=headers, json=payload)
                result = response.json()
                
                # Handle API list response
                if isinstance(result, list) and len(result) > 0:
                    summary = result[0].get('summary_text', sent)
                    simplified_sentences.append(summary)
                # Handle direct object response or error
                elif isinstance(result, dict) and 'summary_text' in result:
                    simplified_sentences.append(result['summary_text'])
                else:
                    simplified_sentences.append(sent)
            except Exception as e:
                print(f"AI API Error: {e}")
                simplified_sentences.append(sent)

        return " ".join(simplified_sentences)

    def simplify(self, text):
        """Main pipeline for simplification."""
        # Stage 1: Dictionary Replacement
        text = self.dictionary_simplify(text)
        
        # Stage 2: Sentence Segmentation
        text = self.spacy_simplify(text)
        
        # Stage 3: AI Rewrite (via API)
        text = self.ai_simplify(text)
        
        return text
