import sentencepiece as spm

print("학습 시작")

spm.SentencePieceTrainer.train(
    input="../data/model-data/kowiki.txt",
    model_prefix="kor-bpe-100k",
    vocab_size=100_000,
    model_type="bpe",
    input_sentence_size=5000000,
    shuffle_input_sentence=True,
    num_threads=8,
)

print("학습 완료")
