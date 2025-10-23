param(
    [string]$Message = "sync: update from Allplan"
)

$ALLPLAN_PATH = "C:\Users\jb\Documents\Nemetschek\Allplan\2026\Usr\Local"
$GIT_PATH = "C:\Users\jb\Documents\Code\allplan-dev"

Write-Host "Copying from Allplan to Git..."

Copy-Item "$ALLPLAN_PATH\Library\" `
  -Destination "$GIT_PATH\library\" -Force -Recurse

Copy-Item "$ALLPLAN_PATH\PythonPartsScripts\" `
  -Destination "$GIT_PATH\pythonparts_scripts\" -Force -Recurse

Write-Host "Files synced"

cd $GIT_PATH

$status = git status --porcelain
if ($status) {
    git add .
    git commit -m $Message
    Write-Host "Changes committed"
} else {
    Write-Host "No changes"
}
