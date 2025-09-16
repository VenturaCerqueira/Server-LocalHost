$content = Get-Content -Path 'servidor_app/services/database_service.py' -Encoding UTF8
$lines = $content -split "`n"

# Find the dump_cmd line
for ($i = 0; $i -lt $lines.Length; $i++) {
    if ($lines[$i] -match 'dump_cmd = \[') {
        # Find the logger.info line
        for ($j = $i; $j -lt $lines.Length; $j++) {
            if ($lines[$j] -match 'logger\.info\(f"Executando mysqldump para \{db_name\}"\)') {
                # Insert db_name and ] before it
                $lines = $lines[0..($j-1)] + '            db_name' + '        ]' + $lines[$j..($lines.Length-1)]
                break
            }
        }
        break
    }
}

$fixedContent = $lines -join "`n"
Set-Content -Path 'servidor_app/services/database_service.py' -Value $fixedContent -Encoding UTF8

Write-Host "Fixed"
