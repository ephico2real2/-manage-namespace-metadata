# -manage-namespace-metadata

### Python Script: `manage_namespace_metadata.py`

### How-to Guide

#### Step 1: Save the Script

Save the above script in a file named `manage_namespace_metadata.py`.

#### Step 2: Prepare an Example Argo CD Application YAML File

Create a sample Argo CD Application YAML file named `sample-application.yaml` in a directory named `yaml_files`. The structure should look like this:

```
yaml_files/
└── sample-application.yaml
```
Here is a sample content for `sample-application.yaml`:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: sample-application
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
  syncPolicy:
    managedNamespaceMetadata:
      annotations:
        existing-annotation: existing-value
      labels:
        existing-label: existing-value
```

#### Step 3: Run the Script

Navigate to the directory containing `manage_namespace_metadata.py` and execute the script with the following command:

```bash
python manage_namespace_metadata.py yaml_files --annotations new-annotation=new-value --labels new-label=new-value --remove-annotations existing-annotation --remove-labels existing-label --dry-run True --verbose
```

### Explanation of Command Arguments

- `yaml_files`: Directory containing the YAML files.
- `--annotations`: Key-value pairs of annotations to add.
- `--labels`: Key-value pairs of labels to add.
- `--remove-annotations`: List of annotations keys to remove.
- `--remove-labels`: List of label keys to remove.
- `--dry-run`: Set to `True` to perform a dry run without making changes.
- `--verbose`: Display verbose output.

#### Example Output

The output will show the actions taken, such as adding, updating, or removing annotations and labels. Since this is a dry run, no actual changes will be made to the files.

#### Applying Changes

To apply the changes, remove the `--dry-run` argument or set it to `False`, and add the `--apply-metadata` argument:

```bash
python3 manage_namespace_metadata.py yaml_files --annotations new-annotation=new-value --labels new-label=new-value --remove-annotations existing-annotation --remove-labels existing-label --apply-metadata True --verbose
```
This command will update the YAML files with the specified annotations and labels.

e.g.

```bash
argo-apps/
└── sample-app.yaml
```

```bash
python3 manage_namespace_metadata.py ./argo-apps/ --annotations linkerd.io/inject=enabled environment=production --remove-labels tier1  --labels hello=world --verbose --apply-metadata=true
```

#### Enhancement

#### Code Before the Change

Here is the original code snippet before the change:

```python
managed_metadata = doc.get('spec', {}).get('syncPolicy', {}).get('managedNamespaceMetadata')
if not managed_metadata:
    managed_metadata = {}
    doc['spec']['syncPolicy']['managedNamespaceMetadata'] = managed_metadata
```

#### Code After the Change

Here is the updated code snippet using the `get` method with a default value:

```python
managed_metadata = doc.get('spec', {}).get('syncPolicy', {}).get('managedNamespaceMetadata', {})
doc['spec']['syncPolicy']['managedNamespaceMetadata'] = managed_metadata
```

#### Explanation

**Before the Change:**
1. **Retrieve Value:** The code attempts to retrieve `managedNamespaceMetadata` from the nested dictionary structure using the `get` method.
2. **Check and Initialize:** If `managedNamespaceMetadata` is `None` or does not exist, the code initializes it as an empty dictionary.
3. **Assign Value:** The code then assigns this newly created empty dictionary back to `doc['spec']['syncPolicy']['managedNamespaceMetadata']`.

**After the Change:**
1. **Retrieve with Default:** The code directly retrieves `managedNamespaceMetadata` using the `get` method with a default value of an empty dictionary (`{}`). This ensures that if `managedNamespaceMetadata` does not exist, it will be initialized as an empty dictionary in one step.
2. **Assign Value:** The code assigns this value back to `doc['spec']['syncPolicy']['managedNamespaceMetadata']` without the need for an additional check and assignment.

#### Benefits of the Change
- **Simplification:** The updated code is more concise and easier to read, as it combines the retrieval and default initialization into a single step.
- **Reduced Redundancy:** It eliminates the need for an explicit check (`if not managed_metadata`) and manual initialization, making the code cleaner and more efficient.

This change streamlines the logic while achieving the same outcome, ensuring `managedNamespaceMetadata` is always a dictionary, either existing or newly created.

#### PR

Thank you for your suggestion. You are absolutely correct that using the get method with a default value simplifies the code and enhances readability. I have implemented your recommendation to provide a default value for managedNamespaceMetadata directly within the get method. This change makes the code more concise and ensures that managedNamespaceMetadata is always properly initialized.


#### Code Before the Change

Here is the original logging configuration:

```python
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
```

#### Code After the Change

Here is the updated logging configuration to include timestamps:

```python
# Set up logging with timestamp
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
```

#### Explanation

**Before the Change:**
- **Logging Configuration:** The logging configuration was set to display the log level (`%(levelname)s`) and the log message (`%(message)s`) without timestamps. This resulted in console log messages that did not include any time information, making it harder to track when each log entry was created.

**After the Change:**
- **Logging Configuration with Timestamps:** The logging configuration has been updated to include the timestamp (`%(asctime)s`) in the log messages. The `format` parameter specifies that each log message should include the timestamp (`%(asctime)s`), the log level (`%(levelname)s`), and the message (`%(message)s`). Additionally, the `datefmt` parameter is used to define the format for the timestamp (`'%Y-%m-%d %H:%M:%S'`), ensuring that the timestamps are displayed in a readable format.

#### Benefits of the Change
- **Enhanced Logging:** By including timestamps in the console logging output, it becomes easier to track when each log entry was made, which is especially useful for debugging and monitoring the script's execution.
- **Consistency:** This change ensures that both the console output and the `change_log.txt` file contain consistent timestamped entries, providing a more comprehensive and synchronized logging experience.

#### Example Output

**Console Output:**

```
2024-07-24 11:47:32 - INFO: Skipping annotation 'linkerd.io/inject=enabled' for file: sample-app.yaml (already exists)
2024-07-24 11:47:32 - INFO: Skipping annotation 'environment=production' for file: sample-app.yaml (already exists)
2024-07-24 11:47:32 - INFO: Skipping label 'hello=world' for file: sample-app.yaml (already exists)
2024-07-24 11:47:46 - INFO: Removing label 'hello' for file: sample-app.yaml
2024-07-24 11:47:46 - INFO: Modified content for file: sample-app.yaml
```

**change_log.txt:**

```
2024-07-24 11:47:32 - Skipping annotation 'linkerd.io/inject=enabled' for file: sample-app.yaml (already exists)
2024-07-24 11:47:32 - Skipping annotation 'environment=production' for file: sample-app.yaml (already exists)
2024-07-24 11:47:32 - Skipping label 'hello=world' for file: sample-app.yaml (already exists)
2024-07-24 11:47:46 - Removing label 'hello' for file: sample-app.yaml
2024-07-24 11:47:46 - Updated file: sample-app.yaml
```

This ensures that all log messages, both in the console and in the log file, are timestamped for better traceability and consistency.
