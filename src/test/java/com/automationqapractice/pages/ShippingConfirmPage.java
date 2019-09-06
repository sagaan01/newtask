package com.automationqapractice.pages;

import static org.testng.Assert.assertTrue;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;

import com.automationqapractice.utils.Userinfo;

public class ShippingConfirmPage extends LoadableComponent<ShippingConfirmPage>{

	private WebDriver driver;
	@SuppressWarnings("unused")
	private LoadableComponent<AdressConfirmPage> AdressConfirmPage;
	Userinfo userInformation = Userinfo.getInstance();
	
	public ShippingConfirmPage(WebDriver driver, LoadableComponent<AdressConfirmPage> AdressConfirmPage) {
		this.driver = driver;
		this.AdressConfirmPage = AdressConfirmPage;
		PageFactory.initElements(driver, this);
	}
	
	@Override
	protected void load() {
	}

	@Override
	protected void isLoaded() throws Error {
		assertTrue(shippingOptionElement.isDisplayed(), "Not on Confirm shipping page");
	}
	
	@FindBy(css = ".delivery_option_radio .checked")
	public WebElement shippingOptionElement;
	
	@FindBy(css = "#cgv")
	public WebElement termsOfServiceCheckboxElement;
	
	@FindBy(name = "processCarrier")
	public WebElement processCarrier;
	
	public boolean isDefaultShippingSelected() {
		return shippingOptionElement.isSelected();
	}

	public void selectDefaultShipping() {
		shippingOptionElement.click();
	}
	
	public void agreeTermsOfService() {
		if(!termsOfServiceCheckboxElement.isSelected())
			termsOfServiceCheckboxElement.click();
	}

	public PaymentConfirmPage next() {
		processCarrier.click();
		return new PaymentConfirmPage(driver, this);
	}
}
