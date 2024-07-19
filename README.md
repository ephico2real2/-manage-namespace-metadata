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

