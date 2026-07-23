import re

file = r'C:\Users\barcik\Desktop\ePrihlasky_Playwright\tests\Riaditel\ZS - Papierova prihlaska na SS.py'

with open(file, 'rb') as f:
    raw = f.read()

# Strip BOM if present
if raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]

# Normalize line endings to \n
raw = raw.replace(b'\r\r\n', b'\n').replace(b'\r\n', b'\n').replace(b'\r', b'\n')

# Decode as UTF-8 (file is valid UTF-8 but content is cp1250 mojibake)
text = raw.decode('utf-8')

# Fix chunk by chunk: non-ASCII runs were originally cp1250 bytes stored as UTF-8
result = []
i = 0
while i < len(text):
    c = text[i]
    if ord(c) < 128:
        result.append(c)
        i += 1
    else:
        j = i
        while j < len(text) and ord(text[j]) >= 128:
            j += 1
        chunk = text[i:j]
        try:
            raw_chunk = chunk.encode('cp1250')
            fixed_chunk = raw_chunk.decode('utf-8')
            result.append(fixed_chunk)
        except (UnicodeEncodeError, UnicodeDecodeError):
            result.append(chunk)
        i = j

fixed = ''.join(result)

# Fix ň specifically (byte 0x88 is undefined in cp1250, so it survives as U+0088)
# After the chunk fix, Ĺ (U+0139) + U+0088 should become ň
fixed = fixed.replace('\u0139\u0088', 'ň')

# Write back as clean UTF-8 with LF line endings
with open(file, 'w', encoding='utf-8', newline='\n') as f:
    f.write(fixed)

print('Done. Sample lines with diacritics:')
for line in fixed.splitlines():
    if 'slovens' in line.lower() or 'Stredna' in line or 'Stredná' in line:
        print(' ', line.strip())
        break
