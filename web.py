import streamlit as st


def calculate_monthly_payment(principal, annual_interest_rate, loan_term_years):
  monthly_interest_rate = annual_interest_rate / 1200  
  number_of_payments = loan_term_years * 12
  monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)
  return monthly_payment

def calculate_expense(age2):
  expense_tiers = {
      (0, 3): 1500,
      (4, 9): 3000,
      (10, 13): 4500,
      (14, 21): 6000,
      (22, 60): 7500,
      (61, 100): 9000
  }

  for age_range, expense in expense_tiers.items():
    if age_range[0] <= age2 <= age_range[1]:
      return expense

  return None


def main():

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    occupations_salary = {
        "Unemployed": 0.0,
        "Software Engineer": 38118.0,
        "Data Scientist": 50942.0,
        "Healthcare Professional": 235102.0,
        "Entrepreneur": 38166.0,
        "Environmental Scientist": 35000.0,
    }
    age = {i: i for i in range(18, 200)}
    children = {i: i for i in range(0, 101)}
    house_fam = {i: i for i in range(0, 101)}
    months = {i: i for i in range(0, 101)}

    total_cost = 0
    expense = 0.0
    income = 0.0
    household_member = 1
    
    cost_per_person = {
        "1-3": 1500,
        "4-9": 3000,
        "9-13": 4500,
        "13-21": 6000,
        "21-60": 7500,
        "60-100": 9000
    }

    age2 = st.selectbox("Age", list(age.keys()))
    expense = calculate_expense(age2)

    work_salary = st.selectbox("Occupations", list(occupations_salary.keys()))
    if work_salary:
        income += occupations_salary[work_salary]

    status_choice = st.selectbox("Category", ["Single", "Married", "Divorce"])
    if status_choice == "Married":
        household_member += 1
        married_salary = st.selectbox("Husband/Wife Occupation", list(occupations_salary.keys()))

        if married_salary:
            income += occupations_salary[married_salary]
            


    num_child = st.selectbox("Children", list(children.keys()))
    if num_child:
        household_member += children[num_child]
    if num_child > 0:
        age_ranges = ["1-3", "4-9", "9-13", "13-21", "21-60", "60-100"]
        selected_age_range = st.selectbox("Select average age range:", age_ranges)
        average_cost_per_person_per_year = cost_per_person[selected_age_range]
        expense += num_child * average_cost_per_person_per_year



    num_fam = st.selectbox("How many other family members live in your home besides your spouse and children?", list(house_fam.keys()))
    if num_fam:
        household_member += house_fam[num_fam]
        expense += household_member * 1500

    st.write("Household Member:", household_member)

    principal = st.number_input("Loan Amount", min_value=1000)
    interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.01, format="%.2f")
    loan_term_years = st.number_input("Loan Term (years)", min_value=1)

    if st.button("Calculate"):
        monthly_payment = calculate_monthly_payment(principal, interest_rate, loan_term_years)
        extra_money = income - expense
        if monthly_payment > extra_money:
            st.error(f"You can`t loan")
        elif monthly_payment < extra_money:
            st.success(f"You can loan")
        st.write(f"Your monthly payment is: ${monthly_payment:.2f}")
        st.write("Expense Cost: ₱", expense)
        st.write("Income Cost: ₱", income)
        if extra_money > 0:
            st.write("Extra Money: ₱", extra_money)

    


if __name__ == "__main__":
    main()
