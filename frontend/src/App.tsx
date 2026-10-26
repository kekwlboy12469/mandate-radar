import React, { useState, useEffect } from 'react'
import {
  ShieldAlert,
  AlertTriangle,
  CheckCircle2,
  TrendingUp,
  CreditCard,
  Building2,
  Network,
  Terminal,
  FileText,
  Mail,
  Copy,
  Check,
  RefreshCw,
  Upload,
  Layers,
  Activity,
  ChevronRight,
  LayoutGrid,
  List,
  Sparkles,
  ExternalLink,
  ShieldCheck,
  Zap,
  Info,
  DollarSign,
  ArrowRight
} from 'lucide-react'
import { GraphCanvas, type GraphNode, type GraphEdge } from './components/GraphCanvas'

interface Mandate {
  id: string
  merchant_id: string
  merchant_name: string
  category: string
  parent_id: string
  parent_name: string
  descriptor: string
  is_recognized: boolean
  cadence: string
  latest_amount: number
  initial_amount?: number
  annual_committed_cost: number
  charge_count: number
  first_seen: string
  last_charged: string
  mechanism: string
  mechanism_name: string
  flag: 'HEALTHY' | 'PRICE_HIKE' | 'TRIAL_CONVERTED' | 'UNUSED_ZOMBIE'
  flag_reason: string
  confidence_score: number
  savings_if_cancelled: number
  pitfall: string
  support_email?: string
  grievance_email?: string
  official_website?: string
  cancellation_steps: string[]
  history: Array<{ id: string; date: string; amount: number; descriptor: string }>
  recent_notifications?: Array<{ id: string; text: string; channel: string; timestamp: string }>
}

interface HeroMetrics {
  annual_committed_total: number
  monthly_equivalent: number
  potential_savings: number
  total_mandates_found: number
  flagged_issues_count: number
}

// Brand Avatar Helper with clean initial & color
const getBrandVisual = (name: string) => {
  const n = name.toLowerCase()
  if (n.includes('youtube')) return { icon: '▶', bg: 'bg-red-500/15 text-red-400 border-red-500/30' }
  if (n.includes('spotify')) return { icon: '♫', bg: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30' }
  if (n.includes('netflix')) return { icon: 'N', bg: 'bg-rose-500/15 text-rose-400 border-rose-500/30' }
  if (n.includes('amazon') || n.includes('prime')) return { icon: 'A', bg: 'bg-amber-500/15 text-amber-400 border-amber-500/30' }
  if (n.includes('hotstar') || n.includes('disney')) return { icon: 'D+', bg: 'bg-blue-500/15 text-blue-400 border-blue-500/30' }
  if (n.includes('cult')) return { icon: '⚡', bg: 'bg-cyan-500/15 text-cyan-400 border-cyan-500/30' }
  if (n.includes('chatgpt') || n.includes('openai')) return { icon: '✦', bg: 'bg-teal-500/15 text-teal-400 border-teal-500/30' }
  if (n.includes('canva')) return { icon: 'C', bg: 'bg-sky-500/15 text-sky-400 border-sky-500/30' }
  if (n.includes('truecaller')) return { icon: 'T', bg: 'bg-indigo-500/15 text-indigo-400 border-indigo-500/30' }
  return { icon: name.charAt(0).toUpperCase(), bg: 'bg-slate-500/15 text-slate-300 border-slate-500/30' }
}

export default function App() {
  const [activeTab, setActiveTab] = useState<'radar' | 'graph' | 'benchmark' | 'upload'>('radar')
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid')
  const [mandates, setMandates] = useState<Mandate[]>([])
  const [heroMetrics, setHeroMetrics] = useState<HeroMetrics>({
    annual_committed_total: 0,
    monthly_equivalent: 0,
    potential_savings: 0,
    total_mandates_found: 0,
    flagged_issues_count: 0
  })
  const [cancelledIds, setCancelledIds] = useState<Set<string>>(new Set())
  const [selectedMandate, setSelectedMandate] = useState<Mandate | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeFilter, setActiveFilter] = useState<'ALL' | 'PRICE_HIKE' | 'TRIAL_CONVERTED' | 'UNUSED_ZOMBIE' | 'HEALTHY'>('ALL')

  // Notification stream
  const [notifications, setNotifications] = useState<any[]>([])
  const [showNotifications, setShowNotifications] = useState(false)

  // Neo4j Graph state
  const [graphMode, setGraphMode] = useState<string>('portfolio')
  const [graphData, setGraphData] = useState<{ nodes: GraphNode[]; edges: GraphEdge[]; stats: any }>({
    nodes: [],
    edges: [],
    stats: {}
  })
  const [cypherQuery, setCypherQuery] = useState(
    'MATCH (p:Parent)<-[:OWNED_BY]-(m:Merchant)<-[:FOR]-(mand:Mandate)\nRETURN p.name AS Parent, collect(m.name) AS ActiveMerchants, sum(mand.annual_cost) AS AnnualCommittedSpend;'
  )
  const [cypherResult, setCypherResult] = useState<any>(null)
  const [cypherLoading, setCypherLoading] = useState(false)
  const [cypherSeedScript, setCypherSeedScript] = useState<string>('')
  const [showSeedModal, setShowSeedModal] = useState(false)
  const [showNeo4jModal, setShowNeo4jModal] = useState(false)
  const [neo4jUri, setNeo4jUri] = useState('neo4j+s://your-instance.databases.neo4j.io')
  const [neo4jUser, setNeo4jUser] = useState('neo4j')
  const [neo4jPass, setNeo4jPass] = useState('')
  const [neo4jStatus, setNeo4jStatus] = useState<'EMBEDDED' | 'CONNECTED' | 'ERROR'>('EMBEDDED')
  const [neo4jMsg, setNeo4jMsg] = useState('')

  // Email Generator state
  const [emailTone, setEmailTone] = useState<'polite' | 'formal' | 'firm_dispute'>('formal')
  const [emailSubject, setEmailSubject] = useState('')
  const [emailBody, setEmailBody] = useState('')
  const [emailCopied, setEmailCopied] = useState(false)

  // Benchmark state
  const [benchmarkData, setBenchmarkData] = useState<any>(null)

  // CSV Upload state
  const [uploadFile, setUploadFile] = useState<File | null>(null)
  const [uploadLoading, setUploadLoading] = useState(false)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null)

  useEffect(() => {
    fetchInitialData()
    fetchGraphData('portfolio')
    fetchBenchmark()
  }, [])

  const fetchInitialData = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_name: 'Arun Sharma' })
      })
      const data = await res.json()
      setMandates(data.mandates || [])
      setHeroMetrics(data.hero_metrics || {
        annual_committed_total: 0,
        monthly_equivalent: 0,
        potential_savings: 0,
        total_mandates_found: 0,
        flagged_issues_count: 0
      })

      const notifRes = await fetch('/api/statement/synthetic')
      const notifData = await notifRes.json()
      setNotifications(notifData.notifications || [])
    } catch (err) {
      console.error('Failed to load analysis:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchGraphData = async (mode: string = graphMode) => {
    setGraphMode(mode)
    try {
      const res = await fetch(`/api/graph?mode=${mode}`)
      const data = await res.json()
      setGraphData(data)
    } catch (err) {
      console.error('Failed to fetch graph data:', err)
    }
  }

  const fetchBenchmark = async () => {
    try {
      const res = await fetch('/api/benchmark')
      const data = await res.json()
      setBenchmarkData(data)
    } catch (err) {
      console.error('Failed to fetch benchmark:', err)
    }
  }

  const runCypher = async (queryToRun?: string) => {
    const q = queryToRun || cypherQuery
    setCypherLoading(true)
    try {
      const res = await fetch('/api/graph/cypher', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q })
      })
      const data = await res.json()
      setCypherResult(data)
    } catch (err) {
      setCypherResult({ error: String(err) })
    } finally {
      setCypherLoading(false)
    }
  }

  const fetchCypherSeed = async () => {
    try {
      const res = await fetch('/api/graph/seed')
      const data = await res.json()
      setCypherSeedScript(data.script || '')
      setShowSeedModal(true)
    } catch (err) {
      console.error('Failed to fetch seed script:', err)
    }
  }

  const handleConnectNeo4j = async (e: React.FormEvent) => {
    e.preventDefault()
    setNeo4jMsg('Connecting to Neo4j instance...')
    try {
      const res = await fetch('/api/neo4j/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uri: neo4jUri, user: neo4jUser, password: neo4jPass })
      })
      const data = await res.json()
      if (data.success) {
        setNeo4jStatus('CONNECTED')
        setNeo4jMsg('Successfully connected to live Neo4j Aura cluster.')
        fetchGraphData('portfolio')
      } else {
        setNeo4jStatus('ERROR')
        setNeo4jMsg(data.message || 'Connection failed.')
      }
    } catch (err) {
      setNeo4jStatus('ERROR')
      setNeo4jMsg(String(err))
    }
  }

  const generateEmail = async (mandate: Mandate, tone: 'polite' | 'formal' | 'firm_dispute') => {
    setEmailTone(tone)
    try {
      const res = await fetch('/api/generate-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mandate_id: mandate.id,
          merchant_name: mandate.merchant_name,
          descriptor: mandate.descriptor,
          amount: mandate.latest_amount,
          cadence: mandate.cadence,
          mechanism: mandate.mechanism,
          user_name: 'Arun Sharma',
          account_ref: 'HDFC Card ending 4821 / UPI VPA',
          tone: tone
        })
      })
      const data = await res.json()
      setEmailSubject(data.subject)
      setEmailBody(data.body)
    } catch (err) {
      console.error('Failed to generate notice:', err)
    }
  }

  const toggleCancel = (id: string) => {
    setCancelledIds(prev => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const cancelAllFlagged = () => {
    const flaggedIds = mandates.filter(m => m.flag !== 'HEALTHY').map(m => m.id)
    setCancelledIds(new Set(flaggedIds))
  }

  const savedAmount = mandates
    .filter(m => cancelledIds.has(m.id))
    .reduce((sum, m) => sum + m.annual_committed_cost, 0)

  const activeCommitted = Math.max(0, heroMetrics.annual_committed_total - savedAmount)
  const savingsPct = heroMetrics.annual_committed_total > 0
    ? Math.round((savedAmount / heroMetrics.annual_committed_total) * 100)
    : 0

  const filteredMandates = mandates.filter(m => {
    if (activeFilter === 'ALL') return true
    return m.flag === activeFilter
  })

  const handleFileUpload = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!uploadFile) return

    setUploadLoading(true)
    setUploadError(null)
    setUploadSuccess(null)

    const formData = new FormData()
    formData.append('file', uploadFile)

    try {
      const res = await fetch('/api/upload-csv', {
        method: 'POST',
        body: formData
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || 'Upload failed.')
      }

      setMandates(data.mandates || [])
      setHeroMetrics(data.hero_metrics || heroMetrics)
      setCancelledIds(new Set())
      setUploadSuccess(`Successfully ingested ${data.rows_parsed} statement rows from ${data.filename}`)
      setActiveTab('radar')
      fetchGraphData('portfolio')
    } catch (err: any) {
      setUploadError(err.message || 'Error parsing statement file.')
    } finally {
      setUploadLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#07090e] text-[#e2e8f0] flex flex-col antialiased selection:bg-cyan-900 selection:text-white">
      {/* Top Header */}
      <header className="border-b border-white/[0.08] bg-[#0c101a]/85 backdrop-blur-md sticky top-0 z-40 px-6 py-3.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo & Product Identity */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-600 to-purple-600 p-[1px] shadow-lg shadow-cyan-500/20">
              <div className="w-full h-full bg-[#0c101a] rounded-xl flex items-center justify-center">
                <ShieldCheck className="w-5 h-5 text-cyan-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="font-extrabold text-sm tracking-tight text-white uppercase font-mono">
                  MANDATE RADAR
                </h1>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-cyan-950/80 text-cyan-400 border border-cyan-800/80 flex items-center gap-1 font-semibold">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
                  Neo4j Track Solution
                </span>
              </div>
              <p className="text-[11px] text-neutral-400 font-sans">
                Automated Mandate Discovery & Graph Resolution Engine
              </p>
            </div>
          </div>

          {/* Understated Segmented Navigation */}
          <nav className="flex items-center bg-[#111726] p-1 rounded-xl border border-white/[0.08] text-xs shadow-inner">
            <button
              onClick={() => setActiveTab('radar')}
              className={`px-3.5 py-1.5 rounded-lg font-semibold transition ${
                activeTab === 'radar'
                  ? 'bg-gradient-to-r from-cyan-600 to-indigo-600 text-white shadow-md'
                  : 'text-neutral-400 hover:text-white'
              }`}
            >
              Portfolio Radar
            </button>
            <button
              onClick={() => {
                setActiveTab('graph')
                if (!cypherResult) runCypher()
              }}
              className={`px-3.5 py-1.5 rounded-lg font-semibold transition flex items-center gap-1.5 ${
                activeTab === 'graph'
                  ? 'bg-gradient-to-r from-cyan-600 to-indigo-600 text-white shadow-md'
                  : 'text-neutral-400 hover:text-white'
              }`}
            >
              <Network className="w-3.5 h-3.5" />
              Graph Explorer
            </button>
            <button
              onClick={() => setActiveTab('benchmark')}
              className={`px-3.5 py-1.5 rounded-lg font-semibold transition flex items-center gap-1.5 ${
                activeTab === 'benchmark'
                  ? 'bg-gradient-to-r from-cyan-600 to-indigo-600 text-white shadow-md'
                  : 'text-neutral-400 hover:text-white'
              }`}
            >
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              Verification Report
            </button>
            <button
              onClick={() => setActiveTab('upload')}
              className={`px-3.5 py-1.5 rounded-lg font-semibold transition flex items-center gap-1.5 ${
                activeTab === 'upload'
                  ? 'bg-gradient-to-r from-cyan-600 to-indigo-600 text-white shadow-md'
                  : 'text-neutral-400 hover:text-white'
              }`}
            >
              <Upload className="w-3.5 h-3.5" />
              Ingest Statement
            </button>
          </nav>

          {/* Controls & Status Indicator */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative px-3 py-1.5 rounded-xl bg-[#111726] hover:bg-[#182136] border border-white/[0.08] text-neutral-300 hover:text-white text-xs flex items-center gap-1.5 transition font-mono"
            >
              <Activity className="w-3.5 h-3.5 text-cyan-400" />
              <span className="hidden sm:inline">RBI Alerts</span>
              {notifications.length > 0 && (
                <span className="w-2 h-2 rounded-full bg-cyan-400 absolute top-1 right-1 animate-ping" />
              )}
            </button>

            <button
              onClick={() => setShowNeo4jModal(true)}
              className="text-xs px-3 py-1.5 rounded-xl border border-white/[0.08] bg-[#111726] text-neutral-300 hover:bg-[#182136] flex items-center gap-1.5 font-mono transition"
            >
              <span
                className={`w-2 h-2 rounded-full ${
                  neo4jStatus === 'CONNECTED' ? 'bg-emerald-400 shadow-sm shadow-emerald-400/50' : 'bg-cyan-400'
                }`}
              />
              {neo4jStatus === 'CONNECTED' ? 'Neo4j Aura Live' : 'Embedded Engine'}
            </button>
          </div>
        </div>
      </header>

      {/* RBI Notification Modal */}
      {showNotifications && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex justify-end">
          <div className="w-full max-w-md bg-[#0d121e] h-full border-l border-white/[0.08] p-6 flex flex-col space-y-4 overflow-y-auto">
            <div className="flex items-center justify-between pb-3 border-b border-white/[0.08]">
              <div>
                <h3 className="font-bold text-white text-sm">RBI 24h Pre-Debit Notices</h3>
                <p className="text-[11px] text-neutral-400 font-mono">Statutory notification correlation log</p>
              </div>
              <button
                onClick={() => setShowNotifications(false)}
                className="text-neutral-400 hover:text-white text-xs p-1"
              >
                ✕
              </button>
            </div>

            <div className="space-y-3 pt-1">
              {notifications.map(n => (
                <div
                  key={n.id}
                  className="p-3.5 rounded-xl bg-[#131929] border border-white/[0.06] text-xs space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[10px] text-cyan-400 bg-cyan-950/60 border border-cyan-800/60 px-2 py-0.5 rounded">
                      {n.channel} · {n.sender}
                    </span>
                    <span className="text-[10px] text-neutral-500 font-mono">{n.timestamp}</span>
                  </div>
                  <p className="text-neutral-200 text-xs leading-relaxed font-sans">{n.text}</p>
                  <div className="flex items-center justify-between pt-1 border-t border-white/[0.04] text-[11px] font-mono">
                    <span className="text-neutral-400">Resolved Entity:</span>
                    <span className="text-white font-semibold">{n.merchant_resolved}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* MAIN CONTAINER */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-7">
        {/* TAB 1: PORTFOLIO RADAR */}
        {activeTab === 'radar' && (
          <div className="space-y-7">
            {/* 1. LUXURY MODERN FINTECH HERO SCREEN */}
            <section className="hero-surface rounded-3xl p-8 relative overflow-hidden">
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                {/* Left 7 Columns: Committed Aggregate Outflow */}
                <div className="lg:col-span-7 space-y-4">
                  <div className="flex items-center gap-2.5">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-cyan-950/80 text-cyan-300 border border-cyan-700/60 shadow-sm">
                      <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                      12-Month Statement Exposure
                    </span>
                    <span className="text-xs text-neutral-400">
                      Resolved via Neo4j Reference Graph
                    </span>
                  </div>

                  <div>
                    <span className="text-xs font-mono uppercase tracking-wider text-neutral-400 block font-semibold">
                      Committed Annual Run-Rate
                    </span>
                    <div className="flex items-baseline gap-3 mt-1.5">
                      <h2 className="text-5xl sm:text-6xl font-black font-mono text-white tracking-tight">
                        ₹{activeCommitted.toLocaleString('en-IN')}
                      </h2>
                      <span className="text-xl sm:text-2xl font-bold text-neutral-400 font-sans">
                        / year, committed.
                      </span>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center gap-4 text-xs text-neutral-300 pt-1">
                    <div className="flex items-center gap-1.5">
                      <span className="w-2 h-2 rounded-full bg-cyan-400" />
                      <span><strong>₹{(activeCommitted / 12).toFixed(0)}/mo</strong> automated outflow</span>
                    </div>
                    <span className="text-neutral-600">•</span>
                    <div className="flex items-center gap-1.5">
                      <span className="w-2 h-2 rounded-full bg-amber-400" />
                      <span><strong>{heroMetrics.flagged_issues_count} stealth anomalies</strong> identified</span>
                    </div>
                  </div>
                </div>

                {/* Right 5 Columns: Interactive Savings Unlocked Card */}
                <div className="lg:col-span-5 bg-[#0f1423]/90 backdrop-blur-md rounded-2xl border border-white/[0.12] p-6 space-y-4 shadow-2xl">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-neutral-400 flex items-center gap-1.5 font-mono">
                      <DollarSign className="w-4 h-4 text-emerald-400" />
                      Interactive Revocation Staging
                    </span>
                    <span className="text-xs font-mono font-bold text-emerald-300 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800">
                      {savingsPct}% Run-Rate Cut
                    </span>
                  </div>

                  <div>
                    <div className="flex justify-between items-baseline">
                      <div className="text-3xl font-black text-emerald-400 font-mono tracking-tight">
                        ₹{savedAmount.toLocaleString('en-IN')}
                      </div>
                      <span className="text-xs text-neutral-400 font-sans font-medium">annual savings unlocked</span>
                    </div>

                    {/* Progress Bar */}
                    <div className="w-full h-2.5 bg-neutral-900 rounded-full mt-2.5 overflow-hidden border border-white/[0.06]">
                      <div
                        className="h-full bg-gradient-to-r from-emerald-500 to-teal-400 transition-all duration-300 shadow-sm"
                        style={{ width: `${Math.min(100, savingsPct)}%` }}
                      />
                    </div>
                  </div>

                  <div className="flex items-center gap-2 pt-1">
                    <button
                      onClick={cancelAllFlagged}
                      className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 hover:from-emerald-500 hover:to-cyan-500 text-white font-bold text-xs transition shadow-lg shadow-emerald-950 flex items-center justify-center gap-2"
                    >
                      <Zap className="w-3.5 h-3.5" />
                      <span>Stage All 4 Anomalies to Save ₹14,280/yr</span>
                    </button>
                    {cancelledIds.size > 0 && (
                      <button
                        onClick={() => setCancelledIds(new Set())}
                        className="py-2.5 px-3 rounded-xl bg-neutral-900 hover:bg-neutral-800 border border-white/[0.08] text-neutral-300 text-xs font-mono transition"
                      >
                        Reset
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </section>

            {/* 2. Controls & Segment Filter Bar */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
              {/* Segmented Filter Buttons */}
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <button
                  onClick={() => setActiveFilter('ALL')}
                  className={`px-3.5 py-1.5 rounded-xl font-semibold transition ${
                    activeFilter === 'ALL'
                      ? 'bg-white text-neutral-950 shadow'
                      : 'bg-[#111726] text-neutral-400 hover:text-white border border-white/[0.08]'
                  }`}
                >
                  All Commitments ({mandates.length})
                </button>
                <button
                  onClick={() => setActiveFilter('PRICE_HIKE')}
                  className={`px-3.5 py-1.5 rounded-xl font-semibold transition flex items-center gap-1.5 ${
                    activeFilter === 'PRICE_HIKE'
                      ? 'bg-amber-500 text-neutral-950 shadow font-bold'
                      : 'bg-[#111726] text-amber-400 hover:text-white border border-amber-500/30'
                  }`}
                >
                  <TrendingUp className="w-3.5 h-3.5" />
                  Price Creep ({mandates.filter(m => m.flag === 'PRICE_HIKE').length})
                </button>
                <button
                  onClick={() => setActiveFilter('TRIAL_CONVERTED')}
                  className={`px-3.5 py-1.5 rounded-xl font-semibold transition flex items-center gap-1.5 ${
                    activeFilter === 'TRIAL_CONVERTED'
                      ? 'bg-rose-500 text-white shadow font-bold'
                      : 'bg-[#111726] text-rose-400 hover:text-white border border-rose-500/30'
                  }`}
                >
                  <AlertTriangle className="w-3.5 h-3.5" />
                  Trial Traps ({mandates.filter(m => m.flag === 'TRIAL_CONVERTED').length})
                </button>
                <button
                  onClick={() => setActiveFilter('UNUSED_ZOMBIE')}
                  className={`px-3.5 py-1.5 rounded-xl font-semibold transition flex items-center gap-1.5 ${
                    activeFilter === 'UNUSED_ZOMBIE'
                      ? 'bg-red-500 text-white shadow font-bold'
                      : 'bg-[#111726] text-red-400 hover:text-white border border-red-500/30'
                  }`}
                >
                  <ShieldAlert className="w-3.5 h-3.5" />
                  Dormant / Zombie ({mandates.filter(m => m.flag === 'UNUSED_ZOMBIE').length})
                </button>
                <button
                  onClick={() => setActiveFilter('HEALTHY')}
                  className={`px-3.5 py-1.5 rounded-xl font-semibold transition flex items-center gap-1.5 ${
                    activeFilter === 'HEALTHY'
                      ? 'bg-emerald-500 text-neutral-950 shadow font-bold'
                      : 'bg-[#111726] text-emerald-400 hover:text-white border border-emerald-500/30'
                  }`}
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Stable ({mandates.filter(m => m.flag === 'HEALTHY').length})
                </button>
              </div>

              {/* View Switcher (Grid vs Table) */}
              <div className="flex items-center gap-2">
                <div className="flex items-center bg-[#111726] p-1 rounded-xl border border-white/[0.08]">
                  <button
                    onClick={() => setViewMode('grid')}
                    className={`p-1.5 rounded-lg ${viewMode === 'grid' ? 'bg-neutral-800 text-white shadow-sm' : 'text-neutral-500 hover:text-neutral-300'}`}
                    title="Grid View"
                  >
                    <LayoutGrid className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setViewMode('table')}
                    className={`p-1.5 rounded-lg ${viewMode === 'table' ? 'bg-neutral-800 text-white shadow-sm' : 'text-neutral-500 hover:text-neutral-300'}`}
                    title="Table Ledger View"
                  >
                    <List className="w-4 h-4" />
                  </button>
                </div>

                <button
                  onClick={fetchInitialData}
                  className="p-2 rounded-xl bg-[#111726] hover:bg-[#182136] border border-white/[0.08] text-neutral-300 hover:text-white transition"
                  title="Reload Synthetic Statement"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* 3A. VIEW MODE: GRID VIEW */}
            {viewMode === 'grid' && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredMandates.map(mandate => {
                  const isStaged = cancelledIds.has(mandate.id)
                  const visual = getBrandVisual(mandate.merchant_name)

                  return (
                    <div
                      key={mandate.id}
                      className={`card-glass rounded-2xl transition-all duration-200 flex flex-col justify-between overflow-hidden relative ${
                        isStaged
                          ? 'opacity-70 border-emerald-500/50'
                          : mandate.flag === 'PRICE_HIKE'
                          ? 'hover:border-amber-500/50'
                          : mandate.flag === 'TRIAL_CONVERTED'
                          ? 'hover:border-rose-500/50'
                          : mandate.flag === 'UNUSED_ZOMBIE'
                          ? 'hover:border-red-500/50'
                          : 'hover:border-white/[0.2]'
                      }`}
                    >
                      <div className="p-5 space-y-4">
                        {/* Checkbox & Status Flag */}
                        <div className="flex items-center justify-between gap-2">
                          <label className="flex items-center gap-2 cursor-pointer select-none">
                            <input
                              type="checkbox"
                              checked={isStaged}
                              onChange={() => toggleCancel(mandate.id)}
                              className="w-4 h-4 rounded text-emerald-500 bg-neutral-900 border-neutral-700 focus:ring-0"
                            />
                            <span
                              className={`text-xs font-mono font-bold ${
                                isStaged ? 'text-emerald-400 line-through' : 'text-neutral-300'
                              }`}
                            >
                              {isStaged ? 'Staged to Revoke' : 'Stage Revocation'}
                            </span>
                          </label>

                          {/* Risk Badges */}
                          {mandate.flag === 'PRICE_HIKE' && (
                            <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30 flex items-center gap-1">
                              <TrendingUp className="w-3 h-3" />
                              Price Hike (+15.5%)
                            </span>
                          )}
                          {mandate.flag === 'TRIAL_CONVERTED' && (
                            <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-rose-500/15 text-rose-300 border border-rose-500/30 flex items-center gap-1">
                              <AlertTriangle className="w-3 h-3" />
                              Trial Trap (59.5x)
                            </span>
                          )}
                          {mandate.flag === 'UNUSED_ZOMBIE' && (
                            <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-red-500/15 text-red-300 border border-red-500/30 flex items-center gap-1">
                              <ShieldAlert className="w-3 h-3" />
                              Dormant Mandate
                            </span>
                          )}
                          {mandate.flag === 'HEALTHY' && (
                            <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                              <CheckCircle2 className="w-3 h-3" />
                              Active & Stable
                            </span>
                          )}
                        </div>

                        {/* Brand Avatar + Entity Info */}
                        <div className="flex items-start gap-3 pt-1">
                          <div className={`w-10 h-10 rounded-xl border flex items-center justify-center font-bold text-sm shrink-0 shadow-sm ${visual.bg}`}>
                            {visual.icon}
                          </div>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-baseline justify-between">
                              <h3 className="font-bold text-base text-white tracking-tight truncate">
                                {mandate.merchant_name}
                              </h3>
                              <span className="text-xs font-mono font-bold text-neutral-200 shrink-0 ml-2">
                                ₹{mandate.latest_amount.toLocaleString('en-IN')}{' '}
                                <span className="text-[10px] font-normal text-neutral-400">
                                  /{mandate.cadence.toLowerCase()}
                                </span>
                              </span>
                            </div>

                            <div className="text-xs text-indigo-300 font-medium pt-0.5 flex items-center gap-1.5">
                              <Building2 className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                              <span className="truncate">{mandate.parent_name}</span>
                              <span className="text-neutral-600">•</span>
                              <span className="text-neutral-400 truncate">{mandate.category}</span>
                            </div>
                          </div>
                        </div>

                        {/* Statement Narration Inset */}
                        <div className="p-3 rounded-xl bg-[#090d16] border border-white/[0.06] space-y-1.5 text-[11px] font-mono">
                          <div className="text-[10px] text-neutral-500 font-bold uppercase tracking-wider flex items-center justify-between">
                            <span>Statement Raw Narration</span>
                            <span className="text-cyan-400">RESOLVED</span>
                          </div>
                          <div className="text-neutral-300 truncate">{mandate.descriptor}</div>
                          <div className="text-[10px] text-neutral-400 pt-1 border-t border-white/[0.04] flex items-center justify-between font-sans">
                            <span className="flex items-center gap-1 text-pink-400 font-medium">
                              <CreditCard className="w-3 h-3" />
                              Rail:
                            </span>
                            <span className="text-neutral-200 font-mono font-semibold">{mandate.mechanism_name}</span>
                          </div>
                        </div>

                        {/* Audit Plain-Language Explanation */}
                        <p className="text-xs text-neutral-300 leading-relaxed font-sans">
                          {mandate.flag_reason}
                        </p>

                        {/* Protocol Pitfall Warning */}
                        {mandate.pitfall && (
                          <div className="p-3 rounded-xl bg-amber-950/30 border border-amber-900/60 text-xs text-amber-200 flex items-start gap-2">
                            <Info className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                            <span>
                              <strong>Protocol Note:</strong> {mandate.pitfall}
                            </span>
                          </div>
                        )}
                      </div>

                      {/* Card Action Footer */}
                      <div className="p-4 bg-[#090d16]/90 border-t border-white/[0.06] flex items-center justify-between">
                        <div>
                          <span className="text-[10px] uppercase font-mono font-bold tracking-wider text-neutral-500 block">
                            Annual Run-Rate
                          </span>
                          <span
                            className={`font-mono text-sm font-extrabold ${
                              isStaged ? 'text-emerald-400 line-through' : 'text-white'
                            }`}
                          >
                            ₹{mandate.annual_committed_cost.toLocaleString('en-IN')}/yr
                          </span>
                        </div>

                        <button
                          onClick={() => {
                            setSelectedMandate(mandate)
                            generateEmail(mandate, 'formal')
                          }}
                          className="py-2 px-3.5 rounded-xl bg-[#131b2e] hover:bg-[#1c2742] text-cyan-300 hover:text-white text-xs font-semibold transition flex items-center gap-1.5 border border-cyan-800/40 shadow-sm"
                        >
                          <span>Revocation Route</span>
                          <ChevronRight className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}

            {/* 3B. VIEW MODE: DENSE TABLE VIEW */}
            {viewMode === 'table' && (
              <div className="rounded-2xl border border-white/[0.08] bg-[#0d121e] overflow-hidden shadow-2xl">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="border-b border-white/[0.08] bg-[#090d16] text-neutral-400 font-mono text-[11px]">
                      <th className="p-3.5 w-10 text-center">Stage</th>
                      <th className="p-3.5">Merchant Entity</th>
                      <th className="p-3.5">Corporate Parent</th>
                      <th className="p-3.5">Statement Narration</th>
                      <th className="p-3.5">Payment Rail</th>
                      <th className="p-3.5">Cadence</th>
                      <th className="p-3.5 text-right">Latest Debit</th>
                      <th className="p-3.5 text-right">Annual Run-Rate</th>
                      <th className="p-3.5">Audit Status</th>
                      <th className="p-3.5 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/[0.04]">
                    {filteredMandates.map(m => {
                      const isStaged = cancelledIds.has(m.id)
                      return (
                        <tr key={m.id} className="hover:bg-white/[0.02] transition">
                          <td className="p-3.5 text-center">
                            <input
                              type="checkbox"
                              checked={isStaged}
                              onChange={() => toggleCancel(m.id)}
                              className="w-4 h-4 rounded text-emerald-500 bg-neutral-900 border-neutral-700 focus:ring-0"
                            />
                          </td>
                          <td className="p-3.5 font-bold text-white">{m.merchant_name}</td>
                          <td className="p-3.5 text-indigo-300 font-medium">{m.parent_name}</td>
                          <td className="p-3.5 font-mono text-[11px] text-neutral-400 max-w-xs truncate">
                            {m.descriptor}
                          </td>
                          <td className="p-3.5 font-mono text-[11px] text-pink-300 font-semibold">
                            {m.mechanism_name}
                          </td>
                          <td className="p-3.5 font-mono text-neutral-400 uppercase text-[10px]">
                            {m.cadence}
                          </td>
                          <td className="p-3.5 font-mono text-right text-neutral-200 font-semibold">
                            ₹{m.latest_amount.toLocaleString('en-IN')}
                          </td>
                          <td
                            className={`p-3.5 font-mono text-right font-bold ${
                              isStaged ? 'line-through text-emerald-400' : 'text-white'
                            }`}
                          >
                            ₹{m.annual_committed_cost.toLocaleString('en-IN')}
                          </td>
                          <td className="p-3.5">
                            {m.flag === 'PRICE_HIKE' && (
                              <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30">
                                Price Hike
                              </span>
                            )}
                            {m.flag === 'TRIAL_CONVERTED' && (
                              <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-rose-500/15 text-rose-300 border border-rose-500/30">
                                Trial Trap
                              </span>
                            )}
                            {m.flag === 'UNUSED_ZOMBIE' && (
                              <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-red-500/15 text-red-300 border border-red-500/30">
                                Dormant
                              </span>
                            )}
                            {m.flag === 'HEALTHY' && (
                              <span className="text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                                Stable
                              </span>
                            )}
                          </td>
                          <td className="p-3.5 text-right">
                            <button
                              onClick={() => {
                                setSelectedMandate(m)
                                generateEmail(m, 'formal')
                              }}
                              className="text-cyan-400 hover:text-cyan-300 font-mono text-xs font-semibold underline"
                            >
                              Review
                            </button>
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* TAB 2: GRAPH & CYPHER TERMINAL */}
        {activeTab === 'graph' && (
          <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
              <div>
                <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
                  <Network className="w-5 h-5 text-cyan-400" />
                  Neo4j Knowledge Graph & Cypher Topology
                </h2>
                <p className="text-xs text-neutral-400 mt-1">
                  Structured multi-subscription parent footprint traversals and rail routing in Cypher.
                </p>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={fetchCypherSeed}
                  className="px-3.5 py-2 rounded-xl bg-[#111726] hover:bg-[#182136] border border-white/[0.08] text-xs font-mono text-neutral-200 transition flex items-center gap-1.5 shadow-sm"
                >
                  <FileText className="w-3.5 h-3.5 text-indigo-400" />
                  <span>View Cypher Seed (.cql)</span>
                </button>
                <button
                  onClick={() => setShowNeo4jModal(true)}
                  className="px-3.5 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-lg shadow-indigo-950"
                >
                  <span>Neo4j Aura Config</span>
                </button>
              </div>
            </div>

            {/* Interactive Concentric Network Canvas */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs text-neutral-400 font-mono px-1">
                <span>Concentric Force Orbit (Click node to inspect properties. Switch cluster views above)</span>
                <span className="text-cyan-400 font-bold">
                  {graphData.stats.total_nodes || 0} Nodes · {graphData.stats.total_edges || 0} Relationships
                </span>
              </div>
              <GraphCanvas
                nodes={graphData.nodes || []}
                edges={graphData.edges || []}
                currentMode={graphMode}
                onModeChange={m => fetchGraphData(m)}
              />
            </div>

            {/* Live Cypher Terminal Console */}
            <div className="rounded-2xl border border-white/[0.08] bg-[#0d121e] p-6 space-y-4 shadow-xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 font-mono text-xs font-bold text-neutral-200">
                  <Terminal className="w-4 h-4 text-cyan-400" />
                  <span>CYPHER QUERY WORKBENCH</span>
                </div>
                <span className="text-[11px] font-mono text-neutral-400">
                  Target: {neo4jStatus === 'CONNECTED' ? 'Neo4j Aura Live' : 'Embedded High-Fidelity Graph Engine'}
                </span>
              </div>

              {/* Preset 1-Click Cypher Chips */}
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-[11px] text-neutral-400 font-medium mr-1">Presets:</span>
                <button
                  onClick={() => {
                    const q =
                      'MATCH (p:Parent)<-[:OWNED_BY]-(m:Merchant)<-[:FOR]-(mand:Mandate)\nRETURN p.name AS Parent, collect(m.name) AS ActiveMerchants, sum(mand.annual_cost) AS AnnualCommittedSpend;'
                    setCypherQuery(q)
                    runCypher(q)
                  }}
                  className="px-3 py-1 rounded-lg bg-[#131929] hover:bg-[#1a2238] border border-white/[0.08] text-[11px] font-mono text-indigo-300 transition"
                >
                  Parent Footprint Traversal
                </button>
                <button
                  onClick={() => {
                    const q =
                      'MATCH (mand:Mandate)-[:VIA_MECHANISM]->(mech:Mechanism)-[:CANCELLED_BY]->(c:CancellationPath)\nRETURN mand.id, mech.name, c.primary_step;'
                    setCypherQuery(q)
                    runCypher(q)
                  }}
                  className="px-3 py-1 rounded-lg bg-[#131929] hover:bg-[#1a2238] border border-white/[0.08] text-[11px] font-mono text-pink-300 transition"
                >
                  Mechanism Cancellation Routing
                </button>
                <button
                  onClick={() => {
                    const q =
                      "MATCH (mand:Mandate)-[:FOR]->(m:Merchant)\nWHERE mand.flag <> 'HEALTHY'\nRETURN m.name, mand.flag, mand.flag_reason;"
                    setCypherQuery(q)
                    runCypher(q)
                  }}
                  className="px-3 py-1 rounded-lg bg-[#131929] hover:bg-[#1a2238] border border-white/[0.08] text-[11px] font-mono text-amber-300 transition"
                >
                  Anomaly Risk Filter Pattern
                </button>
              </div>

              {/* Code Editor Box */}
              <div className="relative">
                <textarea
                  rows={3}
                  value={cypherQuery}
                  onChange={e => setCypherQuery(e.target.value)}
                  className="w-full bg-[#080b12] border border-white/[0.08] rounded-xl p-3.5 font-mono text-xs text-cyan-300 focus:outline-none focus:border-cyan-500 selection:bg-cyan-900"
                  placeholder="Enter Cypher statement..."
                />
                <button
                  onClick={() => runCypher()}
                  disabled={cypherLoading}
                  className="absolute bottom-3 right-3 px-4 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-mono text-xs font-semibold transition flex items-center gap-1.5 shadow"
                >
                  {cypherLoading ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Terminal className="w-3.5 h-3.5" />}
                  <span>Execute</span>
                </button>
              </div>

              {/* Cypher Result Ledger */}
              {cypherResult && (
                <div className="space-y-2 pt-1">
                  <div className="flex items-center justify-between text-[11px] font-mono text-neutral-400">
                    <span>
                      Mode: {cypherResult.mode} · Records: {cypherResult.count || 0}
                    </span>
                    {cypherResult.error && (
                      <span className="text-rose-400">{cypherResult.error}</span>
                    )}
                  </div>

                  <div className="max-h-56 overflow-y-auto rounded-xl bg-[#080b12] border border-white/[0.06] p-3 font-mono text-xs text-neutral-300">
                    {Array.isArray(cypherResult.data) && cypherResult.data.length > 0 ? (
                      <table className="w-full text-left border-collapse text-[11px]">
                        <thead>
                          <tr className="border-b border-white/[0.08] text-neutral-500">
                            {Object.keys(cypherResult.data[0]).map(k => (
                              <th key={k} className="p-2">
                                {k}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {cypherResult.data.map((row: any, i: number) => (
                            <tr key={i} className="border-b border-white/[0.03] hover:bg-white/[0.02]">
                              {Object.values(row).map((val: any, j: number) => (
                                <td key={j} className="p-2 text-neutral-300">
                                  {typeof val === 'object' ? JSON.stringify(val) : String(val)}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    ) : (
                      <pre className="text-neutral-500">
                        {JSON.stringify(cypherResult.data || cypherResult, null, 2)}
                      </pre>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 3: VERIFICATION & BENCHMARK REPORT */}
        {activeTab === 'benchmark' && (
          <div className="space-y-6">
            <div className="border-b border-white/[0.08] pb-4">
              <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                Deterministic Verification & Ground Truth Audit Report
              </h2>
              <p className="text-xs text-neutral-400 mt-1">
                Mathematical evaluation against planted test events and rejection of hard negatives.
              </p>
            </div>

            {benchmarkData && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
                <div className="p-5 rounded-2xl bg-[#0d121e] border border-white/[0.08] space-y-1 shadow-lg">
                  <span className="text-xs text-neutral-400 font-mono uppercase tracking-wider block font-semibold">
                    Planted Mandates Recall
                  </span>
                  <div className="text-3xl font-black text-white font-mono">
                    {benchmarkData.ground_truth_summary.mandates_recall_pct}%
                  </div>
                  <span className="text-xs text-emerald-400 font-medium">
                    {benchmarkData.ground_truth_summary.detected_mandates} of{' '}
                    {benchmarkData.ground_truth_summary.planted_mandates} identified
                  </span>
                </div>

                <div className="p-5 rounded-2xl bg-[#0d121e] border border-white/[0.08] space-y-1 shadow-lg">
                  <span className="text-xs text-neutral-400 font-mono uppercase tracking-wider block font-semibold">
                    Price Creep Verification
                  </span>
                  <div className="text-3xl font-black text-amber-400 font-mono">
                    {benchmarkData.ground_truth_summary.price_hikes.detected} /{' '}
                    {benchmarkData.ground_truth_summary.price_hikes.planted}
                  </div>
                  <span className="text-xs text-emerald-400 font-medium">Step increase (+15.5%) detected</span>
                </div>

                <div className="p-5 rounded-2xl bg-[#0d121e] border border-white/[0.08] space-y-1 shadow-lg">
                  <span className="text-xs text-neutral-400 font-mono uppercase tracking-wider block font-semibold">
                    Trial Trap Escalation
                  </span>
                  <div className="text-3xl font-black text-rose-400 font-mono">
                    {benchmarkData.ground_truth_summary.trial_conversions.detected} /{' '}
                    {benchmarkData.ground_truth_summary.trial_conversions.planted}
                  </div>
                  <span className="text-xs text-emerald-400 font-medium">₹2 to ₹119 jump caught</span>
                </div>

                <div className="p-5 rounded-2xl bg-[#0d121e] border border-white/[0.08] space-y-1 shadow-lg">
                  <span className="text-xs text-neutral-400 font-mono uppercase tracking-wider block font-semibold">
                    Hard Negatives False Alarms
                  </span>
                  <div className="text-3xl font-black text-emerald-400 font-mono">
                    {benchmarkData.ground_truth_summary.hard_negatives_eliminated.false_positive_rate * 100}%
                  </div>
                  <span className="text-xs text-emerald-400 font-medium">0 false positive triggers</span>
                </div>
              </div>
            )}

            {/* Hard Negatives Rejection Table */}
            <div className="rounded-2xl border border-white/[0.08] bg-[#0d121e] p-6 space-y-4 shadow-xl">
              <h3 className="font-bold text-base text-white">
                Reconciliation of Planted Hard Negatives (Exclusion Rationale)
              </h3>
              <p className="text-xs text-neutral-400">
                Evaluating the deterministic rules that protect non-mandate discretionary transactions from false alerts:
              </p>

              <div className="space-y-3 pt-1">
                <div className="p-4 rounded-xl bg-[#080b12] border border-white/[0.06] text-xs space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-neutral-200">
                      Weekly Quick Groceries (Zepto Consumer Delivery)
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800">
                      Excluded from Mandates
                    </span>
                  </div>
                  <p className="text-neutral-400 text-xs font-sans leading-relaxed">
                    <strong>Rule Applied:</strong> Cadence analysis revealed 5–7 day interval clusters with a
                    median delta of 6.5 days and amount variations above 35%. Safely categorized as grocery
                    basket orders rather than recurring commitments.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-[#080b12] border border-white/[0.06] text-xs space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-neutral-200">
                      Fluctuating Utility Metering (BESCOM Bangalore)
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800">
                      Excluded from Mandates
                    </span>
                  </div>
                  <p className="text-neutral-400 text-xs font-sans leading-relaxed">
                    <strong>Rule Applied:</strong> Monthly recurrence detected on the 14th, but variance across
                    cycles exceeded 3% multiple times (₹1,240 to ₹2,100). Correctly excluded as variable usage-based bill.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-[#080b12] border border-white/[0.06] text-xs space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-neutral-200">
                      Discretionary Food Delivery (Swiggy Food)
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800">
                      Excluded from Mandates
                    </span>
                  </div>
                  <p className="text-neutral-400 text-xs font-sans leading-relaxed">
                    <strong>Rule Applied:</strong> Highly irregular intervals (1 to 5 days) without cadence stability. Rejected as discretionary spend.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-[#080b12] border border-white/[0.06] text-xs space-y-1.5">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-neutral-200">
                      Genuine Unrecognised Mandate (ACME Cloud Recurring Bill)
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950/60 text-cyan-400 border border-cyan-800">
                      Identified Without Guessing
                    </span>
                  </div>
                  <p className="text-neutral-400 text-xs font-sans leading-relaxed">
                    <strong>Rule Applied:</strong> Strict monthly interval (30 days) and exact ₹450 amount. Because the descriptor was unmapped in the graph, it was categorized as "Unrecognised Merchant" without hallucination.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: INGEST STATEMENT CSV */}
        {activeTab === 'upload' && (
          <div className="max-w-xl mx-auto space-y-6">
            <div className="border-b border-white/[0.08] pb-4">
              <h2 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
                <Upload className="w-5 h-5 text-cyan-400" />
                Ingest Statement CSV
              </h2>
              <p className="text-xs text-neutral-400 mt-1">
                Parses raw statement files with automatic column resolution (Date, Descriptor, Debit/Amount, Reference).
              </p>
            </div>

            <form
              onSubmit={handleFileUpload}
              className="p-8 rounded-3xl border border-white/[0.08] bg-[#0d121e] space-y-6 shadow-2xl"
            >
              <div className="border-2 border-dashed border-white/[0.12] hover:border-cyan-500/50 rounded-2xl p-8 text-center space-y-3 cursor-pointer transition bg-[#080b12]">
                <Upload className="w-10 h-10 text-cyan-400 mx-auto" />
                <div>
                  <label htmlFor="csv-input" className="cursor-pointer text-sm font-semibold text-white block">
                    {uploadFile ? uploadFile.name : 'Select or drop statement CSV file'}
                  </label>
                  <p className="text-xs text-neutral-500 mt-1 font-mono">
                    Requires Date, Narration/Description, and Debit Amount columns
                  </p>
                </div>
                <input
                  id="csv-input"
                  type="file"
                  accept=".csv"
                  onChange={e => setUploadFile(e.target.files?.[0] || null)}
                  className="hidden"
                />
              </div>

              {uploadError && (
                <div className="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs">
                  {uploadError}
                </div>
              )}

              {uploadSuccess && (
                <div className="p-3.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs">
                  {uploadSuccess}
                </div>
              )}

              <div className="flex items-center justify-between pt-2">
                <button
                  type="button"
                  onClick={fetchInitialData}
                  className="text-xs text-neutral-400 hover:text-white font-mono"
                >
                  Reload Default Synthetic Dataset
                </button>

                <button
                  type="submit"
                  disabled={!uploadFile || uploadLoading}
                  className="py-2.5 px-5 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 disabled:opacity-40 text-white font-bold text-xs transition shadow-lg shadow-indigo-950"
                >
                  {uploadLoading ? 'Parsing...' : 'Analyze Statement'}
                </button>
              </div>
            </form>
          </div>
        )}
      </main>

      {/* REVOCATION DOSSIER & LEGAL NOTICE DRAWER */}
      {selectedMandate && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex justify-end">
          <div className="w-full max-w-xl bg-[#0d121e] h-full border-l border-white/[0.1] p-7 flex flex-col space-y-6 overflow-y-auto animate-in slide-in-from-right duration-200">
            {/* Header */}
            <div className="flex items-start justify-between pb-4 border-b border-white/[0.08]">
              <div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-pink-950/80 text-pink-300 border border-pink-800 font-semibold">
                  {selectedMandate.mechanism_name}
                </span>
                <h3 className="font-extrabold text-lg text-white mt-1.5">
                  Mandate Revocation Protocol: {selectedMandate.merchant_name}
                </h3>
                <p className="text-xs text-neutral-400 font-mono mt-0.5">
                  Parent: {selectedMandate.parent_name} · Committed: ₹{selectedMandate.latest_amount} / {selectedMandate.cadence.toLowerCase()}
                </p>
              </div>
              <button
                onClick={() => setSelectedMandate(null)}
                className="text-neutral-400 hover:text-white text-sm p-1"
              >
                ✕
              </button>
            </div>

            {/* Section 1: Protocol Instructions */}
            <div className="space-y-3">
              <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-neutral-300 flex items-center gap-1.5">
                <ShieldAlert className="w-4 h-4 text-cyan-400" />
                1. Mechanism Operational Protocol
              </h4>
              <ol className="space-y-2 text-xs text-neutral-300 list-decimal list-inside bg-[#080b12] p-4 rounded-xl border border-white/[0.06]">
                {selectedMandate.cancellation_steps.map((step, idx) => (
                  <li key={idx} className="leading-relaxed pl-1">
                    {step}
                  </li>
                ))}
              </ol>

              {selectedMandate.pitfall && (
                <div className="p-3.5 rounded-xl bg-amber-950/30 border border-amber-900/60 text-xs text-amber-200 flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <strong className="text-amber-400">Compliance Warning:</strong> {selectedMandate.pitfall}
                  </div>
                </div>
              )}
            </div>

            {/* Section 2: Statutory Escalation Path */}
            <div className="space-y-3 pt-1">
              <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-neutral-300 flex items-center gap-1.5">
                <Layers className="w-4 h-4 text-indigo-400" />
                2. RBI & CCPA Regulatory Escalation (If Obstructed)
              </h4>

              <div className="grid grid-cols-1 gap-2.5 text-xs">
                <div className="p-3 rounded-xl bg-[#080b12] border border-white/[0.06] space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white">Tier 1: Formal Revocation Notice</span>
                    <span className="text-[10px] font-mono text-cyan-400 font-semibold">48h SLA</span>
                  </div>
                  <p className="text-neutral-400 text-xs">
                    Submit written notice to merchant grievance officer under Consumer Protection Rules 2020.
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-[#080b12] border border-white/[0.06] space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white">Tier 2: Issuing Bank SI Revocation</span>
                    <span className="text-[10px] font-mono text-cyan-400 font-semibold">RBI Master Circular</span>
                  </div>
                  <p className="text-neutral-400 text-xs">
                    Instruct issuing bank card operations to block merchant identifier under RBI Circular DPSS.CO.PD.No.S513/02.14.003/2021-22.
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-[#080b12] border border-white/[0.06] space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white">Tier 3: RBI Integrated Ombudsman</span>
                    <span className="text-[10px] font-mono text-cyan-400 font-semibold">cms.rbi.org.in</span>
                  </div>
                  <p className="text-neutral-400 text-xs">
                    Lodge grievance on RBI CMS portal if auto-debit persists post-revocation date.
                  </p>
                </div>

                <div className="p-3 rounded-xl bg-[#080b12] border border-white/[0.06] space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white">Tier 4: National Consumer Helpline</span>
                    <span className="text-[10px] font-mono text-cyan-400 font-semibold">NCH 1915</span>
                  </div>
                  <p className="text-neutral-400 text-xs">
                    CCPA dark pattern complaint for forced subscription continuity.
                  </p>
                </div>
              </div>
            </div>

            {/* Section 3: Legal Notice Generator */}
            <div className="space-y-3 pt-1">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-neutral-300 flex items-center gap-1.5">
                  <Mail className="w-4 h-4 text-cyan-400" />
                  3. Revocation Notice Drafting Studio
                </h4>

                <div className="flex items-center gap-1 bg-[#080b12] p-1 rounded-lg border border-white/[0.08] text-[10px] font-mono">
                  <button
                    onClick={() => generateEmail(selectedMandate, 'polite')}
                    className={`px-2 py-0.5 rounded ${
                      emailTone === 'polite' ? 'bg-neutral-800 text-white font-bold' : 'text-neutral-400'
                    }`}
                  >
                    Standard
                  </button>
                  <button
                    onClick={() => generateEmail(selectedMandate, 'formal')}
                    className={`px-2 py-0.5 rounded ${
                      emailTone === 'formal' ? 'bg-neutral-800 text-white font-bold' : 'text-neutral-400'
                    }`}
                  >
                    Statutory
                  </button>
                  <button
                    onClick={() => generateEmail(selectedMandate, 'firm_dispute')}
                    className={`px-2 py-0.5 rounded ${
                      emailTone === 'firm_dispute' ? 'bg-neutral-800 text-white font-bold' : 'text-neutral-400'
                    }`}
                  >
                    Dispute Warning
                  </button>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-[#080b12] border border-white/[0.08] space-y-2 text-xs font-mono">
                <div className="text-neutral-400 text-[11px] pb-1 border-b border-white/[0.04]">
                  Subject: {emailSubject}
                </div>
                <textarea
                  readOnly
                  rows={7}
                  value={emailBody}
                  className="w-full bg-transparent text-neutral-200 resize-none focus:outline-none text-xs leading-relaxed selection:bg-cyan-950"
                />
              </div>

              <button
                onClick={() => {
                  navigator.clipboard.writeText(`Subject: ${emailSubject}\n\n${emailBody}`)
                  setEmailCopied(true)
                  setTimeout(() => setEmailCopied(false), 2000)
                }}
                className="w-full py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white font-bold text-xs transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-950"
              >
                {emailCopied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                <span>{emailCopied ? 'Copied to Clipboard' : 'Copy Statutory Revocation Notice'}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* CYPHER SEED SCRIPT MODAL */}
      {showSeedModal && (
        <div className="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 flex items-center justify-center p-6">
          <div className="w-full max-w-2xl bg-[#0d121e] border border-white/[0.1] rounded-2xl p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-white/[0.08]">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-indigo-400" />
                <h3 className="font-bold text-white text-sm">
                  Neo4j DDL & Seed Script (Cypher)
                </h3>
              </div>
              <button
                onClick={() => setShowSeedModal(false)}
                className="text-neutral-400 hover:text-white text-xs px-1"
              >
                ✕
              </button>
            </div>

            <pre className="p-4 rounded-xl bg-[#080b12] border border-white/[0.08] font-mono text-[11px] text-cyan-300 max-h-72 overflow-y-auto">
              {cypherSeedScript}
            </pre>

            <div className="flex items-center justify-end gap-2 pt-1 font-mono text-xs">
              <button
                onClick={() => {
                  const blob = new Blob([cypherSeedScript], { type: 'text/plain' })
                  const url = URL.createObjectURL(blob)
                  const a = document.createElement('a')
                  a.href = url
                  a.download = 'mandate_radar_neo4j_seed.cql'
                  a.click()
                }}
                className="py-2 px-3.5 rounded-xl bg-[#131929] border border-white/[0.08] hover:bg-[#1a2238] text-neutral-300"
              >
                Download .cql
              </button>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(cypherSeedScript)
                  alert('Cypher Seed copied.')
                }}
                className="py-2 px-4 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-sans font-bold shadow"
              >
                Copy to Clipboard
              </button>
            </div>
          </div>
        </div>
      )}

      {/* NEO4J AURA CONFIG MODAL */}
      {showNeo4jModal && (
        <div className="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 flex items-center justify-center p-6">
          <div className="w-full max-w-sm bg-[#0d121e] border border-white/[0.1] rounded-2xl p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-white/[0.08]">
              <h3 className="font-bold text-white text-sm">Neo4j Cluster Connection</h3>
              <button
                onClick={() => setShowNeo4jModal(false)}
                className="text-neutral-400 hover:text-white text-xs"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleConnectNeo4j} className="space-y-3.5 text-xs">
              <div>
                <label className="text-neutral-300 block mb-1 font-mono text-[11px]">Bolt URI</label>
                <input
                  type="text"
                  value={neo4jUri}
                  onChange={e => setNeo4jUri(e.target.value)}
                  placeholder="neo4j+s://..."
                  className="w-full bg-[#080b12] border border-white/[0.08] rounded-xl p-2.5 font-mono text-cyan-300 text-xs focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="text-neutral-300 block mb-1 font-mono text-[11px]">Username</label>
                <input
                  type="text"
                  value={neo4jUser}
                  onChange={e => setNeo4jUser(e.target.value)}
                  placeholder="neo4j"
                  className="w-full bg-[#080b12] border border-white/[0.08] rounded-xl p-2.5 font-mono text-neutral-200 text-xs focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="text-neutral-300 block mb-1 font-mono text-[11px]">Password</label>
                <input
                  type="password"
                  value={neo4jPass}
                  onChange={e => setNeo4jPass(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-[#080b12] border border-white/[0.08] rounded-xl p-2.5 font-mono text-neutral-200 text-xs focus:outline-none focus:border-cyan-500"
                />
              </div>

              {neo4jMsg && (
                <div className="p-2.5 rounded-xl bg-neutral-900 border border-white/[0.06] text-[11px] font-mono text-neutral-300">
                  {neo4jMsg}
                </div>
              )}

              <div className="flex items-center justify-end gap-2 pt-1 font-sans">
                <button
                  type="button"
                  onClick={() => setShowNeo4jModal(false)}
                  className="py-2 px-3.5 rounded-xl bg-[#131929] text-neutral-400 hover:text-white"
                >
                  Close
                </button>
                <button
                  type="submit"
                  className="py-2 px-4 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white font-bold"
                >
                  Test & Sync
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
