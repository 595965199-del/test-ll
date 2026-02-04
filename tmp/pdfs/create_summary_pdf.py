from pathlib import Path

def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_text_stream(lines):
    parts = ["BT"]
    for font, size, x, y, text in lines:
        parts.append(f"/{font} {size} Tf")
        parts.append(f"{x} {y} Td")
        parts.append(f"({pdf_escape(text)}) Tj")
        parts.append("0 0 Td")
    parts.append("ET")
    return "\n".join(parts)


def write_pdf(path: Path, lines):
    stream = build_text_stream(lines)
    stream_bytes = stream.encode("latin-1")

    objects = []
    objects.append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    objects.append("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    objects.append(
        "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> >>\nendobj\n"
    )
    objects.append(
        "4 0 obj\n<< /Length {length} >>\nstream\n{stream}\nendstream\nendobj\n".format(
            length=len(stream_bytes), stream=stream
        )
    )
    objects.append("5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    objects.append("6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")

    content = "%PDF-1.4\n".encode("latin-1")
    xref_positions = [0]
    for obj in objects:
        xref_positions.append(len(content))
        content += obj.encode("latin-1")

    xref_start = len(content)
    xref_lines = ["xref", f"0 {len(objects) + 1}", "0000000000 65535 f "]
    for pos in xref_positions[1:]:
        xref_lines.append(f"{pos:010d} 00000 n ")
    xref = "\n".join(xref_lines) + "\n"
    content += xref.encode("latin-1")

    trailer = (
        "trailer\n<< /Size {size} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
        .format(size=len(objects) + 1, xref=xref_start)
    )
    content += trailer.encode("latin-1")

    path.write_bytes(content)


OUTPUT = Path("/Users/lilin/web/test/output/pdf/app-summary.pdf")

lines = []

def add_line(text, size, x, y, bold=False):
    font = "F2" if bold else "F1"
    lines.append((font, size, x, y, text))

add_line("Registration UI Kit Summary", 22, 72, 740, bold=True)
add_line("Project snapshot for five distinct signup experiences", 11, 72, 718)

add_line("Overview", 14, 72, 680, bold=True)
add_line("This app delivers five visual styles for user registration pages.", 11, 72, 660)
add_line("Each style includes account, email, password, and confirm password fields.", 11, 72, 644)
add_line("Design goal: offer clear visual differentiation for A/B tests or product lines.", 11, 72, 628)

add_line("Pages", 14, 72, 596, bold=True)
add_line("- signup-neon.html: cyber neon, glow and scanline inspired UI.", 11, 72, 576)
add_line("- signup-editorial.html: editorial print feel with stamp and dashed frame.", 11, 72, 560)
add_line("- signup-brutal.html: brutalist blocks, hard borders, bold contrast.", 11, 72, 544)
add_line("- signup-harvest.html: warm seasonal palette with grain texture.", 11, 72, 528)
add_line("- signup-minimal.html: clean workspace style with restrained accents.", 11, 72, 512)

add_line("Entry", 14, 72, 480, bold=True)
add_line("index.html lists the five single pages for quick navigation.", 11, 72, 460)

add_line("Shared Styling", 14, 72, 428, bold=True)
add_line("styles.css provides shared layout, form styling, and theme variations.", 11, 72, 408)

add_line("Notes", 14, 72, 376, bold=True)
add_line("- Forms are static HTML for layout review; no backend wiring included.", 11, 72, 356)
add_line("- Mobile layout adapts via a responsive grid and flexible card widths.", 11, 72, 340)

add_line("Generated on 2026-02-04", 9, 72, 300)

write_pdf(OUTPUT, lines)
print(f"Wrote {OUTPUT}")
