import re
import csv

# Variables to track (ensure they match EXACTLY the COBOL variable names)
target_vars = {
    'var1',
    'var2'  # Corrected variable name
}
results = []

# Read the COBOL program
with open('cbl1.txt', 'r') as f:
    cobol_lines = [line.rstrip('\n') for line in f]  # Preserve original lines

# Process lines
i = 0
while i < len(cobol_lines):
    line = cobol_lines[i].strip()

    # Skip comments (lines with '*' in the 7th position)
    if len(line) > 6 and line[6] == '*':
        i += 1
        continue

    # Check for MOVE statements
    if 'MOVE' in line:
        # Extract the part after MOVE
        move_part = line.split('MOVE', 1)[-1].strip()

        # Check for literals in single quotes, ignoring 'TO' inside the literal
        literal_match = re.search(r"'([^']*)'", move_part)
        source_value = literal_match.group(1) if literal_match else None

        # Check if TO is on the same line
        to_match = re.search(
            r"TO\s+([A-Z0-9-]+)",
            move_part[literal_match.end():] if literal_match else move_part)
        if to_match:
            dest_var = to_match.group(1).strip()
            if source_value and dest_var in target_vars:
                results.append([dest_var, source_value, i + 1])
        else:
            # Check the next line for TO clause
            if i + 1 < len(cobol_lines):
                next_line = cobol_lines[i + 1].strip()
                to_match = re.search(r"TO\s+([A-Z0-9-]+)", next_line)
                if to_match:
                    dest_var = to_match.group(1).strip()
                    if source_value and dest_var in target_vars:
                        results.append([dest_var, source_value, i + 2])
                        i += 1  # Skip next line

    i += 1

# Save results to CSV
with open('cobol_analysis.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Variable', 'Source Value', 'Line Number'])
    csvwriter.writerows(results)

print("Results saved to cobol_analysis.csv!")
