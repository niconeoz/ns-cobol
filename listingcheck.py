import re
import csv

# Regular expressions to extract variable values
decline_reason_regex = r"MOVE\s+([+-]?\d+)\s+TO\s+DECLINE-REASON"
response_code_regex = r"MOVE\s+'(\d{2})'\s+TO\s+RESPONSE-CODE"
decline_narration_regex = r"MOVE\s+'([^']{1,25})'\s+TO\s+DECLINE-NARRATION"

# Initialize a set to store unique combinations
unique_combinations = set()

# Read the COBOL program from a file
with open("decline_processing.cbl", "r") as cobol_file:
    cobol_program = cobol_file.read()

    # Find all matches for DECLINE-REASON, RESPONSE-CODE, and DECLINE-NARRATION
    decline_reasons = re.findall(decline_reason_regex, cobol_program)
    response_codes = re.findall(response_code_regex, cobol_program)
    decline_narrations = re.findall(decline_narration_regex, cobol_program)

    # Combine the values into unique combinations
    for reason, code, narration in zip(decline_reasons, response_codes, decline_narrations):
        unique_combinations.add((reason, code, narration))

# Write the unique combinations to a CSV file
with open("unique_combinations.csv", "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["DECLINE-REASON", "RESPONSE-CODE", "DECLINE-NARRATION"])  # Write header
    writer.writerows(unique_combinations)  # Write rows

print("Unique combinations have been written to 'unique_combinations.csv'.")
