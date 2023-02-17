from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import sys, time
from rich.console import Console
from tqdm import tqdm
import solve

console = Console()

# Get link to puzzle
if len(sys.argv) > 1:
    link = sys.argv[1]
else:
    link = input("Enter link to puzzle: ") # Ex. https://www.nonograms.org/nonograms/i/55852

console.print("\n=== Initializing Selenium... ===\n", style="bold magenta")

# Initialize Selenium and open puzzle
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get(link)

# Get puzzle data
left = []
left_table = driver.find_element(By.CLASS_NAME, "nmtl")
for row in left_table.find_elements(By.TAG_NAME, "tr"):
    rule = []
    for cell in row.find_elements(By.TAG_NAME, "td"):
        if cell.get_attribute("class") != "num_empty":
            rule.append(int(cell.text))
    left.append(rule)

top = {}
top_table = driver.find_element(By.CLASS_NAME, "nmtt")
for cell in top_table.find_elements(By.CLASS_NAME, "num"):
    col, row = map(int, cell.get_attribute("id")[3:].split("_"))
    if col not in top:
        top[col] = []
    top[col].append(int(cell.text))
top = [top[col] for col in range(len(top))]

print(top)
print(left)

console.print("=== Puzzle loaded! Press enter to solve. ===\n", style="bold magenta")
input()

# Solve puzzle
solution = solve.solve(left, top)
console.print("=== Solution found! ===\n", style="bold magenta")
solve.print_grid(solution)
input()

# Fill in solution
console.print("=== Filling in solution... ===\n", style="bold magenta")
solution_grid = driver.find_element(By.CLASS_NAME, "nmtc")

for i, row in enumerate(tqdm(solution)):
    for j, val in enumerate(row):
        if val == 1:
            solution_grid.find_element(By.ID, f"nmf{j}_{i}").click()

console.print("=== Done! Press Enter to Exit. ===\n", style="bold magenta")
input()