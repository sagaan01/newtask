package com.automationqapractice.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;

public class PaymentConfirmPage extends LoadableComponent<PaymentConfirmPage>{

	private WebDriver driver;
	@SuppressWarnings("unused")
	private LoadableComponent<PaymentConfirmPage> confirmShippingPage;
	
	@Override
	protected void load() {
	}

	@Override
	protected void isLoaded() throws Error {
		System.out.println("On confirm Payment page");		
	}
	
	@FindBy(css = ".cheque")
	public WebElement payByChequeElement;
	private LoadableComponent<ShippingConfirmPage> ShippingConfirmPage;
	
	public PaymentConfirmPage(WebDriver driver, LoadableComponent<ShippingConfirmPage> ShippingConfirmPage) {
		this.driver = driver;
		this.ShippingConfirmPage = ShippingConfirmPage;
		PageFactory.initElements(driver, this);
	}
	
	public FinalOrderConfirmPage payByCheck() {
		payByChequeElement.click();
		return new FinalOrderConfirmPage(driver, this);
	}

}