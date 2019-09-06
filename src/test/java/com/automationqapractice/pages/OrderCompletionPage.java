package com.automationqapractice.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.LoadableComponent;

public class OrderCompletionPage extends LoadableComponent<OrderCompletionPage>{

	@SuppressWarnings("unused")
	private WebDriver driver;
	@SuppressWarnings("unused")
	private LoadableComponent<FinalOrderConfirmPage> finalConfirmationOnOrderPage;
	
	@Override
	protected void load() {
		
	}

	@Override
	protected void isLoaded() throws Error {

		System.out.println("On Order completion page");
	}
	
	public OrderCompletionPage(WebDriver driver, LoadableComponent<FinalOrderConfirmPage> finalConfirmationOnOrderPage) {
		this.driver = driver;
		this.finalConfirmationOnOrderPage = finalConfirmationOnOrderPage;
		PageFactory.initElements(driver, this);
	}
	
	@FindBy(css = ".alert.alert-success")
	public WebElement successBanner;
	
	public boolean isOrderSuccessfullyPlaced() {
		return successBanner.getAttribute("innerText").trim().contains("Your order on My Store is complete.");
	}
}