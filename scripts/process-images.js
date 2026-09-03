const fs = require("fs-extra");
const path = require("path");
const { execSync } = require("child_process");

const ROOT = process.cwd();
const packageJson = require(path.join(ROOT, "package.json"));

const args = process.argv.slice(2);
let storyArg;
let includeBackgrounds = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--story") {
    storyArg = args[i + 1];
    i++; // Skip next arg
  } else if (args[i].startsWith("--story=")) {
    storyArg = args[i].split("=")[1];
  } else if (args[i] === "--include-backgrounds") {
    includeBackgrounds = true;
  }
}

const storyInput = storyArg || process.env.npm_config_story || process.env.STORY || packageJson.config?.story || packageJson.buildConfig?.name;

function resolveStorySource(input) {
  const defaultBase = packageJson.buildConfig?.name || "build";

  if (!input) {
    return {
      storyName: defaultBase,
      srcDir: path.join(ROOT, "assets", "image", "src"),
      outputDir: path.join(ROOT, "assets", "image", "src", "processed"),
    };
  }

  // First, check if input is a story name in stories/ directory
  const storyDir = path.join(ROOT, "stories", input);
  if (fs.existsSync(storyDir)) {
    return {
      storyName: input,
      srcDir: path.join(storyDir, "assets", "image", "src"),
      outputDir: path.join(storyDir, "assets", "image", "src", "processed"),
    };
  }

  // Check if input is an absolute path
  let candidate = input;
  if (!path.isAbsolute(candidate)) {
    candidate = path.join(ROOT, candidate);
  }

  // If it's a directory, assume it's a story directory
  if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) {
    const baseName = path.basename(candidate);
    return {
      storyName: baseName,
      srcDir: path.join(candidate, "assets", "image", "src"),
      outputDir: path.join(candidate, "assets", "image", "src", "processed"),
    };
  }

  // Fallback
  return {
    storyName: defaultBase,
    srcDir: path.join(ROOT, "assets", "image", "src"),
    outputDir: path.join(ROOT, "assets", "image"),
  };
}

const source = resolveStorySource(storyInput);

async function processImages() {
  console.log(`🎨 Processing images for story: ${source.storyName}`);
  console.log(`📁 Source: ${source.srcDir}`);
  console.log(`📁 Output: ${source.outputDir}`);

  if (!fs.existsSync(source.srcDir)) {
    console.error(`❌ Source directory not found: ${source.srcDir}`);
    process.exit(1);
  }

  // Ensure output directory exists
  await fs.ensureDir(source.outputDir);

  // Find all image files in src directory
  const imageExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'];
  const imageFiles = [];

  function findImages(dir) {
    const items = fs.readdirSync(dir);
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);

      if (stat.isDirectory()) {
        // Skip backgrounds directory unless --include-backgrounds is set
        if (!includeBackgrounds && (path.basename(fullPath).toLowerCase() === 'backgrounds' || path.basename(fullPath).toLowerCase() === 'bg')) {
          console.log(`⏭️  Skipping backgrounds directory: ${path.relative(source.srcDir, fullPath)}`);
          continue;
        }
        // Skip processed directory entirely
        if (path.basename(fullPath).toLowerCase() === 'processed') {
          console.log(`⏭️  Skipping processed directory: ${path.relative(source.srcDir, fullPath)}`);
          continue;
        }
        findImages(fullPath); // Recurse into subdirectories
      } else if (stat.isFile()) {
        const ext = path.extname(item).toLowerCase();
        if (imageExtensions.includes(ext)) {
          // Skip background images unless --include-backgrounds is set
          const fileName = item.toLowerCase();
          if (!includeBackgrounds && (fileName.includes('background') || fileName.includes('bg'))) {
            console.log(`⏭️  Skipping background image: ${path.relative(source.srcDir, fullPath)}`);
            continue;
          }
          imageFiles.push(fullPath);
        }
      }
    }
  }

  findImages(source.srcDir);

  if (imageFiles.length === 0) {
    console.log("ℹ️  No image files found in source directory");
    return;
  }

  console.log(`📸 Found ${imageFiles.length} image(s) to process`);

  for (const imagePath of imageFiles) {
    const relativePath = path.relative(source.srcDir, imagePath);
    // Change output path to use .png extension
    const outputPath = path.join(source.outputDir, relativePath.replace(/\.[^.]+$/, '.png'));

    // Ensure output subdirectory exists
    const outputDir = path.dirname(outputPath);
    await fs.ensureDir(outputDir);

    console.log(`🔄 Processing: ${relativePath}`);

    try {
      // Run pixel.py with --single --c 64 --outline
      const command = `python pytools/pixel.py "${imagePath}" --c 64 --dither-type none --width 256 --height 256 --remove-bg --outline`;
      execSync(command, { stdio: 'inherit', cwd: ROOT });

      // pixel.py outputs to same directory as input with _64c suffix
      const processedPath = imagePath.replace(/\.[^.]+$/, '_64c.png');

      if (fs.existsSync(processedPath)) {
        // Move to output directory with .png extension
        await fs.move(processedPath, outputPath, { overwrite: true });
        console.log(`✅ Saved: ${path.relative(source.outputDir, outputPath)}`);
      } else {
        console.error(`❌ Processed file not found: ${processedPath}`);
      }
    } catch (error) {
      console.error(`❌ Failed to process ${relativePath}:`, error.message);
    }
  }

  console.log("🎉 Image processing complete!");
}

processImages().catch((err) => {
  console.error("❌ Image processing failed:", err);
  process.exit(1);
});