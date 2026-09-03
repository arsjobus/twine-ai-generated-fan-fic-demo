const { spawn } = require('child_process');
const { execSync } = require('child_process');

// Get arguments passed to this script
const args = process.argv.slice(2);

// Build the build.js command with arguments
const buildArgs = ['scripts/build.js', '--no-strip', '--strip-only', ...args];

// Run build.js
const child = spawn('node', buildArgs, { stdio: 'inherit' });

child.on('exit', (code) => {
  if (code === 0) {
    // Open the build/index.html file
    try {
      execSync('open build/index.html', { stdio: 'inherit' });
    } catch (e) {
      console.error('Failed to open file:', e.message);
      process.exit(1);
    }
  } else {
    process.exit(code);
  }
});
