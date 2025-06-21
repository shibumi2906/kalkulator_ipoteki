from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import io
import openpyxl

app = Flask(__name__)

def calculate_mortgage(principal, years, rate):
    months = years * 12
    monthly_rate = rate / 100 / 12
    if monthly_rate == 0:
        monthly_payment = principal / months if months > 0 else 0
        overpayment = 0
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        total_payment = monthly_payment * months
        overpayment = total_payment - principal
    
    schedule = []
    balance = principal
    for m in range(1, months + 1):
        if balance < 0.01:
            break
        interest = balance * monthly_rate
        principal_part = monthly_payment - interest
        if balance < monthly_payment:
            principal_part = balance
            monthly_payment = principal_part + interest
        balance -= principal_part
        schedule.append({
            'month': m, 'payment': monthly_payment, 'interest': interest, 
            'principal': principal_part, 'prepayment': 0, 'balance': balance
        })
    return round(overpayment, 2), round(monthly_payment, 2), schedule

def parse_prepayments(text):
    preps = {}
    if not text:
        return preps
    for part in text.split(','):
        part = part.strip()
        if not part:
            continue
        try:
            month, amount = part.split(':')
            month = int(month)
            amount = float(amount.replace(',', '.').strip())
            if month > 0 and amount > 0:
                preps[month] = preps.get(month, 0) + amount
        except (ValueError, TypeError):
            continue
    return preps

def calculate_mortgage_with_prepayments(principal, years, rate, prepayments, reduce_type):
    initial_months = years * 12
    monthly_rate = rate / 100 / 12
    
    if monthly_rate == 0:
        monthly_payment = principal / initial_months if initial_months > 0 else 0
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** initial_months) / (((1 + monthly_rate) ** initial_months) - 1)

    balance = principal
    schedule = []
    total_overpayment = 0.0
    
    for m in range(1, initial_months + 2): 
        if balance < 0.01:
            break

        interest = balance * monthly_rate
        
        # Determine payment parts
        principal_part = monthly_payment - interest
        prepayment_amount = prepayments.get(m, 0)

        # Handle final payment and overpayment
        if (balance + prepayment_amount) < principal_part:
            principal_part = balance
            prepayment_amount = 0
            monthly_payment = principal_part + interest

        total_paid_principal = principal_part + prepayment_amount
        if balance < total_paid_principal:
            diff = total_paid_principal - balance
            prepayment_amount -= diff
            if prepayment_amount < 0: prepayment_amount = 0
            principal_part = balance - prepayment_amount
        
        balance -= (principal_part + prepayment_amount)
        total_overpayment += interest
        
        schedule.append({
            'month': m, 'payment': monthly_payment, 'interest': interest, 'principal': principal_part, 
            'prepayment': prepayment_amount, 'balance': balance
        })

        if prepayment_amount > 0:
            if reduce_type == 'payment' and balance > 0.01:
                remaining_months = initial_months - m
                if remaining_months > 0:
                    if monthly_rate == 0:
                        monthly_payment = balance / remaining_months
                    else:
                        monthly_payment = balance * (monthly_rate * (1 + monthly_rate) ** remaining_months) / (((1 + monthly_rate) ** remaining_months) - 1)
    
    final_payment = schedule[-1]['payment'] if schedule else 0
    return round(total_overpayment, 2), round(final_payment, 2), schedule

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    monthly = None
    schedule = None
    if request.method == 'POST':
        try:
            principal = float(request.form['principal'].replace(',', '.').strip())
            years = int(request.form['years'].strip())
            
            if request.form.get('installment', '0') == '1':
                rate = 0.0
            else:
                rate = float(request.form['rate'].replace(',', '.').strip())

            prepayments_str = request.form.get('prepayments', '')
            prepayments = parse_prepayments(prepayments_str)
            reduce_type = request.form.get('reduce_type', 'payment')

            if principal <= 0 or years <= 0 or rate < 0:
                result = 'Ошибка: все значения должны быть положительными.'
            else:
                if prepayments:
                    result, monthly, schedule = calculate_mortgage_with_prepayments(principal, years, rate, prepayments, reduce_type)
                else:
                    result, monthly, schedule = calculate_mortgage(principal, years, rate)
        except (ValueError, TypeError):
            result = 'Ошибка ввода: проверьте формат чисел.'
        except Exception as e:
            result = f'Произошла ошибка: {e}'

    return render_template('index.html', result=result, monthly=monthly, schedule=schedule, form_data=request.form)

@app.route('/export', methods=['POST'])
def export():
    try:
        principal = float(request.form['principal'].replace(',', '.').strip())
        years = int(request.form['years'].strip())
        if request.form.get('installment', '0') == '1':
            rate = 0.0
        else:
            rate = float(request.form['rate'].replace(',', '.').strip())
        prepayments_str = request.form.get('prepayments', '')
        prepayments = parse_prepayments(prepayments_str)
        reduce_type = request.form.get('reduce_type', 'payment')
        if principal <= 0 or years <= 0 or rate < 0:
            return 'Ошибка: все значения должны быть положительными.', 400
        if prepayments:
            _, _, schedule = calculate_mortgage_with_prepayments(principal, years, rate, prepayments, reduce_type)
        else:
            _, _, schedule = calculate_mortgage(principal, years, rate)
        # Формируем Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'График платежей'
        ws.append(['Месяц', 'Платёж', 'Проценты', 'Основной долг', 'Досрочно', 'Остаток долга'])
        for row in schedule:
            ws.append([
                row['month'],
                round(row['payment'],2),
                round(row['interest'],2),
                round(row['principal'],2),
                round(row['prepayment'],2) if row['prepayment'] else '',
                round(row['balance'],2)
            ])
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = 15
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name='mortgage_schedule.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        return f'Ошибка экспорта: {e}', 500

if __name__ == '__main__':
    app.run(debug=True) 