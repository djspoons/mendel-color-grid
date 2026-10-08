# Photo release (CC0 publication)

One release per person shown. Children: a parent or legal guardian signs on the
child's behalf (see RIGHTS.md). Store the signed scan or the recording as
`releases/<release id>.pdf` (or `.m4a`, `.mp4`) and list it in `manifest.json`.

Release id: R-___            Date signed: ____-__-__ (YYYY-MM-DD)

## Who is shown

- Name of person shown: ______________________
- Role (tick one):  [ ] adult, signing for self
                    [ ] child, signed by parent or legal guardian
- If a child: age at signing ____; guardian name ______________________;
  relationship [ ] parent  [ ] legal guardian

## What I agree to

1. The photographer named below may photograph me (or my child) for a
   software-testing photo set.
2. The photographs will be released under the Creative Commons CC0 1.0
   Universal dedication, so anyone may copy, modify and reuse them for any
   purpose, including commercial use, without asking and without credit. This
   cannot be undone for copies already made.
3. The photographs are published without my name, and no personal details are
   stored with them. The metadata (location, device, time) is removed.
4. I am not paid, and I have not been promised that I will be identifiable only
   in particular contexts. Photos may be shown in any software, test or product.
5. I may refuse any photo and may withdraw consent for photos not yet committed.
   Photos already committed and copied cannot be recalled.
6. A child aged 7 or over was asked whether they are happy to be photographed and
   agreed. A child who says no, or looks unhappy, is not photographed.

Signature (or "recorded"): ______________________
Photographer: ______________________        Shoot date: ____-__-__

## Recorded release (instead of a signature)

Record audio or video in which the person (or guardian) says, clearly: their
name, today's date, the release id, and the words "I agree that photographs of
me [or my child, naming them] may be released under CC0 for any purpose."
Store the recording and note `"type": "recorded"` in the manifest.

## Manifest entry to add

```json
{"id": "R-001", "type": "signed", "role": "adult", "file": "releases/R-001.pdf",
 "sha256": "<sha256 of the file>", "signed_on": "YYYY-MM-DD", "covers_cc0": true}
```

For a child add `"role": "minor_by_guardian"` and `"guardian_relationship": "parent"`.
