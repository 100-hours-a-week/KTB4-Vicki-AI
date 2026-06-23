import os
import re
import csv
import json
import unicodedata
import fitz
from html.parser import HTMLParser
from docling.document_converter import DocumentConverter


class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []

    def handle_data(self, data):
        self.texts.append(data.strip())

    def get_text(self):
        return " ".join(t for t in self.texts if t)


class DocumentLoader:
    def __init__(self):
        self.converter = DocumentConverter()

    def preprocess_text(self, text: str) -> str:
        text = unicodedata.normalize("NFKC", text)
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\xad]", "", text)
        text = re.sub(r"-\s*\d+\s*-", "", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _extract_all_pairs(self, element, lines, current_item=None):
        if isinstance(element, dict):
            is_root_dict = current_item is None
            if is_root_dict:
                current_item = []

            for k, v in element.items():
                if isinstance(v, dict):
                    self._extract_all_pairs(v, lines, current_item)
                elif isinstance(v, list):
                    self._extract_all_pairs(v, lines, None)
                else:
                    current_item.append(f"{k}: {v}")

            if is_root_dict and current_item:
                lines.append(", ".join(current_item))
        elif isinstance(element, list):
            for item in element:
                if isinstance(item, (list, dict)):
                    self._extract_all_pairs(item, lines, None)
                else:
                    lines.append(str(item))

    def load_document(self, filepath: str) -> dict:
        _, ext = os.path.splitext(filepath.lower())

        if ext in (".txt", ".md"):
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            return {
                "text": self.preprocess_text(text),
                "metadata": {"source": filepath, "format": ext[1:]},
            }

        elif ext == ".html":
            with open(filepath, "r", encoding="utf-8") as f:
                html = f.read()
            parser = HTMLTextExtractor()
            parser.feed(html)
            return {
                "text": self.preprocess_text(parser.get_text()),
                "metadata": {"source": filepath, "format": "html"},
            }

        elif ext == ".json":
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            lines = []
            self._extract_all_pairs(data, lines, current_item=None)

            texts = "\n".join(lines)

            return {
                "text": self.preprocess_text(texts),
                "metadata": {"source": filepath, "format": "json"},
            }

        elif ext == ".csv":
            texts = []
            for encoding in ["utf-8", "cp949"]:
                try:
                    with open(filepath, "r", encoding=encoding) as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            texts.append(", ".join(f"{k}: {v}" for k, v in row.items()))
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError(f"지원하지 않는 파일 인코딩입니다: {filepath}")
            return {
                "text": self.preprocess_text("\n".join(texts)),
                "metadata": {"source": filepath, "format": "csv"},
            }

        elif ext in (".docx", ".doc"):
            result = self.converter.convert(filepath)
            text = result.document.export_to_markdown()
            return {
                "text": self.preprocess_text(text),
                "metadata": {"source": filepath, "format": ext[1:]},
            }

        elif ext == ".pdf":
            doc = fitz.open(filepath)

            texts = []
            for page in doc:
                text = page.get_text("text")
                if text:
                    texts.append(text)
            return {
                "text": self.preprocess_text("\n".join(texts)),
                "metadata": {"source": filepath, "format": "pdf"},
            }

        else:
            raise ValueError(f"지원하지 않는 형식: {filepath}")
