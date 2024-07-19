### Jira Story

**Summary:**
Create a Python script to manage metadata in Argo CD Application YAML files.

**Description:**
Develop a Python script to update metadata (annotations and labels) in Argo CD Application YAML files. The script should validate YAML files, log changes, and optionally update the files based on provided arguments.

**Acceptance Criteria:**
1. The script should accept the following command-line arguments:
   - Directory containing YAML files
   - Key-value pairs of annotations to add
   - Key-value pairs of labels to add
   - List of annotation keys to remove
   - List of label keys to remove
   - Dry run option
   - Apply metadata changes option
   - Verbose output option

2. The script should:
   - Validate YAML files in the specified directory
   - Log changes to a file
   - Add, update, or remove annotations and labels based on the provided arguments
   - Perform a dry run if the dry run option is specified
   - Apply metadata changes if the apply metadata option is specified

3. Provide a step-by-step guide on how to use the script, including an example of an Argo CD Application YAML file.

**Attachments:**
N/A

**Assignee:**
[Your Name]

**Priority:**
Medium

**Labels:**
Python, YAML, Argo CD, Metadata Management

**Story Points:**
3

**Tasks:**
- [ ] Set up logging for the script.
- [ ] Create a function to validate YAML files.
- [ ] Create functions to add, update, and remove annotations and labels.
- [ ] Implement command-line argument parsing.
- [ ] Develop the main function to coordinate the script's actions.
- [ ] Test the script with various scenarios to ensure it works as expected.
- [ ] Document the usage of the script with examples.
