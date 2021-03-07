The task is to place **products** into the **fixture**, maximizing product profit subject to the usual knapsack problem constraints:

-   **0/1 constraint:** there must be either zero or one of each product on the shelves
-   **shelf capacity constraint:** the sum of the product widths must not exceed the shelf width

**N.B.** please do *not* use an off-the-shelf solver such as `ortools` or `pulp`.
The solution does not have to be optimal, but should represent an appropriate time/profit trade-off.

**Solution:**
Greedy Round Robin Algorithm implementation with two additional steps of optimisation (item exchanges and rearranging).
