# Create an Agent that Stores Information and Creates Templates

## Objective
Develop an agent that merges client data with templates to generate the final legal document and delivers it.

## Implementation Steps

### Template Storage

  - [x] Store templates in formats like `.txt` or `.docx` or `.json` 
  - [x] Define a clear placeholder Syntax
  - [x] Create a mock Define a clear placeholder Syntax
  - [x] Upload the files to the project to test them in local

### Agent Functionality

  - [] Read file from  the localpath
  - [] Read the client information file
  - [] Use `re` library to find all the markers 
  - [] Replace all the markers
  - [] Create a new file

- Data Insertion: Use string replacement or templating libraries to insert data into placeholders.

#### Example Libraries:
- **Python**: `string.Template`, `Jinja2`

### Simplifications
- **No Database**: Templates are stored locally, so no database is needed.
- **Version Control**: Use manual version control (e.g., file backups) during initial development.


