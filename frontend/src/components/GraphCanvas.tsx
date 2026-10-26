import React, { useRef, useEffect, useState } from 'react'

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
}

export interface GraphEdge {
  id: string
  source: string | GraphNode
  target: string | GraphNode
  type: string
  label: string
  color: string
}

interface GraphCanvasProps {
  nodes: GraphNode[]
  edges: GraphEdge[]
  onNodeClick?: (node: GraphNode) => void
  currentMode?: string
  onModeChange?: (mode: string) => void
}

export const GraphCanvas: React.FC<GraphCanvasProps> = ({
  nodes,
  edges,
  onNodeClick,
  currentMode = 'portfolio',
  onModeChange
}) => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null)
  const [hoveredNode, setHoveredNode] = useState<GraphNode | null>(null)
  const [transform, setTransform] = useState({ x: 0, y: 0, scale: 0.95 })
  const isDraggingRef = useRef(false)
  const dragStartRef = useRef({ x: 0, y: 0 })
  const draggedNodeRef = useRef<GraphNode | null>(null)

  const simNodesRef = useRef<GraphNode[]>([])
  const simEdgesRef = useRef<GraphEdge[]>([])
  const animFrameIdRef = useRef<number | null>(null)

  useEffect(() => {
    const width = 960
    const height = 520
    const cx = width / 2
    const cy = height / 2

    const nodeMap = new Map<string, GraphNode>()

    // Arrange nodes in structured concentric orbital rings to avoid tangled hairballs
    const initNodes = nodes.map((n) => {
      let radius = 180
      let baseAngle = Math.random() * 2 * Math.PI

      if (n.group === 'person') {
        // Center node
        return { ...n, x: cx, y: cy, vx: 0, vy: 0, val: 24 }
      } else if (n.group === 'mandate') {
        // Inner ring: Mandates
        radius = 110 + Math.random() * 25
      } else if (n.group === 'merchant') {
        // Middle ring: Merchants
        radius = 200 + Math.random() * 35
      } else if (n.group === 'parent') {
        // Outer ring: Corporate parents
        radius = 290 + Math.random() * 30
      } else if (n.group === 'mechanism') {
        // Outer ring: Payment rails
        radius = 280 + Math.random() * 35
      } else {
        radius = 230 + Math.random() * 40
      }

      const cloned: GraphNode = {
        ...n,
        x: cx + Math.cos(baseAngle) * radius,
        y: cy + Math.sin(baseAngle) * radius,
        vx: 0,
        vy: 0,
        val: n.group === 'parent' ? 20 : n.group === 'merchant' ? 16 : n.group === 'mandate' ? 14 : 12
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
    const decay = 0.992

    const runSimulation = () => {
      const currentNodes = simNodesRef.current
      const currentEdges = simEdgesRef.current as any[]

      if (alpha > 0.005) {
        // 1. Strong Collision Resolution (prevents overlapping circles seen in screenshot)
        for (let i = 0; i < currentNodes.length; i++) {
          for (let j = i + 1; j < currentNodes.length; j++) {
            const n1 = currentNodes[i]
            const n2 = currentNodes[j]
            const dx = (n2.x || 0) - (n1.x || 0)
            const dy = (n2.y || 0) - (n1.y || 0)
            const dist = Math.sqrt(dx * dx + dy * dy) || 1
            const minAllowedDist = (n1.val + n2.val) + 38 // generous clearance margin

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

        // 2. Link Spring Forces
        for (const edge of currentEdges) {
          const s = edge.sourceObj
          const t = edge.targetObj
          if (s && t) {
            const dx = (t.x || 0) - (s.x || 0)
            const dy = (t.y || 0) - (s.y || 0)
            const dist = Math.sqrt(dx * dx + dy * dy) || 1
            const targetDist = 95
            const force = (dist - targetDist) * 0.035 * alpha
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
            n.vx = ((n.vx || 0) + (cx - (n.x || 0)) * 0.003 * alpha) * 0.86
            n.vy = ((n.vy || 0) + (cy - (n.y || 0)) * 0.003 * alpha) * 0.86
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
  }, [nodes, edges])

  const drawCanvas = () => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    ctx.save()
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Sleek background with subtle coordinate crosshairs
    ctx.fillStyle = '#0a0d14'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    // Apply pan & zoom
    ctx.translate(transform.x, transform.y)
    ctx.scale(transform.scale, transform.scale)

    const currentNodes = simNodesRef.current
    const currentEdges = simEdgesRef.current as any[]

    // Active connected set when a node is selected or hovered
    const activeNode = selectedNode || hoveredNode
    const connectedNodeIds = new Set<string>()
    if (activeNode) {
      connectedNodeIds.add(activeNode.id)
      for (const e of currentEdges) {
        if (e.sourceObj?.id === activeNode.id) connectedNodeIds.add(e.targetObj?.id)
        if (e.targetObj?.id === activeNode.id) connectedNodeIds.add(e.sourceObj?.id)
      }
    }

    // 1. Draw Edges
    for (const edge of currentEdges) {
      const s = edge.sourceObj
      const t = edge.targetObj
      if (s && t) {
        const isHighlighted =
          activeNode &&
          (s.id === activeNode.id || t.id === activeNode.id)
        const isDimmed = activeNode && !isHighlighted

        ctx.beginPath()
        ctx.moveTo(s.x || 0, s.y || 0)
        ctx.lineTo(t.x || 0, t.y || 0)

        ctx.strokeStyle = isHighlighted
          ? '#38bdf8'
          : isDimmed
          ? 'rgba(35, 45, 65, 0.25)'
          : 'rgba(56, 70, 95, 0.45)'
        ctx.lineWidth = isHighlighted ? 2.0 : 1.0
        ctx.stroke()

        // Edge label (only when zoomed in or highlighted to avoid messy text)
        if (isHighlighted || (transform.scale > 0.9 && !isDimmed)) {
          const mx = ((s.x || 0) + (t.x || 0)) / 2
          const my = ((s.y || 0) + (t.y || 0)) / 2
          ctx.fillStyle = isHighlighted ? '#bae6fd' : '#475569'
          ctx.font = '8px JetBrains Mono'
          ctx.textAlign = 'center'
          ctx.fillText(edge.label || edge.type, mx, my - 2)
        }
      }
    }

    // 2. Draw Nodes
    for (const n of currentNodes) {
      const isSelected = selectedNode?.id === n.id
      const isHovered = hoveredNode?.id === n.id
      const isConnected = connectedNodeIds.has(n.id)
      const isDimmed = activeNode && !isConnected

      const radius = isSelected ? n.val * 1.25 : isHovered ? n.val * 1.15 : n.val

      // Outer focus / highlight ring
      if (isSelected || isHovered) {
        ctx.beginPath()
        ctx.arc(n.x || 0, n.y || 0, radius + 5, 0, 2 * Math.PI)
        ctx.fillStyle = isSelected ? 'rgba(56, 189, 248, 0.25)' : 'rgba(255, 255, 255, 0.12)'
        ctx.fill()
        ctx.strokeStyle = isSelected ? '#38bdf8' : '#94a3b8'
        ctx.lineWidth = 1.5
        ctx.stroke()
      }

      // Main Node Body (smooth luxury circle with dark border)
      ctx.beginPath()
      ctx.arc(n.x || 0, n.y || 0, radius, 0, 2 * Math.PI)

      // Color coding with subtle contrast
      let nodeColor = n.color || '#475569'
      if (n.group === 'parent') nodeColor = '#6366f1' // Indigo
      if (n.group === 'merchant') nodeColor = '#10b981' // Emerald
      if (n.group === 'mechanism') nodeColor = '#ec4899' // Pink
      if (n.group === 'descriptor') nodeColor = '#8b5cf6' // Purple
      if (n.group === 'mandate') nodeColor = '#f59e0b' // Amber
      if (n.group === 'person') nodeColor = '#06b6d4' // Cyan

      ctx.fillStyle = isDimmed ? 'rgba(40, 50, 70, 0.4)' : nodeColor
      ctx.fill()
      ctx.strokeStyle = '#07090e'
      ctx.lineWidth = 2
      ctx.stroke()

      // Primary Node Text Label
      ctx.fillStyle = isDimmed
        ? 'rgba(100, 116, 139, 0.4)'
        : isSelected || isHovered
        ? '#ffffff'
        : '#e2e8f0'
      ctx.font = isSelected || isHovered ? 'bold 11px Plus Jakarta Sans' : '500 10px Plus Jakarta Sans'
      ctx.textAlign = 'center'

      // Truncate cleanly so labels never overlap
      const maxLen = isSelected || isHovered ? 24 : 16
      const labelText = n.name.length > maxLen ? n.name.slice(0, maxLen - 2) + '…' : n.name
      ctx.fillText(labelText, n.x || 0, (n.y || 0) + radius + 12)

      // Category Pill Above
      if ((isSelected || isHovered || transform.scale > 1.0) && !isDimmed) {
        ctx.fillStyle = '#64748b'
        ctx.font = '7.5px JetBrains Mono'
        ctx.fillText(n.label.toUpperCase(), n.x || 0, (n.y || 0) - radius - 3)
      }
    }

    ctx.restore()
  }

  const getNodeAtPos = (clientX: number, clientY: number): GraphNode | null => {
    const canvas = canvasRef.current
    if (!canvas) return null
    const rect = canvas.getBoundingClientRect()
    const x = (clientX - rect.left - transform.x) / transform.scale
    const y = (clientY - rect.top - transform.y) / transform.scale

    for (const n of simNodesRef.current) {
      const dx = x - (n.x || 0)
      const dy = y - (n.y || 0)
      if (Math.sqrt(dx * dx + dy * dy) <= n.val + 6) {
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
      canvas.style.cursor = node ? 'pointer' : 'grab'
    }
  }

  const handleMouseUp = () => {
    draggedNodeRef.current = null
    isDraggingRef.current = false
  }

  const handleWheel = (e: React.WheelEvent<HTMLCanvasElement>) => {
    e.preventDefault()
    const zoomFactor = e.deltaY < 0 ? 1.08 : 0.92
    setTransform(prev => ({
      ...prev,
      scale: Math.max(0.4, Math.min(2.5, prev.scale * zoomFactor))
    }))
  }

  return (
    <div className="relative w-full h-[520px] bg-[#0a0d14] rounded-2xl border border-white/[0.08] overflow-hidden shadow-2xl">
      <canvas
        ref={canvasRef}
        width={960}
        height={520}
        className="w-full h-full block"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
      />

      {/* Cluster Filter Tabs Row (Solves the 270-node hairball issue!) */}
      <div className="absolute top-3 left-3 flex items-center gap-1.5 bg-[#0f1420]/90 backdrop-blur-md p-1 rounded-xl border border-white/[0.1] text-xs">
        <button
          onClick={() => onModeChange && onModeChange('portfolio')}
          className={`px-3 py-1 rounded-lg font-medium transition ${
            currentMode === 'portfolio'
              ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-semibold shadow-sm'
              : 'text-neutral-400 hover:text-white'
          }`}
        >
          Active Portfolio
        </button>
        <button
          onClick={() => onModeChange && onModeChange('alphabet')}
          className={`px-3 py-1 rounded-lg font-medium transition ${
            currentMode === 'alphabet'
              ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 font-semibold shadow-sm'
              : 'text-neutral-400 hover:text-white'
          }`}
        >
          Alphabet (Google)
        </button>
        <button
          onClick={() => onModeChange && onModeChange('amazon')}
          className={`px-3 py-1 rounded-lg font-medium transition ${
            currentMode === 'amazon'
              ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40 font-semibold shadow-sm'
              : 'text-neutral-400 hover:text-white'
          }`}
        >
          Amazon Footprint
        </button>
        <button
          onClick={() => onModeChange && onModeChange('streaming')}
          className={`px-3 py-1 rounded-lg font-medium transition ${
            currentMode === 'streaming'
              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold shadow-sm'
              : 'text-neutral-400 hover:text-white'
          }`}
        >
          Streaming OTT
        </button>
        <button
          onClick={() => onModeChange && onModeChange('all')}
          className={`px-3 py-1 rounded-lg font-medium transition ${
            currentMode === 'all'
              ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40 font-semibold shadow-sm'
              : 'text-neutral-400 hover:text-white'
          }`}
        >
          Full Catalog (76)
        </button>
      </div>

      {/* Floating Canvas Controls */}
      <div className="absolute bottom-3 right-3 flex items-center gap-1.5 bg-[#0f1420]/90 backdrop-blur-md px-2.5 py-1.5 rounded-xl border border-white/[0.1] text-[11px] text-neutral-400 font-mono">
        <button
          onClick={() => setTransform(prev => ({ ...prev, scale: Math.min(2.5, prev.scale * 1.15) }))}
          className="px-2 py-0.5 rounded hover:bg-white/[0.08] hover:text-white transition"
          title="Zoom In"
        >
          +
        </button>
        <button
          onClick={() => setTransform(prev => ({ ...prev, scale: Math.max(0.4, prev.scale * 0.85) }))}
          className="px-2 py-0.5 rounded hover:bg-white/[0.08] hover:text-white transition"
          title="Zoom Out"
        >
          −
        </button>
        <button
          onClick={() => setTransform({ x: 0, y: 0, scale: 0.95 })}
          className="px-2 py-0.5 rounded hover:bg-white/[0.08] hover:text-white transition"
        >
          Reset
        </button>
        <span className="text-neutral-600 pl-1">{(transform.scale * 100).toFixed(0)}%</span>
      </div>

      {/* Taxonomy Legend */}
      <div className="absolute bottom-3 left-3 flex flex-wrap items-center gap-3 bg-[#0f1420]/90 backdrop-blur-md px-3.5 py-2 rounded-xl border border-white/[0.1] text-[11px]">
        <div className="flex items-center gap-1.5 text-neutral-300">
          <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400/50" />
          <span>Person (Center)</span>
        </div>
        <div className="flex items-center gap-1.5 text-neutral-300">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-400 shadow-sm shadow-amber-400/50" />
          <span>Mandate</span>
        </div>
        <div className="flex items-center gap-1.5 text-neutral-300">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50" />
          <span>Merchant</span>
        </div>
        <div className="flex items-center gap-1.5 text-neutral-300">
          <span className="w-2.5 h-2.5 rounded-full bg-indigo-400 shadow-sm shadow-indigo-400/50" />
          <span>Parent Corp</span>
        </div>
        <div className="flex items-center gap-1.5 text-neutral-300">
          <span className="w-2.5 h-2.5 rounded-full bg-pink-400 shadow-sm shadow-pink-400/50" />
          <span>Payment Rail</span>
        </div>
      </div>

      {/* Node Inspector Flyout */}
      {selectedNode && (
        <div className="absolute top-14 right-3 w-80 bg-[#0f1420]/95 backdrop-blur-md border border-white/[0.12] p-4 rounded-xl shadow-2xl text-xs space-y-2.5 animate-in fade-in duration-150">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-[10px] font-mono tracking-wide text-cyan-400 uppercase bg-cyan-950/60 border border-cyan-800/60 px-2 py-0.5 rounded">
                {selectedNode.label}
              </span>
              <h4 className="font-bold text-white text-sm mt-1.5">{selectedNode.name}</h4>
            </div>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-neutral-500 hover:text-white text-xs px-1"
            >
              ✕
            </button>
          </div>

          <div className="border-t border-white/[0.08] pt-2 space-y-1.5 font-mono text-[11px]">
            {selectedNode.properties &&
              Object.entries(selectedNode.properties)
                .slice(0, 6)
                .map(([k, v]) => (
                  <div key={k} className="flex justify-between gap-2 overflow-hidden">
                    <span className="text-neutral-500 shrink-0">{k}:</span>
                    <span className="text-neutral-200 truncate font-sans font-medium">
                      {typeof v === 'object' ? JSON.stringify(v) : String(v)}
                    </span>
                  </div>
                ))}
          </div>
        </div>
      )}
    </div>
  )
}
