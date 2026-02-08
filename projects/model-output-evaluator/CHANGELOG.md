# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Initial release of model-output-evaluator.
- Five evaluation metrics: exact match, contains match, Levenshtein similarity,
  Jaccard similarity, and simplified unigram BLEU.
- `evaluate` command to score predictions against references.
- `compare` command to compare two sets of predictions against the same references.
- Rich-formatted text table output and JSON output modes.
- Example prediction and reference files.
