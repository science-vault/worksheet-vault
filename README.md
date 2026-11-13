# Worksheet Vault — WA Curriculum Years 7–12

Independent static website repository, not a folder of Science Vault or Practice Studio.

## Directory convention

`uploads/<learning-area>/<subject>/year-<7-10>/<topic-or-strand>/worksheets/`

`uploads/<learning-area>/<subject>/year-<7-10>/<topic-or-strand>/answer-keys/`

The directory structure includes all eight WA Curriculum learning areas. The languages and topics are broad organisational placeholders, **not** an exhaustive, verified list of SCSA curriculum codes or subjects taught at every school. Add subjects and year-specific topics to `catalogue/curriculum-structure.json` as needed.

## Important storage limitation

The upload form is a browser-local prototype. It suggests the correct repository directory but **does not write uploaded files into the repository**. To publish shared worksheets, commit files to the corresponding folder or add authenticated cloud storage and a server-side upload API. Do not upload copyrighted or student-sensitive material without permission.

## Deployment

Create a separate GitHub repository named `worksheet-vault`, upload this folder's contents, then enable GitHub Pages from the main branch/root. GitHub Pages alone is static hosting, not a writable shared worksheet database.

## Years 11–12

Senior secondary worksheets are organised by **year, course pathway (ATAR / General / Foundation / Preliminary / VET), learning area, course, and unit or topic**. Example:

`uploads/senior-secondary/year-12/atar/science/physics/unit-3/worksheets/`

The senior-secondary catalogue lists representative courses, not a certified exhaustive SCSA course list. Courses are not necessarily available in every pathway. Create only valid course/pathway combinations when adding content. The browser-only upload limitation still applies.

## Strand-based filing (v1.1)
Years 7–10: `uploads/<learning-area>/<subject>/year-<year>/<strand>/<topic>/worksheets/` and matching `answer-keys/`.

Years 11–12: `uploads/senior-secondary/year-<year>/<pathway>/<learning-area>/<course>/<unit>/<strand>/<topic>/worksheets/` and matching `answer-keys/`. The supplied senior folders use placeholders until the actual pathway, course unit and strand are confirmed.

The upload form now has separate Strand and Topic fields. Suggested paths do not write to GitHub; browser-only storage remains in effect. Existing folders are retained for compatibility.


## Reviewed resources

Science resources are reviewed by content for SCSA year, strand and topic, resource type, usefulness and publisher. Types include worksheets, information sheets, experiments, activities, revision booklets and teaching guides. Mixed resources can have multiple type tags. Publisher labels require document branding or attribution; image-agency credits do not identify the publisher.

Keep useful enrichment in Extra Worksheets. Exclude unusable files, unrelated material and proven duplicates from the public catalogue while retaining original files. A matching reviewed content hash is required before new or changed files can appear publicly. Unknown sources remain uncredited. The content review and exclusions are recorded in catalogue/resource-review.json and catalogue/withheld-resources.json.
