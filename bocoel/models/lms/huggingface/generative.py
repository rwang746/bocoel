from collections.abc import Sequence

import torch

from bocoel.models.lms.interfaces import GenerativeModel

from .causal import HuggingfaceCausalLM


class HuggingfaceGenerativeLM(HuggingfaceCausalLM, GenerativeModel):
    """
    The generative model backed by huggingface's transformers library.

    Since huggingface's tokenizer needs padding to the left to work,
    padding doesn't guarentee the same positional embeddings, and thus, results.
    If sameness with generating one by one is desired, batch size should be 1.
    """

    def __init__(self, model_path: str, batch_size: int, device: str) -> None:
        super().__init__(model_path=model_path, batch_size=batch_size, device=device)

    @torch.no_grad()
    def generate(self, prompts: Sequence[str], /) -> Sequence[str]:
        results: list[str] = []
        for idx in range(0, len(prompts), self._batch_size):
            results.extend(self._generate_batch(prompts[idx : idx + self._batch_size]))
        return results

    def _generate_batch(self, prompts: Sequence[str]) -> list[str]:
        inputs = self._tokenizer(prompts)
        outputs = self._model.generate(**inputs)
        outputs = self._tokenizer.batch_decode(outputs)
        return outputs
