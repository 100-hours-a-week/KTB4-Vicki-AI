import sentencepiece as spm

sp = spm.SentencePieceProcessor()
sp.load("kor-bpe-100k.model")
