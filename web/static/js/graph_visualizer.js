class GraphVisualizer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    
    this.nodes = [];
    this.links = [];
    this.rawNodes = [];
    this.rawLinks = [];
    this.currentCategory = 'all';
    this.nodeMap = new Map();

    this.scale = 1.0;
    this.panX = 0;
    this.panY = 0;

    this.isDragging = false;
    this.draggedNode = null;
    this.lastMouseX = 0;
    this.lastMouseY = 0;
    this.hoveredNode = null;

    this.highlightedCycleNodes = new Set();
    this.highlightedCycleEdges = new Set();
    this.highlightedPathNodes = new Set();
    this.highlightedPathEdges = new Set();
    this.highlightedBfsNodes = new Set();

    this.particleOffset = 0;

    this.initEvents();
    this.resizeCanvas();
    window.addEventListener('resize', () => this.resizeCanvas());

    this.animate = this.animate.bind(this);
    requestAnimationFrame(this.animate);
  }

  isDark() {
    return document.body.getAttribute('data-theme') === 'dark';
  }

  resizeCanvas() {
    const parent = this.canvas.parentElement;
    this.canvas.width = parent.clientWidth * window.devicePixelRatio;
    this.canvas.height = parent.clientHeight * window.devicePixelRatio;
    this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }

  setData(data) {
    this.rawNodes = data.nodes || [];
    this.rawLinks = data.links || [];
    this.setCategory(this.currentCategory || 'all');
  }

  setCategory(categoryKey) {
    this.currentCategory = categoryKey;
    this.clearHighlights();

    let filteredNodes = [];

    if (categoryKey === 'retail') {
      const ids = new Set(['ACC-501', 'ACC-502', 'ACC-503', 'ACC-504']);
      filteredNodes = this.rawNodes.filter(n => ids.has(n.id));
    } else if (categoryKey === 'rings') {
      const ids = new Set(['ACC-101', 'ACC-102', 'ACC-103', 'ACC-104']);
      filteredNodes = this.rawNodes.filter(n => ids.has(n.id));
    } else if (categoryKey === 'mules') {
      const ids = new Set(['ACC-901', 'ACC-902', 'ACC-903', 'ACC-999']);
      filteredNodes = this.rawNodes.filter(n => ids.has(n.id));
    } else if (categoryKey === 'smurfing') {
      const ids = new Set(['ACC-200', 'ACC-201', 'ACC-202', 'ACC-203', 'ACC-204', 'ACC-205']);
      filteredNodes = this.rawNodes.filter(n => ids.has(n.id));
    } else if (categoryKey === 'offshore') {
      const ids = new Set(['ACC-201', 'ACC-202', 'ACC-203', 'ACC-204', 'ACC-300']);
      filteredNodes = this.rawNodes.filter(n => ids.has(n.id));
    } else if (categoryKey === 'watchlist') {
      filteredNodes = this.rawNodes.filter(n => n.is_flagged || n.risk_score >= 75);
    } else {
      filteredNodes = [...this.rawNodes];
    }

    const activeIds = new Set(filteredNodes.map(n => n.id));
    const filteredLinks = this.rawLinks.filter(l => activeIds.has(l.source) && activeIds.has(l.target));

    this.nodes = filteredNodes;
    this.links = filteredLinks;
    this.nodeMap.clear();

    const width = this.canvas.width / window.devicePixelRatio;
    const height = this.canvas.height / window.devicePixelRatio;
    const cx = width / 2;
    const cy = height / 2;

    if (categoryKey === 'all') {
      const retailIds = new Set(['ACC-501', 'ACC-502', 'ACC-503', 'ACC-504']);
      const muleIds = new Set(['ACC-901', 'ACC-902', 'ACC-903', 'ACC-999']);
      const ringIds = new Set(['ACC-101', 'ACC-102', 'ACC-103', 'ACC-104']);
      const smurfIds = new Set(['ACC-200', 'ACC-201', 'ACC-202', 'ACC-203', 'ACC-204', 'ACC-205', 'ACC-300']);

      const spanX = Math.min(280, width * 0.32);
      const spanY = Math.min(190, height * 0.28);

      const clusterCenters = {
        retail: { x: cx - spanX, y: cy - spanY },
        mules: { x: cx + spanX, y: cy - spanY },
        rings: { x: cx + spanX, y: cy + spanY },
        smurfing: { x: cx - spanX, y: cy + spanY }
      };

      const clusterGroups = { retail: [], mules: [], rings: [], smurfing: [] };
      this.nodes.forEach(node => {
        if (retailIds.has(node.id)) {
          clusterGroups.retail.push(node);
          node.cluster = 'retail';
        } else if (muleIds.has(node.id)) {
          clusterGroups.mules.push(node);
          node.cluster = 'mules';
        } else if (ringIds.has(node.id)) {
          clusterGroups.rings.push(node);
          node.cluster = 'rings';
        } else {
          clusterGroups.smurfing.push(node);
          node.cluster = 'smurfing';
        }
      });

      Object.keys(clusterGroups).forEach(k => {
        const group = clusterGroups[k];
        const center = clusterCenters[k];
        const subRadius = k === 'smurfing' ? 85 : 70;
        group.forEach((node, idx) => {
          const angle = (idx / group.length) * 2 * Math.PI;
          node.x = center.x + subRadius * Math.cos(angle);
          node.y = center.y + subRadius * Math.sin(angle);
          node.anchorX = center.x;
          node.anchorY = center.y;
          node.radius = 22;
          this.nodeMap.set(node.id, node);
        });
      });
    } else {
      const count = this.nodes.length;
      const radius = Math.min(width, height) * (count <= 5 ? 0.30 : 0.36);
      this.nodes.forEach((node, idx) => {
        const angle = (idx / count) * 2 * Math.PI;
        node.x = cx + radius * Math.cos(angle);
        node.y = cy + radius * Math.sin(angle);
        node.anchorX = cx;
        node.anchorY = cy;
        node.radius = count <= 5 ? 26 : 22;
        this.nodeMap.set(node.id, node);
      });
    }

    for (let i = 0; i < 70; i++) {
      this.tickPhysics();
    }

    this.resetView();
  }

  tickPhysics() {
    for (let i = 0; i < this.nodes.length; i++) {
      for (let j = i + 1; j < this.nodes.length; j++) {
        const n1 = this.nodes[i];
        const n2 = this.nodes[j];
        const dx = n2.x - n1.x;
        const dy = n2.y - n1.y;
        const dist = Math.hypot(dx, dy) || 1;
        const sameCluster = n1.cluster && n2.cluster && n1.cluster === n2.cluster;
        const minDist = this.currentCategory === 'all' ? (sameCluster ? 110 : 250) : 130;
        if (dist < minDist) {
          const force = (minDist - dist) / dist * (sameCluster ? 0.15 : 0.28);
          n1.x -= dx * force;
          n1.y -= dy * force;
          n2.x += dx * force;
          n2.y += dy * force;
        }
      }
    }

    for (const link of this.links) {
      const src = this.nodeMap.get(link.source);
      const dest = this.nodeMap.get(link.target);
      if (src && dest) {
        const dx = dest.x - src.x;
        const dy = dest.y - src.y;
        const dist = Math.hypot(dx, dy) || 1;
        const targetDist = 95;
        const force = (dist - targetDist) * 0.02;
        src.x += (dx / dist) * force;
        src.y += (dy / dist) * force;
        dest.x -= (dx / dist) * force;
        dest.y -= (dy / dist) * force;
      }
    }

    if (this.currentCategory === 'all') {
      for (const node of this.nodes) {
        if (node !== this.draggedNode && node.anchorX !== undefined) {
          node.x += (node.anchorX - node.x) * 0.045;
          node.y += (node.anchorY - node.y) * 0.045;
        }
      }
    }
  }

  initEvents() {
    this.canvas.addEventListener('mousedown', (e) => this.onMouseDown(e));
    this.canvas.addEventListener('mousemove', (e) => this.onMouseMove(e));
    window.addEventListener('mouseup', () => this.onMouseUp());
    this.canvas.addEventListener('wheel', (e) => this.onWheel(e));
  }

  getCanvasMousePos(e) {
    const rect = this.canvas.getBoundingClientRect();
    const clientX = e.clientX - rect.left;
    const clientY = e.clientY - rect.top;
    return {
      x: (clientX - this.panX) / this.scale,
      y: (clientY - this.panY) / this.scale
    };
  }

  findNodeAt(x, y) {
    for (let i = this.nodes.length - 1; i >= 0; i--) {
      const n = this.nodes[i];
      const dist = Math.hypot(n.x - x, n.y - y);
      if (dist <= n.radius + 6) return n;
    }
    return null;
  }

  onMouseDown(e) {
    const pos = this.getCanvasMousePos(e);
    const node = this.findNodeAt(pos.x, pos.y);
    if (node) {
      this.draggedNode = node;
      if (window.onNodeSelected) {
        window.onNodeSelected(node);
      }
    } else {
      this.isDragging = true;
      this.lastMouseX = e.clientX;
      this.lastMouseY = e.clientY;
    }
  }

  onMouseMove(e) {
    const pos = this.getCanvasMousePos(e);
    if (this.draggedNode) {
      this.draggedNode.x = pos.x;
      this.draggedNode.y = pos.y;
    } else if (this.isDragging) {
      this.panX += e.clientX - this.lastMouseX;
      this.panY += e.clientY - this.lastMouseY;
      this.lastMouseX = e.clientX;
      this.lastMouseY = e.clientY;
    } else {
      this.hoveredNode = this.findNodeAt(pos.x, pos.y);
      this.canvas.style.cursor = this.hoveredNode ? 'pointer' : 'default';
    }
  }

  onMouseUp() {
    this.isDragging = false;
    this.draggedNode = null;
  }

  onWheel(e) {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.08 : 0.92;
    this.scale = Math.max(0.3, Math.min(3.0, this.scale * zoomFactor));
  }

  zoomIn() { this.scale = Math.min(3.0, this.scale * 1.15); }
  zoomOut() { this.scale = Math.max(0.3, this.scale * 0.85); }
  resetView() {
    this.scale = 1.0;
    this.panX = 0;
    this.panY = 0;
  }

  highlightCycle(cyclePath) {
    this.clearHighlights();
    for (let i = 0; i < cyclePath.length - 1; i++) {
      this.highlightedCycleNodes.add(cyclePath[i]);
      this.highlightedCycleEdges.add(`${cyclePath[i]}->${cyclePath[i+1]}`);
    }
  }

  highlightShortestPath(pathNodes) {
    this.clearHighlights();
    for (let i = 0; i < pathNodes.length - 1; i++) {
      this.highlightedPathNodes.add(pathNodes[i]);
      this.highlightedPathEdges.add(`${pathNodes[i]}->${pathNodes[i+1]}`);
    }
    this.highlightedPathNodes.add(pathNodes[pathNodes.length - 1]);
  }

  highlightBfs(levelsMap) {
    this.clearHighlights();
    for (const lvl in levelsMap) {
      levelsMap[lvl].forEach(acc => this.highlightedBfsNodes.add(acc));
    }
  }

  clearHighlights() {
    this.highlightedCycleNodes.clear();
    this.highlightedCycleEdges.clear();
    this.highlightedPathNodes.clear();
    this.highlightedPathEdges.clear();
    this.highlightedBfsNodes.clear();
  }

  animate() {
    this.particleOffset = (this.particleOffset + 0.015) % 1.0;
    this.render();
    requestAnimationFrame(this.animate);
  }

  render() {
    const ctx = this.ctx;
    const width = this.canvas.width / window.devicePixelRatio;
    const height = this.canvas.height / window.devicePixelRatio;
    const dark = this.isDark();

    ctx.save();
    ctx.clearRect(0, 0, width, height);

    ctx.translate(this.panX, this.panY);
    ctx.scale(this.scale, this.scale);

    this.drawGrid(ctx, width, height, dark);

    for (const link of this.links) {
      const src = this.nodeMap.get(link.source);
      const dest = this.nodeMap.get(link.target);
      if (!src || !dest) continue;

      const edgeKey = `${link.source}->${link.target}`;
      const isCycleEdge = this.highlightedCycleEdges.has(edgeKey);
      const isPathEdge = this.highlightedPathEdges.has(edgeKey);

      ctx.beginPath();
      ctx.moveTo(src.x, src.y);
      ctx.lineTo(dest.x, dest.y);

      if (isCycleEdge) {
        ctx.strokeStyle = dark ? '#ff334b' : '#dc2626';
        ctx.lineWidth = 3.0;
        ctx.shadowColor = dark ? 'rgba(255, 51, 75, 0.6)' : 'rgba(220, 38, 38, 0.4)';
        ctx.shadowBlur = 12;
      } else if (isPathEdge) {
        ctx.strokeStyle = dark ? '#00e5ff' : '#0284c7';
        ctx.lineWidth = 3.0;
        ctx.shadowColor = dark ? 'rgba(0, 229, 255, 0.6)' : 'rgba(2, 132, 199, 0.4)';
        ctx.shadowBlur = 12;
      } else {
        ctx.strokeStyle = dark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(100, 116, 139, 0.35)';
        ctx.lineWidth = 1.2;
        ctx.shadowBlur = 0;
      }
      ctx.stroke();
      ctx.shadowBlur = 0;

      if (isCycleEdge || isPathEdge) {
        const pX = src.x + (dest.x - src.x) * this.particleOffset;
        const pY = src.y + (dest.y - src.y) * this.particleOffset;
        ctx.beginPath();
        ctx.arc(pX, pY, 3.5, 0, 2 * Math.PI);
        ctx.fillStyle = '#ffffff';
        ctx.shadowColor = isCycleEdge ? (dark ? '#ff334b' : '#dc2626') : (dark ? '#00e5ff' : '#0284c7');
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.shadowBlur = 0;
      }

      this.drawArrowHead(ctx, src.x, src.y, dest.x, dest.y, dest.radius, isCycleEdge ? (dark ? '#ff334b' : '#dc2626') : (isPathEdge ? (dark ? '#00e5ff' : '#0284c7') : (dark ? 'rgba(255, 255, 255, 0.3)' : 'rgba(71, 85, 105, 0.5)')));

      const isConnectedToHover = this.hoveredNode && (this.hoveredNode.id === link.source || this.hoveredNode.id === link.target);
      const shouldShowAmount = isCycleEdge || isPathEdge || (this.currentCategory !== 'all') || isConnectedToHover;

      if (shouldShowAmount) {
        const midX = (src.x + dest.x) / 2;
        const midY = (src.y + dest.y) / 2;
        const labelText = `$${link.amount.toLocaleString()}`;
        ctx.font = '700 12px "JetBrains Mono", monospace';
        const textMetrics = ctx.measureText(labelText);
        const textW = textMetrics.width;

        ctx.fillStyle = dark ? 'rgba(15, 23, 42, 0.94)' : 'rgba(255, 255, 255, 0.96)';
        ctx.strokeStyle = isCycleEdge ? (dark ? '#ff334b' : '#dc2626') : (isPathEdge ? (dark ? '#00e5ff' : '#0284c7') : (dark ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.18)'));
        ctx.lineWidth = (isCycleEdge || isPathEdge || isConnectedToHover) ? 1.5 : 1;
        ctx.beginPath();
        if (ctx.roundRect) {
          ctx.roundRect(midX - textW / 2 - 6, midY - 14, textW + 12, 18, 4);
        } else {
          ctx.rect(midX - textW / 2 - 6, midY - 14, textW + 12, 18);
        }
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = isCycleEdge ? (dark ? '#ff6b81' : '#dc2626') : (isPathEdge ? (dark ? '#38bdf8' : '#0284c7') : (dark ? '#f1f5f9' : '#0f172a'));
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(labelText, midX, midY - 5);
        ctx.textBaseline = 'alphabetic';
      }
    }

    for (const node of this.nodes) {
      const isCycleNode = this.highlightedCycleNodes.has(node.id);
      const isPathNode = this.highlightedPathNodes.has(node.id);
      const isBfsNode = this.highlightedBfsNodes.has(node.id);

      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius + 3, 0, 2 * Math.PI);
      ctx.fillStyle = dark ? 'rgba(11, 14, 20, 0.85)' : '#ffffff';
      ctx.fill();
      ctx.strokeStyle = dark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.12)';
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(node.x, node.y, node.radius, 0, 2 * Math.PI);

      let coreColor = dark ? '#10b981' : '#059669';
      if (node.is_flagged || node.risk_score >= 80) {
        coreColor = dark ? '#ff334b' : '#dc2626';
      } else if (node.risk_score >= 50) {
        coreColor = dark ? '#f59e0b' : '#d97706';
      }

      ctx.fillStyle = coreColor;

      if (isCycleNode) {
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2.5;
        ctx.shadowColor = dark ? 'rgba(255, 51, 75, 0.8)' : 'rgba(220, 38, 38, 0.6)';
        ctx.shadowBlur = 16;
      } else if (isPathNode) {
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2.5;
        ctx.shadowColor = dark ? 'rgba(0, 229, 255, 0.8)' : 'rgba(2, 132, 199, 0.6)';
        ctx.shadowBlur = 16;
      } else if (isBfsNode) {
        ctx.strokeStyle = '#a855f7';
        ctx.lineWidth = 2;
        ctx.shadowBlur = 12;
      } else {
        ctx.strokeStyle = dark ? 'rgba(255, 255, 255, 0.2)' : 'rgba(255, 255, 255, 0.8)';
        ctx.lineWidth = 1.5;
        ctx.shadowBlur = 0;
      }

      ctx.fill();
      ctx.stroke();
      ctx.shadowBlur = 0;

      ctx.beginPath();
      ctx.arc(node.x, node.y, 4, 0, 2 * Math.PI);
      ctx.fillStyle = '#ffffff';
      ctx.fill();

      ctx.font = '700 13px "JetBrains Mono", monospace';
      ctx.fillStyle = dark ? '#ffffff' : '#0f172a';
      ctx.textAlign = 'center';
      ctx.fillText(node.id, node.x, node.y + node.radius + 16);

      ctx.font = '600 11.5px "Plus Jakarta Sans", sans-serif';
      ctx.fillStyle = dark ? '#94a3b8' : '#475569';
      const shortName = node.name.length > 17 ? node.name.slice(0, 15) + '..' : node.name;
      ctx.fillText(shortName, node.x, node.y + node.radius + 31);
    }

    if (this.hoveredNode) {
      this.drawDossierTooltip(ctx, this.hoveredNode, dark);
    }

    ctx.restore();
  }

  drawGrid(ctx, width, height, dark) {
    const gridSize = 45;
    const startX = -this.panX / this.scale - gridSize;
    const startY = -this.panY / this.scale - gridSize;
    const endX = startX + width / this.scale + gridSize * 2;
    const endY = startY + height / this.scale + gridSize * 2;

    ctx.beginPath();
    ctx.fillStyle = dark ? 'rgba(255, 255, 255, 0.04)' : 'rgba(15, 23, 42, 0.06)';
    for (let x = startX - (startX % gridSize); x < endX; x += gridSize) {
      for (let y = startY - (startY % gridSize); y < endY; y += gridSize) {
        ctx.fillRect(x, y, 1.2, 1.2);
      }
    }
  }

  drawArrowHead(ctx, fromX, fromY, toX, toY, targetRadius, color) {
    const angle = Math.atan2(toY - fromY, toX - fromX);
    const arrowX = toX - (targetRadius + 2) * Math.cos(angle);
    const arrowY = toY - (targetRadius + 2) * Math.sin(angle);
    const headLen = 6.5;

    ctx.save();
    ctx.beginPath();
    ctx.moveTo(arrowX, arrowY);
    ctx.lineTo(arrowX - headLen * Math.cos(angle - Math.PI / 6), arrowY - headLen * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(arrowX - headLen * Math.cos(angle + Math.PI / 6), arrowY - headLen * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    ctx.restore();
  }

  drawDossierTooltip(ctx, node, dark) {
    const boxW = 215;
    const boxH = 92;
    const boxX = node.x + node.radius + 12;
    const boxY = node.y - 25;

    ctx.fillStyle = dark ? 'rgba(11, 14, 20, 0.96)' : 'rgba(255, 255, 255, 0.98)';
    ctx.strokeStyle = dark ? 'rgba(255, 255, 255, 0.15)' : 'rgba(0, 0, 0, 0.15)';
    ctx.lineWidth = 1;
    ctx.fillRect(boxX, boxY, boxW, boxH);
    ctx.strokeRect(boxX, boxY, boxW, boxH);

    ctx.textAlign = 'left';
    ctx.font = '700 13px "JetBrains Mono", monospace';
    ctx.fillStyle = dark ? '#00e5ff' : '#0284c7';
    ctx.fillText(node.id, boxX + 12, boxY + 22);

    ctx.font = '600 12px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = dark ? '#e2e8f0' : '#0f172a';
    ctx.fillText(node.name, boxX + 12, boxY + 41);

    ctx.font = '700 11px "Plus Jakarta Sans", sans-serif';
    ctx.fillStyle = node.risk_score >= 80 ? (dark ? '#ff334b' : '#dc2626') : (node.risk_score >= 50 ? (dark ? '#f59e0b' : '#d97706') : (dark ? '#10b981' : '#059669'));
    ctx.fillText(`RISK FACTOR: ${node.risk_score}%`, boxX + 12, boxY + 61);

    ctx.font = '600 11.5px "JetBrains Mono", monospace';
    ctx.fillStyle = dark ? '#94a3b8' : '#475569';
    ctx.fillText(`BALANCE: $${node.balance.toLocaleString()}`, boxX + 12, boxY + 79);
  }
}
