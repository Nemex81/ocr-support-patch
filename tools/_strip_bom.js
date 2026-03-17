const fs = require('fs');
const path = require('path');

const gui = 'c:\\Users\\nemex\\OneDrive\\Documenti\\GitHub\\ocr-support-patch\\ocr_support_compatibility_pach\\gui';
const files = ['window_culture.gui', 'window_military.gui', 'window_faith.gui', 'window_inventory.gui'];
const BOM = Buffer.from([0xEF, 0xBB, 0xBF]);
const results = [];

for (const name of files) {
    const filePath = path.join(gui, name);
    const data = fs.readFileSync(filePath);
    const hasBOM = data.length >= 3 && data[0] === 0xEF && data[1] === 0xBB && data[2] === 0xBF;

    if (hasBOM) {
        const noBom = data.slice(3);
        fs.writeFileSync(filePath, noBom);
        results.push(`STRIPPED: ${name} (${data.length} -> ${noBom.length})`);
    } else {
        results.push(`NO-BOM: ${name} (${data.length})`);
    }
}

// Verify
results.push('\n--- VERIFICA ---');
for (const name of files) {
    const filePath = path.join(gui, name);
    const data = fs.readFileSync(filePath);
    const hasBOM = data.length >= 3 && data[0] === 0xEF && data[1] === 0xBB && data[2] === 0xBF;
    results.push(`${name}: ${hasBOM ? 'ERRORE BOM!' : 'OK senza BOM'} (${data.length} bytes)`);
}

const outPath = 'c:\\Users\\nemex\\OneDrive\\Documenti\\GitHub\\ocr-support-patch\\tools\\_bom_results.txt';
fs.writeFileSync(outPath, results.join('\n') + '\n', 'utf8');
