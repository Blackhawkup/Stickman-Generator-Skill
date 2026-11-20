import { copyFileSync, existsSync, readFileSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';

async function main() {
  const arg = process.argv[2] || 'sunk-cost-fallacy';
  let projectDir;
  if (existsSync(arg) && existsSync(join(arg, 'film.json'))) {
    projectDir = resolve(arg);
  } else if (existsSync(join(process.cwd(), arg, 'film.json'))) {
    projectDir = join(process.cwd(), arg);
  } else {
    projectDir = resolve('slideshow-workflow/projects', arg);
  }

  const promptsFile = join(projectDir, 'prompts.json');
  const imagesDir = join(projectDir, 'images');
  if (!existsSync(promptsFile)) {
    console.error(`[Batch Generator] Prompts file missing at: ${promptsFile}`);
    process.exit(1);
  }

  const prompts = JSON.parse(readFileSync(promptsFile, 'utf-8'));

  // Import flow-mcp
  const flowUrl = pathToFileURL('C:/Users/sangw/flow-mcp/dist/flow.js').href;
  const flow = await import(flowUrl);

  console.log(`[Batch Generator] Starting generation for ${prompts.length} items in ${projectDir}...`);

  for (let i = 0; i < prompts.length; i++) {
    const s = prompts[i];
    const aspectRatio = s.aspect_ratio || '1:1';
    const pngPath = join(imagesDir, `${s.name}.png`);
    const jpegPath = join(imagesDir, `${s.name}.jpeg`);

    if (existsSync(pngPath) && !existsSync(jpegPath)) {
      try { copyFileSync(pngPath, jpegPath); } catch {}
    } else if (existsSync(jpegPath) && !existsSync(pngPath)) {
      try { copyFileSync(jpegPath, pngPath); } catch {}
    }

    if (existsSync(pngPath)) {
      console.log(`[${i + 1}/${prompts.length}] "${s.name}" already exists. Skipping.`);
      continue;
    }

    console.log(`\n------------------------------------------------------------`);
    console.log(`[${i + 1}/${prompts.length}] Generating [${aspectRatio}]: ${s.name}`);
    if (s.trigger) console.log(`Trigger: "${s.trigger}"`);
    console.log(`Prompt: ${s.prompt.slice(0, 100)}...`);

    const job = {
      id: `gen-${i + 1}`,
      status: 'running',
      files: [],
      attempts: 1,
      createdAt: new Date().toISOString(),
      params: {
        type: 'image',
        aspect_ratio: aspectRatio,
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
      
      // If thumbnail, also copy to project root
      if (s.type === 'thumbnail') {
        const thumbDest = join(projectDir, `${s.name}.png`);
        try { copyFileSync(pngPath, thumbDest); } catch {}
        console.log(` -> Preserved thumbnail at: ${thumbDest}`);
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

  console.log(`\n[Batch Generator] Finished all prompts.`);
  process.exit(0);
}

main().catch(err => {
  console.error('[Batch Generator] Fatal:', err);
  process.exit(1);
});
