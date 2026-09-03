const fs = require("fs-extra");
const path = require("path");
const archiver = require("archiver");

const ROOT = process.cwd();
const packageJson = require(path.join(ROOT, "package.json"));
const BUILD_DIR = path.join(ROOT, "build");
const BUILD_ASSETS = path.join(BUILD_DIR, "assets");
const DIST_DIR = path.join(ROOT, "dist");

const args = process.argv.slice(2).filter((arg) => arg !== "--");
const skipZip = args.includes("--strip-only");
const stripSource = args.includes("--strip-source");
const noStrip = args.includes("--no-strip");

let storyArg;
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--story") {
    storyArg = args[i + 1];
    break;
  }
  if (args[i].startsWith("--story=")) {
    storyArg = args[i].split("=")[1];
    break;
  }
}

console.log({ args, storyArg, npm_story: process.env.npm_config_story, env_story: process.env.STORY });

const storyInput = storyArg || process.env.npm_config_story || process.env.STORY || packageJson.config?.story || packageJson.buildConfig?.name;

function resolveStorySource(input) {
  const defaultBase = packageJson.buildConfig?.name || "build";
  const defaultHtml = path.join(ROOT, `${defaultBase}.html`);

  if (!input) {
    return {
      html: defaultHtml,
      assets: path.join(ROOT, "assets"),
      buildName: defaultBase,
    };
  }

  function resolveAssetsDir(htmlPath) {
    const htmlDir = path.dirname(htmlPath);
    if (path.basename(htmlDir) === "assets") {
      return htmlDir;
    }
    return path.join(htmlDir, "assets");
  }

  function findHtmlInDirectory(dir, baseName) {
    if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) {
      return null;
    }

    const htmlFiles = fs.readdirSync(dir).filter((file) => file.endsWith(".html"));
    if (htmlFiles.length === 1) {
      return path.join(dir, htmlFiles[0]);
    }

    const namedHtml = path.join(dir, `${baseName}.html`);
    if (fs.existsSync(namedHtml)) {
      return namedHtml;
    }

    const assetsDir = path.join(dir, "assets");
    if (fs.existsSync(assetsDir) && fs.statSync(assetsDir).isDirectory()) {
      const htmlFilesInAssets = fs.readdirSync(assetsDir).filter((file) => file.endsWith(".html"));
      if (htmlFilesInAssets.length === 1) {
        return path.join(assetsDir, htmlFilesInAssets[0]);
      }
      const namedAssetsHtml = path.join(assetsDir, `${baseName}.html`);
      if (fs.existsSync(namedAssetsHtml)) {
        return namedAssetsHtml;
      }
    }

    return null;
  }

  // First, check if input is a story name in stories/ directory
  const storyDir = path.join(ROOT, "stories", input);
  const storyHtml = findHtmlInDirectory(storyDir, input);
  if (storyHtml) {
    return {
      html: storyHtml,
      assets: resolveAssetsDir(storyHtml),
      buildName: input,
    };
  }

  // Check if input is an absolute path
  let candidate = input;
  if (!path.isAbsolute(candidate)) {
    candidate = path.join(ROOT, candidate);
  }

  // If it's a directory, look for HTML files
  if (fs.existsSync(candidate) && fs.statSync(candidate).isDirectory()) {
    const htmlPath = findHtmlInDirectory(candidate, path.basename(candidate));
    if (htmlPath) {
      candidate = htmlPath;
    }
  }

  // If it's an HTML file, use it directly
  if (fs.existsSync(candidate) && candidate.endsWith(".html")) {
    return {
      html: candidate,
      assets: resolveAssetsDir(candidate),
      buildName: path.basename(candidate, ".html"),
    };
  }

  // Fallback to default
  return {
    html: defaultHtml,
    assets: path.join(ROOT, "assets"),
    buildName: defaultBase,
  };
}

const source = resolveStorySource(storyInput);
const INPUT_HTML = source.html;
const ASSETS_DIR = source.assets;
const BUILD_NAME = source.buildName;

function cleanHtml(html) {
  // Convert absolute local story asset imports to relative paths in production
  html = html.replaceAll(/http:\/\/127\.0\.0\.1:8080\/stories\/[^\/]+\/assets\//g, "assets/");

  // Strip other localhost development URLs
  html = html.replaceAll("http://127.0.0.1:8080/", "");

  // Set BASE_URL to blank for production (relative asset loading)
  html = html.replaceAll(/BASE_URL:\s*"[^"]*"/g, 'BASE_URL: ""');

  // Remove base-template path references from story HTML so built pages use relative assets
  html = html.replaceAll(/\/?stories\/base-template\//g, "");

  // Remove the Twine storydata stylesheet import if it points to the shared story.css file
  html = html.replaceAll(/@import url\("assets\/css\/story\.css"\);/g, "");

  // Ensure the loading UI is active before first paint in production.
  html = html.replace(/<html((?![^>]*\bclass=)[^>]*)>/i, '<html$1 class="loading-story">');
  html = html.replace(/<html([^>]*\bclass\s*=\s*["'])([^"']*)(["'][^>]*)>/i, (match, p1, p2, p3) => {
    if (/\bloading-story\b/.test(p2)) return match;
    return `${p1}${p2} loading-story${p3}`;
  });

  let storyCSSPath  = `assets/css/story.css`;
  let storyCSSLink  = `<link rel="stylesheet" href="${storyCSSPath}">`;
  let criticalStyle = `<style id="critical-loading-style">html.loading-story tw-story { opacity: 0 !important; visibility: hidden !important; }</style>`;
  html = html.replace('</head>', storyCSSLink + criticalStyle + '</head>');

  // Blank out runtime host/base URL values in production output
  html = html.replaceAll(/window\.hostURL\s*=\s*"[^"]*"\s*;/g, 'window.hostURL = "";');
  html = html.replaceAll(/window\.baseURL\s*=\s*[^;]+;/g, 'window.baseURL = "";');

  return html;
}
async function copyAssetsExcludingSrc(sourceDir, destDir) {
  // First copy everything
  await fs.copy(sourceDir, destDir);
  
  // Then remove all src directories from the destination
  async function removeSrcDirs(dir) {
    const items = await fs.readdir(dir);
    
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = await fs.stat(fullPath);
      
      if (stat.isDirectory()) {
        if (item === 'src') {
          // Remove the entire src directory
          await fs.remove(fullPath);
          console.log(`🗑️  Excluded src directory: ${path.relative(destDir, fullPath)}`);
        } else {
          // Recurse into subdirectories
          await removeSrcDirs(fullPath);
        }
      }
    }
  }
  
  await removeSrcDirs(destDir);
}
async function stripSourceFile() {
  console.log("🔧 Stripping local dev URLs from source HTML...");
  const html = await fs.readFile(INPUT_HTML, "utf-8");
  const cleaned = cleanHtml(html);
  await fs.writeFile(INPUT_HTML, cleaned);
  console.log(`✔ Source file cleaned: ${BUILD_NAME}.html`);
}

async function run() {
  console.log(`🚀 Starting build for story source: ${INPUT_HTML} ${noStrip ? "(dev/open mode, urls preserved)" : "(production mode, urls stripped)"}`);

  if (!fs.existsSync(INPUT_HTML)) {
    throw new Error(`Story HTML not found: ${INPUT_HTML}`);
  }

  if (!fs.existsSync(ASSETS_DIR)) {
    throw new Error(`Assets directory not found for story: ${ASSETS_DIR}`);
  }

  await fs.remove(BUILD_DIR);
  await fs.remove(DIST_DIR);

  await fs.ensureDir(BUILD_DIR);
  await fs.ensureDir(DIST_DIR);

  let html = await fs.readFile(INPUT_HTML, "utf-8");
  if (!noStrip) {
    html = cleanHtml(html);
  }

  await fs.writeFile(path.join(BUILD_DIR, "index.html"), html);
  console.log("✔ HTML processed");

  const BASE_TEMPLATE_ASSETS = path.join(ROOT, "stories", "base-template", "assets");
  if (fs.existsSync(BASE_TEMPLATE_ASSETS)) {
    await copyAssetsExcludingSrc(BASE_TEMPLATE_ASSETS, BUILD_ASSETS);
    console.log("✔ Base template assets copied (src folders excluded)");
  }

  // Copy story-specific assets and exclude src directories
  await copyAssetsExcludingSrc(ASSETS_DIR, BUILD_ASSETS);
  console.log("✔ Story assets copied (src folders excluded)");

  if (!skipZip) {
    const outputZip = path.join(DIST_DIR, `${BUILD_NAME}.zip`);
    await zipFolder(BUILD_DIR, outputZip);
    console.log(`🎉 Build complete: ${outputZip}`);
  } else {
    console.log("✔ Strip-only build complete: open build/index.html to preview locally.");
  }
}

if (stripSource) {
  stripSourceFile().catch((err) => {
    console.error("❌ Source strip failed:", err);
    process.exit(1);
  });
} else {
  run().catch((err) => {
    console.error("❌ Build failed:", err);
    process.exit(1);
  });
}

function zipFolder(sourceDir, outPath) {
  return new Promise((resolve, reject) => {
    const output = fs.createWriteStream(outPath);
    const archive = archiver("zip", { zlib: { level: 9 } });

    output.on("close", resolve);
    archive.on("error", reject);

    archive.pipe(output);
    archive.directory(sourceDir, false);
    archive.finalize();
  });
}
