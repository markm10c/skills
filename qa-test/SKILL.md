---
name: qa-test
description: Run an agent QA pass over a project's QA sheet on staging - drive the web, admin or app through each row, record PASS/FAIL/SKIP with notes in the sheet, and publish screenshot proof next to the designs. Use when asked to run, test or do an agent pass on a QA/testing sheet. Runs before QA's own first pass; it never replaces it.
---

A pre-check before QA's first pass: does the build match the sheet's rows (the UI and the main flows)? QA still does the full pass. The agent never sets STATUS or touches QA's result columns.

## Gather the inputs first

Ask for these one at a time. Skip any question already answered in the arguments or earlier in the conversation.

1. **Sheet:** the Google Sheet link and tab.
2. **Platforms:** web, admin and/or app, and which sections or rows (default: all the rows for those platforms).
3. **Designs:** Figma links or spec images to compare screenshots against. Default: the images in the spec.
4. **Spec changes:** has anything changed since the sheet was written (client AT feedback, Slack decisions)? If so, check the rows against those changes first, so later changes don't show up as fails.
5. **What the agent may change on staging:** default is view only. Ask whether it may place a small order (Dream Points or a staging test card only, never real card details) or create test data in admin. If yes, prefix anything it creates with "QA AI" so it is easy to find and delete.

## Logins

The agent never types passwords or completes 2FA. A person signs in once, and the agent reuses that session.

- **Web and admin:** start a separate Chrome with its own profile and remote debugging, open the staging URLs, and ask the user to sign in:
  ```bash
  open -na "Google Chrome" --args --remote-debugging-port=9222 --user-data-dir=<project>/.claude/qa-sheets/chrome-profile
  curl -s -X PUT "localhost:9222/json/new?<staging url>"
  ```
  Check the open tabs with `curl -s localhost:9222/json/list`. In argent this browser is `chromium-cdp-9222`.
- **App:** use a running simulator or emulator (argent `list-devices`), with the user signed in on the staging build.
- Use staging and the approved test accounts only. Never production.

## Sheet columns

Insert three columns straight after EXPECTED, before QA's first test columns: **AGENT RESULT**, **AGENT NOTES** and **AGENT PROOF**. Use the Sheets MCP `update_spreadsheet`:
- `insertDimension` for the 3 columns, then write the headers.
- `setDataValidation` on AGENT RESULT: `ONE_OF_LIST` PASS / FAIL / SKIP, with `showCustomUi: true`.
- Three `addConditionalFormatRule` (`TEXT_EQ`) rules: PASS green, FAIL red, SKIP blue.
- Make AGENT NOTES about 280px wide.

If the columns already exist from an earlier pass, reuse them. Don't touch any other column.

## Running the pass

Delegate the testing to a subagent (one per platform section for big sheets), so screenshots don't fill the main context. Give it:
- The rows as a local TSV (`.claude/qa-sheets/<project>/rows.tsv`, exported with `get_values`; line N = sheet row N+1), plus the design images.
- The device id, and an instruction to read the `argent-device-interact` skill before the first argent call. Coordinates come from `describe`, never from screenshot pixels. On Chromium, scroll with `gesture-scroll` and switch tabs with `chromium-tabs`. Content inside iframes (e.g. an admin preview or simulation) may not show in `describe`; small CDP scripts on port 9222 can press buttons there.
- The staging data rules from input 5, and the rule never to log in or type passwords.
- **What to test:** the UI against the design and the main flows. **SKIP with a short reason:** emails, notifications, anything that takes hours or days (auto-reveal on close, scheduled jobs), statistics over many runs, rare data the environment doesn't have, and platforms outside this pass. Use existing test competitions or data first; use admin previews or simulations when real data is missing.
- **Judging:** FAIL only for clear mismatches (wrong or missing copy, missing elements, broken flows). Ignore small pixel differences. Record anything notable the rows don't cover in the final reply, not as new rows.
- **Proof:** save a screenshot per tested row as `proof/r<sheet row>.png` (one screenshot can serve several rows), and note the matching design image.
- **Output:** write `agent-results.tsv` as you go (`sheet_row, result, notes, proof, design`), so a crash keeps partial results.

## Proof page and results

1. Convert the screenshots and design images to JPEG in `site/proof/` and `site/design/` (`sips -s format jpeg -s formatOptions 70 -Z 1400`).
2. Build the page with this skill's helper:
   ```bash
   python3 -I ~/.claude/skills/qa-test/build_proof.py <run dir> ~/.claude/skills/qa-test/proof-template.html "<Project name>"
   ```
   It writes `site/index.html` and `sheet-values.json`.
3. Publish `site/index.html` with the Artifact tool, using `root` = `site` and the images in `files`. The page is private; the user shares it if needed.
4. Replace `{{URL}}` in `sheet-values.json` with the artifact URL, and write the values into the three agent columns. AGENT PROOF links to `<url>#r<row>`.

## Reply

- Counts of PASS, FAIL and SKIP.
- Each FAIL in one line, with its row number. Note when a fail may be a later spec change rather than a bug.
- Anything notable outside the rows.
- What blocked the agent (logins, data, tooling).
- Side effects on staging, such as orders placed or data created.
- The sheet and proof page links.

A full pass costs roughly $10-15 at Opus 5.5 API prices, mostly from re-reading screenshots. Splitting the run per section and using smaller screenshots both keep it down.
