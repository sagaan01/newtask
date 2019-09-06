package com.automationqapractice.pages;

import static org.testng.Assert.assertTrue;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;

public class Homepage extends LoadableComponent<Homepage> {

	private WebDriver driver;
	
	public Homepage(WebDriver driver) {
		this.driver = driver;
		PageFactory.initElements(driver, this);
	}
	
	@Override
	protected void load() {
	}

	@Override
	protected void isLoaded() throws Error {
			assertTrue(driver.getCurrentUrl().contains("automation"), "Not on correct page");
	}
	
	@FindBy (id = "search_query_top")
	public WebElement searchBoxElement;
	
	@FindBy (className = "login")
	public WebElement signInLink;
	
	public Boolean isSearchBoxVisible() {
		return searchBoxElement.isDisplayed();
	}
	
	public LoginPage clickSignInLink() {
		signInLink.click();
		return new LoginPage(this.driver, this);
	}
	

}
