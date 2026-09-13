const fs = require('fs');
const path = require('path');

const rootVersionPath = path.resolve(__dirname, '../../VERSION');
const localVersionPath = path.resolve(__dirname, '../VERSION');

let version = '1.0.0';
if (fs.existsSync(rootVersionPath)) {
    version = fs.readFileSync(rootVersionPath, 'utf8').trim();
} else if (fs.existsSync(localVersionPath)) {
    version = fs.readFileSync(localVersionPath, 'utf8').trim();
}

// Write version.js for browser and webview consumption
const versionJsContent = `// Generated automatically from VERSION file - DO NOT EDIT MANUALLY\nwindow.APP_VERSION = "${version}";\n`;
fs.writeFileSync(path.resolve(__dirname, '../version.js'), versionJsContent, 'utf8');

// Write version.json as static asset
fs.writeFileSync(path.resolve(__dirname, '../version.json'), JSON.stringify({ version }, null, 2), 'utf8');

console.log(`[PYROJA-VERSION] Synchronized version ${version} from VERSION file.`);
