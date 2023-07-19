from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee, Payslip
from django.contrib import messages

# Create your views here.
def employees(request):
    employee_objects = Employee.objects.all()
    return render(request, 'payroll_app/employees.html', {'employees':employee_objects})

def payslips(request):
    employee_objects = Employee.objects.all()
    payslips_objects = Payslip.objects.all()
    if(request.method == "POST"):
        id_input = request.POST.get("employee")
        month_input = request.POST.get("month")
        year_input = request.POST.get("year")
        cycle_input = int(request.POST.get("cycle"))
        if id_input == "All":
            for x in employee_objects:
                ot = x.getOvertime() or 0
                allowance = x.getAllowance() 
                rate = x.getRate()
                if cycle_input == 1:
                    pag_ibig = 100
                    tax = ((rate / 2) + allowance + ot - pag_ibig)*0.2
                    total_pay = ((rate / 2) + allowance + ot - pag_ibig)*0.8
                    # checks if a payslip already exists for an employee
                    existing_payslip = Payslip.objects.filter(id_number=x, month=month_input, year=year_input, pay_cycle=cycle_input).first()
                    if existing_payslip:
                        messages.error(request, f"Payslip already exists: {x.name} ({month_input}-{year_input})")
                    else:
                        Payslip.objects.create(id_number=x, month=month_input, year=year_input, pay_cycle=cycle_input, date_range="1-15",  overtime=ot, rate=rate, earnings_allowance=allowance,deductions_tax=tax, deductions_health=0, pag_ibig=pag_ibig, sss=0, total_pay=total_pay)
                else:
                    sss = rate*0.045
                    philhealth = rate*0.04
                    tax = ((rate / 2) + allowance + ot - sss - philhealth)*0.2
                    deductions_health=philhealth
                    total_pay = ((rate / 2) + allowance + ot - sss - philhealth)*0.8
                    # checks if a payslip already exists for an employee
                    existing_payslip = Payslip.objects.filter(id_number=x, month=month_input, year=year_input, pay_cycle=cycle_input).first()
                    if existing_payslip:
                        messages.error(request, f"Payslip already exists: {x.name} ({month_input}-{year_input})")
                    else:
                        Payslip.objects.create(id_number=x, month=month_input, year=year_input, pay_cycle=cycle_input, date_range="16-30",  overtime=ot, rate=rate, earnings_allowance=allowance,deductions_tax=tax, deductions_health=deductions_health, pag_ibig=0, sss=sss, total_pay=total_pay)
                x.resetOvertime() # 
        else:
            employee = get_object_or_404(Employee, id_number=id_input)
            ot = employee.getOvertime()
            allowance = employee.getAllowance()
            rate = employee.getRate()
            if cycle_input == 1:
                pag_ibig = 100
                tax = ((rate / 2) + allowance + ot - pag_ibig)*0.2
                total_pay = ((rate / 2) + allowance + ot - pag_ibig)*0.8
                # checks if a payslip already exists for an employee
                existing_payslip = Payslip.objects.filter(id_number=employee, month=month_input, year=year_input, pay_cycle=cycle_input).first()
                if existing_payslip:
                    messages.error(request, f"Payslip already exists: {employee.name} ({month_input}-{year_input})")
                else:
                    Payslip.objects.create(id_number=employee, month=month_input, year=year_input, date_range="1-15", pay_cycle=cycle_input, overtime=ot, rate=rate, earnings_allowance=allowance,deductions_tax=tax, deductions_health=0, pag_ibig=pag_ibig, sss=0, total_pay=total_pay)
            else:
                sss = rate*0.045
                philhealth = rate*0.04
                deductions_health=philhealth
                tax = ((rate / 2) + allowance + ot - sss - philhealth)*0.2
                total_pay2 = ((rate / 2) + allowance + ot - sss - philhealth)*0.8
                # checks if a payslip already exists for an employee
                existing_payslip = Payslip.objects.filter(id_number=employee, month=month_input, year=year_input, pay_cycle=cycle_input).first()
                if existing_payslip:
                    messages.error(request, f"Payslip already exists: {employee.name} ({month_input}-{year_input})")
                else:
                    Payslip.objects.create(id_number=employee, month=month_input, year=year_input, date_range="16-30", pay_cycle=cycle_input, overtime=ot, rate=rate, earnings_allowance=allowance,deductions_tax=tax, deductions_health=deductions_health, pag_ibig=0, sss=sss, total_pay=total_pay2)
            employee.resetOvertime() # 
        return redirect('payslips')
    
    else:
        return render(request, 'payroll_app/payslips.html', {'employees':employee_objects, 'payslips':payslips_objects})

def view_payslip(request, id, month, year, cycle):
    employee = get_object_or_404(Employee, id_number = id)
    payslip = get_object_or_404(Payslip, id_number = employee, month = month, year=year, pay_cycle=cycle)
    if cycle == 1:
        return render(request, 'payroll_app/view_payslips1.html', {'d':payslip})
    else: 
        return render(request, 'payroll_app/view_payslips2.html', {'d':payslip})

def add_employee(request):
    if(request.method=="POST"):
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')
        try: 
            Employee.objects.create(name=name, id_number=id_number, rate=rate, allowance=allowance)
            return redirect('add_employee')
        except:
            return redirect('employees')
    else:
        return render(request, 'payroll_app/add_employee.html')
    
def update_employee(request, id_number):
    if(request.method=="POST"):
        name = request.POST.get('name')
        id_number1 = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')
        try: 
            Employee.objects.filter(id_number=id_number).update(name=name, id_number=id_number1, rate=rate, allowance=allowance)
            return redirect('employees')
        except:
            return redirect('add_employee')
    else:
        employee_object = get_object_or_404(Employee, id_number=id_number)
        return render(request, 'payroll_app/update_employee.html', {'x':employee_object})
    
def add_overtime(request, id_number):
    if(request.method=="POST"):
        overtime_hours = request.POST.get('overtime')
        employee = get_object_or_404(Employee, id_number=id_number)
        overtime = (employee.rate/160)*(1.5)*int(overtime_hours) 
        current_overtime = employee.overtime_pay or 0
        Employee.objects.filter(id_number=id_number).update(overtime_pay= float(current_overtime) + float(overtime))
        return redirect('employees')
   
def delete_employee(request, id_number):
    Employee.objects.filter(id_number=id_number).delete()
    return redirect('employees')

def delete_payslip(request, id, month, year, cycle):
    employee = get_object_or_404(Employee, id_number=id)
    Payslip.objects.filter(id_number = employee, month = month, year=year, pay_cycle=cycle).delete()
    return redirect('payslips')

def about_us(request):
    return render(request, 'payroll_app/about_us.html')
        