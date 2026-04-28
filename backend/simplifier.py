import spacy
import re
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class LegalSimplifier:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            self.nlp = None
        
        # Load model and tokenizer directly
        model_name = "t5-small"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Predefined dictionary for legal terms
        self.legal_dict = {
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

    def dictionary_simplify(self, text):
        """Replaces complex legal terms using the dictionary."""
        simplified_text = text
        for pattern, replacement in self.legal_dict.items():
            simplified_text = re.sub(pattern, replacement, simplified_text, flags=re.IGNORECASE)
        return simplified_text

    def spacy_simplify(self, text):
        """Uses spaCy to segment and slightly simplify sentence structure."""
        if not self.nlp:
            return text
            
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        
        # Simple rule: if a sentence is too long (e.g. > 25 words), it might need splitting
        # For now, we'll just return the segmented sentences joined by space
        # AI step will handle the actual rewriting
        return " ".join(sentences)

    def ai_simplify(self, text):
        """Uses Hugging Face Transformers to rewrite the text in simpler terms."""
        # Break down text into sentences for better AI processing
        if not self.nlp:
            sentences = [text]
        else:
            doc = self.nlp(text)
            sentences = [sent.text.strip() for sent in doc.sents]

        simplified_sentences = []
        for sent in sentences:
            if len(sent.split()) < 3: # Skip very short snippets
                simplified_sentences.append(sent)
                continue
                
            # AI simplification via manual inference
            try:
                # For t5-small, we use a prompt
                input_text = f"summarize: {sent}"
                inputs = self.tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
                outputs = self.model.generate(inputs, max_length=128, min_length=5, length_penalty=2.0, num_beams=4, early_stopping=True)
                simplified_sentences.append(self.tokenizer.decode(outputs[0], skip_special_tokens=True))
            except Exception as e:
                print(f"AI Error: {e}")
                simplified_sentences.append(sent)

        return " ".join(simplified_sentences)

    def simplify(self, text):
        """Main pipeline for simplification."""
        # Stage 1: Dictionary Replacement
        text = self.dictionary_simplify(text)
        
        # Stage 2: Sentence Segmentation / Basic Cleaning
        text = self.spacy_simplify(text)
        
        # Stage 3: AI Rewrite
        text = self.ai_simplify(text)
        
        return text

# Example usage (uncomment to test locally)
# if __name__ == "__main__":
#     simplifier = LegalSimplifier()
#     test_text = "The parties hereto agree that the aforementioned agreement shall be interpreted pursuant to the laws of the state."
#     print(simplifier.simplify(test_text))
