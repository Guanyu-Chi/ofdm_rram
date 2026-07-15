#!/usr/bin/env python3
"""Generate a compact PDF flow diagram without external dependencies."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "verification_flow.pdf"


def pdf_escape(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    width, height = 612, 360
    boxes = [
        (40, 235, 125, 64, "Configuration", "size, carriers, QAM"),
        (185, 235, 125, 64, "Matrix", "seeded Ron/Roff"),
        (330, 235, 125, 64, "Netlist", "128x128 read array"),
        (475, 235, 95, 64, "Testbench", "BPF/IQ/LPF"),
        (185, 85, 125, 64, "Simulation", "waveform results"),
        (330, 85, 125, 64, "Checks", "MVM, ADC, power"),
        (475, 85, 95, 64, "Paper", "tables, patches"),
    ]
    commands = ["0.95 0.95 0.95 rg", "0 0 0 RG", "1 w"]
    for x, y, w, h, title, body in boxes:
        commands.append(f"{x} {y} {w} {h} re B")
        commands.append("BT /F1 11 Tf")
        commands.append(f"{x + 10} {y + h - 24} Td ({pdf_escape(title)}) Tj")
        commands.append("ET")
        commands.append("BT /F1 8 Tf")
        commands.append(f"{x + 10} {y + 18} Td ({pdf_escape(body)}) Tj")
        commands.append("ET")
    arrows = [
        (165, 267, 185, 267), (310, 267, 330, 267), (455, 267, 475, 267),
        (247, 235, 247, 149), (310, 117, 330, 117), (455, 117, 475, 117),
    ]
    commands.append("0 0 0 RG")
    for x1, y1, x2, y2 in arrows:
        commands.append(f"{x1} {y1} m {x2} {y2} l S")
        commands.append(f"{x2 - 5} {y2 + 3} m {x2} {y2} l {x2 - 5} {y2 - 3} l S")
    commands.append("BT /F1 13 Tf 40 325 Td (Configuration-driven verification generation flow) Tj ET")
    stream = "\n".join(commands).encode("ascii")
    objects = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>".encode("ascii"))
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream")
    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{idx} 0 obj\n".encode("ascii"))
        out.extend(obj)
        out.extend(b"\nendobj\n")
    xref = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    out.extend(f"trailer << /Root 1 0 R /Size {len(objects) + 1} >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii"))
    OUT.write_bytes(out)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
