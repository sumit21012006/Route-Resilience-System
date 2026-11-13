"""
Generate a comprehensive PDF document explaining the Route Resilience System project.
Uses reportlab (already installed in backend venv).
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem, KeepTogether, HRFlowable
)
from reportlab.lib import colors
import os

# ── Output path ──
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Route_Resilience_System.pdf")

# ── Colours ──
PRIMARY   = HexColor("#1a237e")  # Deep indigo
ACCENT    = HexColor("#0d47a1")  # Blue
LIGHT_BG  = HexColor("#e8eaf6")  # Light indigo background
TABLE_HDR = HexColor("#1565c0")  # Table header blue
DARK_TEXT  = HexColor("#212121")
GREY_TEXT  = HexColor("#616161")
GREEN      = HexColor("#2e7d32")
ORANGE     = HexColor("#e65100")

# ── Styles ──
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    "CoverTitle", parent=styles["Title"],
    fontSize=36, leading=44, textColor=PRIMARY,
    alignment=TA_CENTER, spaceAfter=20, fontName="Helvetica-Bold"
))
styles.add(ParagraphStyle(
    "CoverSubtitle", parent=styles["Normal"],
    fontSize=16, leading=22, textColor=ACCENT,
    alignment=TA_CENTER, spaceAfter=8
))
styles.add(ParagraphStyle(
    "CoverDetail", parent=styles["Normal"],
    fontSize=12, leading=16, textColor=GREY_TEXT,
    alignment=TA_CENTER, spaceAfter=4
))
styles.add(ParagraphStyle(
    "SectionTitle", parent=styles["Heading1"],
    fontSize=22, leading=28, textColor=PRIMARY,
    spaceBefore=24, spaceAfter=12, fontName="Helvetica-Bold"
))
styles.add(ParagraphStyle(
    "SubSection", parent=styles["Heading2"],
    fontSize=16, leading=20, textColor=ACCENT,
    spaceBefore=16, spaceAfter=8, fontName="Helvetica-Bold"
))
styles.add(ParagraphStyle(
    "SubSubSection", parent=styles["Heading3"],
    fontSize=13, leading=17, textColor=HexColor("#1565c0"),
    spaceBefore=10, spaceAfter=6, fontName="Helvetica-Bold"
))
styles.add(ParagraphStyle(
    "BodyText2", parent=styles["Normal"],
    fontSize=11, leading=16, textColor=DARK_TEXT,
    alignment=TA_JUSTIFY, spaceAfter=8
))
styles.add(ParagraphStyle(
    "BulletText", parent=styles["Normal"],
    fontSize=11, leading=16, textColor=DARK_TEXT,
    leftIndent=20, spaceAfter=4
))
styles.add(ParagraphStyle(
    "CodeStyle", parent=styles["Normal"],
    fontSize=9, leading=13, fontName="Courier",
    textColor=HexColor("#37474f"), leftIndent=16, spaceAfter=4,
    backColor=HexColor("#f5f5f5")
))
styles.add(ParagraphStyle(
    "SmallNote", parent=styles["Normal"],
    fontSize=9, leading=12, textColor=GREY_TEXT,
    alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    "TOCEntry", parent=styles["Normal"],
    fontSize=12, leading=18, textColor=ACCENT,
    leftIndent=10, spaceAfter=4
))

# ── Helpers ──
def heading(text):
    return Paragraph(text, styles["SectionTitle"])

def subheading(text):
    return Paragraph(text, styles["SubSection"])

def subsubheading(text):
    return Paragraph(text, styles["SubSubSection"])

def body(text):
    return Paragraph(text, styles["BodyText2"])

def bullet(text):
    return Paragraph(f"• {text}", styles["BulletText"])

def code(text):
    return Paragraph(text, styles["CodeStyle"])

def spacer(h=12):
    return Spacer(1, h)

def hr():
    return HRFlowable(width="100%", thickness=1, color=HexColor("#bdbdbd"), spaceAfter=10, spaceBefore=10)

def make_table(headers, rows, col_widths=None):
    """Create a styled table."""
    data = [headers] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HDR),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME",  (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",  (0, 0), (-1, 0), 10),
        ("FONTSIZE",  (0, 1), (-1, -1), 9),
        ("LEADING",   (0, 0), (-1, -1), 14),
        ("ALIGN",     (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",    (0, 0), (-1, -1), "TOP"),
        ("GRID",      (0, 0), (-1, -1), 0.5, HexColor("#bdbdbd")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 6),
    ]
    t.setStyle(TableStyle(style))
    return t

# ── Page number footer ──
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY_TEXT)
    canvas.drawCentredString(A4[0] / 2, 30, f"Route Resilience System  —  Page {doc.page}")
    canvas.restoreState()

# ══════════════════════════════════════════════════════════════
# BUILD THE DOCUMENT
# ══════════════════════════════════════════════════════════════
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=1.2*cm, rightMargin=1.2*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)
story = []
W = A4[0] - 2.4*cm  # usable width

# ════════════════════════════════════════
# COVER PAGE
# ════════════════════════════════════════
story.append(Spacer(1, 2.5*inch))
story.append(Paragraph("Route Resilience System", styles["CoverTitle"]))
story.append(Spacer(1, 10))
story.append(HRFlowable(width="60%", thickness=2, color=PRIMARY, spaceAfter=14, spaceBefore=6))
story.append(Paragraph("Urban Road-Network Resilience Analysis Platform", styles["CoverSubtitle"]))
story.append(Spacer(1, 20))
story.append(Paragraph("A graph-theoretic approach to identifying critical junctions,<br/>"
                        "simulating disaster scenarios, and planning resilient interventions<br/>"
                        "for urban road networks using satellite imagery and geospatial data.",
                        styles["CoverDetail"]))
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("Technology Stack: Python · FastAPI · Next.js · NetworkX · OSMnx · PyTorch", styles["CoverDetail"]))
story.append(PageBreak())

# ════════════════════════════════════════
# TABLE OF CONTENTS
# ════════════════════════════════════════
story.append(heading("Table of Contents"))
story.append(hr())
toc_items = [
    "1.  Project Overview",
    "2.  Problem Statement",
    "3.  System Architecture & Pipeline",
    "4.  Technology Stack",
    "5.  Directory Structure",
    "6.  Backend — Core Modules",
    "7.  Frontend — User Interface Pages",
    "8.  API Reference",
    "9.  Graph Metrics & Key Statistics",
    "10. Disaster Simulation Engine",
    "11. ML / AI Components",
    "12. External Integrations",
    "13. Feature Coverage Matrix",
    "14. Setup & Quick Start Guide",
    "15. Environment Variables",
    "16. Future Scope",
]
for item in toc_items:
    story.append(Paragraph(item, styles["TOCEntry"]))
story.append(PageBreak())

# ════════════════════════════════════════
# 1. PROJECT OVERVIEW
# ════════════════════════════════════════
story.append(heading("1. Project Overview"))
story.append(body(
    "The <b>Route Resilience System</b> is a full-stack web application that performs "
    "<b>graph-theoretic resilience analysis</b> on urban road networks. It ingests real-world "
    "geospatial data — street graphs from OpenStreetMap, satellite imagery, population density, "
    "and digital elevation models — to build a weighted road graph and then quantifies how "
    "robust the network is against disruptions such as natural disasters, flooding, landslides, "
    "and infrastructure failures."
))
story.append(body(
    "The platform enables city planners, disaster-management authorities, and researchers to:"
))
story.append(bullet("Identify <b>critical junctions</b> whose failure would fragment the road network."))
story.append(bullet("Run <b>disaster simulations</b> (seismic, flood, cascade failure) and observe network degradation."))
story.append(bullet("<b>Simulate counterfactual interventions</b> — bridge additions, bypass roads — and measure their impact."))
story.append(bullet("Visualise <b>criticality heatmaps</b> on interactive Leaflet maps."))
story.append(bullet("Generate <b>automated reports</b> with resilience scores and recommendations."))
story.append(bullet("Interact with an <b>AI Copilot</b> (Groq LLM) for natural-language Q&A about the network."))
story.append(spacer())

# ════════════════════════════════════════
# 2. PROBLEM STATEMENT
# ════════════════════════════════════════
story.append(heading("2. Problem Statement"))
story.append(body(
    "Urban road networks are the backbone of a city's logistics, emergency response, and daily commute. "
    "Yet, most cities lack tooling to answer a simple question: <i>\"If a key junction or road segment fails, "
    "how badly is the network affected, and what can we do about it?\"</i>"
))
story.append(body(
    "This project addresses <b>ISRO NNRMS Hackathon 2026 — Problem Statement PS4</b>: "
    "<i>Urban Road Network Resilience Analysis using Satellite Imagery and Graph Theory</i>. "
    "The objective is to extract road networks from satellite imagery, convert them into weighted graphs, "
    "and apply centrality and resilience metrics to identify vulnerabilities."
))
story.append(spacer())

# ════════════════════════════════════════
# 3. SYSTEM ARCHITECTURE & PIPELINE
# ════════════════════════════════════════
story.append(heading("3. System Architecture & Pipeline"))
story.append(body("The system follows a <b>multi-stage pipeline</b> architecture:"))
story.append(spacer(8))

pipeline_data = [
    ["Stage", "Component", "Description"],
    ["1", "Data Ingestion", "Fetch road graph from OpenStreetMap via OSMnx / Overpass API; "
         "ingest satellite imagery, DEM tiles, population rasters."],
    ["2", "Road Extraction (ML)", "Optional U-Net segmentation model extracts road pixels from "
         "satellite imagery and skeletonizes them into a graph."],
    ["3", "Graph Construction", "Build a NetworkX weighted graph: nodes = intersections, "
         "edges = road segments weighted by length, speed, lanes, and surface quality."],
    ["4", "Metric Computation", "Compute centrality scores (betweenness, closeness, degree, "
         "eigenvector), MST fraction, algebraic connectivity, global efficiency."],
    ["5", "Criticality Analysis", "Rank junctions by composite criticality; identify bridges "
         "and articulation points."],
    ["6", "Disaster Simulation", "Remove nodes/edges matching a hazard scenario; measure "
         "fragmentation, detour lengths, population isolation."],
    ["7", "Counterfactual Healing", "Simulate adding bypass edges; re-measure metrics; "
         "compute resilience gain."],
    ["8", "Visualisation & Reports", "Serve interactive maps, charts, and downloadable PDF/HTML "
         "reports via the web dashboard."],
]
story.append(make_table(pipeline_data[0], pipeline_data[1:], col_widths=[0.06*W, 0.2*W, 0.74*W]))
story.append(spacer())

story.append(subheading("High-Level Data Flow"))
story.append(code("Satellite Imagery / OSM Data"))
story.append(code("        ↓"))
story.append(code("  Road Extraction (U-Net) / OSMnx Graph Download"))
story.append(code("        ↓"))
story.append(code("  Graph Construction (NetworkX weighted graph)"))
story.append(code("        ↓"))
story.append(code("  Centrality & Resilience Metrics"))
story.append(code("        ↓"))
story.append(code("  Critical Junction Detection"))
story.append(code("        ↓"))
story.append(code("  Disaster Simulation  ←→  Counterfactual Interventions"))
story.append(code("        ↓"))
story.append(code("  Dashboard + Reports + AI Copilot"))
story.append(PageBreak())

# ════════════════════════════════════════
# 4. TECHNOLOGY STACK
# ════════════════════════════════════════
story.append(heading("4. Technology Stack"))
story.append(spacer(6))

tech_rows = [
    ["Frontend Framework",   "Next.js 14.2.3 (React 18)"],
    ["UI / Styling",         "Tailwind CSS, Radix UI, shadcn/ui components"],
    ["Maps",                 "Leaflet + react-leaflet"],
    ["Charts",               "Recharts"],
    ["Language (Frontend)",  "TypeScript"],
    ["Backend Framework",    "FastAPI (Python)"],
    ["Graph Library",        "NetworkX"],
    ["Geospatial",           "OSMnx, GeoPandas, Shapely, pyproj, rasterio"],
    ["ML / DL",              "PyTorch, torchvision, segmentation-models-pytorch (optional)"],
    ["LLM Integration",      "Groq API (Llama / Mixtral via groq-sdk)"],
    ["HTTP Server",          "Uvicorn (ASGI)"],
    ["Data Formats",         "GeoJSON, GeoPackage (GPKG), GeoPickle, CSV"],
    ["Package Manager",      "pip (backend), npm (frontend)"],
    ["Version Control",      "Git + GitHub"],
]
story.append(make_table(["Category", "Technology"], tech_rows, col_widths=[0.3*W, 0.7*W]))
story.append(PageBreak())

# ════════════════════════════════════════
# 5. DIRECTORY STRUCTURE
# ════════════════════════════════════════
story.append(heading("5. Directory Structure"))
story.append(spacer(6))

dir_lines = [
    "route-resilience/",
    "├── backend/",
    "│   ├── app/",
    "│   │   ├── main.py                  # FastAPI entry point, CORS, lifespan",
    "│   │   ├── api/                     # API route modules",
    "│   │   │   ├── graph.py             # /graph/* endpoints",
    "│   │   │   ├── simulation.py        # /simulate/* endpoints",
    "│   │   │   ├── accessibility.py     # /accessibility/* endpoints",
    "│   │   │   ├── copilot.py           # /copilot/* endpoints",
    "│   │   │   ├── reports.py           # /reports/* endpoints",
    "│   │   │   ├── bhuvan.py            # /bhuvan/* endpoints",
    "│   │   │   └── segmentation.py      # /segment/* endpoints",
    "│   │   ├── graph_pipeline/          # Core graph analysis",
    "│   │   │   ├── graph_build.py       # Graph construction & loading",
    "│   │   │   ├── centrality.py        # Centrality computations",
    "│   │   │   ├── metrics.py           # Network resilience metrics",
    "│   │   │   ├── mst_healing.py       # MST-based healing strategies",
    "│   │   │   ├── skeletonize.py       # Image → skeleton → graph",
    "│   │   │   └── fingerprint.py       # Graph fingerprinting",
    "│   │   ├── simulation/              # Disaster simulation modules",
    "│   │   │   ├── ablation.py          # Node/edge ablation",
    "│   │   │   ├── cascade.py           # Cascade failure model",
    "│   │   │   ├── resilience.py        # Resilience score computation",
    "│   │   │   ├── scenarios.py         # Predefined disaster scenarios",
    "│   │   │   ├── routing.py           # Shortest-path routing",
    "│   │   │   ├── fragility.py         # Fragility curves",
    "│   │   │   ├── recommendations.py   # Automated recommendations",
    "│   │   │   ├── population.py        # Population impact analysis",
    "│   │   │   ├── topography.py        # Elevation-based analysis",
    "│   │   │   ├── evacuation.py        # Evacuation route planning",
    "│   │   │   ├── equity.py            # Equity-weighted analysis",
    "│   │   │   ├── traffic_impact.py    # Traffic flow impact",
    "│   │   │   ├── temporal_degradation.py # Time-based degradation",
    "│   │   │   └── timeline.py          # Event timeline tracking",
    "│   │   ├── integrations/            # External service clients",
    "│   │   │   ├── bhuvan.py            # ISRO Bhuvan tile proxy",
    "│   │   │   ├── groq_client.py       # Groq LLM integration",
    "│   │   │   ├── nominatim.py         # Geocoding via Nominatim",
    "│   │   │   └── overpass.py          # Overpass API client",
    "│   │   ├── ml/                      # Machine learning pipeline",
    "│   │   │   ├── model.py             # U-Net architecture",
    "│   │   │   ├── inference.py         # Model inference",
    "│   │   │   ├── train.py             # Training loop",
    "│   │   │   ├── augmentations.py     # Data augmentations",
    "│   │   │   ├── explain.py           # Grad-CAM explanations",
    "│   │   │   └── change_detection.py  # Temporal change detection",
    "│   │   └── reports/",
    "│   │       └── generator.py         # PDF/HTML report generation",
    "│   ├── data/                        # Generated data (gitignored)",
    "│   ├── cache/                       # Overpass API cache",
    "│   ├── scripts/",
    "│   │   └── download_data.py         # Data download utility",
    "│   ├── requirements.txt             # Full dependency list",
    "│   └── requirements-core.txt        # Core dependencies only",
    "├── frontend/",
    "│   ├── app/                         # Next.js App Router pages",
    "│   │   ├── page.tsx                 # Dashboard (home page)",
    "│   │   ├── map/page.tsx             # Criticality Heatmap",
    "│   │   ├── simulate/page.tsx        # Disaster Simulation",
    "│   │   ├── analytics/page.tsx       # Analytics dashboard",
    "│   │   ├── copilot/page.tsx         # AI Copilot chat",
    "│   │   ├── reports/page.tsx         # Report generation",
    "│   │   └── explain/page.tsx         # ML Explanation / Segmentation",
    "│   ├── components/                  # Reusable React components",
    "│   ├── lib/                         # Utility functions & API client",
    "│   └── package.json",
    "├── experiments/                     # Research experiment logs",
    "├── .env.example                     # Environment variable template",
    "├── start_demo.ps1                   # Windows demo launcher",
    "└── README.md",
]
for line in dir_lines:
    story.append(code(line))
story.append(PageBreak())

# ════════════════════════════════════════
# 6. BACKEND — CORE MODULES
# ════════════════════════════════════════
story.append(heading("6. Backend — Core Modules"))

# 6.1 Graph Pipeline
story.append(subheading("6.1  Graph Pipeline"))
story.append(body(
    "The graph pipeline is the heart of the system. It handles building the road network graph "
    "from raw geospatial data and computing all resilience-related metrics."
))

modules_gp = [
    ["graph_build.py", "Loads the road network from OpenStreetMap via OSMnx. Supports bounding-box "
     "queries with configurable AOI (default: Bengaluru). Caches the graph as a GeoPickle "
     "file. Adds edge weights based on road length, speed limits, number of lanes, and surface type. "
     "Falls back to a pre-cached Overpass response if the network is unavailable."],
    ["centrality.py", "Computes node-level centrality measures: betweenness centrality, closeness "
     "centrality, degree centrality, eigenvector centrality. Each metric highlights different "
     "aspects of a node's importance in the network."],
    ["metrics.py", "Calculates global network metrics: algebraic connectivity (Fiedler value), "
     "global efficiency, average clustering coefficient, MST fraction, network diameter, "
     "number of connected components, average path length."],
    ["mst_healing.py", "Implements MST-based graph healing: identifies the minimum spanning tree "
     "of the damaged network, proposes new edges to reconnect fragmented components, and "
     "measures the cost-benefit of each proposed edge."],
    ["skeletonize.py", "Converts binary road segmentation masks into 1-pixel-wide skeletons using "
     "morphological thinning, then extracts a graph (nodes at junctions, edges along segments) "
     "from the skeleton."],
    ["fingerprint.py", "Creates a compact 'fingerprint' of the graph topology — degree distribution, "
     "centrality histograms — for quick comparison between pre- and post-disaster states."],
]
story.append(make_table(["Module", "Description"], modules_gp, col_widths=[0.22*W, 0.78*W]))
story.append(spacer())

# 6.2 Simulation Engine
story.append(subheading("6.2  Simulation Engine"))
story.append(body(
    "The simulation package models different disaster scenarios and quantifies their impact "
    "on the road network."
))

modules_sim = [
    ["ablation.py", "Removes a set of nodes or edges from the graph and measures resulting fragmentation."],
    ["cascade.py", "Models cascade failure: removing one node overloads its neighbors, which may "
     "also fail, triggering a chain reaction."],
    ["resilience.py", "Computes the resilience score — the fraction of network functionality retained "
     "after a disruption."],
    ["scenarios.py", "Predefined disaster scenarios: earthquake, flood, landslide, targeted attack. "
     "Each scenario defines which nodes/edges are affected based on spatial and attribute criteria."],
    ["routing.py", "Computes shortest paths and detour analysis: how much longer do routes become "
     "when critical links are removed?"],
    ["fragility.py", "Fragility curve modeling for structural elements under varying hazard intensities."],
    ["population.py", "Overlays population density data (WorldPop) to estimate how many people are "
     "affected by network disruption."],
    ["topography.py", "Uses DEM (elevation) data to identify flood-prone low-lying areas and steep "
     "gradients that affect road vulnerability."],
    ["evacuation.py", "Plans evacuation routes from affected zones to safe shelters, considering "
     "road capacity and damage."],
    ["equity.py", "Equity-weighted analysis: ensures that vulnerable / underserved communities "
     "are not disproportionately affected by network failures."],
    ["traffic_impact.py", "Estimates traffic rerouting costs, congestion buildup, and vehicle-hours "
     "of delay caused by disruptions."],
    ["temporal_degradation.py", "Models how road quality degrades over time without maintenance."],
    ["timeline.py", "Tracks the event timeline of a simulated disaster for step-by-step replay."],
    ["recommendations.py", "Generates automated recommendations: priority repairs, new road "
     "construction, traffic rerouting suggestions."],
]
story.append(make_table(["Module", "Description"], modules_sim, col_widths=[0.25*W, 0.75*W]))
story.append(PageBreak())

# 6.3 Integrations
story.append(subheading("6.3  External Integrations"))
modules_int = [
    ["bhuvan.py", "Proxies satellite imagery tiles from ISRO's Bhuvan geoportal for map overlays."],
    ["groq_client.py", "Connects to the Groq API for LLM-powered natural-language Q&A (Copilot feature). "
     "Supports Llama and Mixtral models."],
    ["nominatim.py", "Geocoding: converts place names to coordinates and vice versa via OpenStreetMap Nominatim."],
    ["overpass.py", "Queries the Overpass API for raw OpenStreetMap data (roads, buildings, POIs) "
     "within the area of interest."],
]
story.append(make_table(["Module", "Description"], modules_int, col_widths=[0.22*W, 0.78*W]))
story.append(spacer())

# 6.4 ML Pipeline
story.append(subheading("6.4  Machine Learning Pipeline"))
story.append(body(
    "An <b>optional</b> ML pipeline (enabled via <font face='Courier'>ENABLE_ML=true</font>) "
    "provides satellite-image-based road extraction. It is disabled by default because it "
    "requires a trained model checkpoint and GPU resources."
))
modules_ml = [
    ["model.py", "Defines the U-Net architecture (encoder–decoder with skip connections) for "
     "semantic segmentation of road pixels in satellite imagery."],
    ["inference.py", "Loads a trained checkpoint and runs inference on new satellite tiles, "
     "producing binary road masks."],
    ["train.py", "Training loop with configurable epochs, learning rate, augmentations, "
     "and validation split."],
    ["augmentations.py", "Data augmentation pipeline: random flips, rotations, colour jitter, "
     "Gaussian blur for training robustness."],
    ["explain.py", "Grad-CAM heatmaps showing which image regions the model focuses on for "
     "road detection — aids interpretability."],
    ["change_detection.py", "Compares road masks from two time periods to detect new construction "
     "or road damage."],
]
story.append(make_table(["Module", "Description"], modules_ml, col_widths=[0.22*W, 0.78*W]))
story.append(spacer())

# 6.5 Reports
story.append(subheading("6.5  Report Generator"))
story.append(body(
    "The <font face='Courier'>reports/generator.py</font> module produces downloadable PDF and "
    "HTML reports summarizing the current state of the network, criticality rankings, simulation "
    "results, and intervention recommendations. Reports are generated on demand via the "
    "<font face='Courier'>/reports/generate</font> API endpoint."
))
story.append(PageBreak())

# ════════════════════════════════════════
# 7. FRONTEND — UI PAGES
# ════════════════════════════════════════
story.append(heading("7. Frontend — User Interface Pages"))
story.append(body(
    "The frontend is built with <b>Next.js 14</b> using the App Router. It provides 7 main pages, "
    "each connected to the backend API. The UI uses <b>shadcn/ui</b> components (Radix UI primitives "
    "styled with Tailwind CSS) for a consistent, modern look."
))
story.append(spacer(6))

pages = [
    ["/ (Dashboard)", "Home page showing a high-level overview: network health score, total nodes "
     "and edges, top critical junctions, quick-action cards linking to simulation and reports."],
    ["/map (Heatmap)", "Interactive Leaflet map overlaying a criticality heatmap on the road network. "
     "Nodes are colour-coded by their composite criticality score (red = most critical). "
     "Supports toggling different centrality layers and Bhuvan satellite imagery."],
    ["/simulate", "Disaster simulation interface. Users select a scenario (earthquake, flood, "
     "targeted attack, custom), configure parameters (intensity, radius, affected area), run "
     "the simulation, and see before/after comparisons of network metrics."],
    ["/analytics", "Charts and visualisations: centrality distributions (histograms), degree "
     "distribution (log-log plot), resilience curves, temporal degradation trends. Built with Recharts."],
    ["/copilot", "Chat interface for the AI Copilot. Users ask natural-language questions about "
     "the network (e.g., \"Which junction, if removed, causes the biggest drop in efficiency?\") "
     "and get context-aware answers powered by the Groq LLM."],
    ["/reports", "Report generation page. Users can configure report parameters and generate "
     "downloadable PDF/HTML resilience reports."],
    ["/explain", "ML explanation page (when ML is enabled). Shows segmentation masks overlaid on "
     "satellite imagery, Grad-CAM attention maps, and change-detection results."],
]
story.append(make_table(["Page", "Description"], pages, col_widths=[0.2*W, 0.8*W]))
story.append(PageBreak())

# ════════════════════════════════════════
# 8. API REFERENCE
# ════════════════════════════════════════
story.append(heading("8. API Reference"))
story.append(body(
    "The backend exposes <b>32+ RESTful endpoints</b> organised under these routers. "
    "All endpoints return JSON."
))
story.append(spacer(6))

api_rows = [
    # Graph
    ["GET",  "/graph/metrics",           "Global network metrics (efficiency, connectivity, etc.)"],
    ["GET",  "/graph/centrality",        "Node-level centrality scores"],
    ["GET",  "/graph/critical-junctions","Top-N most critical junctions"],
    ["GET",  "/graph/geojson",           "Full graph as GeoJSON (nodes + edges)"],
    ["GET",  "/graph/summary",           "Summary statistics: node/edge counts, bounding box"],
    ["GET",  "/graph/mst",               "Minimum Spanning Tree of the graph"],
    ["GET",  "/graph/fingerprint",       "Graph topology fingerprint"],
    ["GET",  "/graph/components",        "Connected component analysis"],
    ["GET",  "/graph/bridges",           "Bridge edges (whose removal disconnects components)"],
    # Simulation
    ["POST", "/simulate/scenario",       "Run a named disaster scenario"],
    ["POST", "/simulate/cascade",        "Run cascade-failure simulation"],
    ["POST", "/simulate/ablation",       "Remove specific nodes/edges and measure impact"],
    ["POST", "/simulate/resilience",     "Compute resilience score for a disruption"],
    ["POST", "/simulate/evacuation",     "Plan evacuation routes"],
    ["POST", "/simulate/equity",         "Equity-weighted disruption analysis"],
    ["POST", "/simulate/traffic-impact", "Traffic rerouting cost estimation"],
    ["POST", "/simulate/temporal",       "Temporal degradation simulation"],
    ["POST", "/simulate/recommendations","Get repair / intervention recommendations"],
    ["GET",  "/simulate/scenarios",      "List available predefined scenarios"],
    # Accessibility
    ["GET",  "/accessibility/isochrone", "Travel-time isochrone from a given node"],
    ["GET",  "/accessibility/score",     "Accessibility score for a location"],
    # Copilot
    ["POST", "/copilot/ask",             "Send a natural-language question to the AI copilot"],
    ["GET",  "/copilot/context",         "Retrieve current graph context for the LLM"],
    # Reports
    ["POST", "/reports/generate",        "Generate a PDF/HTML resilience report"],
    ["GET",  "/reports/list",            "List previously generated reports"],
    # Bhuvan
    ["GET",  "/bhuvan/tile/{z}/{x}/{y}", "Proxy ISRO Bhuvan satellite tiles"],
    ["GET",  "/bhuvan/dem",              "Fetch DEM elevation data for the AOI"],
    # Segmentation (ML)
    ["POST", "/segment/predict",         "Run road segmentation on an uploaded image"],
    ["POST", "/segment/explain",         "Generate Grad-CAM explanation for a segmentation"],
    ["POST", "/segment/change",          "Detect road changes between two images"],
    # Health
    ["GET",  "/health",                  "Health check — returns {status: 'ok'}"],
    ["GET",  "/",                        "Root — returns welcome message"],
]
story.append(make_table(["Method", "Endpoint", "Description"], api_rows,
                        col_widths=[0.08*W, 0.35*W, 0.57*W]))
story.append(PageBreak())

# ════════════════════════════════════════
# 9. GRAPH METRICS
# ════════════════════════════════════════
story.append(heading("9. Graph Metrics & Key Statistics"))
story.append(body(
    "When loaded with the default Bengaluru AOI (Area of Interest), the graph has the following "
    "characteristics:"
))
story.append(spacer(6))

stats_rows = [
    ["Total Nodes (Intersections)", "13,486"],
    ["Total Edges (Road Segments)",  "19,117"],
    ["Graph Type",                   "MultiDiGraph (directed, multi-edge)"],
    ["Coordinate System",           "WGS 84 (EPSG:4326)"],
    ["Average Node Degree",         "~2.84"],
    ["Network Diameter",            "Computed dynamically on largest connected component"],
]
story.append(make_table(["Metric", "Value"], stats_rows, col_widths=[0.4*W, 0.6*W]))
story.append(spacer())

story.append(subheading("Resilience Metrics Explained"))
metrics_explained = [
    ["Global Efficiency", "Average inverse shortest-path length between all node pairs. "
     "Higher = better connected. Ranges 0–1."],
    ["Algebraic Connectivity", "Second-smallest eigenvalue of the Laplacian. Measures how "
     "hard it is to partition the graph. Higher = more resilient."],
    ["MST Fraction", "Ratio of MST weight to total edge weight. Lower = more redundancy "
     "(good for resilience)."],
    ["Average Clustering", "Mean local clustering coefficient. Higher = more triangles / "
     "alternate routes at the local level."],
    ["Connected Components", "Number of disconnected subgraphs. Ideally 1 (fully connected). "
     "Increases after disruptions."],
    ["Betweenness Centrality", "Fraction of shortest paths passing through a node. High "
     "betweenness = critical bottleneck."],
    ["Closeness Centrality", "Inverse of the sum of shortest distances from a node to all "
     "others. High closeness = well-positioned."],
]
story.append(make_table(["Metric", "Meaning"], metrics_explained, col_widths=[0.28*W, 0.72*W]))
story.append(PageBreak())

# ════════════════════════════════════════
# 10. DISASTER SIMULATION ENGINE
# ════════════════════════════════════════
story.append(heading("10. Disaster Simulation Engine"))
story.append(body(
    "The simulation engine is the analytical core of the system. It models various disaster "
    "scenarios and quantifies their impact through multiple lenses."
))
story.append(spacer(6))

story.append(subheading("10.1 Scenario Types"))
scenario_rows = [
    ["Earthquake", "Removes nodes/edges within a radius of the epicentre based on seismic intensity "
     "and fragility curves."],
    ["Flood", "Disables low-elevation road segments (below a configurable water level) using DEM data."],
    ["Landslide", "Targets steep-gradient road segments identified from elevation profiles."],
    ["Targeted Attack", "Removes the top-N most critical nodes (by betweenness centrality) to simulate "
     "worst-case deliberate disruption."],
    ["Random Failure", "Randomly removes a percentage of nodes/edges to model stochastic infrastructure decay."],
    ["Custom", "User-defined: select specific nodes/edges or draw a polygon on the map."],
]
story.append(make_table(["Scenario", "Mechanism"], scenario_rows, col_widths=[0.2*W, 0.8*W]))
story.append(spacer())

story.append(subheading("10.2 Simulation Outputs"))
story.append(bullet("<b>Before / After Metrics:</b> Global efficiency, algebraic connectivity, connected components — compared side-by-side."))
story.append(bullet("<b>Fragmentation Map:</b> GeoJSON of disconnected components, colour-coded by size."))
story.append(bullet("<b>Detour Analysis:</b> For critical OD pairs, the increase in travel time/distance."))
story.append(bullet("<b>Population Impact:</b> Estimated number of people in isolated network fragments."))
story.append(bullet("<b>Cascade Propagation:</b> Step-by-step timeline of which nodes fail in sequence."))
story.append(bullet("<b>Recommendations:</b> Prioritised list of edges to add/repair for maximum resilience recovery."))
story.append(spacer())

story.append(subheading("10.3 Counterfactual Interventions"))
story.append(body(
    "After a simulation, the system can propose <b>healing interventions</b>:"
))
story.append(bullet("MST-based reconnection of fragmented components."))
story.append(bullet("Bridge / bypass road insertion at optimal locations."))
story.append(bullet("Each proposed intervention includes a cost estimate (road length) and "
                    "resilience gain (Δ efficiency, Δ connectivity)."))
story.append(PageBreak())

# ════════════════════════════════════════
# 11. ML / AI COMPONENTS
# ════════════════════════════════════════
story.append(heading("11. ML / AI Components"))

story.append(subheading("11.1 Road Segmentation (U-Net)"))
story.append(body(
    "The optional ML pipeline uses a <b>U-Net</b> encoder-decoder architecture for semantic "
    "segmentation of road pixels in satellite imagery. The encoder uses a pretrained ResNet "
    "backbone, while the decoder upsamples feature maps with skip connections to produce a "
    "pixel-wise binary mask (road vs. non-road)."
))
story.append(bullet("Input: 256×256 satellite image tiles"))
story.append(bullet("Output: Binary segmentation mask"))
story.append(bullet("Loss: Binary cross-entropy + Dice loss"))
story.append(bullet("Augmentations: Random flips, rotations, colour jitter, Gaussian blur"))
story.append(spacer())

story.append(subheading("11.2 Grad-CAM Explanations"))
story.append(body(
    "To improve interpretability, Grad-CAM (Gradient-weighted Class Activation Mapping) "
    "generates attention heatmaps showing which regions of the input image most influence "
    "the model's road predictions. Available via the <font face='Courier'>/explain</font> page."
))
story.append(spacer())

story.append(subheading("11.3 Change Detection"))
story.append(body(
    "By comparing segmentation masks from two time periods (e.g., before and after a disaster), "
    "the system detects <b>new road construction</b> or <b>road damage/destruction</b>. "
    "Output is a change map with three classes: unchanged, added, removed."
))
story.append(spacer())

story.append(subheading("11.4 AI Copilot (Groq LLM)"))
story.append(body(
    "The Copilot feature connects to the <b>Groq API</b> (running Llama or Mixtral models) to "
    "provide natural-language interaction. The system injects the current graph context "
    "(metrics, top critical nodes, recent simulation results) into the LLM prompt, enabling "
    "context-aware Q&A such as:"
))
story.append(bullet("\"Which junction, if removed, causes the biggest efficiency drop?\""))
story.append(bullet("\"How many connected components exist after removing the top 5 critical nodes?\""))
story.append(bullet("\"Suggest the best location for a new bypass road.\""))
story.append(PageBreak())

# ════════════════════════════════════════
# 12. EXTERNAL INTEGRATIONS
# ════════════════════════════════════════
story.append(heading("12. External Integrations"))

int_rows = [
    ["OpenStreetMap / Overpass", "Primary source of road network data. OSMnx queries the Overpass API "
     "to download road graphs for any bounding box worldwide."],
    ["ISRO Bhuvan", "Satellite imagery tile server. The backend proxies tiles from Bhuvan's WMS for "
     "map overlays in the frontend."],
    ["Nominatim", "Geocoding service for converting place names ↔ coordinates."],
    ["Groq API", "Cloud LLM inference for the AI Copilot. Requires a GROQ_API_KEY."],
    ["WorldPop", "Population density raster data for estimating population impact of disruptions."],
]
story.append(make_table(["Service", "Purpose"], int_rows, col_widths=[0.25*W, 0.75*W]))
story.append(PageBreak())

# ════════════════════════════════════════
# 13. FEATURE COVERAGE MATRIX
# ════════════════════════════════════════
story.append(heading("13. Feature Coverage Matrix"))
story.append(body("Status of all major features in the current build:"))
story.append(spacer(6))

feature_rows = [
    ["OSM Graph Ingestion",          "✅ Working",    "Loads from Overpass cache or live API"],
    ["Centrality Computation",       "✅ Working",    "Betweenness, closeness, degree, eigenvector"],
    ["Global Metrics",               "✅ Working",    "Efficiency, algebraic connectivity, clustering"],
    ["Critical Junction Detection",  "✅ Working",    "Composite ranking from multiple centrality measures"],
    ["Interactive Map (Leaflet)",    "✅ Working",    "Heatmap overlay, layer toggles"],
    ["Disaster Simulation",          "✅ Working",    "Multiple scenario types supported"],
    ["Cascade Failure Model",        "✅ Working",    "Chain-reaction node failure simulation"],
    ["Counterfactual Healing (MST)", "✅ Working",    "Propose reconnection edges"],
    ["AI Copilot (Groq LLM)",       "⚠️ Needs Key", "Requires GROQ_API_KEY in .env"],
    ["Report Generation",           "✅ Working",    "PDF/HTML reports via /reports/generate"],
    ["U-Net Road Segmentation",     "⚠️ Optional",  "Requires ENABLE_ML=true + trained model"],
    ["Grad-CAM Explanations",       "⚠️ Optional",  "Requires ML pipeline enabled"],
    ["Change Detection",            "⚠️ Optional",  "Requires two temporal image sets"],
    ["Population Impact Analysis",  "⚠️ Needs Data","Requires WorldPop raster download"],
    ["DEM / Topography Analysis",   "⚠️ Needs Data","Requires DEM tiles download"],
    ["Bhuvan Tile Proxy",           "✅ Working",    "Proxies ISRO satellite imagery tiles"],
    ["Evacuation Planning",         "✅ Working",    "Route planning to safe zones"],
    ["Equity Analysis",             "✅ Working",    "Vulnerability-weighted impact assessment"],
]
story.append(make_table(["Feature", "Status", "Notes"], feature_rows,
                        col_widths=[0.28*W, 0.15*W, 0.57*W]))
story.append(PageBreak())

# ════════════════════════════════════════
# 14. SETUP & QUICK START
# ════════════════════════════════════════
story.append(heading("14. Setup & Quick Start Guide"))

story.append(subheading("Prerequisites"))
story.append(bullet("Python 3.10+ installed and on PATH"))
story.append(bullet("Node.js 18+ and npm installed"))
story.append(bullet("Git installed"))
story.append(spacer())

story.append(subheading("Step 1: Clone the Repository"))
story.append(code("git clone https://github.com/&lt;your-username&gt;/Route-Resilience-System.git"))
story.append(code("cd Route-Resilience-System"))
story.append(spacer(6))

story.append(subheading("Step 2: Backend Setup"))
story.append(code("cd backend"))
story.append(code("python -m venv .venv"))
story.append(code(".venv\\Scripts\\activate        # Windows"))
story.append(code("# source .venv/bin/activate    # Linux/macOS"))
story.append(code("pip install -r requirements-core.txt"))
story.append(spacer(6))

story.append(subheading("Step 3: Configure Environment"))
story.append(code("copy .env.example .env"))
story.append(body("Edit <font face='Courier'>.env</font> and set at minimum:"))
story.append(code("AOI_BBOX=12.9,77.5,13.1,77.7     # Bengaluru bounding box"))
story.append(code("GROQ_API_KEY=gsk_...              # Optional: for AI Copilot"))
story.append(code("ENABLE_ML=false                   # Set true for ML pipeline"))
story.append(spacer(6))

story.append(subheading("Step 4: Start Backend"))
story.append(code("cd backend"))
story.append(code("uvicorn app.main:app --host 127.0.0.1 --port 8000"))
story.append(body("Backend starts at <font face='Courier'>http://127.0.0.1:8000</font>. "
                  "On first run, it downloads and caches the road graph (~30 seconds)."))
story.append(spacer(6))

story.append(subheading("Step 5: Frontend Setup"))
story.append(code("cd frontend"))
story.append(code("npm install"))
story.append(code("npm run dev"))
story.append(body("Frontend starts at <font face='Courier'>http://localhost:3000</font>."))
story.append(spacer(6))

story.append(subheading("Step 6: Open the Application"))
story.append(body(
    "Navigate to <font face='Courier'>http://localhost:3000</font> in your browser. "
    "The dashboard loads automatically and displays network health metrics."
))
story.append(PageBreak())

# ════════════════════════════════════════
# 15. ENVIRONMENT VARIABLES
# ════════════════════════════════════════
story.append(heading("15. Environment Variables"))
story.append(body("All configuration is via a <font face='Courier'>.env</font> file in the project root:"))
story.append(spacer(6))

env_rows = [
    ["AOI_BBOX",       "Bounding box (south, west, north, east) for the area of interest",  "12.9,77.5,13.1,77.7"],
    ["GROQ_API_KEY",   "API key for Groq LLM (enables AI Copilot)",                          "(none)"],
    ["ENABLE_ML",      "Enable the ML segmentation pipeline",                                 "false"],
    ["BACKEND_URL",    "Backend URL for the frontend to connect to",                          "http://127.0.0.1:8000"],
    ["MODEL_PATH",     "Path to the trained U-Net model checkpoint",                          "models/best.pt"],
    ["DEM_PATH",       "Path to DEM (elevation) raster file",                                 "data/dem/"],
    ["WORLDPOP_PATH",  "Path to WorldPop population raster",                                  "data/worldpop/"],
]
story.append(make_table(["Variable", "Description", "Default"], env_rows,
                        col_widths=[0.2*W, 0.55*W, 0.25*W]))
story.append(PageBreak())

# ════════════════════════════════════════
# 16. FUTURE SCOPE
# ════════════════════════════════════════
story.append(heading("16. Future Scope"))
story.append(bullet("Real-time traffic data integration for dynamic edge weighting."))
story.append(bullet("Multi-city support with a city-selector UI."))
story.append(bullet("Live satellite imagery processing for real-time damage assessment."))
story.append(bullet("Integration with ISRO's Bhuvan APIs for higher-resolution imagery."))
story.append(bullet("Mobile-responsive frontend for field teams."))
story.append(bullet("Historical disaster replay: load past events and validate model predictions."))
story.append(bullet("Collaborative annotation: allow multiple users to mark road damage on the map."))
story.append(bullet("Containerisation with Docker / Docker Compose for one-command deployment."))
story.append(bullet("CI/CD pipeline with automated testing and deployment."))
story.append(spacer(20))
story.append(hr())
story.append(Paragraph("— End of Document —", styles["SmallNote"]))

# ── Build ──
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(f"\n✅  PDF generated successfully: {OUTPUT}")
print(f"    Pages: ~{doc.page}")

