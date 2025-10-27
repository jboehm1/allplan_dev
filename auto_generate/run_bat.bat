# Find Allplan.exe
Get-ChildItem -Path "C:\Program Files" -Recurse -Filter "Allplan.exe" -ErrorAction SilentlyContinue 2>$null | Select-Object -ExpandProperty FullName

# If nothing, try Program Files (x86)
Get-ChildItem -Path "C:\Program Files (x86)" -Recurse -Filter "Allplan.exe" -ErrorAction SilentlyContinue 2>$null | Select-Object -ExpandProperty FullName

# Also check the Allplan 2026 specific path
Get-ChildItem -Path "C:\Users\jb\Documents\Nemetschek\Allplan\2026" -Recurse -Filter "Allplan.exe" -ErrorAction SilentlyContinue 2>$null | Select-Object -ExpandProperty FullName
