package com.automationqapractice.test;

import static org.testng.Assert.fail;

import org.openqa.selenium.WebDriver;
import org.testng.ITestContext;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Parameters;

import com.automationqapractice.utils.Testcontext;
import com.automationqapractice.utils.Webdriverfactory;




public class TestBase extends Webdriverfactory{

	public WebDriver driver;
	@SuppressWarnings("unused")
	private ITestContext testContext;
	
	@Parameters({"browser", "url"})
	@BeforeClass (alwaysRun = true, description = "One time initialization code")
	public void setup(String browser, String url, ITestContext testContext){
		try {
			driver = Webdriverfactory.createWebDriver(browser);
			testContext = Testcontext.seTestContext(testContext, driver);
			driver.navigate().to(url);
			driver.manage().window().maximize();
		} catch (Exception e) {
			e.printStackTrace();
			fail();
		}
	}
	
	@AfterClass (alwaysRun = true, description = "Method to take care of final cleanup activities, liking shutting down browsers or closing any open streams")
	public void tearDown(){
		try {
			if(driver != null)
			driver.quit();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
}