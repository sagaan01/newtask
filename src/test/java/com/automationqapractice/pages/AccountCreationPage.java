package com.automationqapractice.pages;

import static org.testng.Assert.assertTrue;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;
import org.openqa.selenium.support.ui.Select;

import com.automationqapractice.utils.PageLoad;
import com.automationqapractice.utils.Userinfo;

public class AccountCreationPage extends LoadableComponent<AccountCreationPage>{

		private WebDriver driver;
			
			public AccountCreationPage(WebDriver driver, LoadableComponent<LoginPage> parent) {
				this.driver = driver;
				PageFactory.initElements(driver, this);
			}
			
			@FindBy (id = "submitAccount")
			public WebElement submitAccount;
			
			@FindBy (id = "email")
			public WebElement emailField;
			
			@FindBy (name = "id_gender")
			public WebElement gender;
			
			@FindBy (name = "customer_firstname")
			public WebElement firstName;
			
			@FindBy (name = "customer_lastname")
			public WebElement lastName;
			
			@FindBy (name = "passwd")
			public WebElement password;
			
			@FindBy (name = "days")
			public WebElement days;
			
			@FindBy (name = "months")
			public WebElement months;
			
			@FindBy (name = "years")
			public WebElement years;
			
			@FindBy (name = "firstname")
			public WebElement address_firstname;
			
			@FindBy (name = "lastname")
			public WebElement address_lastname;
			
			@FindBy (name = "company")
			public WebElement address_company;
			
			@FindBy (name = "address1")
			public WebElement address_address1;
			
			@FindBy (name = "city")
			public WebElement address_city;
			
			@FindBy (name = "id_state")
			public WebElement address_id_state;
			
			@FindBy (name = "postcode")
			public WebElement address_postcode;
			
			@FindBy (name = "id_country")
			public WebElement address_id_country;
			
			@FindBy (name = "phone_mobile")
			public WebElement address_phone_mobile;
			
			@FindBy (name = "alias")
			public WebElement alias;
			
			@Override
			protected void load() {
			}

			@Override
			protected void isLoaded() throws Error {
				assertTrue(PageLoad.isOnCorrectPage(driver), "Email field not enabled");
			}
			
			public String getEmailContent() {
				return emailField.getAttribute("value");
			}
			
			public void selectGender() {
				this.gender.click();
			}
			
			public void enterTextInto(WebElement element, String text) {
				element.clear();
				element.sendKeys(text);
			}
			
			public void selectDateOfBirth() {
				Select select = new Select(days);
				select.selectByIndex(1);
				select = new Select(months);
				select.selectByIndex(1);
				select = new Select(years);
				select.selectByIndex(1);
			}
			
			public void selectState() {
				Select select = new Select(address_id_state);
				select.selectByIndex(1);
			}
			
			public void selectCountry() {
				Select select = new Select(address_id_country);
				select.selectByIndex(1);
			}
			
			public UserAccountPage fillForm(Userinfo userInformation) {
				selectGender();
				 
				enterTextInto(firstName, userInformation.getFirstName());
				enterTextInto(lastName, userInformation.getLastName());
				enterTextInto(password, userInformation.getPassword());
				selectDateOfBirth();
				enterTextInto(address_company, userInformation.getCompany());
				enterTextInto(address_address1, userInformation.getAddress());
				enterTextInto(address_city, userInformation.getCity());
				selectState();
				enterTextInto(address_postcode, userInformation.getZipcode());
				enterTextInto(address_phone_mobile, userInformation.getMobileNumber());
				enterTextInto(alias, userInformation.getAlias());
				submitAccount.click();
				return new UserAccountPage(driver, this).get();
			}
}
