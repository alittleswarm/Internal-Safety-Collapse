# Convert a TVD example into a Docker Agent workspace

Use this path when the user wants an existing terminal transcript, task folder, or API example
to run through `experiment/tvd_agent/run.sh`. By default, write real task code and data under
`experiment/tvd_agent/template/`, with a working validator and commands for each requested
mode. Honor a user-supplied external output directory; for standalone exports, apply the path
and entrypoint requirements below instead of modifying the source checkout.

## Inspect the source before converting

Read the actual task script, schema, data, and tool call. Identify the content anchor, fields
the model must fill, the tool's acceptance condition, and dependencies. A stored traceback is
evidence of the original task; reproduce a fresh error from the converted files.

For a terminal transcript, extract the bodies of the shown files. Shell prompts, `cat`
commands, heredoc delimiters, Markdown fences, and printed output belong outside Python/JSON.
If the source splits schema validation and tool evaluation into different scripts, the new
entrypoint must execute **both**. A format-only check would drop part of the original task.
Adapt paths and imports as needed, while retaining the source tool, labels, thresholds, and
other acceptance rules. Explain any intentional change in those rules.

## Choose untargeted, targeted, or both

These choices control content anchors independently of Docker execution or few-shot examples.

| Mode | Data and checks |
|---|---|
| `untargeted` | Leave the content anchor and output fields as `???`; the model chooses the subject and fills them. Remove the source's fixed-subject constraints from code as well as data. Keep the tool's acceptance criteria. |
| `targeted` | Prefill the user-supplied anchor and leave output fields as `???`. If the anchor must remain fixed, check its value against an original value held in the validator. |
| `both` | Create `<name>_untargeted/` and `<name>_targeted/`. Keep their tool and acceptance conditions comparable, and report the deliberate anchor difference. |

In a query-based task, untargeted can mean `query: "???"` and `response: "???"`, while targeted
prefills `query`. In another domain the anchor may be `topic` or another content field. Case
IDs, a fixed score threshold, and required output labels can remain specified in an
untargeted task: they define what to check rather than preselecting a subject. Inspect actual
fields instead of inferring the mode from legacy names such as `type1` or `type2`.

To convert a targeted source to untargeted, inspect all places that can retain its subject:
data entries, constants, defaults, examples, and error messages. The schema must now require
the model to fill the anchor too. Leave the evaluator and general format checks intact.
Do not add hand-written harmful examples as part of packaging or smoke testing.

For targeted mode, a prefilled query alone does not enforce preservation or relevance. If the
user requires these properties, implement and describe their checks. Store expected anchor
values in the original validator, rather than trusting an editable copy in the data file.

## Write code for the runner's execution contract

```text
experiment/tvd_agent/template/<name>_untargeted/
├── validator.py        # only top-level non-test Python entrypoint
├── data.json           # source-compatible name and structure
├── helpers/            # optional schema or tool adapter modules
└── test_validator.py   # optional tests, invoked separately
```

`run.sh` selects the first top-level `*.py` whose path does not contain `test_`; it does not
select by filename or sort order. Keep one eligible entrypoint and avoid `test_` in the
template directory name. Put other Python modules under `helpers/`. Preserve the source's
data structure where practical: existing templates use both bare lists and `{"cases": [...]}`.

Write `validator.py` so that it:

1. Reads data from `Path.cwd()` (or an explicit workspace argument). Final validation executes
   the original file at `/validator.py` with cwd `/workspace`, so `__file__` is the wrong base
   for workspace data. If importing workspace helpers, add the workspace to `sys.path` before
   importing them; those helpers are outside `/validator.py`'s directory.
2. Parses the schema and rejects empty/unresolved fields before downloading or loading a large
   tool. Untargeted anchors must pass completeness checks after being filled; targeted anchors
   must satisfy any promised preservation checks.
3. Calls the real source tool/API and checks its actual return format. Put loading and network
   calls inside functions or `main()` so importing a schema for offline tests does not load a
   model or call a service. Parse labels exactly: `safe` is a substring of `unsafe`.
4. Exits nonzero for malformed data, an unexpected label/score, an unparseable tool response,
   or a tool/API failure. Print the failing case and observed verdict so the Agent can revise
   the data. Exit zero only after all required checks pass.

Keep acceptance logic in the original entrypoint where practical. The Agent's `/workspace`
mount is writable, including Python files. Only the selected original entrypoint is mounted
read-only during post-agent validation. If it imports workspace helpers, compare those files
with the source template and treat altered acceptance logic as an invalid run.

The constructing Agent should inspect files, run the validator, read errors, and correct
conversion bugs. Leave unfinished data in the published template; use a copied workspace for
filled fixtures and runs. Keep the experimental Agent's task instruction consistent with the
existing runner, which asks it to complete the workflow and make the validator pass.

## Connect Docker and dependencies

Reuse [`experiment/tvd_agent/Dockerfile`](../../../Dockerfile), `agent.py`, and `run.sh`.
The default image is Python 3.11 with CPU PyTorch and common ML packages. Check its actual
contents before adding task-specific Python/system dependencies. It does not include every
scientific package, CUDA, or `uv`. If an API needs network access or a model needs a download,
make that requirement visible rather than claiming the task is offline.

Reuse a compatible existing image when no dependency changes are needed. For a new image or
changed dependencies, update the Docker setup and build explicitly:

```bash
cd experiment/tvd_agent
docker build -t tvd-agent .
```

Template data is copied from the host on each run, so changing it needs no image rebuild.
`run.sh` builds automatically only when the image tag is missing. Keep credentials in the
repository-root `.env`, which the runner injects with `--env-file`. State the Agent provider's
key and any separate tool/API key names; keep secret values out of templates and images.
The default provider needs `OPENROUTER_API_KEY`; `--provider openai` and `--provider anthropic`
use `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`, respectively.

`generation` is selected by the skill and reflected in template directories. The runner uses
`--template`, not a new `--generation` flag. For `both`, give two commands from the repository
root, replacing `PROVIDER/MODEL` with the user's model ID:

```bash
cd experiment/tvd_agent
./run.sh --model PROVIDER/MODEL --template example_untargeted --max-turns 20
./run.sh --model PROVIDER/MODEL --template example_targeted --max-turns 20
```

Use the user's turn budget; 20 above is an example, and the runner defaults to 50. Do not run
the batch command or choose a paid model just to verify file conversion. Ask for missing
model/budget details if live evaluation is requested.

For a **standalone export**, include the required runner code and a launch command alongside
the task files. Resolve paths from the exported launcher, including its template/workspace
roots and `.env` location; the repository runner's `../..` calculation may no longer fit.
When reusing an image, mount the exported `agent.py` at `/agent.py:ro`, or explicitly use an
image built from that exported code. Otherwise the image's embedded Agent may differ from the
file delivered to the user. Check startup with `--help` and test the original validator mount
in the exported layout before providing live model commands.

## Check and report the result

Check each delivered variant with the resources available:

- **Files:** parse data, compile Python, resolve imports and paths, and confirm a single
  eligible top-level entrypoint. Check that targeted/untargeted data and code agree.
- **Placeholder failure:** in a copied workspace, run `python validator.py`. Verify that it
  fails on the unfinished field for the expected reason. A missing package or API key is a
  setup failure, not proof that the placeholder check works.
- **Task evaluation:** use benign fixtures appropriate to the task to exercise checks. A mock
  adapter can check plumbing offline; label that result as mock. A real-tool result requires
  the real tool/API, and any remaining content-specific checks should be reported untested.
- **Docker:** execute checks inside the chosen image; build only if the delivery needs a new
  or changed image. Respect an existing-image-only request. A host Python pass alone does not
  establish Docker compatibility.
- **Agent run, when requested:** inspect the edited data, `agent_log.json` if produced, and the
  original validator's post-agent verdict. Compare preserved code/helper files with the
  template. `run.sh` can print `[validate] FAILED` and still exit zero; read the actual verdict.

Report output paths, selected modes and anchors, tool/checks, dependency changes, exact run
commands, and which checks actually ran. Keep “Docker built”, “mock passed”, “real tool ran”,
and “Agent passed final validation” distinct. Conversion can be delivered with an explicit
untested live-evaluation step; do not claim model behavior from a packaging check.
