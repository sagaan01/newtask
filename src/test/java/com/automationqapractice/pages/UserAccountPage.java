package com.automationqapractice.pages;

import static org.testng.Assert.assertEquals;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.How;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;

import com.automationqapractice.base.Dresscategory;
import com.automationqapractice.utils.Userinfo;

public class UserAccountPage extends LoadableComponent<UserAccountPage>{

	private WebDriver driver;
	private LoadableComponent<?> parent;
	private static Userinfo userInformation = Userinfo.getInstance();
	
	public UserAccountPage(WebDriver driver, LoadableComponent<?> parent) {
		this.driver = driver;
		this.parent = parent;
		PageFactory.initElements(driver, this);
	}
	
	@FindBy(how = How.CLASS_NAME, using = "account")
	public WebElement userAccountInfo;
	
	@FindBy (className =  "logout")
	public WebElement logoutButton;
	
	@FindBy (id = "search_query_top")
	public WebElement searchBox;
	
	@Override
	protected void load() {
	}

	@Override
	protected void isLoaded() throws Error {
		assertEquals(userAccountInfo.getText(), userInformation.getFirstName()+ " " +userInformation.getLastName(), "Name not correct");
	}
	
	public LoginPage signOut() {
		logoutButton.click();
		return new LoginPage(driver, this);
	}
	
	public SearchresultsPage enterSearchText(String text) {
		searchBox.clear();
		searchBox.sendKeys(text);
		searchBox.submit();
		return new SearchresultsPage(driver, this).get();
	}
	
	public SearchresultsPage searchFor(Dresscategory category) {
		return enterSearchText(category.getName());
	}

}