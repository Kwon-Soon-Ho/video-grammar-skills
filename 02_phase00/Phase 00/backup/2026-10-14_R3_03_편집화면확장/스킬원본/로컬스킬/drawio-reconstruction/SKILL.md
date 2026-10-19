---
name: drawio-reconstruction
description: "Reconstruct shot or diagram references by inventorying visible elements, preserving specific geometry and choosing editable native components or limited image support. Adapt fidelity and representation principles to AE; use the original Draw.io workflow only when Draw.io is requested."
metadata:
  ae_capabilities: "composition,infographic,rigging,assets,qa"
  upstream_repository: "HKUSTDial/Supervisor-Skills"
  upstream_commit: "207bc6f7a1aa107e544099c2c7cc86816fba9628"
  edition: "ae-reference-adaptation"
---

# Reference reconstruction — AE integration

For an AE task, read the fidelity contract, visible-element inventory, medium selection and visual-audit sections of [the original skill](UPSTREAM_SKILL.md). Continue producing the requested AE shot. Draw.io files, exports and checks are not AE deliverables or proof.

Inventory visible text, shapes, paths, connectors, curves, material/light details, overlaps and reusable parts. Record bounds, style, reference role, representation and remaining differences. A generic icon or curve with the same meaning is not a faithful reconstruction.

Choose AE live text, semantic shapes, paths and controlled precomps where they can preserve appearance and maintainability. Use independently replaceable bitmap pieces where they better satisfy the user's needs. Test editability rather than equating thousands of traced paths with a maintainable asset. Do not rasterize the whole shot merely because a complex surface is difficult.

Preserve the user's priority between editability and fidelity. The upstream fidelity-over-editability default is not an instruction to discard this user's native-editable preference. Compare geometry, line weight, occlusion, gradients, halos and cropped edges at real size; unresolved defining features remain failed or unverified.

Hand off: element ID → chosen AE medium and controls → reason/tradeoff → final-comp comparison and realistic edit test. Use the existing AE runtime and Director record. Bundled Draw.io helpers are archival source utilities; run them only for an actual Draw.io task after checking their requirements. No delegation follows from reading the original.

Source provenance and original file hashes: [source.json](source.json).
