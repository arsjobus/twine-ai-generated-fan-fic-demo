// scripts/json-to-harlowe.js

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const inputFile = process.argv[2];
const outputFile = process.argv[3] || 'story.html';

const baseTemplatePath = path.join(
    __dirname,
    '..',
    'stories',
    'base-template',
    'base-template.html'
);

if (!inputFile || !fs.existsSync(inputFile)) {
    console.error('Input JSON not found:', inputFile);
    process.exit(1);
}

if (!fs.existsSync(baseTemplatePath)) {
    console.error('base-template.html not found at:', baseTemplatePath);
    process.exit(1);
}

// Read story JSON
const story = JSON.parse(fs.readFileSync(inputFile, 'utf-8'));

// Generate UUID if missing
story.uuid = story.uuid || crypto.randomUUID();

// Read base template
let baseHtml = fs.readFileSync(baseTemplatePath, 'utf-8');

// Escape HTML for Twine passage content
function escapeHtml(str = '') {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Extract dialogue lines
function extractDialogueLines(text) {
    if (!text) return [];
    return text
        .split('\n\n')
        .filter(line => !line.trim().startsWith('[['))
        .map(line => line.trim())
        .filter(Boolean);
}

// Extract choices
function extractChoices(text) {
    if (!text) return [];
    const choiceRegex = /\[\[.*?\]\]/g;
    return text.match(choiceRegex) || [];
}

// Build actor image HTML (escaped)
function buildActorImages(passage) {
    const actors = [];

    if (passage.actor1ImageSrc) actors.push({ key: 'actor1', src: passage.actor1ImageSrc });
    if (passage.actor2ImageSrc) actors.push({ key: 'actor2', src: passage.actor2ImageSrc });
    if (passage.actor3ImageSrc) actors.push({ key: 'actor3', src: passage.actor3ImageSrc });

    if (actors.length === 0) return '';

    let alignments = [];
    if (actors.length === 1) alignments = ['align-m'];
    else if (actors.length === 2) {
        if (passage.actor1ImageSrc && passage.actor2ImageSrc && !passage.actor3ImageSrc) {
            alignments = ['align-l', 'align-r'];
        } else {
            alignments = ['align-m', 'align-m'];
        }
    } else if (actors.length === 3) {
        alignments = ['align-l', 'align-m', 'align-r'];
    }

    const html = actors.map((actor, index) => {
        return `<div class="actress lg ${alignments[index]}">
  <img class="actress-img fade-bottom" src="${actor.src}"/>
</div>`;
    }).join('\n');

    return escapeHtml(html); // ENSURE HTML IS ESCAPED
}

// Build passages
const passagesHtml = story.passages.map(p => {
    const tags = p.tags || '';

    // Actor images
    const actorImagesHtml = buildActorImages(p);

    // Dialogue
    const dialogueLines = extractDialogueLines(p.text);
    let dialogueHtml = '';
    if (dialogueLines.length) {
        const rawDialogue =
            `<div id="dialogue">\n` +
            dialogueLines.map(line => `  <span>${line}</span>`).join('\n') +
            `\n</div>\n`;
        dialogueHtml = escapeHtml(rawDialogue); // ESCAPED
    }

    // Choices
    const choices = extractChoices(p.text);
    let choicesHtml = '';
    if (choices.length) {
        const rawChoices =
            `<div id="player-choice">\n` +
            choices.map(choice => `  ${choice}`).join('\n') +
            `\n</div>\n`;
        choicesHtml = escapeHtml(rawChoices); // ESCAPED
    }

    // Scripts
    const scriptMatches = p.text.match(/<script[\s\S]*?<\/script>/gi) || [];
    const scriptsHtml = escapeHtml(scriptMatches.join('\n')); // ESCAPED

    return `<tw-passagedata pid="${escapeHtml(String(p.id))}" name="${escapeHtml(p.name)}" tags="${escapeHtml(tags)}">
${actorImagesHtml}
${dialogueHtml}
${choicesHtml}
${scriptsHtml}
</tw-passagedata>`;
}).join('\n');

// Replace existing passages in template
baseHtml = baseHtml.replace(
    /<tw-storydata([\s\S]*?)>([\s\S]*?)<\/tw-storydata>/,
    (match, attrs, inner) => {
        const preserved = inner.replace(/<tw-passagedata[\s\S]*?<\/tw-passagedata>/g, '').trim();
        return `<tw-storydata${attrs}>
${passagesHtml}
${preserved ? '\n' + preserved : ''}
</tw-storydata>`;
    }
);

// Update IFID UUID
baseHtml = baseHtml.replace(/ifid="[^"]*"/, `ifid="${story.uuid}"`);

// Write output
fs.writeFileSync(outputFile, baseHtml, 'utf-8');

console.log(`✅ Harlowe story generated -> ${outputFile} (UUID: ${story.uuid})`);