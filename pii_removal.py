import pandas as pd
import re
import requests



class MaskPII():

    def __init__(self):
        
        self.entities = ["PHONE_NUMBER", "CREDIT_CARD",
                         "EMAIL_ADDRESS", "IBAN_CODE",
                         "IP_ADDRESS",
                         "PHONE_NUMBER", "MEDICAL_LICENSE"]
        self.analyzer_url = "http://presidio-analyzer:3000/analyze"
        self.anonymizer_url = "http://presidio-anonymizer:3000/anonymize"

    def fit(self):
        return self

    @staticmethod
    def replace_digits(s):
        # Keep years between 2010 and 2030 as is
        exclusion_list = [str(year) for year in range(2010, 2031)]
        
        def custom_replacement(match):
            matched_string = match.group()
            if matched_string in exclusion_list or len(matched_string) < 4:
                return matched_string
            else:
                return 'X' * len(matched_string)
        
        result = re.sub(r'\d+', custom_replacement, s)
        return result

    def redefine_entities(self, text):
        for ent in self.entities:
            text = text.replace(f'<{ent}>', f'PII_{ent}')
        return text

    @staticmethod
    def mask_email(text):
        def repl(match):
            local_part, domain = match.group(1), match.group(2)
            return 'X' * len(local_part) + '@' + domain
        return re.sub(r'(\S+)@(\S+)', repl, text)

    def anonymize_text(self, text, deep=False):
        # Analyze the text to find PII entities
        if deep:
            analyzer_payload = {
                "text": text,
            "language": "en",
            "entities": self.entities
        }
        analyzer_response = requests.post(
            self.analyzer_url,
            json=analyzer_payload
        )
        analyzer_response.raise_for_status()
        analyzer_results = analyzer_response.json()
        
        # Anonymize the text based on the analyzer results
        anonymizer_payload = {
            "text": text,
            "analyzer_results": analyzer_results,
            "anonymizer_config": {
                "anonymizers": {
                    "DEFAULT": {
                        "type": "replace",
                        "new_value": "<PII>"
                    }
                }
            }
        }
        anonymizer_response = requests.post(
            self.anonymizer_url,
            json=anonymizer_payload
        )
        anonymizer_response.raise_for_status()
        anonymized_text = anonymizer_response.json()["text"]
        
        # Further process the anonymized text
        anonymized_text = self.redefine_entities(anonymized_text)
        anonymized_text = self.replace_digits(anonymized_text)
        anonymized_text = self.mask_email(anonymized_text)
        
        return anonymized_text

    def transform(self, series, deep=False):
        # Ensure series is string type
        series = series.astype(str)
        if deep:
            series = series.apply(self.anonymize_text)

        series = series.apply(self.replace_digits)
        series = series.apply(self.mask_email)
        return series
