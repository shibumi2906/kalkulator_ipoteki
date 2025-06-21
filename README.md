# 🏛️ Baroque Mortgage Calculator

A sophisticated mortgage calculator with a luxurious Baroque design theme, built with Python Flask and modern web technologies.

## ✨ Features

### 🎯 Core Functionality
- **Basic Mortgage Calculations**: Calculate monthly payments, total interest, and loan amortization
- **0% Interest Installment Plans**: Support for interest-free payment plans
- **Early Repayment Options**: 
  - Reduce monthly payment amount
  - Reduce loan term
  - Multiple early payments support
- **Detailed Payment Schedule**: Month-by-month breakdown of payments
- **Excel Export**: Export payment schedule to Excel (.xlsx) format

### 🎨 Design Features
- **Baroque Theme**: Luxurious dark design with gold accents
- **Responsive Layout**: Works on desktop and mobile devices
- **Interactive UI**: Smooth animations and transitions
- **Professional Styling**: Ornamental fonts and elegant color scheme

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>

   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to: `http://127.0.0.1:5000`

## 📋 Requirements

The following Python packages are required:

```
Flask==2.3.3
openpyxl==3.1.5
```

## 🎮 How to Use

### Basic Calculation
1. Enter the **Loan Amount** (e.g., 1000000)
2. Enter the **Loan Term** in months (e.g., 360 for 30 years)
3. Enter the **Interest Rate** as a percentage (e.g., 5.5)
4. Click **"Calculate"** to see results

### Installment Plan (0% Interest)
1. Click the **"Installment"** toggle button
2. The interest rate field will be hidden and set to 0%
3. Enter loan amount and term
4. Click **"Calculate"** for interest-free calculations

### Early Repayment
1. Perform a basic calculation first
2. In the **"Early Repayments"** section:
   - Enter payments in format: `month:amount` (e.g., `12:50000, 24:30000`)
   - Select reduction type: "Reduce Payment" or "Reduce Term"
3. Click **"Calculate"** to see updated schedule

### Export to Excel
1. After calculating, click the **"Export to Excel"** button
2. The payment schedule will be downloaded as an Excel file

## 🏗️ Project Structure

```
kalkulator_ipoteki/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Main HTML template
└── README.md          # This file
```

## 🔧 Technical Details

### Backend (Flask)
- **Framework**: Flask 2.3.3
- **Language**: Python 3.7+
- **Key Libraries**: 
  - `openpyxl` for Excel export functionality
  - Standard Python libraries for calculations

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Baroque styling with custom properties
- **JavaScript**: Interactive functionality
- **Fonts**: Playfair Display (Google Fonts)

### Key Features Implementation
- **Mortgage Calculations**: Standard amortization formulas
- **Early Repayment Logic**: Complex recalculation algorithms
- **Excel Export**: Dynamic worksheet generation
- **Responsive Design**: Mobile-first approach

## 🎨 Design Theme

The application features a **Baroque-inspired design** with:
- **Color Palette**: Dark browns, gold, and bronze
- **Typography**: Elegant serif fonts
- **Layout**: Ornamental borders and decorative elements
- **Animations**: Smooth transitions and hover effects

## 📊 Calculation Methods

### Standard Mortgage Formula
```
Monthly Payment = P × (r(1+r)^n) / ((1+r)^n - 1)
Where:
- P = Principal amount
- r = Monthly interest rate (annual rate ÷ 12)
- n = Total number of payments
```

### Early Repayment Logic
- **Reduce Payment**: Recalculates monthly payment with remaining balance
- **Reduce Term**: Maintains original payment, reduces total months
- **Multiple Payments**: Supports multiple early repayments at different months

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'openpyxl'**
   ```bash
   pip install openpyxl
   ```

2. **Port already in use**
   - Change the port in `app.py` or kill the existing process
   - Default port: 5000

3. **Calculation errors**
   - Ensure all inputs are positive numbers
   - Check that interest rate is reasonable (0-100%)
   - Verify early repayment format: `month:amount`

### Debug Mode
The application runs in debug mode by default. For production:
- Set `debug=False` in `app.py`
- Use a production WSGI server

## 📝 License

This project is created for educational purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📞 Support

For questions or issues, please check the troubleshooting section above or create an issue in the project repository.

---

**Built with ❤️ using Flask and modern web technologies** 