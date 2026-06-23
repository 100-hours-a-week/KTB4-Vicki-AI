class Chunker:
    @staticmethod
    def hierarchical_split(
        text: str, chunk_size: int = 500, separators: list = None
    ) -> list:
        if separators is None:
            separators = ["\n\n", "\n", ". ", " "]

        def split_recursive(sub_text: str, sep_idx: int) -> list:
            if sep_idx >= len(separators):
                return [sub_text]

            sep = separators[sep_idx]
            parts = sub_text.split(sep)
            chunks = []

            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if len(part) <= chunk_size:
                    chunks.append(part)
                else:
                    chunks.extend(split_recursive(part, sep_idx + 1))
            return chunks

        return split_recursive(text, 0)

    @staticmethod
    def fixed_split(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:

        if overlap >= chunk_size:
            raise ValueError("overlap은 chunk_size보다 작아야 합니다.")

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])

            start += chunk_size - overlap

        return chunks
