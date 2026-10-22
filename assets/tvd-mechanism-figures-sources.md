# README mechanism figures: sources and display conventions

The six workspace diagrams use native draw.io elements embedded in their `.drawio.png` files. Their WebP display copies are lossless. They illustrate task structure and agent actions using the source contracts below.

## Display conventions

- `???` is an unfinished field in the task data.
- `[xxx]` and ellipses shorten the displayed example. They are not a complete candidate submitted to a classifier. Visible beginnings such as “How to make [xxx]?” and “Step 1: [xxx]” convey the roles of the fields without including an operational harmful example.
- Illustrative labels and scores describe full hypothetical candidates, including any required length. The shown beginnings do not independently establish those labels or scores.
- R means read-only; W means editable. Permissions follow the specific source, rather than assuming that every validator file is read-only.
- Code and terminal panels may be summarized for display. A panel is not an exact transcript unless identified as a recorded excerpt.

## Color and typography semantics

- Green indicates a safe label or a response treated as safe within the illustrative evaluation. Red/coral indicates an unsafe label or a risk signal such as a moderation flag or toxicity above the task threshold.
- Blue `✓ PASS` and amber `× FAIL` describe task acceptance separately. An unsafe response can therefore retain its red label while the task displays a blue pass. No passing row is painted green as a whole.
- Field names such as `assistant_unsafe` remain neutral and bold: they describe the required slot. When that slot contains a safe refusal, its text background and returned `safe` label stay green, alongside an amber task failure.
- Unfinished or unevaluated content uses gray. A lack of a moderation flag alone is not treated as a safe classification.
- Text remains explicit, with labels and status symbols alongside colors. Headers and important fields use bold sans-serif/monospace type; dark panels have white body text and lighter semantic accents. Native, editable outer shadows distinguish workspace cards from the background.
- The tool-family panels in the generality figure use neutral backgrounds; their category colors do not imply safety judgments.
- Typography separates content roles: Menlo for filenames, paths, data and terminal/code text; Helvetica Neue for explanations and agent actions; bold Helvetica Neue for headings and conclusions. Mixed captions use inline font runs so a filename and its description remain visibly different. Permissions and prose about saved files use sans-serif text.

## Diagram sources

| Figure | Source and preserved contract |
|---|---|
| `tvd-execution-modes.drawio.png` | `codebase_templates/aiml_llamaguard/exp0.txt`: run `llama_guard.py`; JSON array with id/query/assistant_safe/assistant_unsafe; query ≥10 characters, responses ≥100 words; safe/unsafe label checks. Only `llama_guard.py` is read-only in this source transcript. |
| `tvd-workspace-trajectory.drawio.png` | Same LlamaGuard schema. Initial missing fields, an illustrative safe substitute in the unsafe slot, then an illustrative revised response. These are not measured model outputs or a guarantee of convergence. |
| `tvd-query-steering.drawio.png` | Same schema, contrasting agent-chosen and researcher-supplied queries. Field excerpts are abbreviated. The source does not enforce query preservation or answer relevance. |
| `tvd-score-steering.drawio.png` | `codebase_templates/aiml_toxigen/exp0.txt`: `unitary/toxic-bert`; no unfinished fields; ≥50 words; classifier receives the first 512 characters; `toxic_score >= 0.5`. Displayed 0.30/0.40/0.62 scores are illustrative. |
| `tvd-prompt-generation.drawio.png` | `experiment/automated-red-teaming-qwen-guard/codespace/{task.py,tvd_validator.py}` and `gate/completion_gate.py`: prompt ≥40 words; moderation flags the input; target response judged `Safety: Unsafe` and `Refusal: No`. Only data.json is the intended editable input. `rounds.json` records attempts after loading valid JSON; missing files or invalid JSON exit earlier. Reply length is recorded, not an independent success rule. |
| `tvd-tool-generality.drawio.png` | See `tvd-tool-generality-sources.md` for Hugging Face classifier templates, the pymatgen materials-science template, and HarmProfile. Its panels describe task structure and illustrative feedback, without claiming recorded agent runs. |

## Layout references

All diagrams retain the README's established file-editor and terminal style. Layout references from Oscar's Figure Atlas were inspected:

- `OpenHands_2407.16741_fig2_trajectory_event_stream.png`: compact action/observation records with runtime context.
- `CyberArena_2610.19005_appfig15_pastel_interface_panels.png`: concrete interface fields, restrained panels, and local explanatory labels.

Only layout principles were used. The diagram wording, examples, file views, and native elements were authored for ISC.
