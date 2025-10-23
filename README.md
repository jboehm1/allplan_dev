AllPlan Dev

Short scripts and PythonParts to automate object creation for Allplan.

Overview
- This repository contains PythonParts and helper scripts used during development and automation for Nemetschek Allplan.

Repository layout (typical)
- pythonparts/ — Allplan Library content (PythonParts)
- pythonparts_scripts/ — PythonPartsScripts
- sync.ps1.bak — PowerShell sync helper that copies local Allplan folders into this repo (backup)
- .gitignore — ignores *.bak files

Quick usage
- Update paths in sync.ps1.bak ($ALLPLAN_PATH and $GIT_PATH) before running.
- The sync script copies files from your local Allplan folders into the repository and commits changes.

Notes about .bak files
- .gitignore prevents new .bak files from being added, but files already committed remain tracked.
- To stop tracking existing .bak files without deleting them locally:
  git rm --cached path/to/file.bak
  git commit -m "chore: remove tracked .bak files"
  git push

Contributing
- Open issues or PRs for improvements to PythonParts or tooling. Keep commits focused and avoid committing local-only backups.

License
- No license file is included. Add a LICENSE file if you want to grant explicit permissions to reuse this code.

Contact
- Repo owner: jboehm1
