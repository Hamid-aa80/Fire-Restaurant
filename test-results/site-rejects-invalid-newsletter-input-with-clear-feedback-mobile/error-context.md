# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: site.spec.ts >> rejects invalid newsletter input with clear feedback
- Location: tests/site.spec.ts:108:1

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: locator('#newsletterFeedback')
Expected substring: "Please enter your email address to subscribe"
Received string:    ""
Timeout: 5000ms

Call log:
  - Expect "toContainText" with timeout 5000ms
  - waiting for locator('#newsletterFeedback')
    14 × locator resolved to <div role="alert" aria-live="polite" aria-atomic="true" id="newsletterFeedback" class="alert d-none mt-3 mb-0"></div>
       - unexpected value ""

```

```yaml
- navigation:
  - link " Salt & Smoke":
    - /url: index.html
    - heading " Salt & Smoke" [level=1]
  - button "Toggle navigation": 
- heading "Enjoy our Delicious Meal" [level=1]
- paragraph: Experience the perfect blend of flavors and ambiance at Salt & Smoke, where culinary excellence meets warm hospitality. Indulge in our mouthwatering dishes crafted with passion and savor an unforgettable dining experience.
- button "Book A Table"
- heading "About Us" [level=5]
- heading "Welcome to  Salt & Smoke" [level=1]
- paragraph: At Salt & Smoke, we are passionate about delivering an exceptional dining experience that tantalizes your taste buds and leaves you craving for more. Our culinary team combines creativity, skill, and the finest ingredients to craft dishes that are both visually stunning and bursting with flavor.
- paragraph: From the moment you step into our restaurant, you'll be greeted with warm hospitality and a cozy ambiance that sets the stage for an unforgettable meal. Whether you're joining us for a casual lunch, a romantic dinner, or a special celebration, we strive to create memories that linger long after the last bite.
- heading "15" [level=1]
- paragraph: Years of
- heading "Experience" [level=6]
- heading "50" [level=1]
- paragraph: Popular
- heading "Master Chefs" [level=6]
- link "Read More":
  - /url: "#team"
- paragraph: Showing 6 of 6 dishes
- img "Juicy Burger"
- heading "Juicy Burger £25" [level=5]
- text: A juicy burger with fresh ingredients and a perfectly grilled patty.
- img "Grilled Salmon"
- heading "Grilled Salmon £30" [level=5]
- text: A thick salmon fillet rests on a cedar plank, its surface lacquered with a glossy ember‑glaze.
- img "Smoked Steak"
- heading "Smoked Steak £35" [level=5]
- text: A succulent smoked steak, perfectly seared and infused with rich, smoky flavors.
- img "English Breakfast"
- heading "English Breakfast £25" [level=5]
- text: A hearty English breakfast with eggs, bacon, sausages, and beans.
- img "Beer"
- heading "Beer £15" [level=5]
- text: A refreshing pint of beer, perfect for pairing with your meal.
- img "Coffee"
- heading "Coffee £5" [level=5]
- text: A rich and aromatic cup of coffee, perfect for a morning boost or an afternoon pick-me-up.
- heading "Ready for your next smokehouse night?" [level=3]
- paragraph: Reserve a table in seconds and enjoy chef-led fire-grilled dishes, premium ingredients, and warm service in the heart of London.
- link "Book now":
  - /url: "#reservation"
- link "Call us":
  - /url: tel:+442079460958
- paragraph:  Live-fire kitchen
- paragraph:  Fresh daily sourcing
- paragraph:  Top-rated guest experience
- heading "Company" [level=4]
- paragraph: Salt & Smoke brings smokehouse craft and modern hospitality together in one memorable dining experience.
- link "Salt & Smoke":
  - /url: index.html
- link "About Us":
  - /url: "#about"
- link "Contact Us":
  - /url: "#contact"
- link "Menu":
  - /url: "#menu"
- link "Service":
  - /url: "#service"
- link "Book A Table":
  - /url: "#reservation"
- heading "Contact" [level=4]
- paragraph:  123 Street, London, UK
- link "View on Google Maps":
  - /url: https://www.google.com/maps/place/123+Street,+London,+UK
- paragraph:  +44 20 7946 0958
- link "Call Now":
  - /url: tel:+442079460958
- paragraph:  hello@saltandsmoke.co.uk
- link "Email Us":
  - /url: mailto:hello@saltandsmoke.co.uk
- link "":
  - /url: https://twitter.com
- link "":
  - /url: https://facebook.com
- link "":
  - /url: https://youtube.com
- link "":
  - /url: https://linkedin.com
- heading "Opening" [level=4]
- heading "Monday - Friday" [level=5]
- paragraph: 09.00 AM - 09.00 PM
- heading "Sunday" [level=5]
- paragraph: 10.00 AM - 00.00 PM
- heading "Saturday" [level=5]
- paragraph: 10.00 AM - 01.00 PM
- heading "Newsletter" [level=4]
- paragraph: Subscribe to our newsletter for the latest updates and offers.
- text: Email address
- textbox "Email address":
  - /placeholder: Your email
- button "Sign up"
- heading "Feedback" [level=4]
- paragraph: Tell us about your visit and share a photo with your feedback.
- text: Feedback name
- textbox "Feedback name":
  - /placeholder: Feedback name (optional)
- text: Your feedback
- textbox "Your feedback":
  - /placeholder: Tell us what you loved (at least 10 characters)
- text: Add an image
- button "Add an image"
- text: JPG, PNG, GIF, or WebP up to 2MB.
- button "Send feedback" [disabled]
- text: ©
- link "Salt & Smoke":
  - /url: index.html
- text: ", All Right Reserved."
```

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