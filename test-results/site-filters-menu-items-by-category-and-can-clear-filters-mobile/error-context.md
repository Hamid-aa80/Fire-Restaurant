# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: site.spec.ts >> filters menu items by category and can clear filters
- Location: tests/site.spec.ts:188:1

# Error details

```
Test timeout of 30000ms exceeded.
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

```
Error: locator.click: Test timeout of 30000ms exceeded.
Call log:
  - waiting for locator('#menuCategoryFilters button[data-menu-category-chip="dinner"]')

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
  - generic [ref=e20]:
    - generic [ref=e21]:
      - generic [ref=e28]:
        - heading "About Us" [level=5] [ref=e29]
        - heading "Welcome to  Salt & Smoke" [level=1] [ref=e30]:
          - text: Welcome to
          - generic [ref=e31]: 
          - text: Salt & Smoke
        - paragraph [ref=e32]: At Salt & Smoke, we are passionate about delivering an exceptional dining experience that tantalizes your taste buds and leaves you craving for more. Our culinary team combines creativity, skill, and the finest ingredients to craft dishes that are both visually stunning and bursting with flavor.
        - paragraph [ref=e33]: From the moment you step into our restaurant, you'll be greeted with warm hospitality and a cozy ambiance that sets the stage for an unforgettable meal. Whether you're joining us for a casual lunch, a romantic dinner, or a special celebration, we strive to create memories that linger long after the last bite.
        - generic [ref=e34]:
          - generic [ref=e36]:
            - heading "15" [level=1] [ref=e37]
            - generic [ref=e38]:
              - paragraph [ref=e39]: Years of
              - heading "Experience" [level=6] [ref=e40]
          - generic [ref=e42]:
            - heading "50" [level=1] [ref=e43]
            - generic [ref=e44]:
              - paragraph [ref=e45]: Popular
              - heading "Master Chefs" [level=6] [ref=e46]
        - link "Read More" [ref=e47] [cursor=pointer]:
          - /url: "#team"
      - generic [ref=e49]:
        - generic [ref=e50]:
          - generic [ref=e51]:
            - generic [ref=e52]: Search the menu
            - searchbox "Search the menu" [ref=e53]
          - generic [ref=e54]:
            - paragraph [ref=e55]: Filter by category
            - button "Clear filters" [ref=e56] [cursor=pointer]
          - group "Filter menu by category"
          - paragraph [ref=e57]: Showing all categories.
        - paragraph [ref=e59]: Showing 6 of 6 dishes
        - generic [ref=e62]:
          - generic [ref=e64]:
            - img "Juicy Burger" [ref=e65]
            - generic [ref=e66]:
              - heading "Juicy Burger £25" [level=5] [ref=e67]:
                - generic [ref=e68]: Juicy Burger
                - generic [ref=e69]: £25
              - generic [ref=e70]: A juicy burger with fresh ingredients and a perfectly grilled patty.
          - generic [ref=e72]:
            - img "Grilled Salmon" [ref=e73]
            - generic [ref=e74]:
              - heading "Grilled Salmon £30" [level=5] [ref=e75]:
                - generic [ref=e76]: Grilled Salmon
                - generic [ref=e77]: £30
              - generic [ref=e78]: A thick salmon fillet rests on a cedar plank, its surface lacquered with a glossy ember‑glaze.
          - generic [ref=e80]:
            - img "Smoked Steak" [ref=e81]
            - generic [ref=e82]:
              - heading "Smoked Steak £35" [level=5] [ref=e83]:
                - generic [ref=e84]: Smoked Steak
                - generic [ref=e85]: £35
              - generic [ref=e86]: A succulent smoked steak, perfectly seared and infused with rich, smoky flavors.
          - generic [ref=e88]:
            - img "English Breakfast" [ref=e89]
            - generic [ref=e90]:
              - heading "English Breakfast £25" [level=5] [ref=e91]:
                - generic [ref=e92]: English Breakfast
                - generic [ref=e93]: £25
              - generic [ref=e94]: A hearty English breakfast with eggs, bacon, sausages, and beans.
          - generic [ref=e96]:
            - img "Beer" [ref=e97]
            - generic [ref=e98]:
              - heading "Beer £15" [level=5] [ref=e99]:
                - generic [ref=e100]: Beer
                - generic [ref=e101]: £15
              - generic [ref=e102]: A refreshing pint of beer, perfect for pairing with your meal.
          - generic [ref=e104]:
            - img "Coffee" [ref=e105]
            - generic [ref=e106]:
              - heading "Coffee £5" [level=5] [ref=e107]:
                - generic [ref=e108]: Coffee
                - generic [ref=e109]: £5
              - generic [ref=e110]: A rich and aromatic cup of coffee, perfect for a morning boost or an afternoon pick-me-up.
    - option "Select guests" [disabled] [selected]
    - option "Person 1"
    - option "Person 2"
    - option "Person 3"
    - option "Person 4"
```

# Test source

```ts
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
  137 | 
  138 | test("remains responsive across common breakpoints", async ({ page }) => {
  139 |   for (const viewport of [
  140 |     { width: 390, height: 844 },
  141 |     { width: 768, height: 1024 },
  142 |     { width: 1366, height: 900 }
  143 |   ]) {
  144 |     await page.setViewportSize(viewport);
  145 |     await page.goto("/");
  146 |     await page.waitForLoadState("networkidle");
  147 | 
  148 |     await expect(page.locator(".navbar")).toBeVisible();
  149 |     await page.locator("#reservationForm").scrollIntoViewIfNeeded();
  150 |     await expect(page.locator("#reservationForm")).toBeVisible();
  151 |     await page.locator("#menu").scrollIntoViewIfNeeded();
  152 |     await expect(page.locator("#menu")).toBeVisible();
  153 |   }
  154 | });
  155 | 
  156 | test("stays responsive on mobile and keeps navigation usable", async ({ page }) => {
  157 |   await page.setViewportSize({ width: 390, height: 844 });
  158 |   await page.goto("/");
  159 |   await page.waitForLoadState("networkidle");
  160 |   await expect(page.locator(".navbar-toggler")).toBeVisible();
  161 | 
  162 |   await page.locator(".navbar-toggler").click();
  163 |   await expect(page.locator("#navbarCollapse")).toHaveClass(/show/);
  164 |   await page.getByRole("link", { name: "Menu" }).click();
  165 |   await expect(page.locator("#menu")).toBeInViewport();
  166 | 
  167 |   await page.locator(".navbar-toggler").click();
  168 |   await expect(page.locator("#navbarCollapse")).toHaveClass(/show/);
  169 |   await page.getByRole("link", { name: "Reservation" }).click();
  170 |   await expect(page.locator("#reservation")).toBeInViewport();
  171 |   await expect(page.locator("#navbarCollapse")).not.toHaveClass(/show/);
  172 | });
  173 | 
  174 | test("searches menu items by name", async ({ page }) => {
  175 |   await page.locator("#menu").scrollIntoViewIfNeeded();
  176 |   const menuSearch = page.locator("#menuSearch");
  177 | 
  178 |   await menuSearch.fill("coffee");
  179 |   await expect(page.locator('[data-menu-name="Coffee"]')).toBeVisible();
  180 |   await expect(page.locator('[data-menu-name="Juicy Burger"]')).toBeHidden();
  181 |   await expect(page.locator("#menuVisibleCount")).toHaveText("1");
  182 | 
  183 |   await menuSearch.fill("nonexistent dish");
  184 |   await expect(page.locator("#menuEmptyState")).toBeVisible();
  185 |   await expect(page.locator("#menuVisibleCount")).toHaveText("0");
  186 | });
  187 | 
  188 | test("filters menu items by category and can clear filters", async ({ page }) => {
  189 |   await page.locator("#menu").scrollIntoViewIfNeeded();
  190 |   const dinnerFilter = page.locator('#menuCategoryFilters button[data-menu-category-chip="dinner"]');
  191 |   const allFilter = page.locator('#menuCategoryFilters button[data-menu-category-chip="all"]');
  192 |   const menuSearch = page.locator("#menuSearch");
  193 |   const resetFilters = page.locator("#menuResetFilters");
  194 |   const menuFilterStatus = page.locator("#menuFilterStatus");
  195 | 
> 196 |   await dinnerFilter.click();
      |                      ^ Error: locator.click: Test timeout of 30000ms exceeded.
  197 |   await expect(page.locator('[data-menu-name="Grilled Salmon"]')).toBeVisible();
  198 |   await expect(page.locator('[data-menu-name="Smoked Steak"]')).toBeVisible();
  199 |   await expect(page.locator('[data-menu-name="Juicy Burger"]')).toBeHidden();
  200 |   await expect(menuFilterStatus).toContainText("category: Dinner");
  201 |   await expect(page.locator("#menuVisibleCount")).toHaveText("2");
  202 | 
  203 |   await menuSearch.fill("steak");
  204 |   await expect(page.locator('[data-menu-name="Smoked Steak"]')).toBeVisible();
  205 |   await expect(page.locator('[data-menu-name="Grilled Salmon"]')).toBeHidden();
  206 |   await expect(menuFilterStatus).toContainText('search: "steak"');
  207 |   await expect(page.locator("#menuVisibleCount")).toHaveText("1");
  208 | 
  209 |   await resetFilters.click();
  210 |   await expect(allFilter).toHaveClass(/is-active/);
  211 |   await expect(menuFilterStatus).toContainText("Showing all categories.");
  212 |   await expect(page.locator("#menuVisibleCount")).toHaveText("6");
  213 | });
  214 | 
  215 | test("keeps the page free of broken same-origin links", async ({ page }) => {
  216 |   await page.locator("#menu").scrollIntoViewIfNeeded();
  217 |   await expect(page.locator('[data-menu-name="English Breakfast"]')).toBeVisible();
  218 |   await expect(page.locator('[data-menu-name="Juicy Burger"]')).toBeVisible();
  219 | 
  220 |   const links = await page.locator("a[href]").evaluateAll(elements =>
  221 |     elements
  222 |       .map(element => element.getAttribute("href"))
  223 |       .filter((href): href is string => Boolean(href))
  224 |   );
  225 | 
  226 |   const brokenAnchors = [];
  227 |   const invalidLocalTargets = [];
  228 |   for (const link of links) {
  229 |     if (link.startsWith("#")) {
  230 |       const id = link.slice(1);
  231 |       if (id && (await page.locator(`#${id}`).count()) === 0) {
  232 |         brokenAnchors.push(link);
  233 |       }
  234 |       continue;
  235 |     }
  236 | 
  237 |     if (link.startsWith("mailto:") || link.startsWith("tel:") || link.startsWith("https://")) {
  238 |       continue;
  239 |     }
  240 | 
  241 |     const response = await page.request.get(new URL(link, page.url()).toString());
  242 |     if (!response.ok()) {
  243 |       invalidLocalTargets.push(`${link} -> ${response.status()}`);
  244 |     }
  245 |   }
  246 | 
  247 |   expect(brokenAnchors, brokenAnchors.join("\n")).toEqual([]);
  248 |   expect(invalidLocalTargets, invalidLocalTargets.join("\n")).toEqual([]);
  249 | });
  250 | 
  251 | test("restores reservation draft after reload (bug-fix regression)", async ({ page }) => {
  252 |   const tomorrow = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split("T")[0];
  253 |   await page.locator("#reservationForm").scrollIntoViewIfNeeded();
  254 |   await page.getByLabel("Your Name").fill("Draft Name");
  255 |   await page.getByLabel("Your Email").fill("draft@example.com");
  256 |   await page.locator("#datetime").fill(tomorrow);
  257 |   await page.locator("#select1").selectOption("3");
  258 |   await page.getByLabel("Special Request").fill("Draft request details");
  259 |   await page.reload();
  260 |   await page.waitForLoadState("networkidle");
  261 |   await page.locator("#reservationForm").scrollIntoViewIfNeeded();
  262 | 
  263 |   await expect(page.getByLabel("Your Name")).toHaveValue("Draft Name");
  264 |   await expect(page.getByLabel("Your Email")).toHaveValue("draft@example.com");
  265 |   await expect(page.locator("#datetime")).toHaveValue(tomorrow);
  266 |   await expect(page.locator("#select1")).toHaveValue("3");
  267 |   await expect(page.getByLabel("Special Request")).toHaveValue("Draft request details");
  268 | });
  269 | 
  270 | test("handles duplicate newsletter subscription without errors (bug-fix regression)", async ({ page }) => {
  271 |   await page.locator("#newsletterForm").scrollIntoViewIfNeeded();
  272 |   const newsletterEmail = page.locator("#newsletterEmail");
  273 |   const newsletterButton = page.getByRole("button", { name: /sign up/i });
  274 |   const newsletterFeedback = page.locator("#newsletterFeedback");
  275 | 
  276 |   await newsletterEmail.fill("newsletter@example.com");
  277 |   await newsletterButton.click();
  278 |   await expect(newsletterFeedback).toContainText("You're subscribed with newsletter@example.com");
  279 | 
  280 |   await newsletterButton.click();
  281 |   await expect(newsletterFeedback).toContainText("already subscribed with newsletter@example.com");
  282 | });
  283 | 
  284 | test("shows fallback feedback when reservation confirmation is missing (bug-fix regression)", async ({
  285 |   page
  286 | }) => {
  287 |   await page.goto("/submit.html");
  288 |   await page.waitForLoadState("networkidle");
  289 |   await expect(page.getByRole("alert")).toContainText("couldn't find your reservation details");
  290 | });
  291 | 
```