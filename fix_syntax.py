with open('servidor_app/services/database_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Find the dump_cmd
for i in range(len(lines)):
    if 'dump_cmd = [' in lines[i]:
        # Find where the list ends
        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith(']'):
            j += 1
        if j < len(lines):
            # The list ends at j, but if it's not closed, add db_name and ]
            if not lines[j].strip() == ']':
                # Insert db_name before the logger
                k = j
                while k < len(lines):
                    if 'logger.info(f"Executando mysqldump para {db_name}")' in lines[k]:
                        lines.insert(k, '            db_name')
                        lines.insert(k+1, '        ]')
                        break
                    k += 1
        break

fixed_content = '\n'.join(lines)

with open('servidor_app/services/database_service.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("Fixed")
