"""Gather model cards and metadata from HuggingFace Hub."""

import argparse
import json
import os
import re
import shutil
import sys
import traceback
import warnings
from pathlib import Path

from playwright.sync_api import sync_playwright
from huggingface_hub import hf_hub_download, model_info
from huggingface_hub.errors import RepositoryNotFoundError

def download_pdf(url: str, output: Path) -> bool:
    """Download model card as PDF via Playwright (headless Chromium)."""
    if output.exists():
        return True
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            page.pdf(path=str(output))
            browser.close()
        return True
    except Exception:
        print(f"  Failed to download PDF from {url}")
        return False


def download_readme(model: str, output: Path) -> bool:
    """Download README.md from a model repo."""
    if output.exists():
        return True
    try:
        hf_hub_download(repo_id=model, filename="README.md", local_dir=str(output.parent))
        readme_path = output.parent / "README.md"
        if readme_path.exists():
            os.rename(str(readme_path), str(output))
            return True
    except Exception:
        print(f"  Failed to download README.md for {model}")
    return False


def get_context_length(minfo) -> int | None:
    """Try to find context length from model card metadata, then config.json."""
    # Check card metadata first
    if hasattr(minfo, "cardData") and minfo.cardData:
        card_data = minfo.cardData
        if "model-index" in card_data:
            for entry in card_data["model-index"]:
                if "context_length" in entry:
                    return entry["context_length"]

    # Fall back to config.json
    try:
        config_path = hf_hub_download(
            repo_id=minfo.id, filename="config.json", local_dir=str(Path("/tmp") / f"config_{minfo.id.replace('/', '_')}")
        )
        with open(config_path) as f:
            config = json.load(f)
        for field in ["max_position_embeddings", "n_positions", "max_sequence_length", "max_seq_len"]:
            if field in config:
                return config[field]
    except Exception as e:
        print(f"  Error accessing config: {e}")
    return None


# License names for external license URLs that HuggingFace only tags as "other".
# Keys are the `license_link` values seen on model cards; values are the actual license names.
LICENSE_URL_NAMES = {
    "https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/": "nvidia-open-model-license",
    "https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license": "nvidia-open-model-license",
    "https://openmdw.ai/license/1-1/": "openmdw-1.1",
    "https://huggingface.co/tencent/WeMM-Embedding-2B/blob/main/LICENSE": "apache-2.0",
    "https://huggingface.co/tencent/WeMM-Embedding-4B/blob/main/LICENSE": "apache-2.0",
    "https://huggingface.co/tencent/WeMM-Embedding-9B/blob/main/LICENSE": "apache-2.0",
}


def resolve_license(license_name: str, license_file, license_card_name: str | None = None) -> str:
    """Return the best license name available from card metadata.

    Resolution order: standard `license` tag, then a custom `license_name`
    frontmatter field (some cards set this while `license` stays "other"),
    then the license_link URL map.
    """
    if license_name in ("", "other"):
        if license_card_name and license_card_name != "other":
            return license_card_name
        if license_file in LICENSE_URL_NAMES:
            return LICENSE_URL_NAMES[license_file]
    return license_name


# Patterns (in priority order) to detect a canonical license name in model card
# text, used when card metadata carries no usable license.
LICENSE_PATTERNS = [
    (re.compile(r"apache[-\s]?license(?:\s+version)?\s*2(?:\.0)?|apache[-\s]?2\.0", re.I), "apache-2.0"),
    (re.compile(r"\bmit[-\s]?license\b|licensed under (?:the\s+)?mit\b|under the\s+mit\b", re.I), "mit"),
    (re.compile(r"nvidia[-\s]?open[-\s]?model[-\s]?licen[cs]e?s?", re.I), "nvidia-open-model-license"),
    (re.compile(r"openmdw[-\s]?1\.1", re.I), "openmdw-1.1"),
    (re.compile(r"gnu\s+general\s+public\s+license\b|gpl[-\s]?3(?:\.0)?\b", re.I), "gpl-3.0"),
    (re.compile(r"gpl[-\s]2(?:\.0)?\b", re.I), "gpl-2.0"),
    (re.compile(r"bsd[-\s]?3[-\s]?clause|3[-\s]?clause\s+bsd", re.I), "bsd-3-clause"),
    (re.compile(r"cc[-\s]?by[-\s]?4\.0|creative\s+commons\s+by\s+4\.0", re.I), "cc-by-4.0"),
]


def extract_license_section(card_text: str) -> str:
    """Return the body of the first 'License' heading in a model card, else the whole text."""
    lines = card_text.splitlines()
    start = level = None
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m and re.match(r"^\s*license\b", m.group(2), re.I):
            start, level = i + 1, len(m.group(1))
            break
    if start is None:
        return card_text
    body = []
    for line in lines[start:]:
        m = re.match(r"^(#{1,6})\s", line)
        if m and len(m.group(1)) <= level:
            break
        body.append(line)
    return "\n".join(body) if body else card_text


# scancode license keys that map to the canonical names we emit.
LICENSE_KEY_ALIASES = {
    "bsd-new": "bsd-3-clause",
}


def _normalize_license_expression(expr: str) -> str | None:
    """Reduce a license expression to a single license key, or None if ambiguous/unknown."""
    parts = re.split(r"\b(?:AND|OR|WITH)\b", expr, flags=re.I)
    kept = [
        p.strip(" ()")
        for p in parts
        if p.strip()
        and p.strip().lower() != "unknown-license-reference"
        and not p.strip().lower().startswith("license-ref")
    ]
    if len(kept) != 1:
        return None
    key = kept[0].lower()
    return LICENSE_KEY_ALIASES.get(key, key)


def _licensedcode_detection(card_text: str) -> str | None:
    """Detect a license with the licensedcode engine (scancode's SPDX-based detector)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            from licensedcode import detection
        except Exception:
            # System libarchive is broken on this host; licensedcode only needs
            # extractcode.libarchive2 for archive files, never for text detection.
            import types
            fake = types.ModuleType("extractcode.libarchive2")
            fake.extract = lambda *a, **k: (_ for _ in ()).throw(
                RuntimeError("archive extraction unavailable")
            )
            sys.modules["extractcode.libarchive2"] = fake
            try:
                from licensedcode import detection
            except Exception:
                print("  License detector unavailable; falling back to regex patterns only.")
                return None
    try:
        detections = list(detection.detect_licenses(query_string=card_text))
    except Exception:
        return None
    for det in detections:
        normalized = _normalize_license_expression(getattr(det, "license_expression", "") or "")
        if normalized:
            return normalized
    return None


def detect_license_from_card(card_text: str) -> str | None:
    """Detect a canonical license name from model card text."""
    if not card_text:
        return None
    section = extract_license_section(card_text)
    for pattern, name in LICENSE_PATTERNS:
        if pattern.search(section):
            return name
    # Second pass: off-the-shelf SPDX-based detector for licenses the
    # patterns above don't cover.
    return _licensedcode_detection(section)


def base_model_chain_license(model: str, max_depth: int = 5) -> tuple[str | None, str | None]:
    """Walk the base-model chain of a fine-tuned model.

    Returns (license, source_model) of the closest base model that has a
    resolvable license, or (None, None) if the chain has none.
    """
    seen = set()
    current = model
    for _ in range(max_depth):
        if current is None or current in seen:
            return None, None
        seen.add(current)
        try:
            minfo = model_info(current, token=os.environ.get("HF_TOKEN"))
        except Exception:
            return None, None
        card_data = minfo.card_data or {}
        resolved = resolve_license(
            card_data.get("license") or "",
            card_data.get("license_link"),
            card_data.get("license_name"),
        )
        if resolved not in ("", "other"):
            return resolved, current
        base = card_data.get("base_model")
        if isinstance(base, list):
            base = base[0] if base else None
        current = base if isinstance(base, str) else None
    return None, None


def extract_arxiv_tags(tags: list[str]) -> list[str]:
    """Extract arxiv tags from model tags, filtering out dummy entries."""
    arxiv_tags = []
    for t in tags:
        if "arxiv" in t and t != "arxiv:0000.00000":
            arxiv_tags.append(t)
    return arxiv_tags


def build_model_record(model: str, minfo) -> dict:
    """Query HuggingFace API and build a model info record."""
    card_data = minfo.card_data or {}
    license_name = card_data.get("license") or ""
    license_file = card_data.get("license_link")
    license_card_name = card_data.get("license_name")
    record = {
        "releasedate": minfo.created_at.strftime("%Y-%m-%d"),
        "model": model,
        "license": resolve_license(license_name, license_file, license_card_name),
        "license_file": license_file,
        "safetensors": str(minfo.safetensors) if minfo.safetensors else None,
        "arxiv": extract_arxiv_tags(minfo.tags),
        "datasets": card_data.get("datasets"),
        "language": card_data.get("language"),
        "hash": minfo.sha,
        "context_length": get_context_length(minfo),
    }

    # Merge extra license tags into the license string (original notebook behavior)
    license_extra = [t for t in minfo.tags if t == "license" and t != record["license"]]
    if license_extra:
        record["license"] += " " + " ".join(license_extra)

    return record


def process_model(model: str, base_dir: Path, overwrite: bool = False) -> Path:
    """Download all assets for a single model and return the output directory."""
    # Parse maker/name from model name
    parts = model.split("/")
    if len(parts) != 2:
        print(f"ERROR: Invalid model name format '{model}'. Expected 'maker/model_name'.")
        return Path()

    maker, name = parts
    out_dir = base_dir / maker / name
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nProcessing {model}...")

    # 1. Download model card PDF
    pdf_path = out_dir / "model_card.pdf"
    if overwrite or not pdf_path.exists():
        download_pdf(f"https://huggingface.co/{model}", pdf_path)

    # 2. Download README.md as .txt
    readme_path = out_dir / "README.txt"
    if overwrite or not readme_path.exists():
        download_readme(model, readme_path)

    # 3. Query API and build record
    minfo = model_info(model, token=os.environ.get("HF_TOKEN"))
    record = build_model_record(model, minfo)

    # 3b. Detect the license from the card text when metadata is still missing.
    if record["license"] in ("", "other"):
        readme_text = readme_path.read_text(encoding="utf-8", errors="replace") if readme_path.exists() else ""
        detected = detect_license_from_card(readme_text)
        if detected:
            record["license"] = detected
            print(f"  License detected from model card: {detected}")

    # 3c. Inherit the license from the base model if this is a fine-tune.
    if record["license"] in ("", "other"):
        base_license, source = base_model_chain_license(model)
        if base_license:
            record["license"] = base_license
            print(f"  License inherited from base model ({source}): {base_license}")

    # 4. Save model_records.json
    records_path = out_dir / "model_records.json"
    with open(records_path, "w") as f:
        json.dump({model: record}, f, indent=2, default=str)

    # 5. Optionally download license file (commented - enable if needed)
    license_file_url = record["license_file"]
    if license_file_url:
        license_out = out_dir / Path(license_file_url).name
        if not license_out.exists():
            try:
                hf_hub_download(repo_id=model, filename=license_file_url, local_dir=str(license_out.parent))
            except Exception:
                print(f"  Failed to download license file: {license_file_url}")

    # 6. Optionally download arxiv papers (commented - enable if needed)
    # for arxiv_tag in record["arxiv"]:
    #     paper_id = arxiv_tag.split(":")[-1]
    #     paper_path = out_dir / f"reference_{paper_id}.pdf"
    #     if not paper_path.exists():
    #         import arxiv
    #         search = arxiv.Search(id_list=[paper_id])
    #         for result in search.results():
    #             result.download_pdf(filename=str(paper_path))
    #             print(f"  Downloaded: reference_{paper_id}.pdf")

    # Print summary
    print(f"  License:      {record['license']}")
    print(f"  Released:     {record['releasedate']}")
    print(f"  Hash:         {record['hash'][:12]}...")
    print(f"  Context len:  {record['context_length']}")
    if record["arxiv"]:
        print(f"  Arxiv tags:   {record['arxiv']}")
    print(f"  Saved to:     {out_dir}")

    # Clean up hf_hub cache directories
    cache_dirs = [out_dir / ".cache"]
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            shutil.rmtree(cache_dir)

    return out_dir


def process_models(models: list[str], base_dir: Path, overwrite: bool = False) -> tuple[list[str], list[tuple[str, str]]]:
    """Process each model, continuing past individual failures.

    Returns (successes, failures). Each failure is a (slug, reason) pair.
    A model's partial output directory is removed if this run created it
    and the run failed.
    """
    successes: list[str] = []
    failures: list[tuple[str, str]] = []
    for model in models:
        parts = model.split("/")
        if (len(parts) != 2 or not parts[0] or not parts[1]
                or parts[0] in (".", "..") or parts[1] in (".", "..")):
            print(f"ERROR: Invalid model name format '{model}'. Expected 'maker/model_name'.")
            failures.append((model, "not a valid 'maker/name' slug"))
            continue
        out_dir = base_dir / parts[0] / parts[1]
        existed_before = out_dir.exists()
        try:
            process_model(model, base_dir, overwrite=overwrite)
        except RepositoryNotFoundError:
            reason = "slug not found on HuggingFace"
        except Exception as e:
            reason = str(e) or e.__class__.__name__
            traceback.print_exc()
        else:
            successes.append(model)
            continue
        if not existed_before and out_dir.exists():
            shutil.rmtree(out_dir)
        failures.append((model, reason))
        print(f"ERROR: {model} -> {reason}")
    print(f"\nSummary: {len(successes)} succeeded, {len(failures)} failed")
    for slug, reason in failures:
        print(f"  FAILED: {slug} - {reason}")
    return successes, failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Gather model cards and metadata from HuggingFace Hub.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--model", type=str, help="Single model name (e.g. openai/privacy-filter)")
    group.add_argument("--models-file", type=str, help="Path to a file with one model per line")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.home() / "projects" / "model_card_work" / "model_cards",
        help="Base directory for output (default: ~/projects/model_card_work/model_cards/)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-download files that already exist",
    )

    args = parser.parse_args()

    # Resolve model list
    if args.model:
        models = [args.model]
    else:
        models = []
        with open(args.models_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    models.append(line)

    if not models:
        print("No models to process.")
        return 0

    print(f"Processing {len(models)} model(s) -> {args.output_dir.resolve()}\n")

    successes, _ = process_models(models, args.output_dir, overwrite=args.overwrite)

    if not successes:
        return 1

    print(f"\nDone. All outputs saved to {args.output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
