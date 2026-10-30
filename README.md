# model_cards
A place store interesting model cards.

# Disclaimer:
I do not own any of these models, cards, or other content. I am just gathering it for the purpose of review.

## Adding a model (CI)

The cards in this repo are updated by a GitLab CI/CD pipeline. To add a model:

1. Add its HuggingFace slug (`maker/name`) to `model_slugs.txt`, one per line
   (blank lines and `#` comments are ignored).
2. Push to the default branch. The pipeline fetches every slug that does not
   yet have `<maker>/<name>/model_records.json`, verifies the result, and
   commits the new card directories (`model_card.pdf`, `README.txt`,
   `model_records.json`) as `Model Card Bot`.

A slug that fails to fetch is logged and retried on the next pipeline run;
fix or remove the line to stop retrying.

Manual/local use (same machinery in `scripts/gather_models.py`):

    pip install huggingface_hub scancode-toolkit playwright
    python -m playwright install chromium
    python scripts/gather_models.py --models-file model_slugs.txt --output-dir .
    # set HF_TOKEN in the environment for gated repos
