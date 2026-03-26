# Bash Efficiency Patterns

Use these patterns to keep shell work fast and predictable.

## 1) Move/Rename Instead of Recreate

```bash
# Rename a file
mv old-name.txt new-name.txt

# Move files into a new folder
mkdir -p archive && mv *.log archive/
```

## 2) Copy Only When Needed

```bash
# Preserve metadata and recurse
cp -a source/ dest/
```

## 3) Preview Before Mutation

```bash
ls -la
tree -L 2
rg 'needle' -n .
```

## 4) Safe Bulk Replace Flow

```bash
# 1) Preview matching lines
rg 'oldValue' -n

# 2) List target files
rg -l 'oldValue'

# 3) Replace in-place only after preview (safe for spaces/newlines in paths)
rg -l -0 'oldValue' | xargs -0 sed -i 's/oldValue/newValue/g'
```

## 5) Process Files Directly

```bash
# No manual retyping; stream through stdin/stdout
python transform.py < input.json > output.json
```

## 6) Pipes Over Temp Files

```bash
rg 'ERROR' app.log | wc -l
```

## 7) JSON/YAML Quick Edits

```bash
jq '.featureFlag = true' config.json > config.next.json
yq '.service.port = 8081' app.yaml
```

## 8) Archive/Inspect Fast

```bash
tar -tf release.tar.gz
unzip -l package.zip
wc -l src/main.ts
```

## 9) Re-run Reliability

Put repeated command chains into scripts:

```bash
scripts/reindex.sh
make verify
```
