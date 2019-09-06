package com.automationqapractice.test;

import static org.testng.Assert.assertFalse;

import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import com.automationqapractice.base.Dresscategory;
import com.automationqapractice.pages.Homepage;
import com.automationqapractice.pages.LoginPage;
import com.automationqapractice.pages.SearchresultsPage;
import com.automationqapractice.pages.UserAccountPage;
import com.automationqapractice.utils.Extentmanager;
import com.automationqapractice.utils.Userinfo;
import com.aventstack.extentreports.ExtentReports;

public class SearchProductCategoryTest extends TestBase{
	


	private Homepage homePage;
	private static Userinfo userInformation = Userinfo.getInstance();
	ExtentReports test = Extentmanager.getInstance();
	private LoginPage signInPage;
	private UserAccountPage userAccountPage;
	private SearchresultsPage searchResultsPage;
	
	@BeforeClass(description = "Method Level Setup!")
    public void methodLevelSetup() {
        	homePage = new Homepage(driver).get();
    }
	
	@Test
	public void searchProductCategory() {
			signInPage = homePage.clickSignInLink();
			userAccountPage = signInPage.signInWithRegisteredAccount(userInformation.getEmail(), userInformation.getPassword());
			searchResultsPage = userAccountPage.enterSearchText("Dress");
			assertFalse(Dresscategory.values().length > searchResultsPage.getResultCount(), "Wrong number of results shown");
	}
}