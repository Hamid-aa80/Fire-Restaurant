# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: site.spec.ts >> keeps the page free of broken same-origin links
- Location: tests/site.spec.ts:215:1

# Error details

```
Error: Failed to load resource: the server responded with a status of 404 (File not found)

expect(received).toEqual(expected) // deep equality

- Expected  - 1
+ Received  + 3

- Array []
+ Array [
+   "Failed to load resource: the server responded with a status of 404 (File not found)",
+ ]
```

# Page snapshot

```yaml
- generic [ref=e2]:
  - navigation [ref=e3]:
    - link " Salt & Smoke" [ref=e4] [cursor=pointer]:
      - /url: index.html
      - heading " Salt & Smoke" [level=1] [ref=e5]:
        - generic [ref=e6]: 
        - text: Salt & Smoke
    - button "Toggle navigation" [ref=e7] [cursor=pointer]:
      - generic [ref=e8]: 
  - generic [ref=e12]:
    - heading "Enjoy our Delicious Meal" [level=1] [ref=e13]:
      - text: Enjoy our
      - text: Delicious Meal
    - paragraph [ref=e14]: Experience the perfect blend of flavors and ambiance at Salt & Smoke, where culinary excellence meets warm hospitality. Indulge in our mouthwatering dishes crafted with passion and savor an unforgettable dining experience.
    - button "Book A Table" [ref=e15] [cursor=pointer]
  - generic [ref=e18]:
    - generic [ref=e19]: 
    - heading "World's best Chef" [level=5] [ref=e20]
    - paragraph [ref=e21]: Experience culinary excellence with our world-class chefs, crafting unforgettable flavors.
    - generic [ref=e22]: 
    - heading "Quality Food" [level=5] [ref=e23]
    - paragraph [ref=e24]: Indulge in the finest quality food, prepared with care and passion for an exceptional dining experience.
    - generic [ref=e25]: 
    - heading "Online Ordering" [level=5] [ref=e26]
    - paragraph [ref=e27]: Order your favorite dishes online and have them delivered to your doorstep with just a few clicks.
    - generic [ref=e28]: 
    - heading "24/7 Customer Support" [level=5] [ref=e29]
    - paragraph [ref=e30]: Our dedicated support team is available around the clock to assist you with any questions or concerns.
  - generic [ref=e31]:
    - generic [ref=e32]:
      - generic [ref=e33]:
        - generic [ref=e40]:
          - heading "About Us" [level=5] [ref=e41]
          - heading "Welcome to  Salt & Smoke" [level=1] [ref=e42]:
            - text: Welcome to
            - generic [ref=e43]: 
            - text: Salt & Smoke
          - paragraph [ref=e44]: At Salt & Smoke, we are passionate about delivering an exceptional dining experience that tantalizes your taste buds and leaves you craving for more. Our culinary team combines creativity, skill, and the finest ingredients to craft dishes that are both visually stunning and bursting with flavor.
          - paragraph [ref=e45]: From the moment you step into our restaurant, you'll be greeted with warm hospitality and a cozy ambiance that sets the stage for an unforgettable meal. Whether you're joining us for a casual lunch, a romantic dinner, or a special celebration, we strive to create memories that linger long after the last bite.
          - generic [ref=e46]:
            - generic [ref=e48]:
              - heading "15" [level=1] [ref=e49]
              - generic [ref=e50]:
                - paragraph [ref=e51]: Years of
                - heading "Experience" [level=6] [ref=e52]
            - generic [ref=e54]:
              - heading "50" [level=1] [ref=e55]
              - generic [ref=e56]:
                - paragraph [ref=e57]: Popular
                - heading "Master Chefs" [level=6] [ref=e58]
          - link "Read More" [ref=e59] [cursor=pointer]:
            - /url: "#team"
        - generic [ref=e61]:
          - generic [ref=e62]:
            - generic [ref=e63]:
              - generic [ref=e64]: Search the menu
              - searchbox "Search the menu" [ref=e65]
            - generic [ref=e66]:
              - paragraph [ref=e67]: Filter by category
              - button "Clear filters" [ref=e68] [cursor=pointer]
            - group "Filter menu by category"
            - paragraph [ref=e69]: Showing all categories.
          - paragraph [ref=e71]: Showing 6 of 6 dishes
          - generic [ref=e74]:
            - generic [ref=e76]:
              - img "Juicy Burger" [ref=e77]
              - generic [ref=e78]:
                - heading "Juicy Burger £25" [level=5] [ref=e79]:
                  - generic [ref=e80]: Juicy Burger
                  - generic [ref=e81]: £25
                - generic [ref=e82]: A juicy burger with fresh ingredients and a perfectly grilled patty.
            - generic [ref=e84]:
              - img "Grilled Salmon" [ref=e85]
              - generic [ref=e86]:
                - heading "Grilled Salmon £30" [level=5] [ref=e87]:
                  - generic [ref=e88]: Grilled Salmon
                  - generic [ref=e89]: £30
                - generic [ref=e90]: A thick salmon fillet rests on a cedar plank, its surface lacquered with a glossy ember‑glaze.
            - generic [ref=e92]:
              - img "Smoked Steak" [ref=e93]
              - generic [ref=e94]:
                - heading "Smoked Steak £35" [level=5] [ref=e95]:
                  - generic [ref=e96]: Smoked Steak
                  - generic [ref=e97]: £35
                - generic [ref=e98]: A succulent smoked steak, perfectly seared and infused with rich, smoky flavors.
            - generic [ref=e100]:
              - img "English Breakfast" [ref=e101]
              - generic [ref=e102]:
                - heading "English Breakfast £25" [level=5] [ref=e103]:
                  - generic [ref=e104]: English Breakfast
                  - generic [ref=e105]: £25
                - generic [ref=e106]: A hearty English breakfast with eggs, bacon, sausages, and beans.
            - generic [ref=e108]:
              - img "Beer" [ref=e109]
              - generic [ref=e110]:
                - heading "Beer £15" [level=5] [ref=e111]:
                  - generic [ref=e112]: Beer
                  - generic [ref=e113]: £15
                - generic [ref=e114]: A refreshing pint of beer, perfect for pairing with your meal.
            - generic [ref=e116]:
              - img "Coffee" [ref=e117]
              - generic [ref=e118]:
                - heading "Coffee £5" [level=5] [ref=e119]:
                  - generic [ref=e120]: Coffee
                  - generic [ref=e121]: £5
                - generic [ref=e122]: A rich and aromatic cup of coffee, perfect for a morning boost or an afternoon pick-me-up.
      - option "Select guests" [disabled] [selected]
      - option "Person 1"
      - option "Person 2"
      - option "Person 3"
      - option "Person 4"
    - generic [ref=e125]:
      - img "Head chef Alice Johnson" [ref=e126]
      - img "Chef Bob Smith" [ref=e127]
      - img "Chef Charlie Brown" [ref=e128]
      - img "Chef David Wilson" [ref=e129]
```

# Test source

```ts
  1   | import { expect, test } from "@playwright/test";
  2   | import type { Page } from "@playwright/test";
  3   | 
  4   | const reservedConsoleMessages = [
  5   |   /Download the React DevTools/i,
  6   |   /favicon/i
  7   | ];
  8   | 
  9   | const runtimeErrorsByPage = new WeakMap<Page, { pageErrors: string[]; consoleErrors: string[] }>();
  10  | 
  11  | test.beforeEach(async ({ page }) => {
  12  |   const pageErrors: string[] = [];
  13  |   const consoleErrors: string[] = [];
  14  |   runtimeErrorsByPage.set(page, { pageErrors, consoleErrors });
  15  | 
  16  |   page.on("pageerror", error => {
  17  |     pageErrors.push(error.message);
  18  |   });
  19  | 
  20  |   page.on("console", message => {
  21  |     if (message.type() === "error") {
  22  |       const text = message.text();
  23  |       if (!reservedConsoleMessages.some(pattern => pattern.test(text))) {
  24  |         consoleErrors.push(text);
  25  |       }
  26  |     }
  27  |   });
  28  | 
  29  |   await page.goto("/");
  30  |   await page.waitForLoadState("networkidle");
  31  | });
  32  | 
  33  | test.afterEach(async ({ page }) => {
  34  |   const runtimeErrors = runtimeErrorsByPage.get(page);
  35  |   expect(runtimeErrors?.pageErrors ?? [], (runtimeErrors?.pageErrors ?? []).join("\n")).toEqual([]);
> 36  |   expect(runtimeErrors?.consoleErrors ?? [], (runtimeErrors?.consoleErrors ?? []).join("\n")).toEqual([]);
      |                                                                                               ^ Error: Failed to load resource: the server responded with a status of 404 (File not found)
  37  | });
  38  | 
  39  | test("handles valid reservation and newsletter input", async ({ page }) => {
  40  |   const tomorrow = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split("T")[0];
  41  |   await page.locator("#reservationForm").scrollIntoViewIfNeeded();
  42  | 
  43  |   const reservationSubmit = page.locator("#reservationForm button[type=\"submit\"]");
  44  |   await expect(reservationSubmit).toBeDisabled();
  45  | 
  46  |   await page.getByLabel("Your Name").fill("Jordan Smith");
  47  |   await page.getByLabel("Your Email").fill("jordan@example.com");
  48  |   await page.locator("#datetime").fill(tomorrow);
  49  |   await page.locator("#select1").selectOption("2");
  50  |   await page.getByLabel("Special Request").fill("Window table please");
  51  | 
  52  |   await expect(reservationSubmit).toBeEnabled();
  53  | 
  54  |   await reservationSubmit.click();
  55  |   await expect(page).toHaveURL(/submit\.html(\?.*)?$/);
  56  |   await expect(page.getByRole("alert")).toContainText("Your reservation request for Jordan Smith");
  57  | 
  58  |   await page.goto("/");
  59  |   await page.locator("#newsletterForm").scrollIntoViewIfNeeded();
  60  |   await page.locator("#newsletterEmail").fill("newsletter@example.com");
  61  |   await page.getByRole("button", { name: /sign up/i }).click();
  62  |   await expect(page.getByRole("alert")).toContainText("You're subscribed with newsletter@example.com");
  63  | 
  64  |   await page.locator("#feedbackForm").scrollIntoViewIfNeeded();
  65  |   const feedbackSubmit = page.locator("#feedbackSubmitButton");
  66  |   await expect(feedbackSubmit).toBeDisabled();
  67  | 
  68  |   await page.locator("#feedbackMessage").fill("Amazing food, service, and atmosphere.");
  69  |   await page
  70  |     .locator("#feedbackImage")
  71  |     .setInputFiles("assets/img/hero.png");
  72  |   await expect(page.locator("#feedbackPreview")).toBeVisible();
  73  |   await expect(feedbackSubmit).toBeEnabled();
  74  | 
  75  |   await feedbackSubmit.click();
  76  |   await expect(page.locator("#feedbackFeedback")).toContainText(
  77  |     "Thanks for your feedback. Your message and image were sent."
  78  |   );
  79  | });
  80  | 
  81  | test("rejects invalid reservation input with clear feedback", async ({ page }) => {
  82  |   const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString().split("T")[0];
  83  |   await page.locator("#reservationForm").scrollIntoViewIfNeeded();
  84  |   const reservationForm = page.locator("#reservationForm");
  85  | 
  86  |   await reservationForm.dispatchEvent("submit", { bubbles: true, cancelable: true });
  87  |   await expect(page.getByRole("alert")).toContainText("Please enter your full name");
  88  | 
  89  |   await page.getByLabel("Your Name").fill("Jordan Smith");
  90  |   await page.getByLabel("Your Email").fill("invalid-email");
  91  |   await page.locator("#datetime").fill(yesterday);
  92  |   await page.locator("#select1").selectOption("2");
  93  |   await page.getByLabel("Special Request").fill("Hi");
  94  | 
  95  |   await reservationForm.dispatchEvent("submit", { bubbles: true, cancelable: true });
  96  |   await expect(page.getByRole("alert")).toContainText("Please enter a valid email address");
  97  | 
  98  |   await page.getByLabel("Your Email").fill("jordan@example.com");
  99  |   await reservationForm.dispatchEvent("submit", { bubbles: true, cancelable: true });
  100 |   await expect(page.getByRole("alert")).toContainText("must be today or later");
  101 | 
  102 |   const tomorrow = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split("T")[0];
  103 |   await page.locator("#datetime").fill(tomorrow);
  104 |   await reservationForm.dispatchEvent("submit", { bubbles: true, cancelable: true });
  105 |   await expect(page.getByRole("alert")).toContainText("at least 5 characters");
  106 | });
  107 | 
  108 | test("rejects invalid newsletter input with clear feedback", async ({ page }) => {
  109 |   await page.locator("#newsletterForm").scrollIntoViewIfNeeded();
  110 |   const newsletterForm = page.locator("#newsletterForm");
  111 |   const newsletterFeedback = page.locator("#newsletterFeedback");
  112 | 
  113 |   await newsletterForm.dispatchEvent("submit", { bubbles: true, cancelable: true });
  114 |   await expect(newsletterFeedback).toContainText("Please enter your email address to subscribe");
  115 | 
  116 |   await page.locator("#newsletterEmail").fill("invalid-email");
  117 |   await newsletterForm.dispatchEvent("submit", { bubbles: true, cancelable: true });
  118 |   await expect(newsletterFeedback).toContainText("Please enter a valid email address");
  119 | });
  120 | 
  121 | test("rejects invalid feedback input with clear feedback", async ({ page }) => {
  122 |   await page.locator("#feedbackForm").scrollIntoViewIfNeeded();
  123 |   const feedbackForm = page.locator("#feedbackForm");
  124 |   const feedbackAlert = page.locator("#feedbackFeedback");
  125 | 
  126 |   await feedbackForm.dispatchEvent("submit", { bubbles: true, cancelable: true });
  127 |   await expect(feedbackAlert).toContainText("Please enter your feedback before sending");
  128 | 
  129 |   await page.locator("#feedbackMessage").fill("Too short");
  130 |   await feedbackForm.dispatchEvent("submit", { bubbles: true, cancelable: true });
  131 |   await expect(feedbackAlert).toContainText("at least 10 characters");
  132 | 
  133 |   await page.locator("#feedbackMessage").fill("Great visit and excellent food quality.");
  134 |   await feedbackForm.dispatchEvent("submit", { bubbles: true, cancelable: true });
  135 |   await expect(feedbackAlert).toContainText("Please add an image to submit feedback.");
  136 | });
```