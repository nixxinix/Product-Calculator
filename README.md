# Product Cost Calculator

This application helps calculate the cost of producing a product based on ingredient usage, unit conversions, fixed overheads, and selling price. It generates detailed production reports, including revenue, profit, and break-even analysis.

---

## HOW TO USE
- clone repository
- install dependencies
  - flask
- cd src
- python app.py

## Using unittest testcases
- make sure cd to root of repository
- run commands:
  - python -m unittest src.tests.test_input_routes
  - python -m unittest src.tests.test_compute

---

## Product Chosen

**Example Product:** *Energy Drink*

A simple recipe-based product used to demonstrate production costing, including ingredients like water, sugar, caffeine powder, and packaging materials.

---

## Ingredient List

Each ingredient includes:

- Name  
- Available Quantity (with unit)  
- Required Quantity Per Unit of Product (with unit)  
- Cost Per Unit  

### Ingredient Table:

| Ingredient        | Available Qty | Required per Product | Unit  | Cost per Unit (₱) |
|-------------------|----------------|------------------------|--------|--------------------|
| Water             | 500 L          | 0.3                    | L      | 5.00               |
| Sugar             | 30 kg          | 0.04                   | kg     | 20.00              |
| Caffeine Powder   | 500 g          | 0.2                    | g      | 2.50               |
| Citric Acid       | 2000 g         | 2                      | g      | 0.30               |
| Flavoring Syrup   | 2000 mL        | 5                      | mL     | 1.00               |
| Bottle and Cap    | 1000 pcs       | 1                      | pcs    | 5.00               |
| Label Sticker     | 2000 pcs       | 1                      | pcs    | 2.00               |

---

##  Program Usage

### Inputs:
- Product Name  
- Selling Price per Unit  
- Fixed Overhead Cost  
- Ingredients (as detailed above)  

### Outputs:
- Maximum producible units  
- Total raw cost  
- Total cost (including fixed overhead)  
- Cost per unit  
- Revenue  
- Profit  
- Break-even units  
- Ingredient usage and remaining quantities  

---

##  Sample Run

###  Input:
- **Product Name:** Energy Drink  
- **Selling Price:** ₱60  
- **Fixed Overhead:** ₱8000  
- **Ingredients:**
  - Water: 500 L, ₱5/L, 0.3 L per unit  
  - Sugar: 30 kg, ₱20/kg, 0.04 kg per unit  
  - Caffeine Powder: 500 g, ₱2.50/g, 0.2 g per unit  
  - Citric Acid: 2000 g, ₱0.30/g, 2 g per unit  
  - Flavoring Syrup: 2000 mL, ₱1/mL, 5 mL per unit  
  - Bottle and Cap: 1000 pcs, ₱5/pc, 1 pc per unit  
  - Label Sticker: 2000 pcs, ₱2/pc, 1 pc per unit  

### Output:

## Screenshot of Sample Output

![Result Screenshot](/static/images/sample_2.png)
![Result Screenshot](/static/images/sample_1.png)

---

## Group Members:
1. Emmanuel, Tammy Buenafe
2. Garcia, John Michael - @jaygarciaaa
3. Peña, John Rhey D.
4. Rivera, Bernie Jr.
5. Samarita, King Rey Mark - @nixxinix

---

Note: This is a project submitted as a requirement in CPE300 - Optimization Techniques course.
