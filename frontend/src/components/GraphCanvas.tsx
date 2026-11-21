import React, { useRef, useEffect, useState, useMemo } from 'react'
import {
  Search,
  ZoomIn,
  ZoomOut,
  Sparkles,
  Terminal,
  Copy,
  Check,
  ArrowRight
} from 'lucide-react'

export interface GraphNode {
  id: string
  label: string
  name: string
  group: string
  color: string
  val: number
  properties?: Record<string, any>
  x?: number
  y?: number
  vx?: number
  vy?: number
  cluster?: string
}

export interface GraphEdge {
  id: string
  source: string | GraphNode
  target: string | GraphNode
  type: string
  label: string
  color: string
  sourceObj?: GraphNode
  targetObj?: GraphNode
}

interface GraphCanvasProps {
  nodes: GraphNode[]
  edges: GraphEdge[]
  onNodeClick?: (node: GraphNode) => void
  currentMode?: string
  onModeChange?: (mode: string) => void
  onExecuteCypher?: (query: string) => void
}

export const GraphCanvas: React.FC<GraphCanvasProps> = ({
  nodes,
  edges,
  onNodeClick,
  currentMode = 'portfolio',
  onModeChange,
  onExecuteCypher
}) => {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null)
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [copiedCypher, setCopiedCypher] = useState(false)
  const [transform, setTransform] = useState({ x: 0, y: 0, scale: 0.95 })
  const [dimensions, setDimensions] = useState({ width: 1100, height: 600 })
  const [activeLegendFilter, setActiveLegendFilter] = useState<string | null>(null)

  const isDraggingRef = useRef(false)
  const dragStartRef = useRef({ x: 0, y: 0 })
  const draggedNodeRef = useRef<GraphNode | null>(null)

  const simNodesRef = useRef<GraphNode[]>([])
  const simEdgesRef = useRef<GraphEdge[]>([])
  const animFrameIdRef = useRef<number | null>(null)

  // Measure container dimensions dynamically so canvas never stretches or distorts
  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        const { clientWidth, clientHeight } = containerRef.current
        setDimensions({
          width: clientWidth || 1100,
          height: clientHeight || 600
        })
      }
    }
    updateSize()
    window.addEventListener('resize', updateSize)
    return () => window.removeEventListener('resize', updateSize)
  }, [])

  // Initialize Force Simulation with Clustered & Concentric Orbital Layouts
  useEffect(() => {
    const { width, height } = dimensions
    const cx = width / 2
    const cy = height / 2

    const nodeMap = new Map<string, GraphNode>()

    // Determine cluster centers for the 270-node catalog view
    const clusterCenters: Record<string, { x: number; y: number }> = {
      alphabet: { x: cx - 280, y: cy - 140 },
      amazon: { x: cx + 280, y: cy - 140 },
      streaming: { x: cx - 260, y: cy + 150 },
      productivity: { x: cx + 260, y: cy + 150 },
      telecom: { x: cx, y: cy + 220 },
      mechanisms: { x: cx + 380, y: cy },
      user: { x: cx, y: cy }
    }

    const initNodes: GraphNode[] = nodes.map(n => {
      let x = cx
      let y = cy

      if (currentMode === 'portfolio') {
        // High-end Concentric Orbital Layout for User Portfolio
        if (n.group === 'person') {
          x = cx
          y = cy
        } else if (n.group === 'mandate') {
          const angle = Math.random() * 2 * Math.PI
          const r = 120 + Math.random() * 25
          x = cx + Math.cos(angle) * r
          y = cy + Math.sin(angle) * r
        } else if (n.group === 'merchant') {
          const angle = Math.random() * 2 * Math.PI
          const r = 210 + Math.random() * 30
          x = cx + Math.cos(angle) * r
          y = cy + Math.sin(angle) * r
        } else if (n.group === 'parent') {
          const angle = Math.random() * 2 * Math.PI
          const r = 310 + Math.random() * 35
          x = cx + Math.cos(angle) * r
          y = cy + Math.sin(angle) * r
        } else if (n.group === 'mechanism') {
          const angle = Math.random() * 2 * Math.PI
          const r = 290 + Math.random() * 30
          x = cx + Math.cos(angle) * r
          y = cy + Math.sin(angle) * r
        } else {
          const angle = Math.random() * 2 * Math.PI
          const r = 240 + Math.random() * 40
          x = cx + Math.cos(angle) * r
          y = cy + Math.sin(angle) * r
        }
      } else {
        // Clustered Constellation Layout for Subgraphs & Full Catalog
        let center = { x: cx, y: cy }
        const nameLower = (n.name || '').toLowerCase()

        if (n.group === 'person' || n.group === 'mandate') {
          center = clusterCenters.user
        } else if (nameLower.includes('google') || nameLower.includes('alphabet') || nameLower.includes('youtube')) {
          center = clusterCenters.alphabet
        } else if (nameLower.includes('amazon') || nameLower.includes('kindle') || nameLower.includes('audible') || nameLower.includes('aws')) {
          center = clusterCenters.amazon
        } else if (nameLower.includes('netflix') || nameLower.includes('hotstar') || nameLower.includes('spotify') || nameLower.includes('cinema')) {
          center = clusterCenters.streaming
        } else if (n.group === 'mechanism') {
          center = clusterCenters.mechanisms
        } else {
          center = clusterCenters.productivity
        }

        const angle = Math.random() * 2 * Math.PI
        const spread = n.group === 'parent' ? 20 : n.group === 'mechanism' ? 40 : 75 + Math.random() * 60
        x = center.x + Math.cos(angle) * spread
        y = center.y + Math.sin(angle) * spread
      }

      // Base radius calculation for node sizing
      let val = 14
      if (n.group === 'person') val = 24
      else if (n.group === 'parent') val = 20
      else if (n.group === 'mechanism') val = 17
      else if (n.group === 'merchant') val = 15
      else if (n.group === 'mandate') val = 13

      const cloned: GraphNode = {
        ...n,
        x,
        y,
        vx: 0,
        vy: 0,
        val
      }
      nodeMap.set(n.id, cloned)
      return cloned
    })

    const initEdges = edges.map(e => ({
      ...e,
      sourceObj: nodeMap.get(typeof e.source === 'string' ? e.source : e.source.id),
      targetObj: nodeMap.get(typeof e.target === 'string' ? e.target : e.target.id)
    }))

    simNodesRef.current = initNodes
    simEdgesRef.current = initEdges as any

    let alpha = 1.0
    const decay = 0.991

    const runSimulation = () => {
      const currentNodes = simNodesRef.current
      const currentEdges = simEdgesRef.current as any[]

      if (alpha > 0.005) {
        // 1. Strict Collision Clearance (Guarantees zero overlapping circles)
        for (let i = 0; i < currentNodes.length; i++) {
          for (let j = i + 1; j < currentNodes.length; j++) {
            const n1 = currentNodes[i]
            const n2 = currentNodes[j]
            const dx = (n2.x || 0) - (n1.x || 0)
            const dy = (n2.y || 0) - (n1.y || 0)
            const dist = Math.sqrt(dx * dx + dy * dy) || 1
            const minAllowedDist = (n1.val + n2.val) + 36 // Generous margin

            if (dist < minAllowedDist) {
              const overlap = (minAllowedDist - dist) / dist * 0.5 * alpha
              const fx = dx * overlap
              const fy = dy * overlap
              if (n1.group !== 'person') {
                n1.vx = (n1.vx || 0) - fx
                n1.vy = (n1.vy || 0) - fy
              }
              if (n2.group !== 'person') {
                n2.vx = (n2.vx || 0) + fx
                n2.vy = (n2.vy || 0) + fy
              }
            }
          }
        }

        // 2. Spring Forces Along Relationships
        for (const edge of currentEdges) {
          const s = edge.sourceObj
          const t = edge.targetObj
          if (s && t) {
            const dx = (t.x || 0) - (s.x || 0)
            const dy = (t.y || 0) - (s.y || 0)
            const dist = Math.sqrt(dx * dx + dy * dy) || 1
            const targetDist = currentMode === 'portfolio' ? 88 : 72
            const force = (dist - targetDist) * 0.032 * alpha
            const fx = (dx / dist) * force
            const fy = (dy / dist) * force

            if (s.group !== 'person') {
              s.vx = (s.vx || 0) + fx
              s.vy = (s.vy || 0) + fy
            }
            if (t.group !== 'person') {
              t.vx = (t.vx || 0) - fx
              t.vy = (t.vy || 0) - fy
            }
          }
        }

        // 3. Gentle Centering Gravity
        for (const n of currentNodes) {
          if (n !== draggedNodeRef.current && n.group !== 'person') {
            n.vx = ((n.vx || 0) + (cx - (n.x || 0)) * 0.0025 * alpha) * 0.85
            n.vy = ((n.vy || 0) + (cy - (n.y || 0)) * 0.0025 * alpha) * 0.85
            n.x = (n.x || 0) + (n.vx || 0)
            n.y = (n.y || 0) + (n.vy || 0)
          }
        }

        alpha *= decay
      }

      drawCanvas()
      animFrameIdRef.current = requestAnimationFrame(runSimulation)
    }

    animFrameIdRef.current = requestAnimationFrame(runSimulation)

    return () => {
      if (animFrameIdRef.current) cancelAnimationFrame(animFrameIdRef.current)
    }
  }, [nodes, edges, dimensions, currentMode])

  // Sharp, High-DPI Canvas Rendering Engine
  const drawCanvas = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const dpr = window.devicePixelRatio || 1
    const { width, height } = dimensions

    // Match bitmap pixels to physical screen device pixels for 4K/Retina sharpness
    if (canvas.width !== Math.floor(width * dpr) || canvas.height !== Math.floor(height * dpr)) {
      canvas.width = Math.floor(width * dpr)
      canvas.height = Math.floor(height * dpr)
    }

    ctx.save()
    ctx.scale(dpr, dpr)
    ctx.clearRect(0, 0, width, height)

    // Deep Obsidian / Indigo Radial Gradient Background
    const bgGrad = ctx.createRadialGradient(width / 2, height / 2, 50, width / 2, height / 2, width * 0.7)
    bgGrad.addColorStop(0, '#0c111d')
    bgGrad.addColorStop(0.7, '#070a12')
    bgGrad.addColorStop(1, '#04060a')
    ctx.fillStyle = bgGrad
    ctx.fillRect(0, 0, width, height)

    // Subtle Neo4j Coordinate Grid Dots
    ctx.fillStyle = 'rgba(255, 255, 255, 0.03)'
    const gridSize = 40
    for (let gx = 0; gx < width; gx += gridSize) {
      for (let gy = 0; gy < height; gy += gridSize) {
        ctx.fillRect(gx, gy, 1.2, 1.2)
      }
    }

    // Apply pan & zoom
    ctx.translate(transform.x, transform.y)
    ctx.scale(transform.scale, transform.scale)

    const currentNodes = simNodesRef.current
    const currentEdges = simEdgesRef.current as any[]

    // Connected neighbor IDs for active selection / hover
    const activeNode = selectedNode || hoveredNode
    const connectedNodeIds = new Set<string>()
    const connectedEdgeIds = new Set<string>()

    if (activeNode) {
      connectedNodeIds.add(activeNode.id)
      for (const e of currentEdges) {
        if (e.sourceObj?.id === activeNode.id || e.targetObj?.id === activeNode.id) {
          connectedNodeIds.add(e.sourceObj?.id)
          connectedNodeIds.add(e.targetObj?.id)
          connectedEdgeIds.add(e.id)
        }
      }
    }

    // 1. Draw Relationship Edges (Smooth Bezier with Directional Arrows)
    for (const edge of currentEdges) {
      const s = edge.sourceObj
      const t = edge.targetObj
      if (s && t) {
        const isHighlighted = connectedEdgeIds.has(edge.id)
        const isLegendActive = activeLegendFilter ? s.group === activeLegendFilter || t.group === activeLegendFilter : true
        const isDimmed = (activeNode && !isHighlighted) || !isLegendActive

        const sx = s.x || 0
        const sy = s.y || 0
        const tx = t.x || 0
        const ty = t.y || 0

        // Line path
        ctx.beginPath()
        ctx.moveTo(sx, sy)
        ctx.lineTo(tx, ty)

        if (isHighlighted) {
          ctx.strokeStyle = '#38bdf8' // Cyan glow
          ctx.lineWidth = 2.2
          ctx.shadowColor = 'rgba(56, 189, 248, 0.4)'
          ctx.shadowBlur = 6
        } else if (isDimmed) {
          ctx.strokeStyle = 'rgba(40, 52, 75, 0.15)'
          ctx.lineWidth = 0.8
          ctx.shadowBlur = 0
        } else {
          ctx.strokeStyle = 'rgba(75, 95, 130, 0.35)'
          ctx.lineWidth = 1.0
          ctx.shadowBlur = 0
        }
        ctx.stroke()
        ctx.shadowBlur = 0 // Reset shadow

        // Directional Arrow Indicator
        const dx = tx - sx
        const dy = ty - sy
        const angle = Math.atan2(dy, dx)
        const arrowDist = Math.max(16, t.val + 4)
        const ax = tx - Math.cos(angle) * arrowDist
        const ay = ty - Math.sin(angle) * arrowDist

        ctx.beginPath()
        ctx.moveTo(ax, ay)
        ctx.lineTo(ax - 6 * Math.cos(angle - Math.PI / 7), ay - 6 * Math.sin(angle - Math.PI / 7))
        ctx.lineTo(ax - 6 * Math.cos(angle + Math.PI / 7), ay - 6 * Math.sin(angle + Math.PI / 7))
        ctx.closePath()
        ctx.fillStyle = isHighlighted ? '#38bdf8' : isDimmed ? 'rgba(40, 52, 75, 0.2)' : 'rgba(75, 95, 130, 0.45)'
        ctx.fill()

        // Edge Labels: Render ONLY on highlight or deep zoom (>1.35x) to avoid hairball clutter!
        const shouldShowLabel = isHighlighted || (transform.scale > 1.35 && !isDimmed)
        if (shouldShowLabel) {
          const mx = (sx + tx) / 2
          const my = (sy + ty) / 2
          const labelText = edge.label || edge.type

          ctx.font = '8px JetBrains Mono, monospace'
          ctx.textAlign = 'center'
          ctx.textBaseline = 'middle'

          const textWidth = ctx.measureText(labelText).width
          // Draw high-contrast capsule pill behind label so lines don't strike through text
          ctx.fillStyle = isHighlighted ? 'rgba(12, 19, 36, 0.95)' : 'rgba(8, 11, 20, 0.85)'
          ctx.strokeStyle = isHighlighted ? 'rgba(56, 189, 248, 0.6)' : 'rgba(255, 255, 255, 0.1)'
          ctx.lineWidth = 1
          ctx.beginPath()
          ctx.roundRect(mx - textWidth / 2 - 4, my - 6, textWidth + 8, 12, 4)
          ctx.fill()
          ctx.stroke()

          ctx.fillStyle = isHighlighted ? '#bae6fd' : '#94a3b8'
          ctx.fillText(labelText, mx, my)
        }
      }
    }

    // 2. Draw Nodes
    for (const n of currentNodes) {
      const isSelected = selectedNode?.id === n.id
      const isHovered = hoveredNode?.id === n.id
      const isConnected = connectedNodeIds.has(n.id)
      const isLegendActive = activeLegendFilter ? n.group === activeLegendFilter : true
      const isDimmed = (activeNode && !isConnected) || !isLegendActive

      const nx = n.x || 0
      const ny = n.y || 0
      const radius = isSelected ? n.val * 1.3 : isHovered ? n.val * 1.18 : n.val

      // Outer Selection / Focus Aura Glow
      if (isSelected || isHovered) {
        ctx.beginPath()
        ctx.arc(nx, ny, radius + 7, 0, 2 * Math.PI)
        ctx.fillStyle = isSelected ? 'rgba(56, 189, 248, 0.22)' : 'rgba(255, 255, 255, 0.1)'
        ctx.fill()
        ctx.strokeStyle = isSelected ? '#38bdf8' : '#cbd5e1'
        ctx.lineWidth = 1.5
        ctx.stroke()
      }

      // Main Node Disc with Gradient Fill
      ctx.beginPath()
      ctx.arc(nx, ny, radius, 0, 2 * Math.PI)

      let baseColor = n.color || '#64748b'
      if (n.group === 'person') baseColor = '#f59e0b' // Amber/Gold (Center Persona)
      else if (n.group === 'mandate') {
        const flag = n.properties?.flag
        if (flag === 'PRICE_HIKE') baseColor = '#f59e0b'
        else if (flag === 'TRIAL_CONVERTED') baseColor = '#f43f5e'
        else if (flag === 'UNUSED_ZOMBIE') baseColor = '#ef4444'
        else baseColor = '#10b981'
      } else if (n.group === 'merchant') baseColor = '#10b981' // Emerald
      else if (n.group === 'parent') baseColor = '#6366f1' // Indigo
      else if (n.group === 'mechanism') baseColor = '#ec4899' // Pink

      if (isDimmed) {
        ctx.fillStyle = 'rgba(25, 33, 48, 0.5)'
        ctx.fill()
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)'
        ctx.lineWidth = 1.2
        ctx.stroke()
      } else {
        ctx.fillStyle = baseColor
        ctx.fill()
        ctx.strokeStyle = '#05070c'
        ctx.lineWidth = 2.2
        ctx.stroke()
      }

      // Node Name Label
      if (!isDimmed || isSelected || isHovered) {
        ctx.fillStyle = isSelected || isHovered ? '#ffffff' : '#f1f5f9'
        ctx.font = isSelected || isHovered
          ? 'bold 11px Plus Jakarta Sans, sans-serif'
          : n.group === 'person' || n.group === 'parent'
          ? '600 10.5px Plus Jakarta Sans, sans-serif'
          : '500 9.5px Plus Jakarta Sans, sans-serif'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'top'

        // Clean truncation to eliminate messy label collisions
        const maxLen = isSelected || isHovered ? 26 : currentMode === 'all' ? 14 : 18
        const labelText = n.name.length > maxLen ? n.name.slice(0, maxLen - 2) + '…' : n.name
        ctx.fillText(labelText, nx, ny + radius + 7)

        // Entity Meta Tag Pill (Above Node)
        if ((isSelected || isHovered || currentMode === 'portfolio') && !isDimmed) {
          ctx.fillStyle = '#64748b'
          ctx.font = '7.5px JetBrains Mono, monospace'
          ctx.fillText(`:${n.label.toUpperCase()}`, nx, ny - radius - 11)
        }
      }
    }

    ctx.restore()
  }

  // Position Hit Testing for Pointer & Dragging
  const getNodeAtPos = (clientX: number, clientY: number): GraphNode | null => {
    const canvas = canvasRef.current
    if (!canvas) return null
    const rect = canvas.getBoundingClientRect()
    const x = (clientX - rect.left - transform.x) / transform.scale
    const y = (clientY - rect.top - transform.y) / transform.scale

    for (const n of simNodesRef.current) {
      const dx = x - (n.x || 0)
      const dy = y - (n.y || 0)
      if (Math.sqrt(dx * dx + dy * dy) <= n.val + 8) {
        return n
      }
    }
    return null
  }

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const node = getNodeAtPos(e.clientX, e.clientY)
    if (node) {
      draggedNodeRef.current = node
      setSelectedNode(node)
      if (onNodeClick) onNodeClick(node)
    } else {
      isDraggingRef.current = true
      dragStartRef.current = { x: e.clientX - transform.x, y: e.clientY - transform.y }
    }
  }

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current
    if (!canvas) return

    if (draggedNodeRef.current) {
      const rect = canvas.getBoundingClientRect()
      draggedNodeRef.current.x = (e.clientX - rect.left - transform.x) / transform.scale
      draggedNodeRef.current.y = (e.clientY - rect.top - transform.y) / transform.scale
      drawCanvas()
    } else if (isDraggingRef.current) {
      setTransform(prev => ({
        ...prev,
        x: e.clientX - dragStartRef.current.x,
        y: e.clientY - dragStartRef.current.y
      }))
    } else {
      const node = getNodeAtPos(e.clientX, e.clientY)
      setHoveredNode(node)
      canvas.style.cursor = node ? 'pointer' : isDraggingRef.current ? 'grabbing' : 'grab'
    }
  }

  const handleMouseUp = () => {
    draggedNodeRef.current = null
    isDraggingRef.current = false
  }

  const handleWheel = (e: React.WheelEvent<HTMLCanvasElement>) => {
    e.preventDefault()
    const zoomFactor = e.deltaY < 0 ? 1.09 : 0.91
    setTransform(prev => ({
      ...prev,
      scale: Math.max(0.35, Math.min(2.8, prev.scale * zoomFactor))
    }))
  }

  // Zoom & Center on Search Match
  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    const match = simNodesRef.current.find(n =>
      n.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      n.id.toLowerCase().includes(searchQuery.toLowerCase())
    )

    if (match && match.x !== undefined && match.y !== undefined) {
      setSelectedNode(match)
      if (onNodeClick) onNodeClick(match)
      // Center canvas on matching node
      setTransform({
        x: dimensions.width / 2 - match.x * 1.3,
        y: dimensions.height / 2 - match.y * 1.3,
        scale: 1.3
      })
    }
  }

  // Generated Cypher query for selected node
  const cypherSnippet = useMemo(() => {
    if (!selectedNode) return ''
    if (selectedNode.label === 'Merchant') {
      return `MATCH (m:Merchant {id: '${selectedNode.id}'})-[:OWNED_BY]->(p:Parent)\nOPTIONAL MATCH (m)-[:BILLED_VIA]->(mech:Mechanism)\nRETURN m.name, p.name AS Parent, mech.name AS PaymentRail;`
    } else if (selectedNode.label === 'Mandate') {
      return `MATCH (mand:Mandate {id: '${selectedNode.id}'})-[:FOR]->(m:Merchant)\nMATCH (mand)-[:VIA_MECHANISM]->(mech:Mechanism)-[:CANCELLED_BY]->(c:CancellationPath)\nRETURN mand.id, m.name, mand.latest_amount, mech.name, c.primary_step;`
    } else if (selectedNode.label === 'Parent') {
      return `MATCH (p:Parent {id: '${selectedNode.id}'})<-[:OWNED_BY]-(m:Merchant)\nRETURN p.name, collect(m.name) AS SubsidiaryMerchants;`
    } else if (selectedNode.label === 'Mechanism') {
      return `MATCH (mech:Mechanism {code: '${selectedNode.id.replace('mech_', '')}'})-[:CANCELLED_BY]->(c:CancellationPath)\nRETURN mech.name, mech.turnaround_time, c.statutory_steps;`
    }
    return `MATCH (n:${selectedNode.label} {id: '${selectedNode.id}'})-[r]-(neighbor)\nRETURN n, type(r), neighbor;`
  }, [selectedNode])

  const copyCypher = () => {
    if (!cypherSnippet) return
    navigator.clipboard.writeText(cypherSnippet)
    setCopiedCypher(true)
    setTimeout(() => setCopiedCypher(false), 2000)
  }

  return (
    <div
      ref={containerRef}
      className="relative w-full h-[600px] bg-[#070a12] rounded-2xl border border-white/[0.08] overflow-hidden shadow-2xl select-none"
    >
      {/* High-DPI Canvas */}
      <canvas
        ref={canvasRef}
        className="w-full h-full block cursor-grab active:cursor-grabbing"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
      />

      {/* TOP BAR: Cluster Selector Tabs & Node Finder */}
      <div className="absolute top-3 left-3 right-3 flex flex-wrap items-center justify-between gap-2 pointer-events-none">
        {/* Cluster Tabs */}
        <div className="flex items-center gap-1.5 bg-[#0d121f]/90 backdrop-blur-md p-1 rounded-xl border border-white/[0.1] text-xs shadow-xl pointer-events-auto">
          <button
            onClick={() => onModeChange && onModeChange('portfolio')}
            className={`px-3 py-1.5 rounded-lg font-medium transition flex items-center gap-1.5 ${
              currentMode === 'portfolio'
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-semibold shadow-sm'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>Active Portfolio (31)</span>
          </button>
          <button
            onClick={() => onModeChange && onModeChange('alphabet')}
            className={`px-3 py-1.5 rounded-lg font-medium transition ${
              currentMode === 'alphabet'
                ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 font-semibold shadow-sm'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            Alphabet (Google)
          </button>
          <button
            onClick={() => onModeChange && onModeChange('amazon')}
            className={`px-3 py-1.5 rounded-lg font-medium transition ${
              currentMode === 'amazon'
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 font-semibold shadow-sm'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            Amazon Footprint
          </button>
          <button
            onClick={() => onModeChange && onModeChange('streaming')}
            className={`px-3 py-1.5 rounded-lg font-medium transition ${
              currentMode === 'streaming'
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold shadow-sm'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            Streaming OTT
          </button>
          <button
            onClick={() => onModeChange && onModeChange('all')}
            className={`px-3 py-1.5 rounded-lg font-medium transition ${
              currentMode === 'all'
                ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40 font-semibold shadow-sm'
                : 'text-neutral-400 hover:text-white'
            }`}
          >
            Full Catalog (76)
          </button>
        </div>

        {/* Quick Node Search */}
        <form
          onSubmit={handleSearchSubmit}
          className="flex items-center gap-2 bg-[#0d121f]/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/[0.1] shadow-xl pointer-events-auto"
        >
          <Search className="w-3.5 h-3.5 text-neutral-400" />
          <input
            type="text"
            placeholder="Search node..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            className="bg-transparent text-xs text-white placeholder-neutral-500 focus:outline-none w-32 md:w-44 font-mono"
          />
          {searchQuery && (
            <button
              type="submit"
              className="text-[10px] font-mono bg-cyan-500/20 text-cyan-300 px-1.5 py-0.5 rounded border border-cyan-500/30"
            >
              FIND
            </button>
          )}
        </form>
      </div>

      {/* BOTTOM LEFT: Interactive Taxonomy Legend with Filter Isolation */}
      <div className="absolute bottom-3 left-3 flex flex-wrap items-center gap-2 bg-[#0d121f]/90 backdrop-blur-md px-3 py-2 rounded-xl border border-white/[0.1] text-xs shadow-xl">
        <span className="text-[10px] font-mono text-neutral-500 uppercase mr-1">Taxonomy:</span>
        <button
          onClick={() => setActiveLegendFilter(activeLegendFilter === 'person' ? null : 'person')}
          className={`flex items-center gap-1.5 px-2 py-0.5 rounded-lg transition ${
            activeLegendFilter === 'person' ? 'bg-amber-500/20 border border-amber-500/40' : 'hover:bg-white/[0.04]'
          }`}
        >
          <span className="w-2.5 h-2.5 rounded-full bg-amber-400 shadow-sm shadow-amber-400/50" />
          <span className="text-neutral-300 text-[11px]">Person</span>
        </button>
        <button
          onClick={() => setActiveLegendFilter(activeLegendFilter === 'mandate' ? null : 'mandate')}
          className={`flex items-center gap-1.5 px-2 py-0.5 rounded-lg transition ${
            activeLegendFilter === 'mandate' ? 'bg-emerald-500/20 border border-emerald-500/40' : 'hover:bg-white/[0.04]'
          }`}
        >
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50" />
          <span className="text-neutral-300 text-[11px]">Mandate</span>
        </button>
        <button
          onClick={() => setActiveLegendFilter(activeLegendFilter === 'merchant' ? null : 'merchant')}
          className={`flex items-center gap-1.5 px-2 py-0.5 rounded-lg transition ${
            activeLegendFilter === 'merchant' ? 'bg-teal-500/20 border border-teal-500/40' : 'hover:bg-white/[0.04]'
          }`}
        >
          <span className="w-2.5 h-2.5 rounded-full bg-teal-400 shadow-sm shadow-teal-400/50" />
          <span className="text-neutral-300 text-[11px]">Merchant</span>
        </button>
        <button
          onClick={() => setActiveLegendFilter(activeLegendFilter === 'parent' ? null : 'parent')}
          className={`flex items-center gap-1.5 px-2 py-0.5 rounded-lg transition ${
            activeLegendFilter === 'parent' ? 'bg-indigo-500/20 border border-indigo-500/40' : 'hover:bg-white/[0.04]'
          }`}
        >
          <span className="w-2.5 h-2.5 rounded-full bg-indigo-400 shadow-sm shadow-indigo-400/50" />
          <span className="text-neutral-300 text-[11px]">Parent Corp</span>
        </button>
        <button
          onClick={() => setActiveLegendFilter(activeLegendFilter === 'mechanism' ? null : 'mechanism')}
          className={`flex items-center gap-1.5 px-2 py-0.5 rounded-lg transition ${
            activeLegendFilter === 'mechanism' ? 'bg-pink-500/20 border border-pink-500/40' : 'hover:bg-white/[0.04]'
          }`}
        >
          <span className="w-2.5 h-2.5 rounded-full bg-pink-400 shadow-sm shadow-pink-400/50" />
          <span className="text-neutral-300 text-[11px]">Payment Rail</span>
        </button>
      </div>

      {/* BOTTOM RIGHT: Zoom Controls */}
      <div className="absolute bottom-3 right-3 flex items-center gap-1.5 bg-[#0d121f]/90 backdrop-blur-md px-2.5 py-1.5 rounded-xl border border-white/[0.1] text-xs text-neutral-400 font-mono shadow-xl">
        <button
          onClick={() => setTransform(prev => ({ ...prev, scale: Math.min(2.8, prev.scale * 1.15) }))}
          className="p-1 rounded hover:bg-white/[0.08] hover:text-white transition"
          title="Zoom In"
        >
          <ZoomIn className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={() => setTransform(prev => ({ ...prev, scale: Math.max(0.35, prev.scale * 0.85) }))}
          className="p-1 rounded hover:bg-white/[0.08] hover:text-white transition"
          title="Zoom Out"
        >
          <ZoomOut className="w-3.5 h-3.5" />
        </button>
        <button
          onClick={() => setTransform({ x: 0, y: 0, scale: 0.95 })}
          className="px-2 py-0.5 rounded hover:bg-white/[0.08] hover:text-white transition text-[11px]"
          title="Reset View"
        >
          Reset
        </button>
        <span className="text-neutral-500 pl-1 text-[11px]">{(transform.scale * 100).toFixed(0)}%</span>
      </div>

      {/* FLYOUT: Interactive Neo4j Node Inspector with Cypher Generator */}
      {selectedNode && (
        <div className="absolute top-14 right-3 w-88 max-w-[calc(100%-24px)] bg-[#0d121f]/95 backdrop-blur-xl border border-white/[0.15] p-5 rounded-2xl shadow-2xl space-y-3.5 animate-in fade-in slide-in-from-right-4 duration-200 z-20">
          <div className="flex items-start justify-between border-b border-white/[0.08] pb-3">
            <div>
              <span className="text-[10px] font-mono tracking-wider text-cyan-400 uppercase bg-cyan-950/60 border border-cyan-800/60 px-2 py-0.5 rounded-md font-bold">
                :{selectedNode.label}
              </span>
              <h4 className="font-bold text-white text-base mt-1.5 tracking-tight">{selectedNode.name}</h4>
              <p className="text-[11px] font-mono text-neutral-400">ID: {selectedNode.id}</p>
            </div>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-neutral-400 hover:text-white p-1 rounded-lg hover:bg-white/[0.08] transition"
            >
              ✕
            </button>
          </div>

          {/* Node Properties Ledger */}
          <div className="space-y-1.5 font-mono text-[11px] max-h-40 overflow-y-auto pr-1">
            {selectedNode.properties &&
              Object.entries(selectedNode.properties)
                .filter(([k]) => !['history', 'cancellation_steps'].includes(k))
                .slice(0, 8)
                .map(([k, v]) => (
                  <div key={k} className="flex justify-between gap-2 overflow-hidden py-0.5 border-b border-white/[0.03]">
                    <span className="text-neutral-500 shrink-0">{k}:</span>
                    <span className="text-neutral-200 truncate font-sans font-medium text-right">
                      {typeof v === 'object' ? JSON.stringify(v) : String(v)}
                    </span>
                  </div>
                ))}
          </div>

          {/* Neo4j Cypher Traversal Preview */}
          <div className="bg-[#060911] border border-white/[0.08] rounded-xl p-3 space-y-2">
            <div className="flex items-center justify-between text-[10px] font-mono text-neutral-400">
              <span className="flex items-center gap-1 text-cyan-400 font-bold">
                <Terminal className="w-3 h-3" />
                <span>NEO4J CYPHER TRAVERSAL</span>
              </span>
              <button
                onClick={copyCypher}
                className="flex items-center gap-1 text-neutral-400 hover:text-white transition"
              >
                {copiedCypher ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                <span>{copiedCypher ? 'Copied' : 'Copy'}</span>
              </button>
            </div>
            <pre className="text-[10px] font-mono text-cyan-300 overflow-x-auto whitespace-pre-wrap leading-relaxed max-h-24">
              {cypherSnippet}
            </pre>
            {onExecuteCypher && (
              <button
                onClick={() => onExecuteCypher(cypherSnippet)}
                className="w-full py-1.5 px-3 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/40 text-cyan-300 text-xs font-mono font-semibold transition flex items-center justify-center gap-1.5"
              >
                <span>Run in Cypher Workbench</span>
                <ArrowRight className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
