#!/usr/bin/env npx tsx
/**
 * Convex Project Setup Script
 * ===========================
 * 
 * Sets up a new Convex project with the standard directory structure and templates.
 * 
 * USAGE:
 * ------
 * npx tsx ~/.claude/skills/convex/scripts/setup-convex.ts [convex-dir]
 * 
 * ARGUMENTS:
 * ----------
 * convex-dir: Path to the convex directory (default: ./convex)
 * 
 * WHAT IT DOES:
 * -------------
 * 1. Copies AGENTS.md template to convex/AGENTS.md
 * 2. Creates utils/ directory
 * 3. Sets up global schema.ts with aggregation pattern
 * 4. Removes common example files if they exist
 */

import * as fs from 'fs';
import * as path from 'path';

// Get the script's directory to find assets
const scriptDir = path.dirname(new URL(import.meta.url).pathname);
const skillDir = path.resolve(scriptDir, '..');

// Get convex directory from args or use default
const convexDir = process.argv[2] || './convex';

console.log(`\n🚀 Convex Project Setup\n`);
console.log(`Target directory: ${path.resolve(convexDir)}\n`);

// Check if convex directory exists
if (!fs.existsSync(convexDir)) {
    console.error(`❌ Directory not found: ${convexDir}`);
    console.log(`\nMake sure you've scaffolded Convex first. Default (Next.js + Clerk):`);
    console.log(`  pnpm create convex@latest . -- -t nextjs-clerk`);
    console.log(`\nThen run the first Convex cloud configuration in an interactive terminal:`);
    console.log(`  pnpm dlx convex@latest dev`);
    process.exit(1);
}

// 1. Copy AGENTS.md template
const agentsTemplatePath = path.join(skillDir, 'assets', 'AGENTS.template.md');
const agentsDestPath = path.join(convexDir, 'AGENTS.md');

if (fs.existsSync(agentsTemplatePath)) {
    if (fs.existsSync(agentsDestPath)) {
        console.log(`⚠️  AGENTS.md already exists, skipping`);
    } else {
        fs.copyFileSync(agentsTemplatePath, agentsDestPath);
        console.log(`✅ Created AGENTS.md`);
    }
} else {
    console.log(`⚠️  Template not found: ${agentsTemplatePath}`);
}

// 2. Create utils directory
const utilsDir = path.join(convexDir, 'utils');
if (!fs.existsSync(utilsDir)) {
    fs.mkdirSync(utilsDir, { recursive: true });

    // Create a placeholder file
    const helpersPath = path.join(utilsDir, 'helpers.ts');
    fs.writeFileSync(helpersPath, `/**
 * Shared Utilities
 * ================
 * 
 * Common helper functions used across multiple systems.
 */

// Add shared utilities here
`);
    console.log(`✅ Created utils/ directory`);
} else {
    console.log(`⚠️  utils/ already exists, skipping`);
}

// 3. Update schema.ts with aggregation pattern if it's the default
const schemaPath = path.join(convexDir, 'schema.ts');
if (fs.existsSync(schemaPath)) {
    const content = fs.readFileSync(schemaPath, 'utf-8');

    // Check if it's using the old pattern (has defineTable directly)
    if (content.includes('defineTable') && !content.includes('...')) {
        console.log(`ℹ️  schema.ts has tables defined - manually migrate to split schema pattern`);
    }
} else {
    // Create fresh schema.ts with aggregation pattern
    const schemaContent = `import { defineSchema } from "convex/server";
// Import system tables as you add them:
// import { userSystemTables } from "./user_system/schema";
// import { chatSystemTables } from "./chat_system/schema";

export default defineSchema({
    // Spread imported tables here:
    // ...userSystemTables,
    // ...chatSystemTables,
});
`;
    fs.writeFileSync(schemaPath, schemaContent);
    console.log(`✅ Created schema.ts with aggregation pattern`);
}

// 4. Remove common example files
const exampleFiles = [
    'tasks.ts',
    'messages.ts',
    'users.ts',
    'example.ts',
];

let removedCount = 0;
for (const file of exampleFiles) {
    const filePath = path.join(convexDir, file);
    if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
        console.log(`🗑️  Removed example file: ${file}`);
        removedCount++;
    }
}

if (removedCount === 0) {
    console.log(`ℹ️  No example files to remove`);
}

console.log(`\n✨ Setup complete!\n`);
console.log(`Next steps:`);
console.log(`1. Create your first system: mkdir ${convexDir}/user_system`);
console.log(`2. Add schema.ts to your system with validators and tables`);
console.log(`3. Update AGENTS.md as you add systems`);
console.log(`4. Import and spread system tables in global schema.ts\n`);

