# Park City Private Lesson Availability

The GitHub Pages calendar displays ski and snowboard private lesson availability for Canyons Village and Mountain Village. Each base has its own report, last-updated timestamp, monthly totals, and days-needed view.

Select a base on the calendar and click its Upload CSV button. Commit one Ski School Summary counts CSV directly to main. Use [Canyons Village uploads](uploads/) or [Mountain Village uploads](uploads/mountain-village/). GitHub sign-in and repository write access are required. The Publish availability action validates the reports and deploys the site.

The repository is public. Upload only aggregate availability counts.

Run `python3 scripts/import_csv.py` from the repository root to import the latest committed CSV for each base. The existing top-level fields in `data.json` hold Canyons Village data. The optional `mountainVillage` field holds Mountain Village data after its first upload.

## Cloudflare Pages

Connect this repository with the Git integration. Use `main` as the production branch, select no framework, set the build command to `sh scripts/build_cloudflare.sh`, and set the output directory to `dist`. The build imports the latest committed reports for each base and publishes the calendar and its aggregate data feed.

After the first successful deployment, add `afp.jd2012.work` under the Cloudflare Pages project's Custom domains. Verify the domain over HTTPS before retiring the GitHub Pages deployment.
