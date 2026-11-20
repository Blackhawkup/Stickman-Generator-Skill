import { copyFileSync, existsSync, readFileSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';

async function main() {
  const slug = process.argv[2] || 'sunk-cost-fallacy';
  const projectDir = resolve('slideshow-workflow/projects', slug);
  const promptsFile = join(projectDir, 'prompts.json');
  const imagesDir = join(projectDir, 'images');
  const prompts = JSON.parse(readFileSync(promptsFile, 'utf-8'));

  // Import flow-mcp
  const flowUrl = pathToFileURL('C:/Users/sangw/flow-mcp/dist/flow.js').href;
  const flow = await import(flowUrl);

  console.log(`[Batch Generator] Starting generation for ${prompts.length} slides...`);

  for (let i = 0; i < prompts.length; i++) {
    const s = prompts[i];
    const pngPath = join(imagesDir, `${s.name}.png`);
    const jpegPath = join(imagesDir, `${s.name}.jpeg`);

    if (existsSync(pngPath) && !existsSync(jpegPath)) {
      try { copyFileSync(pngPath, jpegPath); } catch {}
    } else if (existsSync(jpegPath) && !existsSync(pngPath)) {
      try { copyFileSync(jpegPath, pngPath); } catch {}
    }

    if (existsSync(pngPath)) {
      console.log(`[${i + 1}/${prompts.length}] Slide "${s.name}" already exists. Skipping.`);
      continue;
    }

    console.log(`\n------------------------------------------------------------`);
    console.log(`[${i + 1}/${prompts.length}] Generating slide: ${s.name}`);
    console.log(`Trigger: "${s.trigger}"`);
    console.log(`Title: "${s.top_title}" | Caption: "${s.bottom_caption}"`);
    console.log(`Prompt: ${s.prompt.slice(0, 100)}...`);

    const job = {
      id: `gen-${i + 1}`,
      status: 'running',
      files: [],
      attempts: 1,
      createdAt: new Date().toISOString(),
      params: {
        type: 'image',
        aspect_ratio: '1:1',
        prompt: s.prompt,
        output_dir: imagesDir,
        file_stem: s.name,
        max_credits: 10
      }
    };

    try {
      const files = await flow.runGeneration(job);
      console.log(` -> Generated:`, files);
      for (const f of files) {
        if (f.endsWith('.jpeg')) {
          copyFileSync(f, pngPath);
        } else if (f.endsWith('.png')) {
          copyFileSync(f, jpegPath);
        }
      }
      console.log(` -> Verified both .png and .jpeg for ${s.name}`);
    } catch (err) {
      console.error(` -> FAILED to generate ${s.name}:`, err.message || err);
      // Retry once after brief pause
      try {
        console.log(` -> Retrying ${s.name} once...`);
        const files = await flow.runGeneration(job);
        console.log(` -> Retry successful:`, files);
        for (const f of files) {
          if (f.endsWith('.jpeg')) copyFileSync(f, pngPath);
        }
      } catch (retryErr) {
        console.error(` -> Retry also failed for ${s.name}:`, retryErr.message || retryErr);
      }
    }
  }

  console.log(`\n[Batch Generator] Finished all slides.`);
  process.exit(0);
}

main().catch(err => {
  console.error('[Batch Generator] Fatal:', err);
  process.exit(1);
});
