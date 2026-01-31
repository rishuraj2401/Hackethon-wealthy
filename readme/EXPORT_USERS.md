# Export User IDs Script

## Overview

This script extracts all distinct user IDs from both SIP and Insurance tables and exports them to a file.

## Usage

### Basic Usage (All Users)

```bash
# Export all user IDs
python scripts/export_user_ids.py
```

This creates two files:
- `user_ids_TIMESTAMP.txt` - Simple text file with one user_id per line
- `user_ids_TIMESTAMP_detailed.csv` - CSV with additional info (has_sip, has_insurance)

### Custom Output File

```bash
# Specify output file name
python scripts/export_user_ids.py -o my_users.txt
```

This creates:
- `my_users.txt` - User IDs
- `my_users_detailed.csv` - Detailed CSV

### Filter by Agent

```bash
# Export users for specific agent
python scripts/export_user_ids.py -a 2116
```

### Combined Options

```bash
# Custom output file + specific agent
python scripts/export_user_ids.py -o agent_2116_users.txt -a 2116
```

## Output Format

### Text File (`user_ids_*.txt`)

```
# Distinct User IDs
# Generated: 2026-01-30 12:00:00
# Total users: 1250
# SIP only: 450
# Insurance only: 200
# Both: 600
#
0169d596-d4fa-4acc-838a-153d6ba76bb9
0c87f048-9f1d-4fb9-9efd-529a619727bc
110bdffa-72e8-4c3c-a2fe-f07a22ad08da
...
```

### CSV File (`user_ids_*_detailed.csv`)

```csv
user_id,has_sip,has_insurance
0169d596-d4fa-4acc-838a-153d6ba76bb9,Yes,No
0c87f048-9f1d-4fb9-9efd-529a619727bc,Yes,Yes
110bdffa-72e8-4c3c-a2fe-f07a22ad08da,Yes,No
...
```

## Statistics Provided

The script shows:
- Total distinct users across both tables
- Users with SIP only (cross-sell opportunity for insurance)
- Users with Insurance only
- Users with both products

## Examples

### Example 1: Export All Users

```bash
cd /Users/rishurajsinha/Desktop/wealthy/Hackethon

# Activate conda environment
conda activate wealthy-dashboard

# Run export
python scripts/export_user_ids.py
```

Output:
```
============================================================
User ID Export Tool
============================================================

🔍 Extracting distinct user IDs...
   Querying SIP records...
   Found 850 unique users in SIP records
   Querying Insurance records...
   Found 650 unique users in Insurance records

✅ Total distinct users: 1250
   - SIP only: 450
   - Insurance only: 250
   - Both SIP & Insurance: 400

📝 Writing to file: user_ids_20260130_120000.txt
✅ Successfully exported 1250 user IDs to user_ids_20260130_120000.txt

📊 Creating detailed CSV: user_ids_20260130_120000_detailed.csv
✅ Detailed CSV created: user_ids_20260130_120000_detailed.csv

============================================================
```

### Example 2: Export for Specific Agent

```bash
# Get users for agent 2116
python scripts/export_user_ids.py -a 2116 -o agent_2116_users.txt
```

### Example 3: Use in Other Scripts

```bash
# Export user IDs
python scripts/export_user_ids.py -o users.txt

# Count users
wc -l users.txt

# Get first 10 users (skip header)
tail -n +8 users.txt | head -10

# Use in a loop
while IFS= read -r user_id; do
    [[ "$user_id" =~ ^# ]] && continue  # Skip comments
    echo "Processing user: $user_id"
    # Your logic here
done < users.txt
```

## Use Cases

### 1. Cross-Sell Campaign

```bash
# Export all users
python scripts/export_user_ids.py -o all_users.txt

# The detailed CSV shows who has what product
# Filter for "SIP only" users for insurance cross-sell
# Filter for "Insurance only" for SIP cross-sell
```

### 2. Agent Performance Analysis

```bash
# Export for each agent
python scripts/export_user_ids.py -a 2116 -o agent_2116.txt
python scripts/export_user_ids.py -a 4220 -o agent_4220.txt

# Compare user counts
wc -l agent_*.txt
```

### 3. Data Integration

```bash
# Export users to integrate with CRM
python scripts/export_user_ids.py -o crm_import.txt

# The CSV file can be imported into Excel/CRM
```

### 4. Client Communication

```bash
# Export users for email campaign
python scripts/export_user_ids.py -o email_campaign_users.txt

# Use with your email system
```

## Command Line Options

```
usage: export_user_ids.py [-h] [-o OUTPUT] [-a AGENT]

Export distinct user IDs from SIP and Insurance tables

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file path (default: user_ids_TIMESTAMP.txt)
  -a AGENT, --agent AGENT
                        Filter by agent_id
```

## File Locations

Generated files are saved in the current working directory:
```
/Users/rishurajsinha/Desktop/wealthy/Hackethon/
├── user_ids_20260130_120000.txt          ← Text file
└── user_ids_20260130_120000_detailed.csv ← CSV file
```

## Integration with APIs

The script extracts the same user IDs that the APIs use:

```bash
# Export user IDs
python scripts/export_user_ids.py -o users.txt

# For each user, query their data via API
for user_id in $(tail -n +8 users.txt); do
    curl "http://localhost:8111/api/clients/$user_id/sips"
    curl "http://localhost:8111/api/clients/$user_id/insurance"
done
```

## Performance

- Fast execution (< 5 seconds for 10K users)
- Minimal memory footprint
- Handles large datasets efficiently

## Troubleshooting

### Issue: Database Connection Error

```bash
# Make sure PostgreSQL is running
./start_postgres.sh

# Verify connection
docker exec -it wealthy_postgres psql -U postgres -d wealthy_dashboard -c "\dt"
```

### Issue: Empty Output

```bash
# Check if data exists
docker exec -it wealthy_postgres psql -U postgres -d wealthy_dashboard \
  -c "SELECT COUNT(*) FROM sip_records;"

docker exec -it wealthy_postgres psql -U postgres -d wealthy_dashboard \
  -c "SELECT COUNT(*) FROM insurance_records;"
```

### Issue: Permission Denied

```bash
# Make script executable
chmod +x scripts/export_user_ids.py

# Or run with python directly
python scripts/export_user_ids.py
```

## Tips

1. **Timestamp in filename**: Default output includes timestamp to avoid overwriting files
2. **CSV for analysis**: Use the detailed CSV file in Excel/Google Sheets for filtering
3. **Agent filtering**: Use `-a` flag to segment by advisor
4. **Automation**: Add to cron job for daily exports

## Related Scripts

- `import_data.py` - Import SIP data
- `import_insurance.py` - Import insurance data
- `test_api.py` - Test API endpoints

---

**Script Location**: `/Users/rishurajsinha/Desktop/wealthy/Hackethon/scripts/export_user_ids.py`
