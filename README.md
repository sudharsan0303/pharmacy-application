# 💊 Pharmacy Application

An online **Pharmacy Application** built with **Flask**, **FastAPI**, and **SQLite** that allows users to upload prescriptions, search medicines, manage carts, and place orders.  
It integrates **OCR (Optical Character Recognition)** using **Tesseract** and **OpenCV** to extract data from medical PDFs for faster and easier order processing.

---

## 🧩 Key Features

- **Role-based access:** Separate dashboards for customers and admins.  
- **Customer functions:** Register/login, search and filter medicines, manage cart, and place orders.  
- **Admin functions:** Add or update medicines (name, description, image, price, stock), view inventory, and manage order statuses.

---

## 📄 OCR Integration

Automatically extracts data from uploaded prescription PDFs using:  
- `pdf2image` + **Poppler** → Page rasterization  
- **OpenCV** → Image enhancement  
- **Tesseract OCR** → Text recognition  
- **Regex** → Extracts key fields such as name, address, medicines, dosage, etc.  

The **FastAPI + Streamlit** interface allows users to preview and correct extracted data before continuing.

---

## 🗃️ Tech Stack

- **Backend:** Flask, FastAPI  
- **Frontend:** Streamlit  
- **Database:** SQLite  
- **Libraries:** OpenCV, Tesseract, pdf2image  

---

## ⚙️ Highlights

- Modular Flask blueprints for clean structure  
- Lightweight local SQLite database for easy development  
- Smooth workflow from OCR upload to order placement  
- Extensible architecture for better security and document parsing  

---

## 🚀 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/pharmacy-application.git
cd pharmacy-application

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
