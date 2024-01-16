import pytest

from bocoel import SBertEmbedder
from tests import utils


@pytest.mark.parametrize("device", utils.torch_devices())
def test_encoding(device: str) -> None:
    sentence_bert = SBertEmbedder(device=device)

    single_sentence = ["This is a sentence"]
    multiple_sentences = ["This is a sentence", "This is another sentence"]

    emb = sentence_bert.encode(single_sentence)
    assert emb.shape == (sentence_bert.dims, 1), {
        "emb.shape": emb.shape,
        "sentence_bert": sentence_bert,
    }

    emb = sentence_bert.encode(multiple_sentences)
    assert emb.shape == (len(multiple_sentences), sentence_bert.dims), {
        "emb.shape": emb.shape,
        "sentence_bert": sentence_bert,
    }
