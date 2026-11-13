"""
Generate a Machine Learning Project Report PDF for Route Resilience System.
Includes visual flowcharts, architecture diagrams, and benefit analysis.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white, Color
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Circle, Group
from reportlab.graphics import renderPDF
from reportlab.graphics.widgets.markers import makeMarker
import os, math

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "Route_Resilience_ML_Project_Report.pdf")

# ── Colours ──
PRIMARY    = HexColor("#1565c0")
DARK_BLUE  = HexColor("#0d47a1")
LIGHT_BLUE = HexColor("#e3f2fd")
ACCENT     = HexColor("#00897b")  # Teal
ACCENT2    = HexColor("#7b1fa2")  # Purple
ORANGE     = HexColor("#ef6c00")
GREEN      = HexColor("#2e7d32")
RED        = HexColor("#c62828")
DARK       = HexColor("#212121")
GREY       = HexColor("#757575")
LIGHT_GREY = HexColor("#f5f5f5")
WHITE      = white
TABLE_HDR  = HexColor("#1565c0")

# Box colours for diagrams
BOX_BLUE   = HexColor("#bbdefb")
BOX_GREEN  = HexColor("#c8e6c9")
BOX_ORANGE = HexColor("#ffe0b2")
BOX_PURPLE = HexColor("#e1bee7")
BOX_TEAL   = HexColor("#b2dfdb")
BOX_RED    = HexColor("#ffcdd2")
BOX_YELLOW = HexColor("#fff9c4")
BORDER_BLUE   = HexColor("#1976d2")
BORDER_GREEN  = HexColor("#388e3c")
BORDER_ORANGE = HexColor("#f57c00")
BORDER_PURPLE = HexColor("#8e24aa")
BORDER_TEAL   = HexColor("#00897b")
BORDER_RED    = HexColor("#d32f2f")

# ── Styles ──
styles = getSampleStyleSheet()

def add_style(name, **kwargs):
    if name not in [s.name for s in styles.byName.values()]:
        styles.add(ParagraphStyle(name, **kwargs))

add_style("CoverTitle", parent=styles["Title"], fontSize=38, leading=46,
          textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=12, fontName="Helvetica-Bold")
add_style("CoverSub", parent=styles["Normal"], fontSize=18, leading=24,
          textColor=PRIMARY, alignment=TA_CENTER, spaceAfter=8, fontName="Helvetica-Bold")
add_style("CoverDetail", parent=styles["Normal"], fontSize=12, leading=17,
          textColor=GREY, alignment=TA_CENTER, spaceAfter=4)
add_style("SectionTitle", parent=styles["Heading1"], fontSize=22, leading=28,
          textColor=DARK_BLUE, spaceBefore=20, spaceAfter=10, fontName="Helvetica-Bold")
add_style("SubSection", parent=styles["Heading2"], fontSize=16, leading=21,
          textColor=PRIMARY, spaceBefore=14, spaceAfter=8, fontName="Helvetica-Bold")
add_style("SubSub", parent=styles["Heading3"], fontSize=13, leading=17,
          textColor=ACCENT, spaceBefore=10, spaceAfter=6, fontName="Helvetica-Bold")
add_style("Body", parent=styles["Normal"], fontSize=11, leading=17,
          textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=8)
add_style("BodyCenter", parent=styles["Normal"], fontSize=11, leading=17,
          textColor=DARK, alignment=TA_CENTER, spaceAfter=8)
add_style("Bullet", parent=styles["Normal"], fontSize=11, leading=17,
          textColor=DARK, leftIndent=24, spaceAfter=5)
add_style("BulletSub", parent=styles["Normal"], fontSize=10, leading=15,
          textColor=GREY, leftIndent=44, spaceAfter=3)
add_style("DiagramCaption", parent=styles["Normal"], fontSize=10, leading=14,
          textColor=GREY, alignment=TA_CENTER, spaceBefore=6, spaceAfter=12,
          fontName="Helvetica-Oblique")
add_style("SmallNote", parent=styles["Normal"], fontSize=9, leading=12,
          textColor=GREY, alignment=TA_CENTER)
add_style("TOCEntry", parent=styles["Normal"], fontSize=12, leading=20,
          textColor=PRIMARY, leftIndent=12, spaceAfter=3)
add_style("HighlightBox", parent=styles["Normal"], fontSize=11, leading=16,
          textColor=DARK, backColor=LIGHT_BLUE, borderPadding=8, spaceAfter=10)
add_style("QuoteStyle", parent=styles["Normal"], fontSize=11, leading=16,
          textColor=HexColor("#37474f"), leftIndent=30, rightIndent=20,
          fontName="Helvetica-Oblique", spaceAfter=10, spaceBefore=6)

# ── Helpers ──
def heading(t):   return Paragraph(t, styles["SectionTitle"])
def subhead(t):   return Paragraph(t, styles["SubSection"])
def subsub(t):    return Paragraph(t, styles["SubSub"])
def body(t):      return Paragraph(t, styles["Body"])
def bodyc(t):     return Paragraph(t, styles["BodyCenter"])
def bullet(t):    return Paragraph(f"• {t}", styles["Bullet"])
def bullet2(t):   return Paragraph(f"  ◦ {t}", styles["BulletSub"])
def spacer(h=12): return Spacer(1, h)
def hr():         return HRFlowable(width="100%", thickness=1, color=HexColor("#bdbdbd"),
                                    spaceAfter=10, spaceBefore=10)
def caption(t):   return Paragraph(t, styles["DiagramCaption"])
def quote(t):     return Paragraph(f'"{t}"', styles["QuoteStyle"])
def highlight(t):
    return Paragraph(t, styles["HighlightBox"])

def make_table(headers, rows, col_widths=None, header_color=TABLE_HDR):
    data = [headers] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), header_color),
        ("TEXTCOLOR",     (0,0), (-1,0), white),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0), 10),
        ("FONTSIZE",      (0,1), (-1,-1), 9.5),
        ("LEADING",       (0,0), (-1,-1), 14),
        ("ALIGN",         (0,0), (-1,-1), "LEFT"),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("GRID",          (0,0), (-1,-1), 0.5, HexColor("#bdbdbd")),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [white, LIGHT_GREY]),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
    ]))
    return t


# ═══════════════════════════════════════════
# DIAGRAM DRAWING HELPERS
# ═══════════════════════════════════════════

def _rounded_rect(d, x, y, w, h, fill, stroke, r=6):
    """Draw a rounded rectangle with border."""
    d.add(Rect(x, y, w, h, rx=r, ry=r, fillColor=fill, strokeColor=stroke, strokeWidth=1.2))

def _box_with_text(d, x, y, w, h, text, fill, stroke, font_size=9, text_color=DARK, bold=False):
    """Draw a rounded box with centered text."""
    _rounded_rect(d, x, y, w, h, fill, stroke)
    fn = "Helvetica-Bold" if bold else "Helvetica"
    # Split text into lines if needed
    lines = text.split("\n")
    line_h = font_size + 2
    total_h = len(lines) * line_h
    start_y = y + h/2 + total_h/2 - font_size/2 - 1
    for i, line in enumerate(lines):
        d.add(String(x + w/2, start_y - i*line_h, line,
                     fontName=fn, fontSize=font_size, fillColor=text_color, textAnchor="middle"))

def _arrow_down(d, x, y1, y2, color=DARK):
    """Draw a downward arrow from (x, y1) to (x, y2)."""
    d.add(Line(x, y1, x, y2+5, strokeColor=color, strokeWidth=1.5))
    # arrowhead
    d.add(Polygon([x-4, y2+8, x+4, y2+8, x, y2],
                  fillColor=color, strokeColor=color, strokeWidth=0.5))

def _arrow_right(d, x1, x2, y, color=DARK):
    """Draw a rightward arrow."""
    d.add(Line(x1, y, x2-5, y, strokeColor=color, strokeWidth=1.5))
    d.add(Polygon([x2-8, y+4, x2-8, y-4, x2, y],
                  fillColor=color, strokeColor=color, strokeWidth=0.5))

def _arrow_left(d, x1, x2, y, color=DARK):
    """Draw a leftward arrow."""
    d.add(Line(x1, y, x2+5, y, strokeColor=color, strokeWidth=1.5))
    d.add(Polygon([x2+8, y+4, x2+8, y-4, x2, y],
                  fillColor=color, strokeColor=color, strokeWidth=0.5))


# ═══════════════════════════════════════════
# DIAGRAM 1: SYSTEM ARCHITECTURE
# ═══════════════════════════════════════════
def create_architecture_diagram():
    dw, dh = 500, 520
    d = Drawing(dw, dh)

    # Title
    d.add(String(dw/2, dh-15, "System Architecture — Route Resilience ML Platform",
                 fontName="Helvetica-Bold", fontSize=12, fillColor=DARK_BLUE, textAnchor="middle"))

    # ── Row 1: Data Sources ──
    y1 = dh - 70
    bw, bh = 105, 40
    _box_with_text(d, 15,  y1, bw, bh, "Satellite\nImagery", BOX_ORANGE, BORDER_ORANGE, 9, bold=True)
    _box_with_text(d, 135, y1, bw, bh, "OpenStreetMap\nRoad Data", BOX_ORANGE, BORDER_ORANGE, 9, bold=True)
    _box_with_text(d, 255, y1, bw, bh, "Population\nDensity (WorldPop)", BOX_ORANGE, BORDER_ORANGE, 8, bold=True)
    _box_with_text(d, 375, y1, bw, bh, "DEM Elevation\nData", BOX_ORANGE, BORDER_ORANGE, 9, bold=True)

    # Label
    d.add(String(dw/2, y1+bh+8, "DATA SOURCES", fontName="Helvetica-Bold", fontSize=8,
                 fillColor=BORDER_ORANGE, textAnchor="middle"))

    # Arrows down from data sources
    for cx in [67, 187, 307, 427]:
        _arrow_down(d, cx, y1, y1-30)

    # ── Row 2: ML Processing ──
    y2 = y1 - 70
    pw = 220
    _box_with_text(d, 15,  y2, pw, 40, "U-Net Road Segmentation\n(PyTorch Deep Learning)", BOX_PURPLE, BORDER_PURPLE, 9, bold=True)
    _box_with_text(d, 255, y2, pw, 40, "Graph Construction\n(OSMnx + NetworkX)", BOX_BLUE, BORDER_BLUE, 9, bold=True)

    d.add(String(dw/2, y2+bh+8, "ML PROCESSING & GRAPH BUILDING", fontName="Helvetica-Bold",
                 fontSize=8, fillColor=BORDER_PURPLE, textAnchor="middle"))

    # Arrow between ML and Graph
    _arrow_right(d, 235, 255, y2+20, BORDER_PURPLE)

    # Arrows down
    _arrow_down(d, 125, y2, y2-30)
    _arrow_down(d, 365, y2, y2-30)

    # ── Row 3: Analysis Engine ──
    y3 = y2 - 70
    aw = 460
    _box_with_text(d, 15, y3, aw, 40, "Graph Analysis Engine — Centrality Metrics, Critical Junction Detection, Resilience Scoring",
                   BOX_GREEN, BORDER_GREEN, 9, bold=True)

    d.add(String(dw/2, y3+bh+8, "CORE ANALYSIS", fontName="Helvetica-Bold", fontSize=8,
                 fillColor=BORDER_GREEN, textAnchor="middle"))

    # Arrows down (two branches)
    _arrow_down(d, 160, y3, y3-30)
    _arrow_down(d, 340, y3, y3-30)

    # ── Row 4: Simulation & AI ──
    y4 = y3 - 70
    _box_with_text(d, 15,  y4, pw, 40, "Disaster Simulation\n(Earthquake, Flood, Cascade)", BOX_RED, BORDER_RED, 9, bold=True)
    _box_with_text(d, 255, y4, pw, 40, "AI Copilot\n(Groq LLM — NLP Q&A)", BOX_PURPLE, BORDER_PURPLE, 9, bold=True)

    d.add(String(dw/2, y4+bh+8, "SIMULATION & AI", fontName="Helvetica-Bold", fontSize=8,
                 fillColor=BORDER_RED, textAnchor="middle"))

    # Arrows down
    _arrow_down(d, 125, y4, y4-30)
    _arrow_down(d, 365, y4, y4-30)

    # ── Row 5: Outputs ──
    y5 = y4 - 70
    _box_with_text(d, 15,  y5, 145, 40, "Counterfactual\nHealing & Fixes", BOX_TEAL, BORDER_TEAL, 9, bold=True)
    _box_with_text(d, 175, y5, 145, 40, "Reports &\nRecommendations", BOX_TEAL, BORDER_TEAL, 9, bold=True)
    _box_with_text(d, 335, y5, 145, 40, "Interactive\nDashboard", BOX_TEAL, BORDER_TEAL, 9, bold=True)

    d.add(String(dw/2, y5+bh+8, "OUTPUTS & VISUALIZATION", fontName="Helvetica-Bold", fontSize=8,
                 fillColor=BORDER_TEAL, textAnchor="middle"))

    # Arrows down to final
    for cx in [87, 247, 407]:
        _arrow_down(d, cx, y5, y5-30)

    # ── Row 6: End Users ──
    y6 = y5 - 70
    _box_with_text(d, 50, y6, 400, 40,
                   "END USERS:  Citizens  |  Government  |  Emergency Services  |  Urban Planners",
                   BOX_YELLOW, HexColor("#f9a825"), 10, bold=True)

    return d


# ═══════════════════════════════════════════
# DIAGRAM 2: ML PIPELINE FLOWCHART
# ═══════════════════════════════════════════
def create_ml_pipeline_diagram():
    dw, dh = 500, 560
    d = Drawing(dw, dh)

    d.add(String(dw/2, dh-15, "Machine Learning Pipeline — Step-by-Step Flow",
                 fontName="Helvetica-Bold", fontSize=12, fillColor=DARK_BLUE, textAnchor="middle"))

    bw, bh = 300, 38
    x0 = (dw - bw) / 2
    gap = 56

    steps = [
        ("1. Input: Satellite Image Tile (256×256)", BOX_ORANGE, BORDER_ORANGE),
        ("2. Data Augmentation\n(Flip, Rotate, Color Jitter, Blur)", BOX_ORANGE, BORDER_ORANGE),
        ("3. U-Net Encoder (ResNet Backbone)\nExtract Multi-Scale Features", BOX_PURPLE, BORDER_PURPLE),
        ("4. U-Net Decoder + Skip Connections\nUpsample to Original Resolution", BOX_PURPLE, BORDER_PURPLE),
        ("5. Output: Binary Road Mask\n(Road vs. Non-Road Pixels)", BOX_GREEN, BORDER_GREEN),
        ("6. Morphological Skeletonization\nThin Roads to 1-Pixel Width", BOX_BLUE, BORDER_BLUE),
        ("7. Graph Extraction\nNodes = Junctions, Edges = Road Segments", BOX_BLUE, BORDER_BLUE),
        ("8. Grad-CAM Explanation\nVisualize Model Attention Regions", BOX_TEAL, BORDER_TEAL),
    ]

    y = dh - 55
    for i, (text, fill, stroke) in enumerate(steps):
        _box_with_text(d, x0, y, bw, bh, text, fill, stroke, 9, bold=True)
        if i < len(steps) - 1:
            _arrow_down(d, dw/2, y, y - (gap - bh))
        y -= gap

    # Side annotation for loss
    ly = dh - 55 - 2*gap
    d.add(Line(x0 + bw, ly + bh/2, x0 + bw + 30, ly + bh/2,
               strokeColor=RED, strokeWidth=1.2, strokeDashArray=[4,2]))
    _box_with_text(d, x0+bw+32, ly-2, 100, bh+4,
                   "Loss Function:\nBCE + Dice Loss\n(Backpropagation)", BOX_RED, BORDER_RED, 8)

    return d


# ═══════════════════════════════════════════
# DIAGRAM 3: BENEFIT FLOW
# ═══════════════════════════════════════════
def create_benefit_diagram():
    dw, dh = 500, 340
    d = Drawing(dw, dh)

    d.add(String(dw/2, dh-15, "Who Benefits & How?",
                 fontName="Helvetica-Bold", fontSize=12, fillColor=DARK_BLUE, textAnchor="middle"))

    # Center box
    cx, cy = dw/2, dh/2
    cw, ch = 160, 45
    _box_with_text(d, cx-cw/2, cy-ch/2, cw, ch,
                   "Route Resilience\nML System", BOX_BLUE, BORDER_BLUE, 11, bold=True)

    # Surrounding benefit boxes
    benefits = [
        (cx-200, cy+90,  150, 38, "Citizens\nSafer roads, faster\nemergency response", BOX_GREEN, BORDER_GREEN),
        (cx+50,  cy+90,  150, 38, "Government\nData-driven planning,\ncost-effective repairs", BOX_ORANGE, BORDER_ORANGE),
        (cx-200, cy-130, 150, 38, "Emergency Services\nOptimal evacuation\nroute planning", BOX_RED, BORDER_RED),
        (cx+50,  cy-130, 150, 38, "Urban Planners\nPrioritise infrastructure\ninvestments", BOX_PURPLE, BORDER_PURPLE),
    ]

    for bx, by, bw2, bh2, text, fill, stroke in benefits:
        _box_with_text(d, bx, by, bw2, bh2, text, fill, stroke, 8, bold=False)

    # Connect lines
    # Top-left
    d.add(Line(cx-cw/2, cy+ch/2, cx-125, cy+90, strokeColor=GREY, strokeWidth=1.2))
    # Top-right
    d.add(Line(cx+cw/2, cy+ch/2, cx+125, cy+90, strokeColor=GREY, strokeWidth=1.2))
    # Bottom-left
    d.add(Line(cx-cw/2, cy-ch/2, cx-125, cy-92, strokeColor=GREY, strokeWidth=1.2))
    # Bottom-right
    d.add(Line(cx+cw/2, cy-ch/2, cx+125, cy-92, strokeColor=GREY, strokeWidth=1.2))

    return d


# ═══════════════════════════════════════════
# DIAGRAM 4: DATA FLOW
# ═══════════════════════════════════════════
def create_data_flow_diagram():
    dw, dh = 500, 200
    d = Drawing(dw, dh)

    d.add(String(dw/2, dh-12, "End-to-End Data Flow",
                 fontName="Helvetica-Bold", fontSize=11, fillColor=DARK_BLUE, textAnchor="middle"))

    bw, bh = 80, 55
    y = dh/2 - bh/2 - 5
    gap = 95

    boxes = [
        ("Raw\nData", BOX_ORANGE, BORDER_ORANGE),
        ("ML\nProcessing", BOX_PURPLE, BORDER_PURPLE),
        ("Graph\nAnalysis", BOX_GREEN, BORDER_GREEN),
        ("Simulation\n& AI", BOX_RED, BORDER_RED),
        ("Dashboard\n& Reports", BOX_TEAL, BORDER_TEAL),
    ]

    for i, (text, fill, stroke) in enumerate(boxes):
        x = 10 + i * gap
        _box_with_text(d, x, y, bw, bh, text, fill, stroke, 9, bold=True)
        if i < len(boxes)-1:
            _arrow_right(d, x+bw, x+gap, y+bh/2)

    return d


# ═══════════════════════════════════════════
# DIAGRAM 5: U-Net Architecture (simplified)
# ═══════════════════════════════════════════
def create_unet_diagram():
    dw, dh = 500, 300
    d = Drawing(dw, dh)

    d.add(String(dw/2, dh-12, "U-Net Architecture for Road Segmentation",
                 fontName="Helvetica-Bold", fontSize=11, fillColor=DARK_BLUE, textAnchor="middle"))

    # Encoder blocks (left, going down)
    enc_x = 30
    enc_widths = [90, 80, 70, 60]
    enc_heights = [35, 35, 35, 35]
    enc_labels = ["Conv Block 1\n64 filters", "Conv Block 2\n128 filters",
                  "Conv Block 3\n256 filters", "Conv Block 4\n512 filters"]
    y = dh - 55
    enc_positions = []
    for i, (w, h, label) in enumerate(zip(enc_widths, enc_heights, enc_labels)):
        _box_with_text(d, enc_x, y, w, h, label, BOX_BLUE, BORDER_BLUE, 8)
        enc_positions.append((enc_x, y, w, h))
        if i < 3:
            _arrow_down(d, enc_x + w/2, y, y - 18)
        y -= 53

    # Bottleneck
    bn_y = y + 10
    _box_with_text(d, 170, bn_y, 100, 35, "Bottleneck\n1024 filters", BOX_RED, BORDER_RED, 8, bold=True)
    # Arrow from last encoder to bottleneck
    _arrow_right(d, enc_x + 60, 170, bn_y + 17)

    # Decoder blocks (right, going up)
    dec_x = 340
    dec_widths = [60, 70, 80, 90]
    dec_labels = ["Up Block 4\n512 filters", "Up Block 3\n256 filters",
                  "Up Block 2\n128 filters", "Up Block 1\n64 filters"]
    y = bn_y
    dec_positions = []
    for i, (w, h, label) in enumerate(zip(dec_widths, enc_heights, dec_labels)):
        _box_with_text(d, dec_x, y, w, h, label, BOX_GREEN, BORDER_GREEN, 8)
        dec_positions.append((dec_x, y, w, h))
        if i < 3:
            _arrow_down(d, dec_x + w/2, y + h, y + h + 18, BORDER_GREEN)
        y += 53

    # Arrow from bottleneck to first decoder
    _arrow_right(d, 270, dec_x, bn_y + 17)

    # Skip connections (dashed lines)
    for i in range(4):
        ex, ey, ew, eh = enc_positions[i]
        dx, dy, dw2, dh2 = dec_positions[3 - i]
        mid_y = ey + eh/2
        d.add(Line(ex + ew, mid_y, dx, dy + dh2/2,
                   strokeColor=ORANGE, strokeWidth=1, strokeDashArray=[4, 3]))

    # Label skip connections
    d.add(String(240, dh-45, "Skip Connections", fontName="Helvetica-Oblique",
                 fontSize=8, fillColor=ORANGE, textAnchor="middle"))

    # Output
    out_y = dec_positions[-1][1] + 35
    _box_with_text(d, dec_x, out_y + 10, 90, 30, "Road Mask\nOutput", BOX_YELLOW, HexColor("#f9a825"), 8, bold=True)
    _arrow_down(d, dec_x + 45, out_y + 10 + 30, out_y + 10 + 30 + 5, BORDER_GREEN)

    # Labels
    d.add(String(enc_x + 20, dh-30, "ENCODER", fontName="Helvetica-Bold", fontSize=9, fillColor=BORDER_BLUE))
    d.add(String(dec_x + 10, dh-30, "DECODER", fontName="Helvetica-Bold", fontSize=9, fillColor=BORDER_GREEN))

    return d


# ══════════════════════════════════════════════
# BUILD THE PDF
# ══════════════════════════════════════════════
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=1.2*cm, rightMargin=1.2*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)
story = []
W = A4[0] - 2.4*cm

def footer_fn(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawCentredString(A4[0]/2, 28, f"Route Resilience System — ML Project Report  |  Page {doc.page}")
    canvas.restoreState()


# ════════════════════════════════════════
# COVER PAGE
# ════════════════════════════════════════
story.append(Spacer(1, 1.8*inch))
story.append(Paragraph("Route Resilience System", styles["CoverTitle"]))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="55%", thickness=2.5, color=PRIMARY, spaceAfter=16, spaceBefore=4))
story.append(Paragraph("Machine Learning Project Report", styles["CoverSub"]))
story.append(Spacer(1, 16))
story.append(Paragraph(
    "Urban Road Network Resilience Analysis using<br/>"
    "Deep Learning, Graph Theory &amp; Geospatial Intelligence",
    styles["CoverDetail"]))
story.append(Spacer(1, 30))
story.append(Paragraph("—", styles["CoverDetail"]))
story.append(Spacer(1, 10))
story.append(Paragraph("Key Technologies", styles["CoverDetail"]))
story.append(Paragraph(
    "<b>Python  ·  PyTorch  ·  U-Net  ·  NetworkX  ·  FastAPI  ·  Next.js  ·  OSMnx</b>",
    styles["CoverDetail"]))
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("A Machine Learning approach to making cities safer and more resilient",
                        styles["CoverDetail"]))
story.append(PageBreak())


# ════════════════════════════════════════
# TABLE OF CONTENTS
# ════════════════════════════════════════
story.append(heading("Table of Contents"))
story.append(hr())
toc = [
    "1.  Introduction — What Is This Project?",
    "2.  Problem Statement — Why Do We Need This?",
    "3.  System Architecture (Diagram)",
    "4.  Machine Learning Pipeline (Flowchart)",
    "5.  U-Net Architecture (Diagram)",
    "6.  How It Works — Step by Step",
    "7.  Key ML Techniques Used",
    "8.  Benefits to Citizens & Society",
    "9.  Benefits to Government & Administration",
    "10. Benefits to Emergency Services & Disaster Management",
    "11. Economic & Long-Term Benefits",
    "12. Real-World Use Cases",
    "13. Technology Stack",
    "14. Data Flow (Diagram)",
    "15. Results & Outputs",
    "16. Future Scope",
    "17. Conclusion",
]
for item in toc:
    story.append(Paragraph(item, styles["TOCEntry"]))
story.append(PageBreak())


# ════════════════════════════════════════
# 1. INTRODUCTION
# ════════════════════════════════════════
story.append(heading("1. Introduction — What Is This Project?"))
story.append(body(
    "The <b>Route Resilience System</b> is a <b>Machine Learning project</b> that analyses "
    "urban road networks to find out <b>how strong or weak</b> they are against disasters "
    "like earthquakes, floods, and landslides."
))
story.append(body(
    "Think of a city's road network like a spider web. If you cut one strand in the middle, "
    "the whole web becomes weak. Similarly, if a critical road junction in a city gets damaged, "
    "thousands of people could get stuck — ambulances can't reach hospitals, fire trucks can't "
    "reach fires, and daily commuters face hours of delay."
))
story.append(body(
    "This project uses <b>Deep Learning (U-Net)</b> to extract road networks from satellite "
    "images, converts them into mathematical graphs, and then uses <b>graph theory algorithms</b> "
    "to identify the most critical junctions. It then simulates disasters to show what would "
    "happen if those junctions fail — and suggests fixes."
))
story.append(spacer())
story.append(highlight(
    "<b>In Simple Terms:</b> This ML system looks at satellite images of a city, understands "
    "the road network, finds the weak points, simulates what happens when disasters strike, "
    "and tells the government exactly where to invest to make the city safer."
))
story.append(spacer())

story.append(subhead("Key Objectives"))
story.append(bullet("<b>Extract</b> road networks from satellite imagery using deep learning (U-Net)."))
story.append(bullet("<b>Build</b> a mathematical graph of the city's roads (nodes = intersections, edges = roads)."))
story.append(bullet("<b>Identify</b> critical junctions whose failure would cause maximum disruption."))
story.append(bullet("<b>Simulate</b> natural disasters and measure their impact on the road network."))
story.append(bullet("<b>Recommend</b> where to build new roads or repair existing ones for maximum resilience."))
story.append(bullet("<b>Visualise</b> everything on an interactive web dashboard for easy decision-making."))
story.append(PageBreak())


# ════════════════════════════════════════
# 2. PROBLEM STATEMENT
# ════════════════════════════════════════
story.append(heading("2. Problem Statement — Why Do We Need This?"))
story.append(body(
    "India's cities are growing rapidly. Roads that were built decades ago now carry 10× more "
    "traffic. When a natural disaster strikes — an earthquake in Gujarat, flooding in Chennai, "
    "or landslides in Uttarakhand — the road network is often the first thing to fail."
))
story.append(spacer(4))
story.append(quote(
    "In the 2015 Chennai floods, over 500 roads were submerged and hundreds of thousands of "
    "people were stranded for days. Emergency vehicles couldn't reach critical areas because "
    "nobody knew which alternative routes were still functional."
))
story.append(spacer(4))
story.append(body("<b>The core problem:</b>"))
story.append(bullet("Cities don't know which road junctions are <b>most critical</b> to the entire network."))
story.append(bullet("There is no way to <b>simulate disasters in advance</b> and predict road failures."))
story.append(bullet("Government decisions on road repair and new construction are often based on "
                    "<b>political pressure</b> rather than <b>data-driven analysis</b>."))
story.append(bullet("During disasters, there is no tool to <b>quickly identify alternative routes</b> "
                    "and plan evacuations."))
story.append(spacer())
story.append(body(
    "This project solves all of these problems using <b>Machine Learning and Graph Theory</b>."
))
story.append(spacer())

story.append(subhead("Problem Statement Context"))
story.append(body(
    "This project addresses <b>ISRO NNRMS Hackathon 2026 — Problem Statement PS4</b>: "
    "<i>\"Urban Road Network Resilience Analysis using Satellite Imagery and Graph Theory.\"</i> "
    "The challenge requires extracting road networks from satellite data, constructing weighted "
    "graphs, computing centrality metrics, and simulating disruptions to assess network resilience."
))
story.append(PageBreak())


# ════════════════════════════════════════
# 3. SYSTEM ARCHITECTURE
# ════════════════════════════════════════
story.append(heading("3. System Architecture"))
story.append(body(
    "The diagram below shows the complete system architecture — from raw data input to the "
    "final dashboard used by citizens and government officials."
))
story.append(spacer(6))
story.append(create_architecture_diagram())
story.append(caption("Figure 1: Complete System Architecture of the Route Resilience ML Platform"))
story.append(spacer())
story.append(body(
    "The system is divided into <b>5 layers</b>:"
))
story.append(bullet("<b>Data Sources Layer:</b> Satellite images, OSM road data, population density, elevation models."))
story.append(bullet("<b>ML Processing Layer:</b> U-Net deep learning model extracts roads from images; OSMnx builds graphs."))
story.append(bullet("<b>Analysis Layer:</b> Graph algorithms compute centrality, detect critical junctions, score resilience."))
story.append(bullet("<b>Simulation & AI Layer:</b> Disaster simulations + AI Copilot for natural-language insights."))
story.append(bullet("<b>Output Layer:</b> Interactive dashboard, auto-generated reports, and healing recommendations."))
story.append(PageBreak())


# ════════════════════════════════════════
# 4. ML PIPELINE FLOWCHART
# ════════════════════════════════════════
story.append(heading("4. Machine Learning Pipeline"))
story.append(body(
    "The ML pipeline is the core intelligence of the system. Here is the step-by-step flowchart "
    "showing how a satellite image gets transformed into actionable road network insights."
))
story.append(spacer(6))
story.append(create_ml_pipeline_diagram())
story.append(caption("Figure 2: Machine Learning Pipeline — From Satellite Image to Road Graph"))
story.append(spacer())
story.append(body(
    "<b>How it works in simple words:</b> A satellite photo of the city goes in → the ML model "
    "(U-Net) identifies which pixels are roads → those road pixels are thinned to single lines → "
    "the lines are converted to a mathematical graph → the graph is analysed for weak points."
))
story.append(PageBreak())


# ════════════════════════════════════════
# 5. U-NET ARCHITECTURE
# ════════════════════════════════════════
story.append(heading("5. U-Net Architecture"))
story.append(body(
    "The U-Net is a <b>convolutional neural network</b> specifically designed for image "
    "segmentation. It has an <b>encoder</b> (downsampling path) that captures context and a "
    "<b>decoder</b> (upsampling path) that enables precise localisation. <b>Skip connections</b> "
    "bridge the two paths to preserve fine details."
))
story.append(spacer(6))
story.append(create_unet_diagram())
story.append(caption("Figure 3: Simplified U-Net Architecture Used for Road Segmentation"))
story.append(spacer())

story.append(subhead("Why U-Net for Road Segmentation?"))
story.append(bullet("<b>Pixel-level accuracy:</b> U-Net classifies every pixel as road or non-road."))
story.append(bullet("<b>Skip connections:</b> Preserve fine details like narrow roads and sharp turns."))
story.append(bullet("<b>Works with limited data:</b> Originally designed for biomedical images with few samples."))
story.append(bullet("<b>Fast inference:</b> Processes a 256×256 tile in milliseconds."))
story.append(spacer())

story.append(subhead("Training Details"))
train_rows = [
    ["Input Size",       "256 × 256 × 3 (RGB satellite tile)"],
    ["Output",           "256 × 256 × 1 (binary mask: road / non-road)"],
    ["Encoder Backbone", "ResNet (pretrained on ImageNet)"],
    ["Loss Function",    "Binary Cross-Entropy + Dice Loss"],
    ["Optimizer",        "Adam (lr = 1e-4)"],
    ["Augmentations",    "Random flip, rotation, colour jitter, Gaussian blur"],
    ["Framework",        "PyTorch + segmentation-models-pytorch"],
]
story.append(make_table(["Parameter", "Value"], train_rows, col_widths=[0.3*W, 0.7*W]))
story.append(PageBreak())


# ════════════════════════════════════════
# 6. HOW IT WORKS — STEP BY STEP
# ════════════════════════════════════════
story.append(heading("6. How It Works — Step by Step"))
story.append(body("Here is a simple, easy-to-follow explanation of how the system works:"))
story.append(spacer(6))

steps_data = [
    ["Step", "What Happens", "Technology Used"],
    ["1", "Satellite images of the target city are obtained (or road data is fetched from OpenStreetMap).",
     "OSMnx, Overpass API"],
    ["2", "The U-Net ML model scans the satellite images and identifies road pixels — like highlighting roads with a marker.",
     "PyTorch, U-Net CNN"],
    ["3", "Road pixels are 'skeletonized' — thinned to single-pixel-wide lines so the computer can trace each road.",
     "Morphological Thinning"],
    ["4", "The road skeleton is converted into a mathematical graph: every intersection becomes a 'node', every road between intersections becomes an 'edge'.",
     "NetworkX"],
    ["5", "The system calculates how important each junction is using centrality algorithms (betweenness, closeness, degree, eigenvector).",
     "NetworkX, NumPy"],
    ["6", "Critical junctions are identified — these are the junctions whose failure would cause the most damage to the overall network.",
     "Graph Theory"],
    ["7", "The user selects a disaster scenario (earthquake, flood, etc.) and the system removes affected junctions/roads from the graph.",
     "Simulation Engine"],
    ["8", "The system measures how badly the network is damaged: How many pieces did it break into? How much longer are routes now?",
     "Resilience Metrics"],
    ["9", "The system suggests fixes: 'Build a bypass road here' or 'Repair this junction first' — each with a cost-benefit score.",
     "MST Healing Algorithm"],
    ["10", "Everything is displayed on a beautiful interactive dashboard with maps, charts, and downloadable reports.",
     "Next.js, Leaflet, Recharts"],
]
story.append(make_table(steps_data[0], steps_data[1:], col_widths=[0.06*W, 0.54*W, 0.4*W]))
story.append(PageBreak())


# ════════════════════════════════════════
# 7. KEY ML TECHNIQUES
# ════════════════════════════════════════
story.append(heading("7. Key ML Techniques Used"))

ml_tech_rows = [
    ["U-Net (CNN)", "Semantic Segmentation",
     "Classifies every pixel in a satellite image as 'road' or 'not road'. The encoder-decoder "
     "architecture with skip connections enables pixel-precise road extraction."],
    ["Transfer Learning", "Pre-trained Backbone",
     "The encoder uses a ResNet backbone pre-trained on ImageNet, which provides robust feature "
     "extraction even with limited satellite training data."],
    ["Grad-CAM", "Model Explainability",
     "Gradient-weighted Class Activation Mapping generates heatmaps showing which image regions "
     "the model focuses on — critical for building trust in ML predictions."],
    ["Change Detection", "Temporal Analysis",
     "Compares road segmentation masks from two time periods to detect new roads or damage. "
     "Uses difference maps on model outputs."],
    ["Graph Neural Concepts", "Centrality Analysis",
     "While not a GNN, the project applies graph-theoretic metrics (betweenness, eigenvector "
     "centrality) to the extracted road graph — a core ML-adjacent technique."],
    ["NLP (LLM)", "AI Copilot",
     "Integrates Groq's LLM (Llama/Mixtral) for natural-language Q&A about the road network. "
     "Context injection feeds graph metrics into the LLM prompt."],
    ["Data Augmentation", "Training Robustness",
     "Random flips, rotations, colour jitter, and Gaussian blur prevent overfitting and make "
     "the model generalise to different satellite sources and lighting conditions."],
]
story.append(make_table(["Technique", "Category", "How It's Used"], ml_tech_rows,
                        col_widths=[0.18*W, 0.17*W, 0.65*W]))
story.append(PageBreak())


# ════════════════════════════════════════
# 8. BENEFITS TO CITIZENS
# ════════════════════════════════════════
story.append(heading("8. Benefits to Citizens & Society"))
story.append(spacer(4))
story.append(create_benefit_diagram())
story.append(caption("Figure 4: Stakeholders Who Benefit from the Route Resilience System"))
story.append(spacer())

story.append(subhead("How Citizens Benefit"))
story.append(bullet("<b>Safer commutes:</b> The system identifies dangerous junctions that could fail. Once fixed, daily commuters face fewer risks."))
story.append(bullet("<b>Faster emergency response:</b> During disasters, evacuation routes are pre-computed. Ambulances, fire trucks, and rescue teams know exactly which roads are still functional."))
story.append(bullet("<b>Less disruption:</b> By predicting which roads will fail during floods or earthquakes, the government can proactively strengthen them — meaning fewer road closures and detours."))
story.append(bullet("<b>Equity in infrastructure:</b> The equity analysis module ensures that poorer neighbourhoods (which are often ignored) get fair attention in road resilience planning."))
story.append(bullet("<b>Real-time information:</b> The interactive dashboard can show citizens which roads are safe and which are damaged, helping them plan their routes during emergencies."))
story.append(spacer())

story.append(subhead("Social Impact"))
story.append(body(
    "In India, road accidents and disaster-related road failures cause thousands of deaths annually. "
    "A system that can predict weak points and suggest fixes <b>before</b> a disaster strikes can "
    "save lives. The population impact analysis also ensures that areas with the highest population "
    "density get priority attention."
))
story.append(PageBreak())


# ════════════════════════════════════════
# 9. BENEFITS TO GOVERNMENT
# ════════════════════════════════════════
story.append(heading("9. Benefits to Government & Administration"))

story.append(subhead("9.1 Data-Driven Decision Making"))
story.append(body(
    "Currently, most road repair and construction decisions are made based on complaints, "
    "political pressure, or visual inspection. This system provides <b>quantitative, data-driven "
    "evidence</b> for every decision:"
))
story.append(bullet("\"Junction X has a betweenness centrality of 0.47 — if it fails, 23% of all shortest paths in the city are disrupted.\""))
story.append(bullet("\"Building a bypass road between Node A and Node B would improve network resilience by 18% at a cost of only 2.3 km of new road.\""))
story.append(spacer())

story.append(subhead("9.2 Cost Optimization"))
story.append(body(
    "Government budgets for road infrastructure are limited. This system helps allocate funds "
    "where they matter most:"
))
story.append(bullet("<b>Prioritised repair lists:</b> Instead of fixing roads randomly, the system ranks repairs by impact on overall network resilience."))
story.append(bullet("<b>Cost-benefit analysis:</b> Every proposed intervention comes with a resilience gain score vs. construction cost."))
story.append(bullet("<b>Avoid over-investment:</b> Some roads look important but aren't critical to the network. The system identifies them, saving unnecessary spending."))
story.append(spacer())

story.append(subhead("9.3 Disaster Preparedness"))
story.append(bullet("<b>Pre-disaster planning:</b> Simulate earthquake/flood scenarios and prepare response plans before the disaster actually hits."))
story.append(bullet("<b>Evacuation route pre-computation:</b> Know in advance which routes to use for evacuation under different disaster scenarios."))
story.append(bullet("<b>NDMA integration potential:</b> Can feed directly into the National Disaster Management Authority's planning systems."))
story.append(spacer())

story.append(subhead("9.4 Urban Planning"))
story.append(bullet("Identify areas where the road network is <b>too sparse</b> and needs new connections."))
story.append(bullet("Plan <b>smart city</b> road networks with built-in resilience."))
story.append(bullet("Evaluate the impact of proposed new roads/flyovers before construction begins."))
story.append(PageBreak())


# ════════════════════════════════════════
# 10. EMERGENCY SERVICES
# ════════════════════════════════════════
story.append(heading("10. Benefits to Emergency Services & Disaster Management"))

story.append(subhead("During a Disaster"))
story.append(bullet("<b>Real-time network status:</b> Instantly see which roads are damaged and which are still functional."))
story.append(bullet("<b>Optimal evacuation routes:</b> The evacuation module computes the fastest routes from danger zones to safety, considering road capacity and damage."))
story.append(bullet("<b>Resource allocation:</b> Know which areas are completely cut off and need helicopter/boat rescue vs. those reachable by road."))
story.append(spacer())

story.append(subhead("Before a Disaster"))
story.append(bullet("<b>Vulnerability mapping:</b> Identify which neighbourhoods would be isolated if specific roads fail."))
story.append(bullet("<b>Drill planning:</b> Use simulation results to design realistic disaster response drills."))
story.append(bullet("<b>Strategic positioning:</b> Position fire stations, ambulance depots, and relief centres at locations that remain accessible even when critical junctions fail."))
story.append(spacer())

story.append(subhead("After a Disaster"))
story.append(bullet("<b>Prioritised recovery:</b> Which roads should be cleared first to restore maximum connectivity?"))
story.append(bullet("<b>Damage assessment:</b> Change detection (ML) compares pre-disaster and post-disaster satellite images to automatically map road damage."))
story.append(bullet("<b>Cascade prevention:</b> The cascade failure model shows which damaged roads could trigger further failures — helping teams prevent secondary disasters."))
story.append(PageBreak())


# ════════════════════════════════════════
# 11. ECONOMIC BENEFITS
# ════════════════════════════════════════
story.append(heading("11. Economic & Long-Term Benefits"))

econ_rows = [
    ["Reduced Disaster Losses", "By strengthening critical junctions before disasters, the economic "
     "losses from road network failures can be significantly reduced. India loses an estimated "
     "₹1.5 lakh crore annually to natural disasters."],
    ["Lower Repair Costs", "Proactive maintenance (fixing weak points early) is 3-5× cheaper than "
     "emergency repairs after a disaster."],
    ["Fuel & Time Savings", "When critical junctions fail, commuters take long detours. The system's "
     "recommendations reduce average detour lengths, saving fuel and commute time across millions of trips."],
    ["Insurance Benefits", "Cities with quantified resilience scores may qualify for lower disaster "
     "insurance premiums."],
    ["Tourism & Business", "A resilient road network improves a city's reputation, attracting "
     "business investment and tourism."],
    ["Job Creation", "Building recommended bypass roads and bridges creates construction jobs while "
     "improving the city's infrastructure."],
    ["Healthcare Access", "Ensuring hospitals remain reachable during disasters reduces mortality "
     "and healthcare costs."],
]
story.append(make_table(["Benefit Area", "Description"], econ_rows, col_widths=[0.25*W, 0.75*W]))
story.append(PageBreak())


# ════════════════════════════════════════
# 12. REAL-WORLD USE CASES
# ════════════════════════════════════════
story.append(heading("12. Real-World Use Cases"))
story.append(spacer(4))

uc_rows = [
    ["Chennai Flood\nPreparedness", "Simulate monsoon flooding by disabling low-elevation roads. "
     "Identify which hospitals, schools, and residential areas get cut off. Pre-position rescue "
     "boats and plan elevated evacuation corridors."],
    ["Earthquake\nResponse\n(Gujarat)", "Simulate a magnitude 7.0 earthquake with a configurable "
     "epicentre. The cascade model shows how infrastructure failure propagates. Emergency teams "
     "pre-plan response based on worst-case fragmentation."],
    ["Smart City\nPlanning", "Before building a new smart city, simulate the proposed road network. "
     "Test its resilience by removing junctions. Iterate the design until the network meets "
     "minimum resilience thresholds."],
    ["Highway\nAuthority\n(NHAI)", "NHAI can use the system to identify critical segments of "
     "national highways. Prioritise maintenance budgets based on betweenness centrality and "
     "population impact scores."],
    ["Military |\nDefence", "Identify strategically critical road junctions for national security. "
     "Simulate enemy attacks on key infrastructure and plan redundant supply routes."],
    ["Post-Disaster\nDamage Survey", "After a landslide, upload post-disaster satellite images. "
     "The change detection ML model automatically identifies damaged roads by comparing with "
     "pre-disaster images — no manual surveying needed."],
]
story.append(make_table(["Use Case", "How the System Helps"], uc_rows, col_widths=[0.2*W, 0.8*W]))
story.append(PageBreak())


# ════════════════════════════════════════
# 13. TECHNOLOGY STACK
# ════════════════════════════════════════
story.append(heading("13. Technology Stack"))

tech_rows = [
    ["Machine Learning",    "PyTorch, torchvision, segmentation-models-pytorch"],
    ["Deep Learning Model", "U-Net with ResNet encoder backbone"],
    ["Explainability",      "Grad-CAM (Gradient-weighted Class Activation Mapping)"],
    ["Graph Analysis",      "NetworkX (centrality, MST, shortest paths, components)"],
    ["Geospatial",          "OSMnx, GeoPandas, Shapely, pyproj, rasterio"],
    ["Backend API",         "FastAPI (Python) + Uvicorn ASGI server"],
    ["Frontend",            "Next.js 14, React 18, TypeScript"],
    ["UI Components",       "Tailwind CSS, Radix UI, shadcn/ui"],
    ["Maps",                "Leaflet + react-leaflet (interactive map visualization)"],
    ["Charts",              "Recharts (data visualization library)"],
    ["LLM / NLP",           "Groq API (Llama / Mixtral for AI Copilot)"],
    ["Data Sources",        "OpenStreetMap, ISRO Bhuvan, WorldPop, SRTM DEM"],
]
story.append(make_table(["Category", "Technology"], tech_rows, col_widths=[0.25*W, 0.75*W]))
story.append(spacer())


# ════════════════════════════════════════
# 14. DATA FLOW
# ════════════════════════════════════════
story.append(heading("14. Data Flow"))
story.append(spacer(6))
story.append(create_data_flow_diagram())
story.append(caption("Figure 5: End-to-End Data Flow Through the System"))
story.append(spacer())

story.append(body(
    "<b>Detailed data flow:</b>"
))
story.append(bullet("<b>Raw Data →</b> Satellite images (GeoTIFF) + OSM road data (XML/JSON) + Population rasters + DEM tiles"))
story.append(bullet("<b>ML Processing →</b> U-Net segments road pixels → Skeletonize → Extract graph topology"))
story.append(bullet("<b>Graph Analysis →</b> Compute centrality metrics → Rank critical junctions → Calculate resilience score"))
story.append(bullet("<b>Simulation & AI →</b> Run disaster scenarios → Measure fragmentation → AI Copilot answers questions"))
story.append(bullet("<b>Dashboard & Reports →</b> Interactive maps + Charts + PDF reports + Healing recommendations"))
story.append(PageBreak())


# ════════════════════════════════════════
# 15. RESULTS & OUTPUTS
# ════════════════════════════════════════
story.append(heading("15. Results & Outputs"))

story.append(subhead("15.1 Graph Statistics (Bengaluru AOI)"))
stat_rows = [
    ["Total Nodes (Intersections)",   "13,486"],
    ["Total Edges (Road Segments)",    "19,117"],
    ["Average Node Degree",            "~2.84"],
    ["Graph Type",                     "MultiDiGraph (directed, weighted)"],
    ["Coordinate System",             "WGS 84 (EPSG:4326)"],
]
story.append(make_table(["Metric", "Value"], stat_rows, col_widths=[0.4*W, 0.6*W]))
story.append(spacer())

story.append(subhead("15.2 System Outputs"))
output_rows = [
    ["Criticality Heatmap", "Interactive map showing colour-coded junctions (red = most critical, green = least critical). Helps visually identify weak points at a glance."],
    ["Resilience Score", "A single number (0–1) representing overall network health. Drops after disasters, rises after interventions. Easy to track over time."],
    ["Disaster Impact Report", "Before/after comparison of all metrics: efficiency drop, new connected components, average detour increase, population isolated."],
    ["Healing Recommendations", "Ranked list of proposed new road segments with cost (km) and resilience gain (Δ efficiency). Actionable for government planners."],
    ["Evacuation Routes", "Computed safest paths from danger zones to shelters, considering road capacity and predicted damage."],
    ["AI Copilot Responses", "Natural-language answers to questions about the network, powered by Groq LLM with injected graph context."],
    ["PDF/HTML Reports", "Downloadable reports summarizing all findings — suitable for presentations to government officials."],
    ["Change Detection Maps", "Before/after satellite image comparison showing where roads were damaged or newly built."],
]
story.append(make_table(["Output", "Description"], output_rows, col_widths=[0.22*W, 0.78*W]))
story.append(PageBreak())


# ════════════════════════════════════════
# 16. FUTURE SCOPE
# ════════════════════════════════════════
story.append(heading("16. Future Scope"))
story.append(body("The project has significant potential for expansion:"))
story.append(spacer(4))

future_rows = [
    ["Real-Time Traffic Integration", "Connect to Google Maps / HERE traffic APIs to add real-time "
     "traffic flow as edge weights. Makes simulations more realistic."],
    ["Multi-City Support", "Currently focused on Bengaluru. Can be extended to any city worldwide "
     "with a city-selector UI and automatic OSM data download."],
    ["Live Satellite Monitoring", "Integrate with satellite data providers for near-real-time damage "
     "detection after disasters using the change detection ML model."],
    ["Mobile App", "Build a lightweight mobile app for field teams to report road damage and view "
     "evacuation routes during disasters."],
    ["GNN Integration", "Replace classical centrality with Graph Neural Network-based importance "
     "scoring for more nuanced predictions."],
    ["NDMA / SDMA Integration", "Direct API integration with National/State Disaster Management "
     "Authority systems for automated alert generation."],
    ["Historical Replay", "Load past disaster data and validate model predictions against actual "
     "damage — improving model accuracy over time."],
    ["Docker Deployment", "Containerise the entire system for one-command deployment on cloud "
     "platforms (AWS, GCP, Azure)."],
    ["Reinforcement Learning", "Use RL to optimize intervention strategies: which combination of "
     "new roads gives the best resilience gain within a fixed budget?"],
]
story.append(make_table(["Enhancement", "Description"], future_rows, col_widths=[0.28*W, 0.72*W]))
story.append(PageBreak())


# ════════════════════════════════════════
# 17. CONCLUSION
# ════════════════════════════════════════
story.append(heading("17. Conclusion"))
story.append(body(
    "The <b>Route Resilience System</b> demonstrates how <b>Machine Learning</b> can be applied "
    "to a real-world problem that affects millions of people. By combining <b>deep learning "
    "(U-Net)</b> for road extraction, <b>graph theory</b> for network analysis, and <b>simulation "
    "algorithms</b> for disaster modeling, the system provides a complete, end-to-end solution "
    "for urban road network resilience."
))
story.append(spacer(4))
story.append(body(
    "The system is not just a theoretical exercise — it produces <b>actionable insights</b> that "
    "governments can use to save lives and money. From identifying the single junction whose failure "
    "would cause the most damage, to recommending exactly where a new bypass road should be built, "
    "every output is designed to be <b>practical and decision-ready</b>."
))
story.append(spacer(4))
story.append(body(
    "With its <b>interactive dashboard</b>, <b>AI Copilot</b>, and <b>automated report generation</b>, "
    "the system makes complex ML and graph theory results accessible to non-technical users — "
    "city planners, disaster management officials, and even citizens."
))
story.append(spacer(8))

story.append(highlight(
    "<b>Key Takeaway:</b> This ML project proves that Deep Learning + Graph Theory can make "
    "cities safer, save government money, speed up emergency response, and ultimately save "
    "lives — all from satellite images and open-source road data."
))

story.append(spacer(20))
story.append(hr())
story.append(Paragraph("— End of ML Project Report —", styles["SmallNote"]))


# ═══════════ BUILD ═══════════
doc.build(story, onFirstPage=footer_fn, onLaterPages=footer_fn)
print(f"\n✅  PDF generated successfully: {OUTPUT}")
print(f"    Pages: ~{doc.page}")

