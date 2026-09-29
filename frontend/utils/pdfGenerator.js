/**
 * Client-side minimal PDF generator for certificates and reports.
 * Emits standard PDF-1.4 format without external binary bloat.
 */
export function generateClientPdfBlob(title, subtitle, paragraphs = []) {
  const escapePdf = (str) =>
    (str || "")
      .replace(/[^\x20-\x7E]/g, " ")
      .replaceAll("\\", "\\\\")
      .replaceAll("(", "\\(")
      .replaceAll(")", "\\)");

  const lines = [
    "BT",
    "/F1 16 Tf",
    "50 740 Td",
    `(${escapePdf(title)}) Tj`,
    "/F1 10 Tf",
    "0 -22 Td",
    `(${escapePdf(subtitle)}) Tj`,
    "0 -18 Td",
    "(--------------------------------------------------------------------------------) Tj",
    "/F1 9 Tf",
  ];
  paragraphs.slice(0, 24).forEach((p) => {
    lines.push("0 -15 Td");
    lines.push(`(${escapePdf((p || "").slice(0, 95))}) Tj`);
  });
  lines.push("ET");
  const streamContent = lines.join("\n");
  const streamLen = streamContent.length;

  const part1 = "%PDF-1.4\n";
  const part2 = "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n";
  const part3 = "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n";
  const part4 =
    "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n";
  const part5 = `4 0 obj\n<< /Length ${streamLen} >>\nstream\n${streamContent}\nendstream\nendobj\n`;
  const part6 =
    "5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n";

  const body = part1 + part2 + part3 + part4 + part5 + part6;
  const o1 = body.indexOf("1 0 obj");
  const o2 = body.indexOf("2 0 obj");
  const o3 = body.indexOf("3 0 obj");
  const o4 = body.indexOf("4 0 obj");
  const o5 = body.indexOf("5 0 obj");
  const xrefPos = body.length;

  const pad10 = (n) => String(n).padStart(10, "0");
  const xref =
    `xref\n0 6\n` +
    `0000000000 65535 f \n` +
    `${pad10(o1)} 00000 n \n` +
    `${pad10(o2)} 00000 n \n` +
    `${pad10(o3)} 00000 n \n` +
    `${pad10(o4)} 00000 n \n` +
    `${pad10(o5)} 00000 n \n` +
    `trailer\n<< /Size 6 /Root 1 0 R >>\n` +
    `startxref\n${xrefPos}\n%%EOF\n`;

  return new Blob([body + xref], { type: "application/pdf" });
}
