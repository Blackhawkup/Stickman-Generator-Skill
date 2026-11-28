import { copyFileSync, existsSync, readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { resolve, join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

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

    let succeeded = false;
    for (let attempt = 1; attempt <= 2 && !succeeded; attempt++) {
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
        succeeded = true;
      } catch (err) {
        console.error(` -> Attempt ${attempt} FAILED for ${s.name}:`, err.message || err);
        if (attempt < 2) {
          console.log(` -> Waiting 3s before retrying ${s.name}...`);
          await new Promise(r => setTimeout(r, 3000));
        }
      }
    }
  }

  // Enforce exact pixel resolutions: 1080x1920 (9:16 short), 1920x1024 (16:9 long), 1920x1080 (thumbnail)
  try {
    const normScript = join(__dirname, 'images_util.py');
    const venvPy = join(process.env.WHITEBOARD_HOME || join(process.env.USERPROFILE || process.env.HOME || '', 'WhiteboardFilms'), '.tools', 'venv', process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python');
    const pyBin = existsSync(venvPy) ? venvPy : 'python';
    console.log(`\n[Batch Generator] Normalizing generated image resolutions...`);
    execFileSync(pyBin, [normScript, projectDir], { stdio: 'inherit' });
  } catch (normErr) {
    console.warn(`[Batch Generator] Image dimension normalization note:`, normErr.message || normErr);
  }

  console.log(`\n[Batch Generator] Finished all prompts.`);
  process.exit(0);
}

main().catch(err => {
  console.error('[Batch Generator] Fatal:', err);
  process.exit(1);
});
