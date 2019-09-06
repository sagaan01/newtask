package com.automationqapractice.pages;

import static org.testng.Assert.assertTrue;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;

public class FinalOrderConfirmPage extends LoadableComponent<FinalOrderConfirmPage>{

	private WebDriver driver;
	@SuppressWarnings("unused")
	private LoadableComponent<PaymentConfirmPage> PaymentConfirmPage;
	
	@Override
	protected void load() {
	}

	@Override
	protected void isLoaded() throws Error {
		System.out.println("Is on FinalConfirmationOnOrderPage");
		assertTrue(submitButtonElement.isDisplayed(), "Submit button not displayed");
	}
	
	@FindBy(css = ".cart_navigation button")
	public WebElement submitButtonElement;
	
	public FinalOrderConfirmPage(WebDriver driver, LoadableComponent<PaymentConfirmPage> PaymentConfirmPage) {
		this.driver = driver;
		this.PaymentConfirmPage = PaymentConfirmPage;
		PageFactory.initElements(driver, this);
	}
	
	public OrderCompletionPage submitOrder() {
		submitButtonElement.click();
		return new OrderCompletionPage(driver, this);
	}

}