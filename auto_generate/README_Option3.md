# Solar Carport Array - External Script Documentation

## Overview

External Python script that connects to a running Allplan instance and generates solar PV arrays programmatically. Ideal for integration with external systems, web applications, or automated workflows.

## Prerequisites

1. **Allplan 2026** (or compatible) installed
2. **Python 3.x** (can use Allplan's bundled Python)
3. **Active Allplan document** must be open before running script

## Installation

1. **Create directory:**
   ```
   C:\AutoGeneration\External\
   ```

2. **Copy files:**
   - `auto_generate_solar.py`
   - `solar_config.json`
   - `README.md`

3. **Verify Allplan API path:**
   Open `auto_generate_solar.py` and check line ~13:
   ```python
   ALLPLAN_API_PATH = "C:/Program Files/Allplan/Allplan 2026/Etc/PythonPartsFramework"
   ```

## Usage

### Step 1: Prepare Allplan

1. Open Allplan
2. Create or open a project
3. Open a document (drawing sheet)
4. Keep Allplan running

### Step 2: Run Script

**Command Line:**
```cmd
python auto_generate_solar.py solar_config.json
```

**Or with custom config:**
```cmd
python auto_generate_solar.py my_custom_config.json
```

### Step 3: Check Results

- Elements appear in Allplan document
- `generation_log.txt` shows execution details
- Both projects are placed at configured coordinates

## Configuration File Structure

**solar_config.json** contains:

```json
{
  "projects": [
    {
      "name": "ProjectName",
      "enabled": true,
      "modules": {
        "rows": 3,
        "cols": 4,
        "width": 1000,
        "height": 2000,
        "thickness": 35
      },
      "gaps": {
        "row": 50,
        "col": 50
      },
      "plate": {
        "thickness": 50,
        "offset": 0
      },
      "roof": {
        "createSecondSide": true,
        "angle": 15,
        "ridgeHeight": 1000
      },
      "placement": {
        "x": 0,
        "y": 0,
        "z": 0
      },
      "colors": {
        "plate": 7,
        "frame": 4,
        "pv": 21
      }
    }
  ]
}
```

### Key Parameters

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Project identifier |
| `enabled` | boolean | Skip if false |
| `modules.rows` | integer | Number of rows (1-20) |
| `modules.cols` | integer | Number of columns (1-20) |
| `modules.width` | float | Width per module (mm) |
| `modules.height` | float | Height per module (mm) |
| `placement.x/y/z` | float | Placement coordinates (mm) |
| `colors.plate` | int | Allplan color ID (grey=7) |
| `colors.frame` | int | Allplan color ID (blue=4) |
| `colors.pv` | int | Allplan color ID (dark blue=21) |

## Troubleshooting

### "Cannot import Allplan Python API"

**Solution:**
1. Check Allplan installation path
2. Verify Python version matches Allplan's
3. Open `auto_generate_solar.py` line 13 and update path

### "No active Allplan document found"

**Solution:**
1. Open Allplan before running script
2. Create/open a project
3. Open a document (drawing sheet)
4. Keep Allplan open while script runs

### Elements not appearing

**Check:**
1. Placement coordinates in JSON (default is 0,0,0)
2. `generation_log.txt` for errors
3. Check Allplan document scale matches mm units

### Script exits with error

**Check log file:**
```cmd
type generation_log.txt
```

**Common issues:**
- JSON syntax error → validate with online JSON validator
- Missing Allplan API → check installation
- Permission issues → run as Administrator

## Logging

**Log file:** `generation_log.txt`

**Log levels:**
- `INFO` - Normal operations
- `SUCCESS` - Task completed
- `WARNING` - Non-critical issues
- `ERROR` - Critical failures

**Example:**
```
[2025-10-25 14:30:45] [INFO] Loading configuration from: solar_config.json
[2025-10-25 14:30:45] [INFO] Configuration loaded successfully
[2025-10-25 14:30:46] [INFO] Connecting to Allplan...
[2025-10-25 14:30:46] [INFO] Connected to document: Drawing01
[2025-10-25 14:30:47] [INFO] Generating solar array: Project_A_Standard
[2025-10-25 14:30:47] [SUCCESS] PROJECT COMPLETED: Project_A_Standard
```

## Integration Examples

### Web Application (Flask)

```python
from flask import Flask, request
import subprocess
import json

@app.route('/generate', methods=['POST'])
def generate_solar():
    config = request.json
    
    with open('temp_config.json', 'w') as f:
        json.dump(config, f)
    
    result = subprocess.run([
        'python',
        'auto_generate_solar.py',
        'temp_config.json'
    ])
    
    return {'status': 'success' if result.returncode == 0 else 'failed'}
```

### Database Integration

```python
import sqlite3
import json
import subprocess

conn = sqlite3.connect('projects.db')
cursor = conn.execute('SELECT * FROM solar_projects WHERE status = "pending"')

projects = []
for row in cursor:
    projects.append({
        'name': row[1],
        'modules': json.loads(row[2]),
        'placement': json.loads(row[3])
    })

config = {'projects': projects}
with open('db_config.json', 'w') as f:
    json.dump(config, f)

subprocess.run(['python', 'auto_generate_solar.py', 'db_config.json'])
```

### Grasshopper Integration

Use GHPython component:

```python
import subprocess
import json

config = {
    'projects': [{
        'name': 'GH_Project',
        'enabled': True,
        'modules': {'rows': rows, 'cols': cols, 'width': width, 'height': height, 'thickness': thickness},
        'gaps': {'row': row_gap, 'col': col_gap},
        'plate': {'thickness': plate_t, 'offset': 0},
        'roof': {'createSecondSide': False, 'angle': 0, 'ridgeHeight': 0},
        'placement': {'x': x, 'y': y, 'z': z},
        'colors': {'plate': 7, 'frame': 4, 'pv': 21}
    }]
}

with open(r'C:\Temp\gh_config.json', 'w') as f:
    json.dump(config, f)

subprocess.run([
    r'C:\Program Files\Allplan\Allplan 2026\Prg\Python\python.exe',
    r'C:\AutoGeneration\External\auto_generate_solar.py',
    r'C:\Temp\gh_config.json'
])
```

## Performance

| Modules | Generation Time |
|---------|-----------------|
| 12 (3x4) | ~1 second |
| 30 (5x6) | ~2 seconds |
| 100 (10x10) | ~5 seconds |
| 400 (20x20) | ~20 seconds |

## Support

1. Check `generation_log.txt`
2. Verify Allplan is open with active document
3. Validate JSON syntax
4. Check file permissions

## Author

JB - 2025-10-25

## License

MIT
