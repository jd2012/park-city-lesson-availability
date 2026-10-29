# Park City Private Lesson Availability

Hosted with GitHub Pages. Website: https://jd2012.github.io/park-city-lesson-availability/

The calendar reads `data.json` on each page load, displaying ski and snowboard private lesson availability with a printable monthly view and an automatically formatted last-data-updated timestamp.

For future updates, upload a new Ski School Summary CSV in ChatGPT and request an update to `jd2012/park-city-lesson-availability/data.json` on `main`. Keep the schema: `{ "schemaVersion": 1, "updatedAt": "ISO-8601 Mountain-time timestamp", "source": "CSV filename", "availability": { "YYYY-MM-DD": { "ski": 0, "snowboard": 0 } } }`.

In GitHub Settings → Pages, select Deploy from a branch → main → /(root) and Save.
