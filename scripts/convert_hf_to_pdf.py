from datasets import load_from_disk
from fpdf import FPDF
from pathlib import Path

# Output directory for PDFs
output_dir = Path("Therapy_Guides")
output_dir.mkdir(exist_ok=True)

# Path to the DejaVuSans.ttf font file (user must download and place in project root)
FONT_PATH = "DejaVuSans.ttf"  # Download from https://dejavu-fonts.github.io/

def dataset_to_pdf(dataset_path, text_fields, output_pdf):
    ds = load_from_disk(dataset_path)
    print(f"\n--- {dataset_path} ---")
    print("Available fields:", ds.column_names)
    print("First row:", ds[0] if len(ds) > 0 else "No data")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=12)

    count = 0
    for row in ds:
        text = "\n".join([str(row.get(f, "")) for f in text_fields if f in row and row[f]])
        if text.strip():
            pdf.multi_cell(0, 10, text)
            pdf.ln(5)
            count += 1

    pdf.output(str(output_pdf))
    print(f"Saved {output_pdf} with {count} entries.")

if __name__ == "__main__":
    # Convert local_counsel_chat (use correct field names)
    dataset_to_pdf(
        "local_counsel_chat",
        ["questionText", "answerText"],
        output_dir / "counsel_chat.pdf"
    )
    # Convert local_mental_health_counseling (use correct field names)
    dataset_to_pdf(
        "local_mental_health_counseling",
        ["Context", "Response"],
        output_dir / "mental_health_counseling.pdf"
    )
    # Convert local_psych8k
    dataset_to_pdf(
        "local_psych8k",
        ["input", "output"],
        output_dir / "psych8k.pdf"
    )

# INSTRUCTIONS:
# Download DejaVuSans.ttf from https://dejavu-fonts.github.io/ and place it in your project root before running this script. 