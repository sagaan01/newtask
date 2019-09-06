package com.automationqapractice.pages;

import static org.testng.Assert.assertTrue;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;

public class LoginPage extends LoadableComponent<LoginPage>{
		
		private WebDriver driver;
		private LoadableComponent<?> parent;
		
		public LoginPage(WebDriver driver, LoadableComponent<?> parent) {
			this.driver = driver;
			this.parent = parent;
			PageFactory.initElements(driver, this);
		}

		@FindBy (id = "SubmitCreate")
		public WebElement createAccountButton;
		
		@FindBy (id = "email_create")
		public WebElement emailAddressNew;
		
		@FindBy (id = "email")
		public WebElement registeredEmailField;
		
		@FindBy (id = "passwd")
		public WebElement passwordField;
		
		@FindBy (id = "SubmitLogin")
		public WebElement loginButton;
		
		@Override
		protected void load() {
		}

		@Override
		protected void isLoaded() throws Error {
			assertTrue(createAccountButton.isDisplayed(), "Create Account button not visible");
		}
		
		public void enterEmail(String email) {
			emailAddressNew.sendKeys(email);
		}
		
		public AccountCreationPage submit()
		{
			createAccountButton.submit();
			return new AccountCreationPage(driver, this).get();
		}
		
		public UserAccountPage signInWithRegisteredAccount(String email, String password) {
			registeredEmailField.clear();
			registeredEmailField.sendKeys(email);
			passwordField.clear();
			passwordField.sendKeys(password);
			loginButton.click();
			return new UserAccountPage(driver, this);
		}

	}

