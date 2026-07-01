# AGENTS.md

## Cursor Cloud specific instructions

### What this project is
A Selenium + TestNG UI test-automation framework (Maven, Java 8 target). There is no
long-running application/server — the "app" is the test suite. Tests, page objects and
utilities live under `src/test/java`; the TestNG suite is `src/main/resources/testSuite.xml`.
Standard commands are in `pom.xml` and `README.md`.

### Toolchain (already present in the snapshot)
- Java 21 is the JDK. It compiles the project's `source/target 1.8` fine (obsolete-version
  warnings are expected and harmless).
- Maven 3.8.7 is installed (`mvn`).
- Google Chrome is installed system-wide (currently v148). No `chromedriver` is installed.

### Build / compile (works today)
- `mvn clean test-compile` → `BUILD SUCCESS` (compiles all sources under `src/test/java`).
- There is no separate linter; compilation is the effective static check.

### Running the suite — known blockers (durable, NOT fixable via env setup)
`mvn test` currently cannot run the suite on Linux without code changes, due to pre-existing
code/external issues (do not "fix" these as part of environment setup):
1. **Dead target site.** Tests drive `http://automationpractice.com/index.php`, which is now a
   parked InMotion Hosting page. Any UI flow (create account / search / order) fails on element
   lookups regardless of setup.
2. **Linux report path bug.** `com.automationqapractice.utils.Extentmanager.createInstance()`
   only sets an ExtentReports path for `MAC`/`WINDOWS`; on Linux it returns `null`, so
   `new ExtentHtmlReporter(null)` throws and TestNG fails with
   `Cannot instantiate class Listeners.TestListener` before any test runs.
3. **ChromeDriver pin.** `Webdriverfactory` pins `WebDriverManager.chromedriver().version("76.0.3809.126")`
   via WebDriverManager 3.6.2, which cannot resolve drivers for Chrome >115. It will not launch
   the installed Chrome 148.

### Verifying the Selenium stack actually works (browser automation smoke)
To prove browser automation works in this VM without touching repo code:
- Download a `chromedriver` whose major version matches the installed Chrome from Chrome for
  Testing, e.g.
  `https://storage.googleapis.com/chrome-for-testing-public/<FULL_CHROME_VERSION>/linux64/chromedriver-linux64.zip`.
- Chrome must run headless here (no display). Use options
  `--headless=new --no-sandbox --disable-dev-shm-usage --disable-gpu`.
- Build the dependency classpath with `mvn -q dependency:build-classpath -Dmdep.outputFile=/tmp/cp.txt`
  and run a small standalone Selenium program against a live demo site (the project's own
  Selenium 3.141.59 dependency works fine with a matching modern chromedriver in W3C mode).
