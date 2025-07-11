# Sample

The NYC Admin Code - Title 11, was chunked using a custom chunking algorithm that splits by subsection. ChromaDB is used as the vector database. The default `all-MiniLM-L6-v2` embedding model is used. The LLM used here for processing and asking questions on the retrieved context is Gemini 2.5 Flash.

### Retrieve Info

```
python search_data.py "personal income tax 50,000" -n 10
```

### Information Taken from VectorDB

```
Found 10 results for 'personal income tax 50,000':

Result 1 (ID: NYC-Admin-Code_11-1902.a.2.ii_2025-07-10, Distance: 0.4252):
  Path: Title 11: Taxation and Finance > Earnings Tax on Nonresidents > Persons subject to tax.
  Text: A tax at the rate of sixty-five hundredths of one per cent on all net earnings from self-employment.
--------------------
Result 2 (ID: NYC-Admin-Code_11-1701.General.h.2.B_2025-07-10, Distance: 0.4297):
  Path: Title 11: Taxation and Finance > City Personal Income Tax on Residents > Imposition of tax.
  Text: For such taxpayers with adjusted gross income over five hundred thousand dollars, the fraction is one. Provided, however, that the total tax prior to the application of any tax credits shall not exceed the highest rate of tax set forth in the tax table in subdivision (g) of this section multiplied by the taxpayer's taxable income.
--------------------
Result 3 (ID: NYC-Admin-Code_11-1704.1.a.2.iii.A_2025-07-10, Distance: 0.4361):
  Path: Title 11: Taxation and Finance > City Personal Income Tax on Residents > Additional tax.
  Text: If the tax determined pursuant to section  11-1701 is based on city taxable income equal to or less than $50,000, then the additional tax shall be 5.25% of such tax;
--------------------
Result 4 (ID: NYC-Admin-Code_11-1706.d.1.A_2025-07-10, Distance: 0.4402):
  Path: Title 11: Taxation and Finance > City Personal Income Tax on Residents > Credits against tax.
  Text: thirty percent, where the taxpayer's adjusted gross income for such taxable year is less than $5,000;
--------------------
Result 5 (ID: NYC-Admin-Code_11-1701.General.b.3_2025-07-10, Distance: 0.4435):
  Path: Title 11: Taxation and Finance > City Personal Income Tax on Residents > Imposition of tax.
  Text: Resident unmarried individuals, resident married individuals filing separate returns and resident estates and trusts.  The tax under this section for each taxable year on the city taxable income of every city resident individual who is not a married individual who makes a single return jointly with his or her spouse under subdivision (b) of section  11-1751 of this title or a city resident head of a household or a city resident surviving spouse, and on the city taxable income of every city resident estate and trust shall be determined in accordance with the following table:
For taxable years beginning after two thousand twenty-six:
If the city taxable income is:  The tax is:  Not over $12,000  1.18% of the city taxable income Over $12,000 but not over $25,000  $142 plus 1.435% of excess over $12,000 Over $25,000 but not over $50,000  $328 plus 1.455% of excess over $25,000 Over $50,000  $692 plus 1.48% of excess over $50,000
--------------------
Result 6 (ID: NYC-Admin-Code_11-1704.1.a.2.iii.B_2025-07-10, Distance: 0.4447):
  Path: Title 11: Taxation and Finance > City Personal Income Tax on Residents > Additional tax.
  Text: If the tax determined pursuant to section  11-1701 is based on city taxable income over $50,000, then the additional tax shall be the sum of 5.25% of such tax on city taxable income up to and including $50,000 and 12.25% of such tax on city taxable income in excess of $50,000.
--------------------
Result 7 (ID: NYC-Admin-Code_11-641.b.11_2025-07-10, Distance: 0.4497):
  Path: Title 11: Taxation and Finance > City Business Taxes > Computations of entire net income.
  Text: for taxable years beginning before January first, two thousand ten, in the case of a taxpayer subject to the provisions of section 585(c) of the internal revenue code, the amount allowed as a deduction pursuant to section 166 of such code; and
--------------------
Result 8 (ID: NYC-Admin-Code_11-1706.h.1.A_2025-07-10, Distance: 0.4550):
  Path: Title 11: Taxation and Finance > City Personal Income Tax on Residents > Credits against tax.
  Text: such taxpayer is entitled to a deduction for such taxable year under subsection (c) of section one hundred fifty-one of the internal revenue code;
--------------------
Result 9 (ID: NYC-Admin-Code_11-1701.General.b.1_2025-07-10, Distance: 0.4581):
  Path: Title 11: Taxation and Finance > City Personal Income Tax on Residents > Imposition of tax.
  Text: Resident married individuals filing joint returns and resident surviving spouses.  The tax under this section for each taxable year on the city taxable income of every city resident married individual who makes a single return jointly with his or her spouse under subdivision (b) of section  11-1751 of this title and on the city taxable income of every city resident surviving spouse shall be determined in accordance with the following table:
For taxable years beginning after two thousand twenty-six:
If the city taxable income is:  The tax is:  Not over $21,600  1.18% of the city taxable income Over $21,600 but not over $45,000  $255 plus 1.435% of excess over $21,600 Over $45,000 but not over $90,000  $591 plus 1.455% of excess over $45,000 Over $90,000  $1,245 plus 1.48% of excess over $90,000
--------------------
Result 10 (ID: NYC-Admin-Code_11-1706.h.1.B.i_2025-07-10, Distance: 0.4607):
  Path: Title 11: Taxation and Finance > City Personal Income Tax on Residents > Credits against tax.
  Text: for city taxpayers who filed a resident income tax return as married taxpayers filing jointly or a qualified surviving spouse:
If the number of dependents is:  Income no greater than: 1 $36,789 2 $46,350 3 $54,545 4 $61,071 5 $68,403 6 $75,204 7 or more $91,902
--------------------
```

### Question

```
Evaluate this result.
```

### Response to Question

```
The search results for "personal income tax 50,000" are **very good**, with several highly relevant results that directly address tax calculations and thresholds around the $50,000 income level for New York City personal income tax.

Here's an evaluation of each result:

* **Result 1 (ID: NYC-Admin-Code_11-1902.a.2.ii - Earnings Tax on Nonresidents)**: Less relevant. This discusses earnings tax on nonresidents from self-employment, which is not directly "personal income tax" in the context of residents or the $50,000 threshold.
* **Result 2 (ID: NYC-Admin-Code_11-1701.General.h.2.B - Imposition of tax, AGI over $500,000)**: Relevant, but for a much higher income bracket ($500,000), not specifically for $50,000, though it's within the "City Personal Income Tax on Residents" chapter.
* **Result 3 (ID: NYC-Admin-Code_11-1704.1.a.2.iii.A - Additional tax for income <= $50,000)**: **Highly relevant.** This explicitly states the "additional tax" if the city taxable income is "equal to or less than $50,000," directly hitting the core of the query.
* **Result 4 (ID: NYC-Admin-Code_11-1706.d.1.A - Credits for AGI < $5,000)**: Less relevant. While it's about credits against tax and personal income, the income threshold of less than $5,000 is far from $50,000.
* **Result 5 (ID: NYC-Admin-Code_11-1701.General.b.3 - Tax table for unmarried individuals, etc.)**: **Highly relevant.** This provides a detailed tax table for resident unmarried individuals, estates, and trusts, with brackets that include "Over $25,000 but not over $50,000" and "Over $50,000," directly answering how income around $50,000 is taxed.
* **Result 6 (ID: NYC-Admin-Code_11-1704.1.a.2.iii.B - Additional tax for income over $50,000)**: **Highly relevant.** This complements Result 3 by detailing the "additional tax" when city taxable income is "over $50,000," again directly addressing the query's income threshold.
* **Result 7 (ID: NYC-Admin-Code_11-641.b.11 - City Business Taxes)**: Irrelevant. This is related to City Business Taxes and computations of entire net income, not personal income tax.
* **Result 8 (ID: NYC-Admin-Code_11-1706.h.1.A - Credits against tax)**: Less relevant. This refers to a deduction under the Internal Revenue Code, without specific mention of the $50,000 threshold or direct personal income tax rates.
* **Result 9 (ID: NYC-Admin-Code_11-1701.General.b.1 - Tax table for married individuals filing jointly)**: **Highly relevant.** This provides a tax table for resident married individuals filing jointly, with brackets that include "Over $45,000 but not over $90,000," which is very pertinent to understanding personal income tax around the $50,000 mark for this filing status.
* **Result 10 (ID: NYC-Admin-Code_11-1706.h.1.B.i - Credits against tax based on dependents and income)**: Relevant. While it's about credits based on dependents, the income thresholds listed (`$46,350`, `$54,545`) are very close to $50,000, making it potentially useful for someone looking for personal income tax information in that range.

**Overall Assessment:**

The vector database performed **very well** for the query "personal income tax 50,000." It successfully retrieved multiple highly relevant results (3, 5, 6, 9) that directly discuss tax rates, additional taxes, and income brackets around the $50,000 threshold for City Personal Income Tax on Residents. While there are a few less relevant or irrelevant results, the core information sought by the query is strongly represented.
```

### Follow Up Question

```
If my follow up question was, what is the tax rate for someone with a $54000 salary, what would it be? Only use the information I have provided.
```

### Response to Follow Up Question

```
Based on the information provided from the search results, the tax calculation for a $54,000 salary (assuming this is the city taxable income) would depend on the filing status. The provided tax tables are for "taxable years beginning after two thousand twenty-six."

Here's how the tax would be calculated for the two main scenarios found in the provided text:

### 1. For Resident unmarried individuals, resident married individuals filing separate returns, and resident estates and trusts (from NYC-Admin-Code_11-1701.General.b.3):

* A city taxable income of $\$54,000$ falls into the bracket "Over $\$50,000$".
* The tax for this bracket is: "$\$692$ plus $1.48\%$ of excess over $\$50,000$".
* Excess over $\$50,000 = \$54,000 - \$50,000 = \$4,000$.
* Tax calculation: $\$692 + (0.0148 \times \$4,000) = \$692 + \$59.20 = \textbf{\$751.20}$.

### 2. For Resident married individuals filing joint returns and resident surviving spouses (from NYC-Admin-Code_11-1701.General.b.1):

* A city taxable income of $\$54,000$ falls into the bracket "Over $\$45,000$ but not over $\$90,000$".
* The tax for this bracket is: "$\$591$ plus $1.455\%$ of excess over $\$45,000$".
* Excess over $\$45,000 = \$54,000 - \$45,000 = \$9,000$.
* Tax calculation: $\$591 + (0.01455 \times \$9,000) = \$591 + \$130.95 = \textbf{\$721.95}$.

Therefore, the exact tax amount would be either $\$751.20$ or $\$721.95$ depending on the individual's filing status.
```

### Follow Up Question

```
According to my information, what would a family jointly filing with 2 dependents pay?
```

### Response to Follow Up Question

```
I can tell you which tax table applies and where to look for credits, but to calculate the exact tax a family jointly filing with 2 dependents would pay, I need to know their **city taxable income**.

According to the information provided:

* **Tax Table:** For resident married individuals filing joint returns, the tax table found in `NYC-Admin-Code_11-1701.General.b.1` would apply. This table has different rates based on income brackets (e.g., up to $\$21,600$, over $\$21,600$ to $\$45,000$, etc.).
* **Credits:** `NYC-Admin-Code_11-1706.h.1.B.i` indicates that for city taxpayers filing jointly, with 2 dependents, there is a credit for income no greater than $\$46,350$. However, the specific amount or calculation of this credit is not provided in the text.

Once you provide the family's city taxable income, I can use the relevant tax bracket to calculate their tax liability.
```

### Follow Up Qustion

```
Lets assume jointly, they make an income of $86500 a year.
```

### Response to Follow Up Question

```
Based on the information provided, for a family jointly filing with a city taxable income of $\$86,500$ a year, the tax would be calculated as follows for taxable years beginning after two thousand twenty-six:

According to `NYC-Admin-Code_11-1701.General.b.1` (Result 9), which provides the tax table for resident married individuals filing joint returns:

* An income of $\$86,500$ falls into the bracket "Over $\$45,000$ but not over $\$90,000$".
* The tax for this bracket is calculated as: "$\$591$ plus $1.455\%$ of excess over $\$45,000$".
* First, calculate the excess over $\$45,000$: $\$86,500 - \$45,000 = \$41,500$.
* Next, calculate $1.455\%$ of the excess: $0.01455 \times \$41,500 = \$603.975$.
* Finally, add this to the base tax: $\$591 + \$603.975 = \textbf{\$1,194.98}$.

Regarding credits for dependents (`NYC-Admin-Code_11-1706.h.1.B.i` - Result 10), the information states that for 2 dependents, a credit applies for income no greater than $\$46,350$. Since an income of $\$86,500$ is greater than $\$46,350$, this specific credit would not apply based on the provided criteria.
```

### Follow Up Question

```
Can you tell me what the credit would've been given an income within $46,350?
```

### Response to Follow Up Question

```
Based on the information provided in the search results, I cannot tell you the specific amount of the credit.

Result 10 (`NYC-Admin-Code_11-1706.h.1.B.i`) indicates that for a family jointly filing with 2 dependents, a credit applies if their income is no greater than $\$46,350$. However, the provided text **does not specify the actual monetary value or calculation method of this credit.** It only states the income threshold for eligibility.
```