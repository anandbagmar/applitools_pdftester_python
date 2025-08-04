import os
import argparse
from pathlib import Path
from applitools.images import Eyes, Target
from applitools.common import Configuration, BatchInfo
from pdf2image import convert_from_path


def validate_pdf(pdf_path: Path, api_key: str, app_name: str):
    # test_name = pdf_path.stem  # File name without extension
    folder_name = pdf_path.parent.name
    file_stem = pdf_path.stem
    base_test_name = f"{folder_name}_{file_stem}"

    config = Configuration()
    config.api_key = api_key
    config.server_url = os.getenv("APPLITOOLS_SERVER_URL", "https://eyes.applitools.com")
    config.app_name = app_name
    config.host_app = app_name
    config.batch = BatchInfo(app_name)
    config.set_save_new_tests(True)
    config.set_match_level("Strict")
    config.ignore_displacements = True

    eyes = Eyes()
    eyes.set_configuration(config)

    try:
        pages = convert_from_path(str(pdf_path))
        print(f"\n📄 Processing '{pdf_path}' with {len(pages)} pages")
        slice_count = 1

        for i, image in enumerate(pages):
            if i % 100 == 0:
                eyes.open(app_name, f"{base_test_name}-{slice_count}")

            print(f"  ✔️ Page #{slice_count}-{i + 1}")
            eyes.check(f"Page #{slice_count}-{i + 1}", Target.image(image))

            if (i + 1) % 100 == 0 or (i + 1) == len(pages):
                result = eyes.close(False)
                print("  ✅ TestResult:", result)
                slice_count += 1

    except Exception as e:
        print(f"  ❌ Error processing '{pdf_path.name}':", e)
    # finally:
        # eyes.abort_if_not_closed()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visual validation of PDFs using Applitools Eyes")
    parser.add_argument("--api-key", help="Applitools API key (fallback to APPLITOOLS_API_KEY env var)")
    parser.add_argument("--pdf-folder", required=True, help="Path to folder containing PDFs (searched recursively)")
    parser.add_argument("--app-name", required=True, help="Application name to use in Applitools")

    args = parser.parse_args()
    api_key = args.api_key or os.getenv("APPLITOOLS_API_KEY")

    if not api_key:
        raise ValueError("Applitools API key must be provided via --api-key or APPLITOOLS_API_KEY env var")

    pdf_folder = Path(args.pdf_folder)
    if not pdf_folder.exists() or not pdf_folder.is_dir():
        raise ValueError(f"Provided path '{pdf_folder}' is not a valid directory")

    # 🔍 Recursively search for PDF files
    print(f"Scanning: {pdf_folder.resolve()}")
    pdf_files = [p for p in pdf_folder.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf"]
    if not pdf_files:
        print("No PDF files found in the folder or subfolders.")
    else:
        print(f"Found {len(pdf_files)} PDF file(s):")
        for pdf_file in pdf_files:
            print(f" - {pdf_file.resolve()}")
            validate_pdf(pdf_file, api_key, args.app_name)
