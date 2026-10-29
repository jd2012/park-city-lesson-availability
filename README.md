# Park City Private Lesson Availability

Public printable ski and snowboard lesson availability calendar.

## Hosting

Enable GitHub Pages in **Settings → Pages → Build and deployment → Deploy from a branch**, choose **main** and **/(root)**, then **Save**.

The expected public URL is: https://jd2012.github.io/park-city-lesson-availability/

## CSV refresh workflow

Future updates only require replacing `data.json` with the validated latest Ski School Summary CSV data, retaining the same schema. The `updatedAt` ISO timestamp should reflect the actual data update time using the correct Mountain Time offset. The calendar fetches `data.json` from this public repository on each visit, and falls back to the original bundled data if unavailable.

Do not add staff names, contact info, or other private records to this public repository.
