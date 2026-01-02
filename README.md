# Excel Matrix to SQL ETL Pipeline

## Overview
This project simulates a production ETL pipeline for ingesting operational Excel reports with merged cells, multi-level headers and logically distinct matrices into a SQL Server reporting table

## Source Data Challenges
- MultiIndex column headers (Date / Provider)
- Merged cells requiring forward-fill
- Multiple logically distinct matrices within a single worksheet
- Tables that grow dynamically in both row and column dimensions, making fixed positions unreliable

## Pipeline Design
- Pandas for extraction, transformation and reshaping
- SQL Server Staging tables for controlled bulk loading
- Stored procedures for downstream processing and reporting transformations

## Key Engineering Decisions
### Vectorised unpivoting of matrix-style data
- The source Excel worksheet is built for human use and presents data as multiple matrices with dates and providers stacked across columns. The pipeline uses melt() to unpivot the data as it is a vectorised solution that handles multi-indexed data well
### Window-based extraction of multiple matrices
- The worksheet contains multiple logically distinct matrices separated by header and total rows. Start and end indices for each matrix are identified using their text value (e.g. totals rows). This avoids hard-coding row numbers and allows the pipeline to tolerate layout changes such as additional rows or reordering
### Separation of Python and SQL responsibilities
- Python is used for data extraction, structural reshaping, and quality enforcement, while SQL Server stored procedures handle business rules and reporting logic. This separation keeps Python code focused and testable, while allowing SQL logic to remain close to the reporting layer where performance and maintainability are critical
### Use of staging tables prior to reporting loads
- Data is first loaded into staging tables before being processed into reporting tables. This provides isolation from downstream consumers, enables replayability, and mirrors the processing of other data sources into the same reporting dataset for consistency and tracability
### Explicit handling of pandas views and copies
- Filtered DataFrames are explicitly copied where there is a risk of operating on a view. This avoids the risk of operating on a view, rather than an altered DataFrames

## Data Flow
- Excel → Pandas → SQL Staging → Stored Procedures → Reporting Table

## Limitations & Next Steps
- Incremental loads
- Row-level change detection using row-hashing
- Add logging and error handling
