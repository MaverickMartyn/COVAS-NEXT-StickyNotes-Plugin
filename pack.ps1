# Delete dist if it already exists
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Create dist
New-Item "dist" -ItemType Directory

# Install dependencies
if (Test-Path "requirements.txt") {
    pip install --target ./deps -r requirements.txt
}

# Remember to add any additional files, and change the name of the plugin
$artifacts = "StickyNotes.py", "requirements.txt", "manifest.json", "NotesStore.py", "__init__.py"

if (Test-Path "deps") {
    $artifacts += "deps"
}

$compress = @{
LiteralPath = $artifacts
CompressionLevel = "Fastest"
DestinationPath = "dist\StickyNotesPlugin.zip" # Change the name of the plugin
}
Compress-Archive @compress