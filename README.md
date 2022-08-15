# Github Action for executing an Upsolver SQLake worksheet

This Github Action allows you to execute a set of SQLake SQL commands that create a data pipeline.
SQL commands are written in a SQLake Worksheet in sequantial order. This means that creating connections and tables must come before creating jobs or executing SQL queries against tables.

Here is an example of a Github Action workflow that finds worksheets in your repo and executes the SQL
commands within each of them.

```yaml
name: Run a SQLake Worksheet
on:
  push:
    branches:
      - master
jobs:
  run_worksheet:
    runs-on: ubuntu-latest
    name: Run Worksheet
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run Worksheet
        uses: rhasson/sqlake_action@main
        id: run_step
        with:
          worksheet_path: src/worksheets
          api_key: ${{ secrets.API_KEY }}
      - name: Print Results
        run: echo ${{ steps.run_step.outputs.query_results }}
```
<br>

## Configuring your Action
The Github Action takes as parameter the path to your worksheets inside the repo and the Upsolver API token you will use to authenticate with SQLake.

```yaml
with:
    worksheet_path: src/worksheets
    api_key: ${{ secrets.API_KEY }}
```
`worksheet_path` is a relative path within your repository where Worksheets are stored
`api_key` is the SQLake API token that you create within the Upsolver platform. Note, that the key should be stored in Github Secrets within your repo.