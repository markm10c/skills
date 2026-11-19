---
name: prepare-qa-sheet
description: Draft the up-front QA test rows for a project from its spec and final designs, in the team's Google Sheet format. Use when asked to prepare, draft or write a QA/testing sheet or test cases for a spec, or to fill a copied QA template.
---

Write the rows QA would prepare before testing starts. The rows describe what the spec and designs say should happen. QA reviews them, adds their own, and logs issues during testing. They are not exhaustive test plans.

## Gather the inputs first

Ask for these one at a time, in this order. Each answer can be one link or several, and the questions after the spec can be skipped. Skip any question already answered in the arguments or earlier in the conversation, and don't start drafting until you have the spec and the sheet.

1. **Spec:** links to the spec (gist or markdown). Several parts are fine.
2. **Designs:** Figma links, per platform if they are separate (web, app, admin). If none are given, use the images in the spec.
3. **Other files:** anything else relevant, such as HackMD notes, test plans or earlier decisions. Read these for context only; rows still come from the spec and designs.
4. **Sheet:** the Google Sheet link, usually a fresh copy of the QA template.

Source rules:
- **Designs:** use the final frames and their sticky notes (the blue boxes) only. Never read Figma comments.
- **Not sources:** repo code (it is never the source of expected behaviour) and other projects' QA sheets, except as examples of the format.
- **Sheet:** write into a new tab duplicated from the template tab ("New QA Testing" or "Project Fulfilment Testing Template"), unless told to use an existing one. Read the header row and match columns by name.

## Steps

1. Read the spec end to end, then every design (images and Figma frames), then the other files. Note which platforms are in scope (web, app, admin) and in what order the spec covers them.
2. List where the spec and the designs disagree: copy, behaviour, things only drawn or only written. These go in your reply as questions for the spec writer, not as rows. Where they disagree, the row follows the spec, unless a sticky note clearly overrides it.
3. Write the rows (rules below). Save them to a local TSV first (`.claude/qa-sheets/<project>/rows.tsv`), then write them to the sheet starting at row 2.
4. Reply with: the tab link, row counts per platform section, the spec/design mismatches, and any part of the spec you left out and why.

## Columns

Fill only TOP LOCATION / Location level 1, SECTION / Location Level 2, TEST CASE and EXPECTED. Leave Status, Side, Priority, the result columns and everything to the right empty: testers fill them in. Use no IDs; QA and AT reference numbers are added only when issues are logged.

## Structure

- First rows: a **General** row (EXPECTED = 1-3 sentences from the spec intro on why the project exists), then a **Design** row (TEST CASE = "Design", EXPECTED = the Figma link).
- **Platform header rows** have text in column A only, in capitals (`WEB`, `APP`, `ADMIN`, `WEB & APP`), with a blank row before each. Follow the spec's order.
- TOP LOCATION is the page or feature area from the spec ("Competition Page", "Order Success", "Setting Up Incentives"). SECTION is the sub-area or variant ("FAQ", "Dream Points", "A/B Test"), and is often blank. Keep rows grouped in spec order.

## How to write a row

- **EXPECTED** is the spec sentence or bullet, copied nearly word for word in the spec's own voice ("We're adding...", "Admins can..."), typos included. Paste exact UI copy in quotes.
- **TEST CASE** is blank or a short label of 1-8 words: the element ("Share message", "+X more games"), a condition ("No goals set up", "For Dream Points reward:"), or sticky-note text as written.
- **One behaviour per row.** If 2-3 spec sentences describe the same element, merge them into one row rather than splitting off rows that only restate copy or layout. A spec list becomes a lead-in row plus one row per item when each item is separately testable (statuses, prize types, game types).
- A row may have a TEST CASE label and an empty EXPECTED when it is just "check this screen against the design" ("Order Success screen").
- **Design-only details:** add a row only when a sticky note or a drawn state describes behaviour the spec doesn't ("Hide the add button after the second image"). Skip pure visual details such as sizes, colours and spacing; the Design link covers those.
- **Scenario rows:** where the spec's behaviour depends on counts or outcomes, add a few concrete scenarios in TEST CASE with the result in EXPECTED. For example "12 tickets" -> "Packs of 5, 5 and 2", "100 tickets, no win" -> "Results screen shows no win". Keep it to the cases the spec's rules imply (boundaries the spec names, win vs no win), 2-5 per rule. Don't invent edge cases.

## App section

- Open with "Test old version of the app for compatability" and "Uses the same logic as the web designs."
- Then **repeat the testable behaviour rows from WEB** that apply on the app: flows, result states, counts and scenarios, reveal logic, notifications and emails triggered from the app. Replace placeholders with concrete values where the spec gives them. App-only bugs are found in these rows, so don't collapse them into "same as web".
- Skip web rows that are purely about web layout (desktop widths, hover states), and add the app-only rows the spec or designs have (tablet, native screens, push notifications).

## Admin section

Admin rows are fewer and coarser than web rows: one row per setting or screen behaviour (what the option does, what's required, what's shown on the overview page), not one per button or label.

## Amount

Roughly 2-8 rows per spec sub-section. As a guide, a mid-size project (one main flow plus admin settings) lands around 80-120 rows, and a large one with web and full app repetition around 150-200. If you're well over that, you're splitting copy into separate rows; if well under, you're summarising the spec instead of copying it.

## Don't

- Write steps, Given/When/Then, "should" assertions or IDs.
- Add edge cases, negative tests or device checks the spec doesn't mention. QA adds those during testing.
- Add rows for scope listed on the canvas or in Slack but not in the spec. Mention it in the reply instead.
- Touch existing tabs or other people's rows.
