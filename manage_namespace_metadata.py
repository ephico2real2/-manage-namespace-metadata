# Filename: manage_namespace_metadata.py

import os
import yaml
import argparse
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
change_log = 'change_log.txt'

def log_change(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(change_log, 'a') as log_file:
        log_file.write(f"{timestamp} - {message}\n")

def validate_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            documents = list(yaml.safe_load_all(file))
        return True, documents
    except yaml.YAMLError as e:
        logging.error(f"YAML validation error in {file_path}: {e}")
        return False, None

def update_yaml_files(directory, annotations, labels, remove_annotations, remove_labels, dry_run, apply_metadata, verbose):
    if not os.path.isdir(directory):
        logging.error(f"Directory does not exist: {directory}")
        return

    try:
        for filename in os.listdir(directory):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                file_path = os.path.join(directory, filename)
                
                valid, documents = validate_yaml(file_path)
                if not valid:
                    continue
                
                updated = False
                for doc in documents:
                    if doc.get('kind') == 'Application':
                        managed_metadata = doc.get('spec', {}).get('syncPolicy', {}).get('managedNamespaceMetadata')
                        if not managed_metadata:
                            managed_metadata = {}
                            doc['spec']['syncPolicy']['managedNamespaceMetadata'] = managed_metadata
                            
                        # Update annotations
                        metadata_annotations = managed_metadata.get('annotations', {})
                        for key, value in annotations.items():
                            if key in metadata_annotations:
                                if metadata_annotations[key] == value:
                                    logging.info(f"Skipping annotation '{key}={value}' for file: {filename} (already exists)")
                                    log_change(f"Skipping annotation '{key}={value}' for file: {filename} (already exists)")
                                else:
                                    logging.info(f"Updating annotation '{key}' from '{metadata_annotations[key]}' to '{value}' for file: {filename}")
                                    log_change(f"Updating annotation '{key}' from '{metadata_annotations[key]}' to '{value}' for file: {filename}")
                                    metadata_annotations[key] = value
                                    updated = True
                            else:
                                metadata_annotations[key] = value
                                updated = True
                        
                        for key in remove_annotations:
                            if key in metadata_annotations:
                                logging.info(f"Removing annotation '{key}' for file: {filename}")
                                log_change(f"Removing annotation '{key}' for file: {filename}")
                                del metadata_annotations[key]
                                updated = True
                        
                        managed_metadata['annotations'] = metadata_annotations
                        
                        # Update labels
                        metadata_labels = managed_metadata.get('labels', {})
                        for key, value in labels.items():
                            if key in metadata_labels:
                                if metadata_labels[key] == value:
                                    logging.info(f"Skipping label '{key}={value}' for file: {filename} (already exists)")
                                    log_change(f"Skipping label '{key}={value}' for file: {filename} (already exists)")
                                else:
                                    logging.info(f"Updating label '{key}' from '{metadata_labels[key]}' to '{value}' for file: {filename}")
                                    log_change(f"Updating label '{key}' from '{metadata_labels[key]}' to '{value}' for file: {filename}")
                                    metadata_labels[key] = value
                                    updated = True
                            else:
                                metadata_labels[key] = value
                                updated = True
                        
                        for key in remove_labels:
                            if key in metadata_labels:
                                logging.info(f"Removing label '{key}' for file: {filename}")
                                log_change(f"Removing label '{key}' for file: {filename}")
                                del metadata_labels[key]
                                updated = True

                        managed_metadata['labels'] = metadata_labels

                if updated:
                    if verbose:
                        logging.info(f"Modified content for file: {filename}")
                        logging.info(yaml.dump_all(documents))
                    
                    if dry_run:
                        logging.info(f"Would update file: {filename}")
                        log_change(f"Would update file: {filename}")
                    elif apply_metadata:
                        with open(file_path, 'w') as file:
                            yaml.safe_dump_all(documents, file)
                        logging.info(f"Updated file: {filename}")
                        log_change(f"Updated file: {filename}")
                    else:
                        logging.info(f"Skipping actual update for file: {filename}")
                        log_change(f"Skipping actual update for file: {filename}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

def parse_key_value_pairs(pairs):
    result = {}
    for pair in pairs:
        if '=' not in pair:
            logging.error(f"Invalid key=value pair: {pair}")
            continue
        key, value = pair.split('=', 1)
        result[key] = value
    return result

def main():
    parser = argparse.ArgumentParser(description="Validate, log changes, and update Argo CD Application YAML files with Linkerd annotations and labels")
    parser.add_argument('directory', help="Directory containing YAML files")
    parser.add_argument('--annotations', nargs='+', help="Annotation key=value pairs to add", default=[])
    parser.add_argument('--labels', nargs='+', help="Label key=value pairs to add", default=[])
    parser.add_argument('--remove-annotations', nargs='+', help="Annotation keys to remove", default=[])
    parser.add_argument('--remove-labels', nargs='+', help="Label keys to remove", default=[])
    parser.add_argument('--dry-run', type=bool, help="Perform a dry run without making changes", default=False)
    parser.add_argument('--apply-metadata', type=bool, help="Apply metadata changes to the files", default=False)
    parser.add_argument('--verbose', action='store_true', help="Display verbose output")
    args = parser.parse_args()
    
    annotations = parse_key_value_pairs(args.annotations)
    labels = parse_key_value_pairs(args.labels)
    
    update_yaml_files(args.directory, annotations, labels, args.remove_annotations, args.remove_labels, args.dry_run, args.apply_metadata, args.verbose)

if __name__ == "__main__":
    main()

