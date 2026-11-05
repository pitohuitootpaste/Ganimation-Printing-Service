from modules.storage import load_data

def view_all_quotations():
    quotations = load_data("quotations.json")
    print("\n========== ALL QUOTATIONS ==========")

    if not quotations:
        print("No quotations found.")
        return

    for quotation in quotations:
        print("----------------------------------------")
        print(f"Quotation ID: {quotation['quotation_id']}")
        print(f"Customer: {quotation['customer_name']}")
        print(f"Product: {quotation['product_name']}")
        print(f"Total: PHP {quotation['total_price']:,.2f}")
        print(f"Status: {quotation['status']}")


def view_pending_quotations():
    quotations = load_data("quotations.json")
    pending = [quotation for quotation in quotations if quotation["status"] == "Draft"]

    print("\n========== PENDING QUOTATIONS ==========")

    if not pending:
        print("No pending quotations found.")
        return

    for quotation in pending:
        print("----------------------------------------")
        print(f"Quotation ID: {quotation['quotation_id']}")
        print(f"Customer: {quotation['customer_name']}")
        print(f"Product: {quotation['product_name']}")
        print(f"Total: PHP {quotation['total_price']:,.2f}")
        print(f"Status: {quotation['status']}")


def view_finalized_quotations():
    quotations = load_data("quotations.json")
    finalized = [quotation for quotation in quotations if quotation["status"] == "Finalized"]

    print("\n========== FINALIZED QUOTATIONS ==========")

    if not finalized:
        print("No finalized quotations found.")
        return

    for quotation in finalized:
        print("----------------------------------------")
        print(f"Quotation ID: {quotation['quotation_id']}")
        print(f"Customer: {quotation['customer_name']}")
        print(f"Product: {quotation['product_name']}")
        print(f"Total: PHP {quotation['total_price']:,.2f}")
        print(f"Status: {quotation['status']}")


def view_quotation_menu():

    while True:

        print("\n================================")
        print("          VIEW QUOTATIONS")
        print("================================")
        print("1. View All Quotations")
        print("2. View Pending Quotations")
        print("3. View Finalized Quotations")
        print("0. Back")
        print("================================")
        choice = input("Enter choice: ")

        if choice == "1":
            view_all_quotations()

        elif choice == "2":
            view_pending_quotations()

        elif choice == "3":
            view_finalized_quotations()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
