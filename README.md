"# Hometask" 
Framework specifications:

Programming Language: JAVA

Test Framwork: TestNG

Reporting Framework: ExtentReports

Build Tool: MAVEN

Automation Framework: SELENIUM

Url and browser values are configurable in pom.xml. Default is dev profile that launches the tests in chrome at http://automationpractice.com/index.php. Can be launched using command "mvn clean install" Test profile can be activated by "mvn clean install -Denv=test" WebDriverManager plugin is used to manage selenium drivers.

ExtentReports generated after the test suite can be found under "\TestReport" folder. Page Object model with Page Factory approach is implemented
