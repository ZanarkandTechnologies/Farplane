import {
  ArrowLeft,
  CheckCircle2,
  CircleAlert,
  FileJson,
  FolderOpen,
  ListFilter,
  RefreshCw,
  Search,
  Upload,
} from 'lucide-react'
import type React from 'react'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { ScrollArea } from '@/components/ui/scroll-area'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'

type Verdict = 'A' | 'B' | 'C' | 'D' | string

type SummaryTask = {
  task_id: string
  title: string
  verdict: Verdict
  pass: boolean
  reason: string
  detail_path?: string
}

type EvalSummary = {
  job_id: string
  label: string
  created_at: string
  harness: string
  judge_harness: string
  suite: string
  task_files: string[]
  task_count: number
  pass_rate: number
  verdict_counts: Record<string, number>
  tasks: SummaryTask[]
}

type EvalTask = {
  id: string
  title: string
  query: string
  reference_points: string[]
  tags?: string[]
  notes?: string
}

type ReferencePointResult = {
  reference_point: string
  met: boolean
  reason: string
}

type TaskDetail = {
  task: EvalTask
  run_config: {
    harness: string
    judge_harness: string
  }
  agent: {
    returncode: number
    answer_path: string
    answer_text?: string
  }
  judge: {
    verdict: Verdict
    pass: boolean
    rubric: Record<string, string>
    reference_point_results: ReferencePointResult[]
    reason: string
    raw_response?: string
  }
}

const RUNS_BASE = '/runs'

function getRouteTaskId(): string {
  const match = window.location.pathname.match(/^\/tasks\/([^/]+)$/)
  return match ? decodeURIComponent(match[1]) : ''
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null
}

function isSummaryTask(value: unknown): value is SummaryTask {
  if (!isRecord(value)) return false
  return (
    typeof value.task_id === 'string' &&
    typeof value.title === 'string' &&
    typeof value.verdict === 'string' &&
    typeof value.pass === 'boolean' &&
    typeof value.reason === 'string'
  )
}

function isEvalSummary(value: unknown): value is EvalSummary {
  if (!isRecord(value)) return false
  return (
    typeof value.job_id === 'string' &&
    typeof value.label === 'string' &&
    typeof value.created_at === 'string' &&
    typeof value.farplane === 'string' &&
    typeof value.judge_harness === 'string' &&
    typeof value.suite === 'string' &&
    typeof value.task_count === 'number' &&
    typeof value.pass_rate === 'number' &&
    Array.isArray(value.task_files) &&
    value.task_files.every((item) => typeof item === 'string') &&
    isRecord(value.verdict_counts) &&
    Array.isArray(value.tasks) &&
    value.tasks.every(isSummaryTask)
  )
}

function isTaskDetail(value: unknown): value is TaskDetail {
  if (!isRecord(value) || !isRecord(value.task) || !isRecord(value.judge)) return false
  return (
    typeof value.task.id === 'string' &&
    typeof value.task.title === 'string' &&
    typeof value.task.query === 'string' &&
    Array.isArray(value.task.reference_points) &&
    value.task.reference_points.every((item) => typeof item === 'string') &&
    typeof value.judge.verdict === 'string' &&
    typeof value.judge.pass === 'boolean'
  )
}

async function readJsonFile(file: File): Promise<unknown> {
  return JSON.parse(await file.text()) as unknown
}

function formatDate(value: string): string {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date)
}

function formatPercent(value: number): string {
  return `${Math.round(value * 100)}%`
}

function verdictBadgeVariant(verdict: Verdict): 'default' | 'secondary' | 'destructive' | 'outline' {
  if (verdict === 'A') return 'default'
  if (verdict === 'B') return 'secondary'
  if (verdict === 'C') return 'outline'
  return 'destructive'
}

function App() {
  const summaryInputRef = useRef<HTMLInputElement>(null)
  const detailInputRef = useRef<HTMLInputElement>(null)
  const [summary, setSummary] = useState<EvalSummary | null>(null)
  const [details, setDetails] = useState<Map<string, TaskDetail>>(new Map())
  const [selectedTaskId, setSelectedTaskId] = useState('')
  const [routeTaskId, setRouteTaskId] = useState(getRouteTaskId)
  const [query, setQuery] = useState('')
  const [filter, setFilter] = useState('all')
  const [status, setStatus] = useState('No run loaded')

  useEffect(() => {
    function handlePopState(): void {
      setRouteTaskId(getRouteTaskId())
    }

    window.addEventListener('popstate', handlePopState)
    return () => window.removeEventListener('popstate', handlePopState)
  }, [])

  const selectedTask = useMemo(() => {
    if (!summary) return null
    const activeTaskId = routeTaskId || selectedTaskId
    return summary.tasks.find((task) => task.task_id === activeTaskId) ?? summary.tasks[0] ?? null
  }, [routeTaskId, selectedTaskId, summary])

  const selectedDetail = selectedTask ? details.get(selectedTask.task_id) : undefined

  const filteredTasks = useMemo(() => {
    if (!summary) return []
    const needle = query.trim().toLowerCase()
    return summary.tasks.filter((task) => {
      const detail = details.get(task.task_id)
      const blob = [
        task.task_id,
        task.title,
        task.reason,
        detail?.task.query,
        detail?.task.tags?.join(' '),
      ]
        .join(' ')
        .toLowerCase()
      const matchesText = needle.length === 0 || blob.includes(needle)
      const matchesFilter =
        filter === 'all' ||
        task.verdict === filter ||
        (filter === 'pass' && task.pass) ||
        (filter === 'fail' && !task.pass)
      return matchesText && matchesFilter
    })
  }, [details, filter, query, summary])

  const applySummary = useCallback((nextSummary: EvalSummary): void => {
    setSummary(nextSummary)
    setSelectedTaskId(nextSummary.tasks[0]?.task_id ?? '')
    setStatus(`Loaded ${nextSummary.job_id}`)
  }, [])

  function navigateToTask(taskId: string): void {
    setSelectedTaskId(taskId)
    const nextPath = `/tasks/${encodeURIComponent(taskId)}`
    window.history.pushState({}, '', nextPath)
    setRouteTaskId(taskId)
  }

  function navigateHome(): void {
    window.history.pushState({}, '', '/')
    setRouteTaskId('')
  }

  const loadLatestRun = useCallback(async (): Promise<void> => {
    setStatus('Loading runs/index.json')
    const indexResponse = await fetch(`${RUNS_BASE}/index.json`)
    if (!indexResponse.ok) {
      setStatus('Could not load local runs index')
      return
    }
    const indexJson = (await indexResponse.json()) as unknown
    if (!Array.isArray(indexJson) || !isRecord(indexJson[0]) || typeof indexJson[0].job_id !== 'string') {
      setStatus('Runs index did not contain a latest job')
      return
    }
    const jobId = indexJson[0].job_id
    const summaryResponse = await fetch(`${RUNS_BASE}/${jobId}/summary.json`)
    const summaryJson = (await summaryResponse.json()) as unknown
    if (!isEvalSummary(summaryJson)) {
      setStatus('Latest summary did not match eval shape')
      return
    }
    applySummary(summaryJson)

    const loadedDetails = new Map<string, TaskDetail>()
    await Promise.all(
      summaryJson.tasks.map(async (task) => {
        const detailResponse = await fetch(`${RUNS_BASE}/${jobId}/tasks/${task.task_id}.json`)
        if (!detailResponse.ok) return
        const detailJson = (await detailResponse.json()) as unknown
        if (isTaskDetail(detailJson)) {
          const answerResponse = await fetch(`${RUNS_BASE}/${jobId}/tasks/${task.task_id}/agent_answer.txt`)
          if (answerResponse.ok) {
            detailJson.agent.answer_text = await answerResponse.text()
          }
          loadedDetails.set(detailJson.task.id, detailJson)
        }
      })
    )
    setDetails(loadedDetails)
    setStatus(`Loaded ${summaryJson.job_id} with ${loadedDetails.size} task details`)
  }, [applySummary])

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void loadLatestRun()
    }, 0)

    return () => window.clearTimeout(timer)
  }, [loadLatestRun])

  async function handleSummaryFiles(files: FileList | null): Promise<void> {
    const file = files?.[0]
    if (!file) return
    const json = await readJsonFile(file)
    if (!isEvalSummary(json)) {
      setStatus('That file is not a summary.json')
      return
    }
    applySummary(json)
  }

  async function handleDetailFiles(files: FileList | null): Promise<void> {
    if (!files) return
    const loaded = new Map(details)
    let count = 0
    for (const file of Array.from(files)) {
      if (!file.name.endsWith('.json')) continue
      const json = await readJsonFile(file)
      if (isTaskDetail(json)) {
        loaded.set(json.task.id, json)
        count += 1
      }
    }
    setDetails(loaded)
    setStatus(`Loaded ${count} task detail file${count === 1 ? '' : 's'}`)
  }

  return (
    <main className="min-h-screen bg-background text-foreground">
      <div className="mx-auto flex w-full max-w-[1500px] flex-col gap-4 px-5 py-5 lg:px-8">
        <header className="flex flex-col gap-4 rounded-lg border bg-card p-5 shadow-sm md:flex-row md:items-end md:justify-between">
          <div className="grid gap-2">
            <div className="flex flex-wrap items-center gap-2">
              <Badge variant="outline">harness evals</Badge>
              <Badge variant="secondary">{status}</Badge>
            </div>
            <div className="grid gap-1">
              <h1 className="text-2xl font-semibold leading-tight md:text-3xl">Eval Run Viewer</h1>
              <p className="max-w-3xl text-sm leading-6 text-muted-foreground">
                A shadcn React surface for reading `summary.json` and task detail artifacts from the local eval runner.
              </p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button onClick={loadLatestRun}>
              <RefreshCw />
              Load latest
            </Button>
            <Button variant="outline" onClick={() => summaryInputRef.current?.click()}>
              <Upload />
              Summary
            </Button>
            <Button variant="outline" onClick={() => detailInputRef.current?.click()}>
              <FolderOpen />
              Details
            </Button>
            <input
              id="summary-file"
              ref={summaryInputRef}
              className="hidden"
              type="file"
              accept=".json,application/json"
              onChange={(event) => void handleSummaryFiles(event.target.files)}
            />
            <input
              id="detail-files"
              ref={detailInputRef}
              className="hidden"
              type="file"
              accept=".json,application/json"
              multiple
              onChange={(event) => void handleDetailFiles(event.target.files)}
            />
          </div>
        </header>

        {routeTaskId ? (
          <TaskRoutePage detail={selectedDetail} fallback={selectedTask} onBack={navigateHome} />
        ) : (
          <section className="grid gap-4 lg:grid-cols-[360px_minmax(0,1fr)]">
            <aside className="grid gap-4">
              <Card>
                <CardHeader>
                  <CardTitle>Run</CardTitle>
                  <CardDescription>
                    {summary ? `${summary.label} / ${summary.job_id}` : 'Load a summary to begin.'}
                  </CardDescription>
                </CardHeader>
                <CardContent className="grid gap-3">
                  <Metric label="Pass rate" value={summary ? formatPercent(summary.pass_rate) : '--'} />
                  <Metric label="Tasks" value={summary ? String(summary.task_count) : '--'} />
                  <Metric label="Harness" value={summary?.farplane ?? '--'} />
                  <Metric label="Judge" value={summary?.judge_harness ?? '--'} />
                  {summary ? <p className="text-xs text-muted-foreground">{formatDate(summary.created_at)}</p> : null}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Verdicts</CardTitle>
                  <CardDescription>A is the only pass tier.</CardDescription>
                </CardHeader>
                <CardContent className="flex flex-wrap gap-2">
                  {summary
                    ? Object.entries(summary.verdict_counts).map(([verdict, count]) => (
                        <Badge key={verdict} variant={verdictBadgeVariant(verdict)}>
                          {verdict}: {count}
                        </Badge>
                      ))
                    : <Badge variant="outline">No verdicts</Badge>}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Filters</CardTitle>
                  <CardDescription>Find the failures first.</CardDescription>
                </CardHeader>
                <CardContent className="grid gap-3">
                  <div className="relative">
                    <Search className="pointer-events-none absolute left-2.5 top-2.5 size-4 text-muted-foreground" />
                    <Input
                      className="pl-8"
                      placeholder="Search tasks"
                      value={query}
                      onChange={(event) => setQuery(event.target.value)}
                    />
                  </div>
                  <Select value={filter} onValueChange={(value) => setFilter(value ?? 'all')}>
                    <SelectTrigger>
                      <ListFilter className="size-4" />
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All tasks</SelectItem>
                      <SelectItem value="pass">Pass only</SelectItem>
                      <SelectItem value="fail">Needs work</SelectItem>
                      <SelectItem value="A">A</SelectItem>
                      <SelectItem value="B">B</SelectItem>
                      <SelectItem value="C">C</SelectItem>
                      <SelectItem value="D">D</SelectItem>
                    </SelectContent>
                  </Select>
                </CardContent>
              </Card>
            </aside>

            <section>
              <Card className="min-h-[680px]">
                <CardHeader>
                  <CardTitle>Tasks</CardTitle>
                  <CardDescription>Click a task to inspect the full eval trace. {filteredTasks.length} visible.</CardDescription>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-[680px] pr-3">
                    <div className="grid gap-2 md:grid-cols-2 xl:grid-cols-3">
                      {filteredTasks.map((task) => (
                        <button
                          key={task.task_id}
                          type="button"
                          onClick={() => navigateToTask(task.task_id)}
                          className={`rounded-lg border p-3 text-left transition hover:bg-accent ${
                            selectedTask?.task_id === task.task_id ? 'border-primary bg-accent' : 'border-border bg-card'
                          }`}
                        >
                          <div className="mb-2 flex items-start justify-between gap-2">
                            <h2 className="text-sm font-medium leading-5">{task.title}</h2>
                            <Badge variant={verdictBadgeVariant(task.verdict)}>{task.verdict}</Badge>
                          </div>
                          <p className="line-clamp-3 text-xs leading-5 text-muted-foreground">{task.reason}</p>
                          <div className="mt-3 flex flex-wrap gap-1.5">
                            <Badge variant={task.pass ? 'default' : 'destructive'}>
                              {task.pass ? <CheckCircle2 /> : <CircleAlert />}
                              {task.pass ? 'pass' : 'needs work'}
                            </Badge>
                            <Badge variant="outline">{details.has(task.task_id) ? 'detail loaded' : 'summary only'}</Badge>
                          </div>
                        </button>
                      ))}
                    </div>
                  </ScrollArea>
                </CardContent>
              </Card>
            </section>
          </section>
        )}
      </div>
    </main>
  )
}

function TaskRoutePage({
  detail,
  fallback,
  onBack,
}: {
  detail?: TaskDetail
  fallback: SummaryTask | null
  onBack: () => void
}) {
  return (
    <section className="grid gap-4">
      <div className="flex flex-col gap-3 rounded-lg border bg-card p-5 shadow-sm md:flex-row md:items-start md:justify-between">
        <div className="flex min-w-0 gap-3">
          <Button variant="outline" size="icon" onClick={onBack} aria-label="Back to tasks">
            <ArrowLeft />
          </Button>
          <div className="grid min-w-0 gap-1">
            <div className="flex flex-wrap items-center gap-2">
              {fallback ? <Badge variant={verdictBadgeVariant(fallback.verdict)}>{fallback.verdict}</Badge> : null}
              {fallback ? (
                <Badge variant={fallback.pass ? 'default' : 'destructive'}>
                  {fallback.pass ? 'pass' : 'needs work'}
                </Badge>
              ) : null}
            </div>
            <h2 className="text-2xl font-semibold leading-tight md:text-3xl">
              {fallback?.title ?? 'Task detail'}
            </h2>
            <p className="break-all text-sm text-muted-foreground">{fallback?.task_id ?? 'No task selected'}</p>
          </div>
        </div>
        {fallback ? <p className="max-w-2xl text-sm leading-6 text-muted-foreground">{fallback.reason}</p> : null}
      </div>

      <Card>
        <CardContent className="p-5 md:p-6">
          <TaskDetailPanel detail={detail} fallback={fallback} />
        </CardContent>
      </Card>
    </section>
  )
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-lg border bg-muted/40 px-3 py-2">
      <span className="text-xs text-muted-foreground">{label}</span>
      <strong className="text-sm font-medium">{value}</strong>
    </div>
  )
}

function TaskDetailPanel({ detail, fallback }: { detail?: TaskDetail; fallback: SummaryTask | null }) {
  if (!fallback) {
    return (
      <div className="flex min-h-[320px] items-center justify-center text-center text-sm text-muted-foreground">
        Load an eval run to inspect task details.
      </div>
    )
  }

  if (!detail) {
    return (
      <div className="grid gap-4">
        <Badge className="w-fit" variant={verdictBadgeVariant(fallback.verdict)}>
          {fallback.verdict}
        </Badge>
        <p className="text-sm leading-6 text-muted-foreground">{fallback.reason}</p>
        <Separator />
        <p className="text-sm text-muted-foreground">
          Load the task JSON files to see the rubric, reference points, and artifact paths.
        </p>
      </div>
    )
  }

  return (
    <div className="grid gap-6">
        <ReportSection title="Task" description="The input task the harness received.">
          <div className="rounded-lg border bg-muted/30 p-3">
            <p className="text-sm leading-6">{detail.task.query}</p>
          </div>
          <div className="flex flex-wrap gap-2">
            {detail.task.tags?.map((tag) => (
              <Badge key={tag} variant="outline">{tag}</Badge>
            ))}
          </div>
          {detail.task.notes ? <p className="text-sm leading-6 text-muted-foreground">{detail.task.notes}</p> : null}
          <div className="grid gap-2">
            {detail.task.reference_points.map((point) => (
              <div key={point} className="flex gap-2 rounded-lg border bg-card p-3 text-sm leading-5">
                <FileJson className="mt-0.5 size-4 shrink-0 text-primary" />
                <span>{point}</span>
              </div>
            ))}
          </div>
        </ReportSection>

        <ReportSection title="Agent response" description="The harness answer before judging.">
          {detail.agent.answer_text ? (
            <pre className="max-h-[420px] overflow-auto rounded-lg border bg-muted/30 p-3 text-xs leading-5 whitespace-pre-wrap">
              {detail.agent.answer_text}
            </pre>
          ) : (
            <p className="text-sm leading-6 text-muted-foreground">
              Agent response text is not loaded for this task. Use the path at the bottom to inspect the artifact.
            </p>
          )}
        </ReportSection>

        <ReportSection title="Judge analysis" description="The final judge explanation and per-point checks.">
          <p className="text-sm leading-6 text-muted-foreground">{detail.judge.reason}</p>
          <div className="grid gap-2">
            {detail.judge.reference_point_results.map((result) => (
              <div key={result.reference_point} className="rounded-lg border bg-muted/30 p-3">
                <div className="mb-2 flex items-start justify-between gap-3">
                  <p className="text-sm font-medium leading-5">{result.reference_point}</p>
                  <Badge variant={result.met ? 'default' : 'destructive'}>{result.met ? 'met' : 'missed'}</Badge>
                </div>
                <p className="text-xs leading-5 text-muted-foreground">{result.reason}</p>
              </div>
            ))}
          </div>
        </ReportSection>

        <ReportSection title="Rubric" description="Tier grades from the judge prompt.">
          <div className="grid gap-3 sm:grid-cols-2">
            {Object.entries(detail.judge.rubric).map(([name, grade]) => (
              <div key={name} className="rounded-lg border bg-muted/30 p-3">
                <p className="mb-1 text-xs text-muted-foreground">{name.replace(/_/g, ' ')}</p>
                <p className="text-xl font-semibold">{grade}</p>
              </div>
            ))}
          </div>
        </ReportSection>

        <ReportSection title="Paths" description="Raw artifacts and run configuration.">
          <PathRow label="Agent answer" value={detail.agent.answer_path} />
          <PathRow label="Harness" value={detail.run_config.farplane} />
          <PathRow label="Judge" value={detail.run_config.judge_harness} />
        </ReportSection>
    </div>
  )
}

function ReportSection({
  title,
  description,
  children,
}: {
  title: string
  description: string
  children: React.ReactNode
}) {
  return (
    <section className="grid gap-3">
      <div className="grid gap-1">
        <h3 className="text-sm font-semibold">{title}</h3>
        <p className="text-xs leading-5 text-muted-foreground">{description}</p>
      </div>
      {children}
      <Separator />
    </section>
  )
}

function PathRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="grid gap-1 rounded-lg border bg-muted/30 p-3">
      <span className="text-xs text-muted-foreground">{label}</span>
      <code className="break-all text-xs text-foreground">{value}</code>
    </div>
  )
}

export default App
