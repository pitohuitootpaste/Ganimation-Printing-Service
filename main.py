from modules.createQuotation import create_quotation
from modules.manageQuotations import manage_quotations_menu
from modules.viewQuotations import view_quotation_menu

while True:

    print("\n================================")
    print("    GANIMATION PRINTING SERVICE")
    print("================================")
    print("1. Create Quotation")
    print("2. View Quotation")
    print("3. Manage Quotations")
    print("0. Exit")
    print("================================")
    choice = input("Enter choice: ")

    if choice == "1":
        create_quotation()

    elif choice == "2":
        view_quotation_menu()

    elif choice == "3":
        manage_quotations_menu()

    elif choice == "0":
        print("Exiting Ganimation Printing Service...")
        break

    else:
        print("Invalid choice. Please try again.")
