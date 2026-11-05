from datetime import datetime

from modules.storage import load_data, save_data
from modules.emailSender import send_finalized_quotation_email
from modules.pricing import calculate_totals

def show_available_quotations(quotations, heading, empty_message):
    print(f"\n========== {heading} ==========")

    if not quotations:
        print(empty_message)
        return False

    for quotation in quotations:
        print("----------------------------------------")
        print(f"Quotation ID: {quotation['quotation_id']}")
        print(f"Customer: {quotation['customer_name']}")
        print(f"Product: {quotation['product_name']}")
        print(f"Total: PHP {quotation['total_price']:,.2f}")
        print(f"Status: {quotation['status']}")

    return True

def edit_quotation():
    quotations = load_data("quotations.json")
    editable = [q for q in quotations if q["status"] == "Draft"]

    if not show_available_quotations(
        editable,
        "QUOTATIONS AVAILABLE TO EDIT",
        "No draft quotations are available to edit."
    ):
        return

    quotation_id = input("\nEnter Quotation ID (or . to exit): ").strip()
    if quotation_id == ".":
        print("Edit cancelled.")
        return

    try:
        quotation_id = int(quotation_id)
    except ValueError:
        print("Invalid quotation ID.")
        return

    quotation = next(
        (q for q in editable if q["quotation_id"] == quotation_id),
        None
    )

    if quotation is None:
        print("That quotation is not available to edit.")
        return

    print("\nLeave a field blank to keep its current value.")
    customer_name = input(f"Customer Name ({quotation['customer_name']}): ").strip()
    phone_number = input(
        f"Phone Number ({quotation['phone_number']}) (Enter = keep, ... = clear): "
    ).strip()
    email = input(f"Email ({quotation['email']}): ").strip()
    product_name = input(f"Product ({quotation['product_name']}): ").strip()

    if customer_name:
        quotation["customer_name"] = customer_name

    if phone_number == "...":
        quotation["phone_number"] = ""
    elif phone_number:
        quotation["phone_number"] = phone_number

    if email:
        if email.count("@") == 1 and "." in email.rsplit("@", 1)[1]:
            quotation["email"] = email
        else:
            print("Email was not changed because it is not valid.")

    if product_name:
        quotation["product_name"] = product_name

    while True:
        current_rush = "Y" if quotation.get("is_rush_order", False) else "N"
        rush_input = input(
            f"Rush Order? (Y/N) [{current_rush}; Enter = keep]: "
        ).strip().lower()

        if not rush_input:
            break
        if rush_input == "y":
            quotation["is_rush_order"] = True
            break
        if rush_input == "n":
            quotation["is_rush_order"] = False
            break
        print("Please enter Y, N, or press Enter to keep the current value.")

    while True:
        quantity = input(f"Quantity ({quotation['quantity']}): ")
        
        if not quantity:
            break

        try:
            quantity = int(quantity)

            if quantity <= 0:
                print("Quantity must be greater than 0.")
                continue

            quotation["quantity"] = quantity
            break
        
        except ValueError:
            print("Invalid quantity.")

    while True:
        price = input(f"Price Per Product ({quotation['price_per_product']}): ")

        if not price:
            break

        try:
            price = float(price)

            if price < 0:
                print("Price cannot be negative.")
                continue

            quotation["price_per_product"] = price
            break

        except ValueError:
            print("Invalid price.")

    while True:
        discount = input(f"Discount ({quotation['discount']}%): ")

        if not discount:
            break

        try:
            discount = float(discount)

            if discount < 0 or discount > 100:
                print("Discount must be between 0 and 100.")
                continue

            quotation["discount"] = discount
            break

        except ValueError:
            print("Invalid discount.")

    instructions = input(
        f"Special Instructions ({quotation['special_instructions']}) "
        "(Enter = keep, ... = clear): "
    ).strip()

    if instructions == "...":
        quotation["special_instructions"] = ""
    elif instructions:
        quotation["special_instructions"] = instructions

    subtotal, rush_fee, total_price = calculate_totals(
        quotation["quantity"],
        quotation["price_per_product"],
        quotation["discount"],
        quotation.get("is_rush_order", False)
    )
    quotation["subtotal"] = subtotal
    quotation["rush_fee"] = rush_fee
    quotation["total_price"] = total_price
    save_data("quotations.json", quotations)
    print("\nQuotation updated successfully!")

def delete_quotation():

    quotations = load_data("quotations.json")
    deletable = [q for q in quotations if q["status"] == "Draft"]

    if not show_available_quotations(
        deletable,
        "QUOTATIONS AVAILABLE TO DELETE",
        "No draft quotations are available to delete."
    ):
        return

    quotation_id = input("\nEnter Quotation ID (or . to exit): ").strip()
    if quotation_id == ".":
        print("Deletion cancelled.")
        return

    try:
        quotation_id = int(quotation_id)
    except ValueError:
        print("Invalid quotation ID.")
        return

    quotation = next(
        (q for q in deletable if q["quotation_id"] == quotation_id),
        None
    )

    if quotation is None:
        print("That quotation is not available to delete.")
        return

    confirm = input(
        f"Delete quotation {quotation_id}? (Y/N): "
    ).lower()

    if confirm != "y":
        print("Deletion cancelled.")
        return

    quotations.remove(quotation)
    save_data("quotations.json", quotations)
    print("Quotation deleted successfully!")

def finalize_quotation():

    quotations = load_data("quotations.json")
    finalizable = [q for q in quotations if q["status"] == "Draft"]

    if not show_available_quotations(
        finalizable,
        "QUOTATIONS AVAILABLE TO FINALIZE",
        "No draft quotations are available to finalize."
    ):
        return

    quotation_id = input("\nEnter Quotation ID (or . to exit): ").strip()
    if quotation_id == ".":
        print("Finalization cancelled.")
        return

    try:
        quotation_id = int(quotation_id)
    except ValueError:
        print("Invalid quotation ID.")
        return

    quotation = next(
        (q for q in finalizable if q["quotation_id"] == quotation_id),
        None
    )

    if quotation is None:
        print("That quotation is not available to finalize.")
        return

    print("\n========== FINALIZE QUOTATION ==========")
    print(f"Customer: {quotation['customer_name']}")
    print(f"Product: {quotation['product_name']}")
    print(f"Total: PHP {quotation['total_price']:,.2f}")
    confirm = input("\nFinalize this quotation? (Y/N): ").lower()

    if confirm != "y":
        print("Finalization cancelled.")
        return

    quotation["status"] = "Finalized"
    quotation["date_finalized"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_data("quotations.json", quotations)
    print("\nQuotation finalized successfully!")
    print("Status: Finalized")

def manage_quotations_menu():
    while True:
        print("\n================================")
        print("        MANAGE QUOTATIONS")
        print("================================")
        print("1. Edit Quotation")
        print("2. Delete Quotation")
        print("3. Finalize Quotation")
        print("4. Email Finalized Quotation")
        print("0. Back")
        print("================================")
        choice = input("Enter choice: ")

        if choice == "1":
            edit_quotation()
        elif choice == "2":
            delete_quotation()
        elif choice == "3":
            finalize_quotation()
        elif choice == "4":
            send_finalized_quotation_email()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
