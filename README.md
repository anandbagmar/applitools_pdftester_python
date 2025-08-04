# PDF Visual Validation with Applitools Eyes

This script performs automated visual validation of PDF documents using the [Applitools Eyes](https://applitools.com/) Images SDK.  
It converts each page of a PDF to an image and sends it to Applitools for visual validation against a baseline.

> 📁 GitHub Repo: [https://github.com/anandbagmar/applitools_pdftester_python](https://github.com/anandbagmar/applitools_pdftester_python)

---

## 🔧 Requirements

- Python 3.7+
- [Poppler](https://github.com/jalan/pdfsandbox/wiki/Installing-Poppler) (used by `pdf2image`)
- Applitools Eyes API key

---

## 📦 Setup

### 1. Clone the repository

```bash
git clone https://github.com/anandbagmar/applitools_pdftester_python.git
cd tutorial-images-python
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Poppler

**macOS:**

```bash
brew install poppler
```

**Ubuntu/Debian:**

```bash
sudo apt install poppler-utils
```

**Windows:**

- Download Poppler for Windows: https://blog.alivate.com.au/poppler-windows/
- Extract and add the `bin/` folder to your `PATH` environment variable

---

## 🚀 Usage

```bash
python pdfTester.py \
  --api-key <APPLITOOLS_API_KEY> \
  --pdf-folder "/path/to/folder/with/pdfs" \
  --app-name "MyApp"
```

Or use environment variables:

```bash
export APPLITOOLS_API_KEY=<your_key>
python pdfTester.py --pdf-folder "/path/to/folder"
```

---

## 📂 What It Does

- Loops through all `.pdf` files in the given folder.
- Converts each page of the PDF to an image using `pdf2image`.
- Uses the filename (without `.pdf`) as the Applitools test name.
- Opens a new Eyes test every 100 pages (to avoid payload limits).
- Performs visual checks on each page image.
- Prints Applitools test results to the console.

---

## 🛠 Command-Line Arguments

| Argument         | Required | Description                                                          |
|------------------|----------|----------------------------------------------------------------------|
| `--api-key`      | No       | Applitools API key (fallback: `APPLITOOLS_API_KEY` env var)          |
| `--pdf-folder`   | Yes      | Path to folder containing PDF files                                  |
| `--app-name`     | No       | App name used in Applitools dashboard                                |

---

## ✅ Sample Output

```
📄 Processing 'Document_ABC.pdf' with 12 pages
  ✔️ Page #1-1
  ✔️ Page #1-2
  ...
  ✅ TestResult: TestResults(status=Passed, steps=12)
```

---

## 🧪 Tips

- For large PDFs, test with a few pages first to ensure setup works.
- Adjust DPI if image quality needs to be improved in `convert_from_path()`.
- View and manage baselines in the [Applitools Test Manager](https://eyes.applitools.com/).

---

## 📎 License

MIT license.

---

## 🙌 Contributing

Feel free to fork this repo and submit pull requests to add features, fix bugs, or improve performance.
