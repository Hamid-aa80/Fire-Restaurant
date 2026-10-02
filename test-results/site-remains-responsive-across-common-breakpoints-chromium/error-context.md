# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: site.spec.ts >> remains responsive across common breakpoints
- Location: tests/site.spec.ts:138:1

# Error details

```
Error: Failed to load resource: net::ERR_CONNECTION_RESET
Failed to load resource: the server responded with a status of 404 (File not found)
Failed to load resource: the server responded with a status of 404 (File not found)
Failed to load resource: the server responded with a status of 404 (File not found)
Failed to load resource: the server responded with a status of 404 (File not found)

expect(received).toEqual(expected) // deep equality

- Expected  - 1
+ Received  + 7

- Array []
+ Array [
+   "Failed to load resource: net::ERR_CONNECTION_RESET",
+   "Failed to load resource: the server responded with a status of 404 (File not found)",
+   "Failed to load resource: the server responded with a status of 404 (File not found)",
+   "Failed to load resource: the server responded with a status of 404 (File not found)",
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
    - text: 
    - generic [ref=e8]:
      - link "Home" [ref=e9] [cursor=pointer]:
        - /url: index.html
      - link "About" [ref=e10] [cursor=pointer]:
        - /url: "#about"
      - link "Service" [ref=e11] [cursor=pointer]:
        - /url: "#service"
      - link "Menu" [ref=e12] [cursor=pointer]:
        - /url: "#menu"
      - link "Reservation" [ref=e13] [cursor=pointer]:
        - /url: "#reservation"
      - link "Contact" [ref=e14] [cursor=pointer]:
        - /url: "#contact"
  - generic [ref=e18]:
    - heading "Enjoy our Delicious Meal" [level=1] [ref=e19]:
      - text: Enjoy our
      - text: Delicious Meal
    - paragraph [ref=e20]: Experience the perfect blend of flavors and ambiance at Salt & Smoke, where culinary excellence meets warm hospitality. Indulge in our mouthwatering dishes crafted with passion and savor an unforgettable dining experience.
    - button "Book A Table" [ref=e21] [cursor=pointer]
  - generic [ref=e24]:
    - generic [ref=e27]:
      - generic [ref=e28]: 
      - heading "World's best Chef" [level=5] [ref=e29]
      - paragraph [ref=e30]: Experience culinary excellence with our world-class chefs, crafting unforgettable flavors.
    - generic [ref=e33]:
      - generic [ref=e34]: 
      - heading "Quality Food" [level=5] [ref=e35]
      - paragraph [ref=e36]: Indulge in the finest quality food, prepared with care and passion for an exceptional dining experience.
    - generic [ref=e39]:
      - generic [ref=e40]: 
      - heading "Online Ordering" [level=5] [ref=e41]
      - paragraph [ref=e42]: Order your favorite dishes online and have them delivered to your doorstep with just a few clicks.
    - generic [ref=e45]:
      - generic [ref=e46]: 
      - heading "24/7 Customer Support" [level=5] [ref=e47]
      - paragraph [ref=e48]: Our dedicated support team is available around the clock to assist you with any questions or concerns.
  - generic [ref=e49]:
    - generic [ref=e50]:
      - generic [ref=e51]:
        - generic [ref=e58]:
          - heading "About Us" [level=5] [ref=e59]
          - heading "Welcome to  Salt & Smoke" [level=1] [ref=e60]:
            - text: Welcome to
            - generic [ref=e61]: 
            - text: Salt & Smoke
          - paragraph [ref=e62]: At Salt & Smoke, we are passionate about delivering an exceptional dining experience that tantalizes your taste buds and leaves you craving for more. Our culinary team combines creativity, skill, and the finest ingredients to craft dishes that are both visually stunning and bursting with flavor.
          - paragraph [ref=e63]: From the moment you step into our restaurant, you'll be greeted with warm hospitality and a cozy ambiance that sets the stage for an unforgettable meal. Whether you're joining us for a casual lunch, a romantic dinner, or a special celebration, we strive to create memories that linger long after the last bite.
          - generic [ref=e64]:
            - generic [ref=e66]:
              - heading "15" [level=1] [ref=e67]
              - generic [ref=e68]:
                - paragraph [ref=e69]: Years of
                - heading "Experience" [level=6] [ref=e70]
            - generic [ref=e72]:
              - heading "50" [level=1] [ref=e73]
              - generic [ref=e74]:
                - paragraph [ref=e75]: Popular
                - heading "Master Chefs" [level=6] [ref=e76]
          - link "Read More" [ref=e77] [cursor=pointer]:
            - /url: "#team"
        - generic [ref=e79]:
          - paragraph [ref=e81]: Showing 6 of 6 dishes
          - generic [ref=e84]:
            - generic [ref=e86]:
              - img "Juicy Burger" [ref=e87]
              - generic [ref=e88]:
                - heading "Juicy Burger £25" [level=5] [ref=e89]:
                  - generic [ref=e90]: Juicy Burger
                  - generic [ref=e91]: £25
                - generic [ref=e92]: A juicy burger with fresh ingredients and a perfectly grilled patty.
            - generic [ref=e94]:
              - img "Grilled Salmon" [ref=e95]
              - generic [ref=e96]:
                - heading "Grilled Salmon £30" [level=5] [ref=e97]:
                  - generic [ref=e98]: Grilled Salmon
                  - generic [ref=e99]: £30
                - generic [ref=e100]: A thick salmon fillet rests on a cedar plank, its surface lacquered with a glossy ember‑glaze.
            - generic [ref=e102]:
              - img "Smoked Steak" [ref=e103]
              - generic [ref=e104]:
                - heading "Smoked Steak £35" [level=5] [ref=e105]:
                  - generic [ref=e106]: Smoked Steak
                  - generic [ref=e107]: £35
                - generic [ref=e108]: A succulent smoked steak, perfectly seared and infused with rich, smoky flavors.
            - generic [ref=e110]:
              - img "English Breakfast" [ref=e111]
              - generic [ref=e112]:
                - heading "English Breakfast £25" [level=5] [ref=e113]:
                  - generic [ref=e114]: English Breakfast
                  - generic [ref=e115]: £25
                - generic [ref=e116]: A hearty English breakfast with eggs, bacon, sausages, and beans.
            - generic [ref=e118]:
              - img "Beer" [ref=e119]
              - generic [ref=e120]:
                - heading "Beer £15" [level=5] [ref=e121]:
                  - generic [ref=e122]: Beer
                  - generic [ref=e123]: £15
                - generic [ref=e124]: A refreshing pint of beer, perfect for pairing with your meal.
            - generic [ref=e126]:
              - img "Coffee" [ref=e127]
              - generic [ref=e128]:
                - heading "Coffee £5" [level=5] [ref=e129]:
                  - generic [ref=e130]: Coffee
                  - generic [ref=e131]: £5
                - generic [ref=e132]: A rich and aromatic cup of coffee, perfect for a morning boost or an afternoon pick-me-up.
      - generic [ref=e134]:
        - img "Chef preparing a signature meal" [ref=e137]
        - generic [ref=e139]:
          - heading "Reservation" [level=5] [ref=e140]
          - heading "Book A Table Online" [level=1] [ref=e141]
          - paragraph [ref=e142]: Reserve your table online and enjoy a seamless dining experience at Salt & Smoke. Our easy-to-use reservation system allows you to secure your spot with just a few clicks.
          - generic [ref=e144]:
            - generic [ref=e146]:
              - textbox "Your Name" [ref=e147]
              - generic: Your Name
            - generic [ref=e149]:
              - textbox "Your Email" [ref=e150]
              - generic: Your Email
            - generic [ref=e152]:
              - textbox "Select Date & Time" [ref=e153]
              - generic: Select Date & Time
            - generic [ref=e155]:
              - combobox "Select Person" [ref=e156]:
                - option "Select guests" [disabled] [selected]
                - option "Person 1"
                - option "Person 2"
                - option "Person 3"
                - option "Person 4"
              - generic: Select Person
            - generic [ref=e158]:
              - textbox "Special Request" [ref=e159]
              - generic: Special Request
            - button "Book A Table" [ref=e161] [cursor=pointer]
    - generic [ref=e163]:
      - generic [ref=e164]:
        - heading "Team Members" [level=5] [ref=e165]
        - heading "Our Master Chefs" [level=1] [ref=e166]
      - generic [ref=e167]:
        - generic [ref=e169]:
          - img "Head chef Alice Johnson" [ref=e171]
          - heading "Alice Johnson" [level=5] [ref=e172]
          - text: Chef
          - generic [ref=e173]:
            - link "" [ref=e174] [cursor=pointer]:
              - /url: https://facebook.com
              - generic [ref=e175]: 
            - link "" [ref=e176] [cursor=pointer]:
              - /url: https://twitter.com
              - generic [ref=e177]: 
            - link "" [ref=e178] [cursor=pointer]:
              - /url: https://instagram.com
              - generic [ref=e179]: 
            - link "" [ref=e180] [cursor=pointer]:
              - /url: https://linkedin.com
              - generic [ref=e181]: 
        - generic [ref=e183]:
          - img "Chef Bob Smith" [ref=e185]
          - heading "Bob Smith" [level=5] [ref=e186]
          - text: Chef
          - generic [ref=e187]:
            - link "" [ref=e188] [cursor=pointer]:
              - /url: https://facebook.com
              - generic [ref=e189]: 
            - link "" [ref=e190] [cursor=pointer]:
              - /url: https://twitter.com
              - generic [ref=e191]: 
            - link "" [ref=e192] [cursor=pointer]:
              - /url: https://instagram.com
              - generic [ref=e193]: 
            - link "" [ref=e194] [cursor=pointer]:
              - /url: https://linkedin.com
              - generic [ref=e195]: 
        - generic [ref=e197]:
          - img "Chef Charlie Brown" [ref=e199]
          - heading "Charlie Brown" [level=5] [ref=e200]
          - text: Chef
          - generic [ref=e201]:
            - link "" [ref=e202] [cursor=pointer]:
              - /url: https://facebook.com
              - generic [ref=e203]: 
            - link "" [ref=e204] [cursor=pointer]:
              - /url: https://twitter.com
              - generic [ref=e205]: 
            - link "" [ref=e206] [cursor=pointer]:
              - /url: https://instagram.com
              - generic [ref=e207]: 
            - link "" [ref=e208] [cursor=pointer]:
              - /url: https://linkedin.com
              - generic [ref=e209]: 
        - generic [ref=e211]:
          - img "Chef David Wilson" [ref=e213]
          - heading "David Wilson" [level=5] [ref=e214]
          - text: Chef
          - generic [ref=e215]:
            - link "" [ref=e216] [cursor=pointer]:
              - /url: https://facebook.com
              - generic [ref=e217]: 
            - link "" [ref=e218] [cursor=pointer]:
              - /url: https://twitter.com
              - generic [ref=e219]: 
            - link "" [ref=e220] [cursor=pointer]:
              - /url: https://instagram.com
              - generic [ref=e221]: 
            - link "" [ref=e222] [cursor=pointer]:
              - /url: https://linkedin.com
              - generic [ref=e223]: 
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
      |                                                                                               ^ Error: Failed to load resource: net::ERR_CONNECTION_RESET
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