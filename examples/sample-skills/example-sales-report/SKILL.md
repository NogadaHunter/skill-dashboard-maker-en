---
name: example-sales-report
description: "(Made-up skill for the example) Takes a sales spreadsheet and builds a report XLSX and a one-page PDF with a monthly trend chart and summary. Use this skill when the user: - asks for a sales report (\"make a sales report\") - wants a spreadsheet analyzed (\"analyze this spreadsheet and summarize it\") - asks for a trend chart (\"chart the monthly trend\")"
---

# example-sales-report

A made-up skill that exists only to show what skill-dashboard-maker produces.

## Input
- Sales data as XLSX or CSV (date, product and amount columns)

## Steps
1. Find the date and amount columns and total them by month.
2. Work out the month-over-month change and the top 5 products.
3. Build a summary sheet with a monthly trend chart.
4. Save a report XLSX and a one-page summary PDF.

## Requires
- Code execution (file creation)
