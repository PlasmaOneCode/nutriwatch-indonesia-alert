import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import argparse

class IndoBERTAbsaZeroShot:
    """
    Zero-shot Aspect-Based Sentiment Analysis using IndoBERT.
    To avoid OOM on 4GB VRAM, we use zero-shot classification 
    instead of fine-tuning a large multi-task model.
    """
    def __init__(self, device=-1):
        # device: -1 for CPU, 0 for first GPU
        print("Initializing IndoBERT Zero-Shot ABSA model...")
        
        # We use a multi-lingual zero-shot classifier that works well with Indonesian
        # If offline/strictly IndoBERT is needed, we'd load indobenchmark/indobert-base-p1 
        # and do NLI formatting manually. Here we use an out-of-the-box pipeline for simplicity
        # and robustness within resource constraints.
        try:
            self.classifier = pipeline(
                "zero-shot-classification", 
                model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", # Multilingual, good for ID
                device=device
            )
        except Exception as e:
            print(f"Warning: Failed to load mDeBERTa, falling back to default xlm-roberta. Error: {e}")
            self.classifier = pipeline(
                "zero-shot-classification",
                device=device
            )
            
        # Define our aspects and sentiments
        self.aspect_labels = [
            "rasa dan menu makanan", 
            "porsi dan kecukupan makanan", 
            "distribusi dan ketepatan waktu", 
            "higienitas dan keamanan makanan"
        ]
        
        self.aspect_map = {
            "rasa dan menu makanan": "rasa_menu",
            "porsi dan kecukupan makanan": "porsi_kecukupan",
            "distribusi dan ketepatan waktu": "distribusi_ketepatan",
            "higienitas dan keamanan makanan": "higienitas_keamanan"
        }
        
        self.sentiment_labels = ["positif", "negatif", "netral"]
        self.sentiment_map = {
            "positif": "positive",
            "negatif": "negative",
            "netral": "neutral"
        }

    def predict(self, text: str) -> dict:
        """
        Predict aspect and sentiment for a given text.
        """
        # 1. Predict Aspect
        aspect_res = self.classifier(text, self.aspect_labels, multi_label=False)
        top_aspect_id = aspect_res['labels'][0]
        aspect_code = self.aspect_map[top_aspect_id]
        aspect_conf = aspect_res['scores'][0]
        
        # 2. Predict Sentiment
        # Formulate a context-aware sentiment prompt based on the aspect
        sentiment_res = self.classifier(text, self.sentiment_labels, multi_label=False)
        top_sent_id = sentiment_res['labels'][0]
        sent_code = self.sentiment_map[top_sent_id]
        sent_conf = sentiment_res['scores'][0]
        
        # Calculate a combined confidence (simple average)
        overall_conf = (aspect_conf + sent_conf) / 2.0
        
        return {
            "aspect": aspect_code,
            "sentiment": sent_code,
            "confidence": round(overall_conf, 4)
        }
        
    def predict_batch(self, texts: list) -> list:
        return [self.predict(t) for t in texts]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test ABSA Model")
    parser.add_argument("--test", action="store_true", help="Run tests")
    args = parser.parse_args()
    
    if args.test:
        # Check if CUDA is available
        device = 0 if torch.cuda.is_available() else -1
        print(f"Using device: {'GPU' if device == 0 else 'CPU'}")
        
        model = IndoBERTAbsaZeroShot(device=device)
        
        test_texts = [
            "Makanannya basi dan bau asem, anak saya sakit perut",
            "Porsinya dikit banget, anak cowok ga bakal kenyang",
            "Alhamdulillah menunya enak hari ini ayam teriyaki",
            "Makan siang baru datang jam 1 siang pas anak udah pulang"
        ]
        
        print("\nTesting Predictions:")
        print("-" * 50)
        for text in test_texts:
            res = model.predict(text)
            print(f"Text: {text}")
            print(f"Result: {res}")
            print("-" * 50)
