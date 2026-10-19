---
name: pixel
description: "Analyze shot references into measured or estimated layout, typography, color and appearance specifications, and compare reconstructed results. Use for AE reference decomposition and visual fidelity; also supports explicit web mockup reproduction."
metadata:
  ae_capabilities: "composition,color,typography,qa"
  upstream_repository: "simota/agent-skills"
  upstream_commit: "f425adcb2111ca8c0be88b325888ff61b64dec49"
  edition: "ae-reference-adaptation"
---

# Pixel reference analysis — AE integration

For an AE request, use the upstream analysis and comparison methods while continuing the user's AE project. This is analysis expertise; it does not provide an AE connection or a validated glass recipe.

- Read [design extraction](reference/design-extraction.md) for multi-pass observation, element bounds, color/type/spacing and confidence. Distinguish measured data, visual estimates and implementation hypotheses. Preserve the actual reference rather than snapping it to a guessed 4/8px web grid.
- Read [precision specification](reference/precision-spec.md) for structured properties and tolerances. Translate relevant fields to AE comp coordinates, visible bounds, paths, live text and material controls; ignore HTML/CSS runtime fields.
- Read [visual verification](reference/visual-verification.md) for component comparisons. Compare the top-level AE result at the intended size and inspect critical crops. Aggregate scores and a three-iteration cap cannot override a failed required feature or missing evidence. Use the current project's authorized evidence mode.
- Read [gap analysis](reference/gap-analysis-report.md) when diagnosing a mismatch. Identify the changed feature and likely cause before changing construction.
- Read [animation extraction](reference/animation-extraction.md) only when motion interpretation matters. A static image does not establish timing or a loop; prioritize explicit motion instructions or video evidence.

Hand off: feature/requirement ID → observed property and uncertainty → candidate AE representation/control → observable comparison. Use the current AE implementation skill and Director's QA for execution and acceptance. Improve the design separately from a requested faithful reconstruction.

The complete [upstream entrypoint](UPSTREAM_SKILL.md) and its references are preserved. For an explicitly requested HTML/CSS task, consult that workflow. Other agents and shared package links in the original are optional source context, not installed dependencies or authorization to delegate.

Source provenance and original file hashes: [source.json](source.json).
