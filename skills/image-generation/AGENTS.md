# Image Generation Skill Instructions

This module is the inference.sh image-generation category skill. Keep `SKILL.md` as the active root with the umbrella model map and Codexter gates.

The files under `references/tools/` are copied upstream inference.sh `SKILL.md` files for specific image tool branches. Refresh them from upstream instead of rewriting them by hand.

Do not turn each upstream image model into a public active Codexter skill. Route through `image-generation`, then load the specific reference.

Keep the built-in `imagegen` skill as the default for normal Codex-native bitmap generation/editing when inference.sh is not needed.
