The task is to place **products** into the **fixture**, maximizing product profit subject to the usual knapsack problem constraints:

-   **0/1 constraint:** there must be either zero or one of each product on the shelves
-   **shelf capacity constraint:** the sum of the product widths must not exceed the shelf width

**N.B.** please do *not* use an off-the-shelf solver such as `ortools` or `pulp`.
The solution does not have to be optimal, but should represent an appropriate time/profit trade-off.

`planogram.py` contains a minimal implementation.

To proceed:

1.  clone this repository
2.  **working on a new branch**, complete the implementation of `planogram.py:planogram()`.
    You are free to use your choice of additional libraries;
    make sure to update `pyproject.toml` / `requirements.txt` as necessary.
3.  get the code back to us:
    -   **private** repository on bitbucket (preferred) github, etc, or
    -   zip/tar project files and email us
