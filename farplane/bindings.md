---
kind: project-bindings
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-15
framework_template_version: "0.1.0"
owner: project-pm-automation
---

# Farplane Bindings

Non-secret coordinates that bind generic skills to this project.

Skills own capabilities.
Bindings provide project-specific IDs, URLs, labels, and aliases.
Secrets stay in the secure runtime environment.

```project-bindings
project {
  id: farplane
  name: "Farplane"
  root: "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
}

github {
  enabled: true
  repo: "ZanarkandTechnologies/Farplane"
  remote: "git@github.com:ZanarkandTechnologies/Farplane.git"
  default_branch: "main"
}

notion {
  enabled: false
  project_name: "Farplane"
  project_page_url: null
  task_database_alias: null
  write_policy: local_first
}

posthog {
  enabled: false
  project_id: null
  host: null
  dashboard_url: null
}

vercel {
  enabled: false
  project_id: null
  project_url: null
  production_url: null
}

workos {
  enabled: false
  tenant_alias: null
  dashboard_url: null
}
```

## Policy

- Store only non-secret project coordinates here.
- Put credentials in environment variables, secret stores, or the runtime
  connector config.
- If a skill needs a binding that is missing, create a ticket to add the
  binding or create the data-access skill.
