import numpy as np
import pandas as pd


def planogram(fixture, products):
    """
    Arguments:
    - fixture :: DataFrame[["shelf_no", "shelf_width_cm"]]
    - products :: DataFrame[["product_id", "product_width_mm", "profit"]]

    Returns: DataFrame[["shelf_no", "product_id"]]
    """

    # DataFrames setup
    products = products.copy()
    distribution = pd.DataFrame({'shelf_no': [], 'product_id': []})

    # Products setup (adding quality and shelf assignment columns)
    products['product_quality'] = products.profit / products.product_width_mm
    products = products.sort_values(by='product_quality', ascending=False)
    products = products.reset_index(drop=True)
    products['shelf_no'] = 0 # 0 -> unassigned item

    # Knapsack greedy round robin algorithm
    remaining_capacity = [10 * width for width in fixture['shelf_width_cm']]  # cm -> mm
    current_shelf = 0  # Round robin token indicator
    # Every product
    for product_index in products.index:
        item_width = products.at[product_index, 'product_width_mm']
        # Every shelf (starting at current shelf)
        for shelf_offset in range(len(fixture)):  # maximum offset = number of shelves
            # Calculate index - Round robin item distribution (more balanced distribution)
            shelf_index = (current_shelf + shelf_offset) % len(fixture)
            # If item fits
            if remaining_capacity[shelf_index] > item_width:
                # Save shelf number
                products.at[product_index, 'shelf_no'] = shelf_index + 1 # shelf_no numbered starting from 1
                # Update state
                remaining_capacity[shelf_index] -= item_width  # Update capacity
                current_shelf = (shelf_index + 1) % len(fixture)  # Update RR token
                break  # Cannot be added to other shelves

    # Exchange optimisation algorithm
    # Swaps products between shelves if it allows for a new item to be inserted
    for product_index_A in products.index:
        product_width_A = products.at[product_index_A, 'product_width_mm']
        shelf_no_A = products.at[product_index_A, 'shelf_no']
        if shelf_no_A != 0: # Check if product used
            for product_index_B in range(product_index_A+1, len(products)):
                product_width_B = products.at[product_index_B, 'product_width_mm']
                shelf_no_B = products.at[product_index_B, 'shelf_no']
                if shelf_no_B != 0 and shelf_no_B != shelf_no_A: # Check if product used or on the same shelf
                    # Reassign based on size
                    if product_width_A > product_width_B:
                        product_index_bigger = product_index_A
                        product_width_bigger = product_width_A
                        shelf_no_bigger = shelf_no_A
                        product_index_smaller = product_index_B
                        product_width_smaller = product_width_B
                        shelf_no_smaller = shelf_no_B
                    else:
                        product_index_bigger = product_index_B
                        product_width_bigger = product_width_B
                        shelf_no_bigger = shelf_no_B
                        product_index_smaller = product_index_A
                        product_width_smaller = product_width_A
                        shelf_no_smaller = shelf_no_A

                    dif = product_width_bigger - product_width_smaller
                    candidate_index = -1
                    candidate_profit = -1

                    # Check if swap possible
                    if dif <= remaining_capacity[shelf_no_smaller-1]:
                        # Search for best item in the given capacity
                        for product_index_C in range(len(products)):
                            product_width_C = products.at[product_index_C, 'product_width_mm']
                            profit_C = products.at[product_index_C, 'profit']
                            shelf_no_C = products.at[product_index_C, 'shelf_no']
                            # If unselected, fits and more profitable
                            if shelf_no_C == 0 and remaining_capacity[shelf_no_bigger-1] + dif >= product_width_C and profit_C > candidate_profit:
                                candidate_index = product_index_C
                                candidate_profit = profit_C
                        # If new item found
                        if candidate_index != -1:
                            products.at[product_index_bigger, 'shelf_no'] = shelf_no_smaller
                            products.at[product_index_smaller, 'shelf_no'] = shelf_no_bigger
                            products.at[candidate_index, 'shelf_no'] = shelf_no_bigger
                            remaining_capacity[shelf_no_smaller-1] -= dif
                            remaining_capacity[shelf_no_bigger-1] += dif - products.at[candidate_index, 'product_width_mm']

    # Exchange optimisation algorithm
    # Attempts to exclude one item from each knapsack and tries to replace it with one or more unpicked items
    for product_index_A in reversed(products.index): # starting with worst quality items
        product_width_A = products.at[product_index_A, 'product_width_mm']
        shelf_no_A = products.at[product_index_A, 'shelf_no']
        if shelf_no_A != 0: # Check if product used
            # Excluding item
            alternative_capacity = remaining_capacity[shelf_no_A-1] + product_width_A
            alternative_indexes = []
            alternative_profit = 0
            for product_index_B in products.index:
                product_width_B = products.at[product_index_B, 'product_width_mm']
                shelf_no_B = products.at[product_index_B, 'shelf_no']
                # Check if unused and fits
                if shelf_no_B == 0 and product_width_B <= alternative_capacity:
                    # Update alternative
                    alternative_capacity -= product_width_B
                    alternative_indexes.append(product_index_B)
                    alternative_profit += products.at[product_index_B, 'profit']
            # Compare to alternative
            if alternative_profit > products.at[product_index_A, 'profit']:
                # Update
                products.at[product_index_A, 'shelf_no'] = 0
                for index in alternative_indexes:
                    products.at[index, 'shelf_no'] = shelf_no_A
                remaining_capacity[shelf_no_A-1] = alternative_capacity

    # Populate distribution dataframe
    for product_index in products.index:
        # Exclude unassigned items
        if products.at[product_index, 'shelf_no'] != 0:
            # Prepare distribution record
            assignment = \
                {'shelf_no': products.at[product_index, 'shelf_no'],
                 'product_id': products.at[product_index, 'product_id']
                 }
            # Add record to current distribution plan
            distribution = distribution.append(assignment, ignore_index=True)

    # Display 
    # print("------------------------------")
    # print(fixture)
    # print(products)
    # print(distribution)
    # print("------------------------------")

    return distribution


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--products",
        type=argparse.FileType(mode="r"),
        default="products.csv",
        help="products input file",
    )
    parser.add_argument(
        "--fixture",
        type=argparse.FileType(mode="r"),
        default="fixture.csv",
        help="fixture input file",
    )
    parser.add_argument(
        "--out", "-o", default="solution.csv", help="solution output file"
    )

    args = parser.parse_args()

    fixture = pd.read_csv(args.fixture)
    products = pd.read_csv(args.products)

    solution = planogram(fixture, products)

    solution.to_csv(args.out, index=False)

    print(
        "stats:",
        solution[["shelf_no", "product_id"]]
            .merge(fixture, on="shelf_no")
            .merge(products, on="product_id")
            .assign(n_products=1)
            .pivot_table(
            index=["shelf_no", "shelf_width_cm"],
            values=["n_products", "profit", "product_width_mm"],
            aggfunc=np.sum,
            margins=True,
        ),
        sep="\n",
    )
